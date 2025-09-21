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
python -m venv venv
source venv/bin/activate    # On Linux/Mac
venv\Scripts\activate       # On Windows
pip install -r requirements.txt
python app.py
http://127.0.0.1:5000/

