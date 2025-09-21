import cv2
import numpy as np
import supervision as sv
from tqdm import tqdm
from ultralytics import YOLO
from collections import defaultdict, deque
import pandas as pd
from datetime import datetime

class ViewTransformer:
    def __init__(self, source: np.ndarray, target: np.ndarray):
        source = source.astype(np.float32)
        target = target.astype(np.float32)
        self.m = cv2.getPerspectiveTransform(source, target)

    def transform_points(self, points: np.ndarray) -> np.ndarray:
        if points.size == 0:
            return points
        reshaped_points = points.reshape(-1, 1, 2).astype(np.float32)
        transformed_points = cv2.perspectiveTransform(reshaped_points, self.m)
        return transformed_points.reshape(-1, 2)

def process_video(input_video_path, output_video_path, output_excel_path):
    CONFIDENCE_THRESHOLD = 0.3
    IOU_THRESHOLD = 0.5
    MODEL_RESOLUTION = 1280
    SELECTED_CLASSES = ['car', 'motorcycle', 'bus', 'truck']
    MIN_FRAMES_FOR_SPEED = 5

    SOURCE_POINTS = np.array([[1252, 787], [2298, 803], [5039, 2159], [-550, 2159]])
    TARGET_POINTS = np.array([[0, 0], [25, 0], [25, 250], [0, 250]])

    model = YOLO('yolov8x.pt')
    class_names = model.model.names
    selected_class_ids = [k for k, v in class_names.items() if v in SELECTED_CLASSES]

    color_mapping = {
        'car': (0, 255, 0),
        'motorcycle': (255, 0, 0),
        'bus': (0, 0, 255),
        'truck': (0, 255, 255)
    }

    coordinates = defaultdict(lambda: deque(maxlen=30))
    vehicle_data = []

    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file {input_video_path}")

    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H264 codec for browser compatibility

    video_info = sv.VideoInfo.from_video_path(input_video_path)
    out = cv2.VideoWriter(output_video_path, fourcc, video_info.fps, video_info.resolution_wh)

    byte_tracker = sv.ByteTrack(frame_rate=video_info.fps)
    view_transformer = ViewTransformer(source=SOURCE_POINTS, target=TARGET_POINTS)

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for frame_idx in tqdm(range(frame_count), desc="Processing frames"):
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, imgsz=MODEL_RESOLUTION, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(results)

        detections = detections[detections.confidence > CONFIDENCE_THRESHOLD]
        detections = detections[np.isin(detections.class_id, selected_class_ids)]
        detections = detections.with_nms(IOU_THRESHOLD)

        detections = byte_tracker.update_with_detections(detections)

        points = detections.get_anchors_coordinates(sv.Position.BOTTOM_CENTER)
        transformed_points = view_transformer.transform_points(points)

        speeds = []
        for tracker_id, (x, y), class_id in zip(detections.tracker_id, transformed_points, detections.class_id):
            coordinates[tracker_id].append((frame_idx, y))
            speed = 0
            distance = 0

            if len(coordinates[tracker_id]) >= MIN_FRAMES_FOR_SPEED:
                oldest_frame, oldest_y = coordinates[tracker_id][0]
                newest_frame, newest_y = coordinates[tracker_id][-1]

                distance = abs(newest_y - oldest_y)
                frames_passed = newest_frame - oldest_frame
                time_elapsed = frames_passed / video_info.fps

                if time_elapsed > 0:
                    speed = (distance / time_elapsed) * 3.6

            speeds.append(speed)

            class_name = class_names[class_id]
            vehicle_data.append({
                'frame_id': frame_idx,
                'tracker_id': int(tracker_id),
                'vehicle_type': class_name,
                'speed': speed,
                'distance': distance,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

        annotated_frame = frame.copy()
        for (tracker_id, (x, y), speed, class_id) in zip(detections.tracker_id, transformed_points, speeds, detections.class_id):
            box = detections.xyxy[detections.tracker_id == tracker_id]
            if box.size > 0:
                x1, y1, x2, y2 = box[0]

                text_position = (int(x1), int(y1) - 10)
                class_name = class_names[class_id]
                output_string = f"{class_name} ID:{tracker_id}, spd:{int(speed)} km/h, dis:{distance:.1f} m"
                cv2.putText(annotated_frame, output_string, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                color = color_mapping.get(class_name, (255, 255, 255))
                cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)

        out.write(annotated_frame)

    cap.release()
    out.release()

    try:
        df = pd.DataFrame(vehicle_data)
        df.to_excel(output_excel_path, index=False, engine='openpyxl')
        print(f"Data exported successfully to {output_excel_path}")
    except Exception as e:
        print(f"Error exporting data: {e}")