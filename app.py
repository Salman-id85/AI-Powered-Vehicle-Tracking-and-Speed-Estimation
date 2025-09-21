from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
import os
from werkzeug.utils import secure_filename
import pandas as pd
from your_backend import process_video
import uuid
from datetime import datetime
import sqlite3
import logging

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get('CSRF_SECRET_KEY', os.urandom(24))

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB max upload size

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Setup logging to terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Output logs to terminal
    ]
)

# Contact Form
class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Your Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file size limit errors."""
    flash('File is too large. Maximum upload size is 500MB.', 'error')
    return redirect(url_for('index') + '#upload'), 413

# Custom filter to mimic Django's floatformat
@app.template_filter('floatformat')
def floatformat_filter(value, precision=1):
    try:
        return f"{float(value):.{precision}f}"
    except (ValueError, TypeError):
        return value

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handle video upload and render landing page."""
    if request.method == 'POST':
        if 'video' not in request.files:
            flash('No video file part in the request', 'error')
            return redirect(url_for('index') + '#upload')
        file = request.files['video']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('index') + '#upload')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_id = f"{uuid.uuid4()}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
            output_video_path = os.path.join(app.config['OUTPUT_FOLDER'], f"output_{unique_id}.mp4")
            output_excel_path = os.path.join(app.config['OUTPUT_FOLDER'], f"vehicle_data_{unique_id}.xlsx")
            file.save(input_path)

            try:
                logging.info(f"Processing video: {input_path}")
                process_video(input_path, output_video_path, output_excel_path)
                session['output_video'] = f"output_{unique_id}.mp4"
                session['output_excel'] = f"vehicle_data_{unique_id}.xlsx"
                flash('Video processed successfully!', 'message')
                return redirect(url_for('results'))
            except Exception as e:
                logging.error(f"Error processing video: {e}")
                flash(f'Error processing video: {e}', 'error')
                return redirect(url_for('index') + '#upload')
        else:
            flash('Allowed video types are mp4, avi, mov', 'error')
            return redirect(url_for('index') + '#upload')
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    """Handle search by tracker ID and display processed video and results."""
    output_excel_path = os.path.join(app.config['OUTPUT_FOLDER'], session.get('output_excel', 'vehicle_data.xlsx'))
    output_video = session.get('output_video', 'output_video.mp4')
    filtered_data = None
    vehicle_id = None

    if request.method == 'POST':
        vehicle_id = request.form.get('tracker_id')
        if vehicle_id and vehicle_id.isdigit():
            vehicle_id = int(vehicle_id)
            try:
                if not os.path.exists(output_excel_path):
                    flash('No vehicle data available. Please upload and process a video first.', 'error')
                    return redirect(url_for('results'))
                
                df = pd.read_excel(output_excel_path)
                if 'tracker_id' not in df.columns:
                    flash('Tracker ID column not found in data.', 'error')
                    return redirect(url_for('results'))
                
                # Filter data by tracker_id
                filtered_data = df[df['tracker_id'] == vehicle_id].copy()
                if filtered_data.empty:
                    flash(f'No data found for Vehicle Tracker ID: {vehicle_id}', 'error')
                else:
                    flash(f'Data found for Vehicle Tracker ID: {vehicle_id}', 'message')
            except Exception as e:
                logging.error(f"Error reading Excel data: {e}")
                flash(f'Error reading data: {e}', 'error')
        else:
            flash('Please enter a valid numeric Tracker ID.', 'error')

    return render_template('results.html', video_file=output_video, data=filtered_data, vehicle_id=vehicle_id)

@app.route('/download_excel')
def download_excel():
    """Serve the Excel file for download."""
    output_excel_path = os.path.join(app.config['OUTPUT_FOLDER'], session.get('output_excel', 'vehicle_data.xlsx'))
    if os.path.exists(output_excel_path):
        return send_file(output_excel_path, as_attachment=True)
    else:
        flash('Excel file not found.', 'error')
        return redirect(url_for('index') + '#upload')

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission."""
    form = ContactForm()
    if form.validate_on_submit():
        try:
            with sqlite3.connect('contacts.db') as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS contacts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT,
                        subject TEXT,
                        message TEXT,
                        timestamp TEXT
                    )
                ''')
                conn.execute(
                    'INSERT INTO contacts (name, email, subject, message, timestamp) VALUES (?, ?, ?, ?, ?)',
                    (form.name.data, form.email.data, form.subject.data, form.message.data, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                )
                conn.commit()
            logging.info(f"Contact form submitted: {form.name.data}, {form.email.data}")
            flash('Thank you for your message! We will get back to you soon.', 'message')
        except Exception as e:
            logging.error(f"Error saving contact form: {e}")
            flash('Error saving your message. Please try again.', 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field.capitalize()}: {error}', 'error')
    return redirect(url_for('index') + '#contact')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)