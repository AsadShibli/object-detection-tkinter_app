# Object Detection with YOLOv8 and Tkinter

This project uses YOLOv8 for object detection in videos and provides a graphical user interface (GUI) using Tkinter and CustomTkinter. Users can upload a video file, and the application processes it to detect objects frame by frame, showing a progress bar during the process.

## Features

- Upload video files (`.mp4`, `.avi`, `.mov`, `.mkv`)
- Process videos to detect objects using YOLOv8
- Show real-time progress during video processing
- Display completion messages after processing

## Demo

## Requirements

- Python 3.7+
- Tkinter
- CustomTkinter
- OpenCV
- Ultralytics YOLO
- Supervision

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/AsadShibli/object-detection-tkinter_app.git
    cd object-detection-tkinter_app
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Ensure you have the YOLOv8 model:**

    Download the `yolov8l.pt` model from the Ultralytics website or just run ```app.py``` file,thenn place it in the same directory as your script.

## Usage

1. **Run the application:**

    ```bash
    python app.py
    ```

2. **Upload a video:**

    - Click the "Upload Video" button.
    - Select a video file (`.mp4`, `.avi`, `.mov`, `.mkv`) from your file system.

3. **Processing:**

    - The progress bar will display the processing status.
    - A message will be displayed when processing is complete.

## Project Structure
```
object-detection-tkinter_app/
│
├── uploads/ # Folder for uploaded videos
├── processed/ # Folder for processed videos
├── app.py # Main application script
├── requirements.txt # List of dependencies
└── README.md # Project README file
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Ultralytics YOLO](https://github.com/ultralytics/yolov5) for the object detection model.
- [Supervision](https://github.com/roboflow/supervision) for the annotation tools.
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the enhanced Tkinter widgets.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any improvements.

## Contact

For any questions or comments, please feel free to open an issue or contact me at [mdasadullahshibli@gmail.com](mailto:mdasadullahshibli@gmail.com).

