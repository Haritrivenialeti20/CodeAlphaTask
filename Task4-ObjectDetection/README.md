# Task 4 - Object Detection and Tracking



## Description



This project demonstrates object detection and object tracking using an AI-based computer vision model.



The project uses the DETR (DEtection TRansformer) model from Hugging Face to detect objects in images and videos. A centroid-based tracking algorithm is used to assign and maintain object IDs across video frames.



## Features



- Detect objects in images

- Draw bounding boxes around detected objects

- Display object names and confidence scores

- Track detected objects across video frames

- Assign unique IDs to tracked objects

- Save detection and tracking results



## Technologies Used



- Python

- PyTorch

- Hugging Face Transformers

- DETR (DEtection TRansformer)

- OpenCV

- Pillow

- Streamlit

- Centroid Tracking



## Project Structure



```text

Task4-ObjectDetection/

├── input/

│   ├── input.jpg

│   └── input.mp4

├── output/

│   ├── detected.jpg

│   └── tracked.mp4

├── src/

│   ├── main.py

│   ├── tracker.py

│   └── track\_video.py

├── .gitignore

├── README.md

└── requirements.txt

