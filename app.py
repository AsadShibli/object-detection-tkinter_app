import os
import cv2
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from queue import Queue, Empty
import customtkinter as ctk
from ultralytics import YOLO
import supervision as sv

# System Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Our App Frame
app = ctk.CTk()
app.geometry("740x420")
app.title("Object Detection")

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

model = YOLO("yolov8l.pt")
names = model.model.names

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_video(filepath, filename, queue):
    try:
        cap = cv2.VideoCapture(filepath)
        if not cap.isOpened():
            queue.put(("error", "Error reading video file"))
            return

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        current_frame = 0

        w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
        output_path = os.path.join(PROCESSED_FOLDER, filename)
        video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

        while cap.isOpened():
            success, im0 = cap.read()
            if not success:
                break

            result = model(im0)[0]
            detections = sv.Detections.from_ultralytics(result)

            detections['names'] = [
                model.model.names[class_id]
                for class_id in detections.class_id
            ]

            triangle_annotator = sv.TriangleAnnotator()
            label_annotator = sv.LabelAnnotator(text_position=sv.Position.CENTER)
            annotated_frame = triangle_annotator.annotate(
                scene=im0.copy(),
                detections=detections
            )
            annotated_frame = label_annotator.annotate(
                scene=annotated_frame.copy(),
                detections=detections
            )
            video_writer.write(annotated_frame)

            current_frame += 1
            progress = (current_frame / total_frames) * 100
            queue.put(("progress", progress))

        cap.release()
        video_writer.release()

        queue.put(("complete", "File processing is completed! Please check the processed folder."))
    except Exception as e:
        queue.put(("error", str(e)))

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path and allowed_file(file_path):
        filename = os.path.basename(file_path)
        message_label.configure(text="Processing video...")
        progress_bar.set(0)
        progress_bar.pack(pady=12, padx=10)  # Show the progress bar
        processing_thread = threading.Thread(target=process_video, args=(file_path, filename, queue))
        processing_thread.start()
    else:
        messagebox.showerror("Invalid File", "Invalid file type")

def update_gui():
    try:
        while True:
            msg_type, msg_value = queue.get_nowait()
            if msg_type == "progress":
                progress_bar.set(msg_value / 100)
            elif msg_type == "complete":
                message_label.configure(text=msg_value)
                progress_bar.pack_forget()  # Hide the progress bar
            elif msg_type == "error":
                message_label.configure(text=msg_value)
                progress_bar.pack_forget()  # Hide the progress bar
    except Empty:
        pass
    app.after(100, update_gui)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

# GUI Elements
frame = ctk.CTkFrame(app)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = ctk.CTkLabel(frame, text="Object Detection", font=("Roboto", 24))
label.pack(pady=12, padx=10)

upload_button = ctk.CTkButton(frame, text="Upload Video", command=upload_file)
upload_button.pack(pady=12, padx=10)

progress_bar = ctk.CTkProgressBar(frame, orientation="horizontal", mode="determinate", width=300)
progress_bar.pack_forget()  # Initially hide the progress bar

message_label = ctk.CTkLabel(frame, text="", font=("Roboto", 14))
message_label.pack(pady=12, padx=10)

queue = Queue()

# Start the GUI update loop
app.after(100, update_gui)

# Run App
app.mainloop()
