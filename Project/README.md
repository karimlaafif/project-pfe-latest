# 🔬 Interactive Computer Vision Project

This project combines **Mathematical Morphology**, **Image Filtering**, and **YOLO Object Detection** into a single interactive application.

## 🚀 Features

### 1. Mathematical Morphology (`morphology_opencv_examples.py`)
- **Operations**: Erosion, Dilation, Opening, Closing, Gradient, Top Hat, Black Hat.
- **Interactive Controls**: Kernel shape (Rectangle, Cross, Ellipse), Kernel size (3x3 to 21x21), Iterations.
- **Real-time Visualization**: See the effect of morphological operations instantly.

### 2. Image Filtering
- **Gaussian Blur**: Smoothing and noise reduction.
- **Bilateral Filter**: Smoothing while preserving edges.
- **Median Blur**: Effective for salt-and-pepper noise.
- **Edge Detection**: Sobel and Canny edge detectors.
- **Sharpening**: Laplacian filter.

### 3. YOLO Object Detection
- **Model**: YOLOv8 (Nano, Small, Medium, Large).
- **Real-time Detection**: Detects 80 classes of objects (people, cars, etc.).
- **Confidence Control**: Adjust detection sensitivity.

## 📦 Installation

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the interactive application:
   ```bash
   python morphology_yolo_interactive.py
   ```

## 🎮 How to Use

1. **Top Menu**:
   - `Load Image`: Open an image from your computer.
   - `Start Webcam`: Use your camera for real-time processing.
   - `Save Result`: Save the current original, processed, and detected images.

2. **Control Panel (Left)**:
   - **Morphology**: Select operations like Morphological Gradient to see outlines.
   - **Filters**: Apply filters like Gaussian Blur to smooth the image before processing.
   - **Detection**: Enable YOLO to detect objects on top of the processed image.

3. **Display (Right)**:
   - View **Original**, **Processed** (Morph + Filter), and **Detected** (YOLO) images side-by-side.

## 🧩 Course Concepts Applied

- **Morphological Gradient**: Used for edge detection.
- **Opening/Closing**: Used for noise removal and hole filling.
- **Bilateral Filtering**: Advanced filtering that respects edges.
- **Deep Learning**: State-of-the-art object detection with YOLOv8.

---
*Created for the Image Processing & Computer Vision Course Project*
