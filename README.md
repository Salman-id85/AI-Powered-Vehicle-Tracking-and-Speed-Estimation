# AI-Powered-Vehicle-Tracking-and-Speed-Estimation
Human-level perception for traffic safety in sensitive urban zones
  
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)]()  
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Object%20Detection-red)]()  
[![Flask](https://img.shields.io/badge/Framework-Flask-lightgrey)]()  

## Overview  
This project introduces an **AI-driven vehicle surveillance system** designed for **restricted traffic zones** (school areas, hospitals, and pedestrian-dense zones).  

The system integrates **YOLOv8**, **ByteTrack**, and **OpenCV** within a **Flask web platform** to detect, track, and estimate vehicle speeds in uploaded videos. It provides accurate analytics for **urban safety, traffic monitoring, and regulatory compliance**.  

**Key Highlights:**  
- **Real-time vehicle detection** using YOLOv8  
- **Robust multi-object tracking** with ByteTrack  
- **Speed estimation** with perspective transformation (MAE ≈ 2.5 km/h)  
- **Web interface** (Flask) for video uploads up to **500 MB**  
- **Export results** in annotated videos + Excel reports  
- **Modular & scalable architecture** (future cloud integration, async processing)  

---

## Tech Stack  
- **Deep Learning:** YOLOv8  
- **Tracking:** ByteTrack  
- **Computer Vision:** OpenCV  
- **Backend Framework:** Flask  
- **Database:** SQLite  
- **Data Handling:** Pandas, NumPy  

---

## Project Structure

AI-Powered-Vehicle-Tracking-and-Speed-Estimation/
│── app.py # Flask main application
│── requirements.txt # Dependencies
│── static/ # CSS, JS, assets
│── templates/ # HTML templates
│── models/ # Pre-trained YOLOv8 weights
│── utils/ # Helper functions (tracking, speed calc, etc.)
│── uploads/ # Uploaded videos
│── results/ # Processed outputs (videos, reports)
│── README.md # Project documentation
│── Conference_Paper.pdf # Research paper


---

## Installation  

1. **Clone the repository**  
```bash
git clone https://github.com/Salman-id85/AI-Powered-Vehicle-Tracking-and-Speed-Estimation.git
cd AI-Powered-Vehicle-Tracking-and-Speed-Estimation
 ```
2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate    # On Linux/Mac
venv\Scripts\activate       # On Windows
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
4. **Run the Flask app**
```bash
python app.py
```
5. **Open in browser**
```bash
http://127.0.0.1:5000/
```

---

**Usage**

1. Upload a traffic video (MP4/AVI, max 500 MB).
2. System detects, tracks, and estimates speed of vehicles.
3. Download annotated video and Excel report with speed stats.

---

**Results**

- Detection Precision: 0.94
- Tracking Success Rate: 0.91
- Speed Estimation Error (MAE): 2.5 km/h

---

**Sample Output:**

- Annotated Video
- Excel Report with vehicle IDs, classes, and speeds

---

**Research Paper**

For detailed methodology and results, see Conference_Paper.pdf

---

**Future Enhancements**

- Cloud-based video storage & processing
- Real-time violation detection (overspeed alerts)
- License Plate Recognition (LPR)
- Multi-camera integration for crowded zones

---

**Contributors**

- Salman S
- Prasanth Kumar R
- Sai Niresh N
- Guided by Mrs. P Revathi (Assistant Professor, CSE Dept)
- H.O.D: Dr. K. Abrar Ahmed (Assistant Professor, CSE Dept)

---

**License**
This project is licensed under the MIT License.

