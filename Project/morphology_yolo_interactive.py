"""
🔬 Interactive Computer Vision Demo
Combining Mathematical Morphology, Image Filtering & YOLO Object Detection

Features:
- Real-time webcam or image processing
- Mathematical morphology operations
- Image filtering (Gaussian, Bilateral, Median, etc.)
- YOLO v8 object detection
- Interactive parameter controls
- Side-by-side comparisons
"""

import cv2
import numpy as np
from ultralytics import YOLO
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
from typing import Optional, Tuple, Dict
from dataclasses import dataclass
import time


@dataclass
class ProcessingConfig:
    """Configuration for image processing parameters"""
    # Morphology
    morph_operation: str = "None"
    morph_kernel_size: int = 5
    morph_kernel_shape: str = "Rectangle"
    morph_iterations: int = 1
    
    # Filtering
    filter_type: str = "None"
    gaussian_kernel: int = 5
    bilateral_d: int = 9
    bilateral_sigma_color: int = 75
    bilateral_sigma_space: int = 75
    median_kernel: int = 5
    
    # Detection
    use_yolo: bool = False
    yolo_confidence: float = 0.5
    yolo_model: str = "yolov8n.pt"
    
    # Display
    show_original: bool = True
    show_processed: bool = True
    show_detected: bool = True


class MorphologyYOLOApp:
    """Main application class for interactive CV demo"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔬 Morphology + Filtering + YOLO Interactive Demo")
        self.root.geometry("1600x900")
        
        # Initialize configuration
        self.config = ProcessingConfig()
        
        # Video/Image source
        self.camera = None
        self.current_frame = None
        self.is_running = False
        self.use_webcam = False
        
        # YOLO model
        self.yolo_model: Optional[YOLO] = None
        self.yolo_loaded = False
        
        # Processing state
        self.processing_thread = None
        self.fps = 0
        self.last_time = time.time()
        
        # Create UI
        self.create_ui()
        
        # Load YOLO model in background
        self.load_yolo_model()
    
    def create_ui(self):
        """Create the user interface"""
        
        # ============ TOP MENU ============
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(menu_frame, text="📁 Load Image", 
                  command=self.load_image).pack(side=tk.LEFT, padx=2)
        ttk.Button(menu_frame, text="📹 Start Webcam", 
                  command=self.start_webcam).pack(side=tk.LEFT, padx=2)
        ttk.Button(menu_frame, text="⏹️ Stop", 
                  command=self.stop_processing).pack(side=tk.LEFT, padx=2)
        ttk.Button(menu_frame, text="💾 Save Result", 
                  command=self.save_results).pack(side=tk.LEFT, padx=2)
        
        self.status_label = ttk.Label(menu_frame, text="Status: Ready", 
                                     font=("Arial", 10, "bold"))
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
        # ============ MAIN CONTAINER ============
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # LEFT PANEL - Controls
        control_panel = self.create_control_panel()
        main_container.add(control_panel)
        
        # RIGHT PANEL - Display
        display_panel = self.create_display_panel()
        main_container.add(display_panel, weight=3)
    
    def create_control_panel(self):
        """Create control panel with all parameters"""
        
        panel = ttk.Frame(self.root, width=300)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(panel)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Morphology
        morph_tab = self.create_morphology_tab(notebook)
        notebook.add(morph_tab, text="🔧 Morphology")
        
        # Tab 2: Filtering
        filter_tab = self.create_filtering_tab(notebook)
        notebook.add(filter_tab, text="🎨 Filters")
        
        # Tab 3: YOLO Detection
        yolo_tab = self.create_yolo_tab(notebook)
        notebook.add(yolo_tab, text="🎯 Detection")
        
        # Tab 4: Display Options
        display_tab = self.create_display_tab(notebook)
        notebook.add(display_tab, text="📊 Display")
        
        return panel
    
    def create_morphology_tab(self, parent):
        """Create morphology controls tab"""
        
        frame = ttk.Frame(parent)
        
        # Operation selection
        ttk.Label(frame, text="Morphological Operation:", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        operations = ["None", "Erosion", "Dilation", "Opening", "Closing", 
                     "Gradient", "Top Hat", "Black Hat"]
        morph_var = tk.StringVar(value=self.config.morph_operation)
        morph_combo = ttk.Combobox(frame, textvariable=morph_var, 
                                   values=operations, state="readonly")
        morph_combo.pack(fill=tk.X, padx=10)
        morph_combo.bind("<<ComboboxSelected>>", 
                        lambda e: self.update_morph_operation(morph_var.get()))
        
        # Kernel shape
        ttk.Label(frame, text="\nKernel Shape:", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        shapes = ["Rectangle", "Ellipse", "Cross"]
        shape_var = tk.StringVar(value=self.config.morph_kernel_shape)
        shape_combo = ttk.Combobox(frame, textvariable=shape_var, 
                                   values=shapes, state="readonly")
        shape_combo.pack(fill=tk.X, padx=10)
        shape_combo.bind("<<ComboboxSelected>>", 
                        lambda e: self.update_morph_shape(shape_var.get()))
        
        # Kernel size
        ttk.Label(frame, text="\nKernel Size:", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        size_var = tk.IntVar(value=self.config.morph_kernel_size)
        size_scale = ttk.Scale(frame, from_=3, to=21, variable=size_var,
                              orient=tk.HORIZONTAL, 
                              command=lambda v: self.update_morph_size(int(float(v))))
        size_scale.pack(fill=tk.X, padx=10)
        
        size_label = ttk.Label(frame, text=f"{self.config.morph_kernel_size}x{self.config.morph_kernel_size}")
        size_label.pack()
        
        # Store label reference for updates
        size_scale.config(command=lambda v: self.update_size_label(int(float(v)), size_label))
        
        # Iterations
        ttk.Label(frame, text="\nIterations:", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        iter_var = tk.IntVar(value=self.config.morph_iterations)
        iter_scale = ttk.Scale(frame, from_=1, to=10, variable=iter_var,
                              orient=tk.HORIZONTAL,
                              command=lambda v: self.update_iterations(int(float(v))))
        iter_scale.pack(fill=tk.X, padx=10)
        
        iter_label = ttk.Label(frame, text=f"{self.config.morph_iterations}")
        iter_label.pack()
        
        iter_scale.config(command=lambda v: self.update_iter_label(int(float(v)), iter_label))
        
        # Info box
        info_text = """
        📚 Morphology Operations:
        
        • Erosion: Shrinks objects
        • Dilation: Expands objects
        • Opening: Remove noise
        • Closing: Fill holes
        • Gradient: Edge detection
        • Top Hat: Extract bright details
        • Black Hat: Extract dark details
        """
        
        info_box = tk.Text(frame, height=12, wrap=tk.WORD, 
                          bg="#f0f0f0", font=("Arial", 8))
        info_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        info_box.insert("1.0", info_text)
        info_box.config(state=tk.DISABLED)
        
        return frame
    
    def create_filtering_tab(self, parent):
        """Create filtering controls tab"""
        
        frame = ttk.Frame(parent)
        
        # Filter selection
        ttk.Label(frame, text="Filter Type:", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        filters = ["None", "Gaussian", "Bilateral", "Median", "Mean", 
                  "Laplacian", "Sobel", "Canny"]
        filter_var = tk.StringVar(value=self.config.filter_type)
        filter_combo = ttk.Combobox(frame, textvariable=filter_var, 
                                    values=filters, state="readonly")
        filter_combo.pack(fill=tk.X, padx=10)
        filter_combo.bind("<<ComboboxSelected>>", 
                         lambda e: self.update_filter_type(filter_var.get()))
        
        # Gaussian kernel
        ttk.Label(frame, text="\nGaussian Kernel Size:", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        gauss_var = tk.IntVar(value=self.config.gaussian_kernel)
        gauss_scale = ttk.Scale(frame, from_=1, to=31, variable=gauss_var,
                               orient=tk.HORIZONTAL,
                               command=lambda v: self.update_gaussian(int(float(v))))
        gauss_scale.pack(fill=tk.X, padx=10)
        
        gauss_label = ttk.Label(frame, text=f"{self.config.gaussian_kernel}")
        gauss_label.pack()
        
        gauss_scale.config(command=lambda v: self.update_gauss_label(int(float(v)), gauss_label))
        
        # Bilateral filter parameters
        ttk.Label(frame, text="\nBilateral - Sigma Color:", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        bil_color_var = tk.IntVar(value=self.config.bilateral_sigma_color)
        bil_color_scale = ttk.Scale(frame, from_=10, to=200, variable=bil_color_var,
                                   orient=tk.HORIZONTAL,
                                   command=lambda v: self.update_bilateral_color(int(float(v))))
        bil_color_scale.pack(fill=tk.X, padx=10)
        
        bil_color_label = ttk.Label(frame, text=f"{self.config.bilateral_sigma_color}")
        bil_color_label.pack()
        
        bil_color_scale.config(command=lambda v: self.update_bil_color_label(int(float(v)), bil_color_label))
        
        # Info box
        info_text = """
        🎨 Filtering Operations:
        
        • Gaussian: Smooth + blur
        • Bilateral: Smooth while preserving edges
        • Median: Remove salt-pepper noise
        • Mean: Simple averaging
        • Laplacian: Edge enhancement
        • Sobel: Gradient detection
        • Canny: Edge detection
        """
        
        info_box = tk.Text(frame, height=10, wrap=tk.WORD, 
                          bg="#f0f0f0", font=("Arial", 8))
        info_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        info_box.insert("1.0", info_text)
        info_box.config(state=tk.DISABLED)
        
        return frame
    
    def create_yolo_tab(self, parent):
        """Create YOLO detection controls tab"""
        
        frame = ttk.Frame(parent)
        
        # Enable YOLO checkbox
        yolo_var = tk.BooleanVar(value=self.config.use_yolo)
        yolo_check = ttk.Checkbutton(frame, text="Enable YOLO Detection", 
                                     variable=yolo_var,
                                     command=lambda: self.toggle_yolo(yolo_var.get()))
        yolo_check.pack(pady=10)
        
        # Model selection
        ttk.Label(frame, text="YOLO Model:", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        models = ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt"]
        model_var = tk.StringVar(value=self.config.yolo_model)
        model_combo = ttk.Combobox(frame, textvariable=model_var, 
                                   values=models, state="readonly")
        model_combo.pack(fill=tk.X, padx=10)
        model_combo.bind("<<ComboboxSelected>>", 
                        lambda e: self.update_yolo_model(model_var.get()))
        
        # Confidence threshold
        ttk.Label(frame, text="\nConfidence Threshold:", 
                 font=("Arial", 10, "bold")).pack(pady=5)
        
        conf_var = tk.DoubleVar(value=self.config.yolo_confidence)
        conf_scale = ttk.Scale(frame, from_=0.1, to=1.0, variable=conf_var,
                              orient=tk.HORIZONTAL,
                              command=lambda v: self.update_yolo_conf(float(v)))
        conf_scale.pack(fill=tk.X, padx=10)
        
        conf_label = ttk.Label(frame, text=f"{self.config.yolo_confidence:.2f}")
        conf_label.pack()
        
        conf_scale.config(command=lambda v: self.update_conf_label(float(v), conf_label))
        
        # YOLO status
        self.yolo_status_label = ttk.Label(frame, text="YOLO Status: Loading...", 
                                          font=("Arial", 9), foreground="orange")
        self.yolo_status_label.pack(pady=10)
        
        # Info box
        info_text = """
        🎯 YOLO Detection:
        
        YOLOv8 can detect 80 object classes including:
        
        • People, animals
        • Vehicles (car, truck, bus, etc.)
        • Common objects (bottle, cup, etc.)
        • Electronics, furniture
        • And much more!
        
        Lower models (n, s) are faster
        Higher models (m, l) are more accurate
        """
        
        info_box = tk.Text(frame, height=15, wrap=tk.WORD, 
                          bg="#f0f0f0", font=("Arial", 8))
        info_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        info_box.insert("1.0", info_text)
        info_box.config(state=tk.DISABLED)
        
        return frame
    
    def create_display_tab(self, parent):
        """Create display options tab"""
        
        frame = ttk.Frame(parent)
        
        ttk.Label(frame, text="Display Options:", 
                 font=("Arial", 10, "bold")).pack(pady=10)
        
        # Checkboxes for display panels
        orig_var = tk.BooleanVar(value=self.config.show_original)
        ttk.Checkbutton(frame, text="Show Original", 
                       variable=orig_var,
                       command=lambda: self.toggle_display('original', orig_var.get())).pack(anchor=tk.W, padx=20)
        
        proc_var = tk.BooleanVar(value=self.config.show_processed)
        ttk.Checkbutton(frame, text="Show Processed", 
                       variable=proc_var,
                       command=lambda: self.toggle_display('processed', proc_var.get())).pack(anchor=tk.W, padx=20)
        
        det_var = tk.BooleanVar(value=self.config.show_detected)
        ttk.Checkbutton(frame, text="Show Detection", 
                       variable=det_var,
                       command=lambda: self.toggle_display('detected', det_var.get())).pack(anchor=tk.W, padx=20)
        
        # FPS display
        ttk.Label(frame, text="\nPerformance:", 
                 font=("Arial", 10, "bold")).pack(pady=10)
        
        self.fps_label = ttk.Label(frame, text="FPS: 0", font=("Arial", 12))
        self.fps_label.pack(pady=5)
        
        # Keyboard shortcuts info
        shortcuts_text = """
        ⌨️ Keyboard Shortcuts:
        
        • Space: Pause/Resume
        • S: Save screenshot
        • R: Reset parameters
        • Q: Quit
        • 1-7: Quick filter switch
        • M: Cycle morphology ops
        """
        
        shortcuts_box = tk.Text(frame, height=10, wrap=tk.WORD, 
                               bg="#f0f0f0", font=("Arial", 8))
        shortcuts_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        shortcuts_box.insert("1.0", shortcuts_text)
        shortcuts_box.config(state=tk.DISABLED)
        
        return frame
    
    def create_display_panel(self):
        """Create image display panel"""
        
        panel = ttk.Frame(self.root)
        
        # Create canvas for images
        self.canvas_frame = ttk.Frame(panel)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Three image panels (Original, Processed, Detected)
        self.canvases = {}
        titles = ["Original", "Processed (Morph + Filter)", "YOLO Detection"]
        
        for i, title in enumerate(titles):
            col_frame = ttk.LabelFrame(self.canvas_frame, text=title)
            col_frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            
            canvas = tk.Canvas(col_frame, bg="black", width=400, height=400)
            canvas.pack(fill=tk.BOTH, expand=True)
            
            self.canvases[title] = canvas
        
        # Configure grid weights for responsive resizing
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(1, weight=1)
        self.canvas_frame.grid_columnconfigure(2, weight=1)
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        
        return panel
    
    # ========== UI Callback Methods ==========
    
    def update_morph_operation(self, op):
        self.config.morph_operation = op
    
    def update_morph_shape(self, shape):
        self.config.morph_kernel_shape = shape
    
    def update_morph_size(self, size):
        # Ensure odd number
        if size % 2 == 0:
            size += 1
        self.config.morph_kernel_size = size
    
    def update_size_label(self, size, label):
        if size % 2 == 0:
            size += 1
        self.config.morph_kernel_size = size
        label.config(text=f"{size}x{size}")
    
    def update_iterations(self, iters):
        self.config.morph_iterations = iters
    
    def update_iter_label(self, iters, label):
        self.config.morph_iterations = iters
        label.config(text=f"{iters}")
    
    def update_filter_type(self, ftype):
        self.config.filter_type = ftype
    
    def update_gaussian(self, size):
        if size % 2 == 0:
            size += 1
        self.config.gaussian_kernel = size
    
    def update_gauss_label(self, size, label):
        if size % 2 == 0:
            size += 1
        self.config.gaussian_kernel = size
        label.config(text=f"{size}")
    
    def update_bilateral_color(self, val):
        self.config.bilateral_sigma_color = val
    
    def update_bil_color_label(self, val, label):
        self.config.bilateral_sigma_color = val
        label.config(text=f"{val}")
    
    def toggle_yolo(self, enabled):
        self.config.use_yolo = enabled
        if enabled and not self.yolo_loaded:
            self.load_yolo_model()
    
    def update_yolo_model(self, model):
        self.config.yolo_model = model
        self.load_yolo_model()
    
    def update_yolo_conf(self, conf):
        self.config.yolo_confidence = conf
    
    def update_conf_label(self, conf, label):
        self.config.yolo_confidence = conf
        label.config(text=f"{conf:.2f}")
    
    def toggle_display(self, panel, show):
        if panel == 'original':
            self.config.show_original = show
        elif panel == 'processed':
            self.config.show_processed = show
        elif panel == 'detected':
            self.config.show_detected = show
    
    # ========== Core Processing Methods ==========
    
    def load_yolo_model(self):
        """Load YOLO model in background thread"""
        
        def load_model():
            try:
                self.yolo_status_label.config(text="YOLO Status: Loading...", 
                                            foreground="orange")
                self.yolo_model = YOLO(self.config.yolo_model)
                self.yolo_loaded = True
                self.yolo_status_label.config(text="YOLO Status: Ready ✓", 
                                            foreground="green")
            except Exception as e:
                self.yolo_loaded = False
                self.yolo_status_label.config(text=f"YOLO Status: Error - {str(e)[:30]}", 
                                            foreground="red")
                messagebox.showerror("YOLO Error", 
                                   f"Failed to load YOLO model: {str(e)}\n\n"
                                   "Will download on first use if internet available.")
        
        threading.Thread(target=load_model, daemon=True).start()
    
    def apply_morphology(self, image: np.ndarray) -> np.ndarray:
        """Apply morphological operation"""
        
        if self.config.morph_operation == "None":
            return image
        
        # Create structuring element
        shape_map = {
            "Rectangle": cv2.MORPH_RECT,
            "Ellipse": cv2.MORPH_ELLIPSE,
            "Cross": cv2.MORPH_CROSS
        }
        
        shape = shape_map.get(self.config.morph_kernel_shape, cv2.MORPH_RECT)
        kernel = cv2.getStructuringElement(shape, 
                                           (self.config.morph_kernel_size, 
                                            self.config.morph_kernel_size))
        
        # Apply operation
        op_map = {
            "Erosion": cv2.MORPH_ERODE,
            "Dilation": cv2.MORPH_DILATE,
            "Opening": cv2.MORPH_OPEN,
            "Closing": cv2.MORPH_CLOSE,
            "Gradient": cv2.MORPH_GRADIENT,
            "Top Hat": cv2.MORPH_TOPHAT,
            "Black Hat": cv2.MORPH_BLACKHAT
        }
        
        operation = op_map.get(self.config.morph_operation)
        
        if operation in [cv2.MORPH_ERODE, cv2.MORPH_DILATE]:
            if operation == cv2.MORPH_ERODE:
                result = cv2.erode(image, kernel, iterations=self.config.morph_iterations)
            else:
                result = cv2.dilate(image, kernel, iterations=self.config.morph_iterations)
        else:
            result = cv2.morphologyEx(image, operation, kernel, 
                                     iterations=self.config.morph_iterations)
        
        return result
    
    def apply_filter(self, image: np.ndarray) -> np.ndarray:
        """Apply image filter"""
        
        if self.config.filter_type == "None":
            return image
        
        # Ensure kernel sizes are odd
        gauss_k = self.config.gaussian_kernel if self.config.gaussian_kernel % 2 == 1 else self.config.gaussian_kernel + 1
        median_k = self.config.median_kernel if self.config.median_kernel % 2 == 1 else self.config.median_kernel + 1
        
        if self.config.filter_type == "Gaussian":
            result = cv2.GaussianBlur(image, (gauss_k, gauss_k), 0)
        
        elif self.config.filter_type == "Bilateral":
            result = cv2.bilateralFilter(image, 
                                         self.config.bilateral_d,
                                         self.config.bilateral_sigma_color,
                                         self.config.bilateral_sigma_space)
        
        elif self.config.filter_type == "Median":
            result = cv2.medianBlur(image, median_k)
        
        elif self.config.filter_type == "Mean":
            result = cv2.blur(image, (gauss_k, gauss_k))
        
        elif self.config.filter_type == "Laplacian":
            # Convert to grayscale for Laplacian
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            result = np.uint8(np.absolute(laplacian))
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        
        elif self.config.filter_type == "Sobel":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            sobel = np.sqrt(sobelx**2 + sobely**2)
            result = np.uint8(sobel / sobel.max() * 255)
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        
        elif self.config.filter_type == "Canny":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            edges = cv2.Canny(gray, 50, 150)
            result = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        else:
            result = image
        
        return result
    
    def detect_objects(self, image: np.ndarray) -> np.ndarray:
        """Apply YOLO object detection"""
        
        if not self.config.use_yolo or not self.yolo_loaded:
            return image
        
        try:
            # Run YOLO inference
            results = self.yolo_model(image, conf=self.config.yolo_confidence, verbose=False)
            
            # Draw results on image
            annotated = results[0].plot()
            
            return annotated
        
        except Exception as e:
            print(f"YOLO detection error: {e}")
            return image
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Process a single frame through the pipeline"""
        
        # Original
        original = frame.copy()
        
        # Apply morphology
        processed = self.apply_morphology(frame)
        
        # Apply filter
        processed = self.apply_filter(processed)
        
        # Apply YOLO detection
        detected = self.detect_objects(frame)
        
        return original, processed, detected
    
    def display_images(self, original, processed, detected):
        """Display images on canvases"""
        
        images = {
            "Original": original if self.config.show_original else None,
            "Processed (Morph + Filter)": processed if self.config.show_processed else None,
            "YOLO Detection": detected if self.config.show_detected else None
        }
        
        for title, image in images.items():
            canvas = self.canvases[title]
            
            if image is None:
                # Clear canvas
                canvas.delete("all")
                continue
            
            # Resize to fit canvas
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:
                # Convert BGR to RGB
                if len(image.shape) == 3:
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                else:
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                
                # Resize maintaining aspect ratio
                h, w = image_rgb.shape[:2]
                scale = min(canvas_width / w, canvas_height / h)
                new_w, new_h = int(w * scale), int(h * scale)
                
                image_resized = cv2.resize(image_rgb, (new_w, new_h))
                
                # Convert to PIL Image
                pil_image = Image.fromarray(image_resized)
                photo = ImageTk.PhotoImage(pil_image)
                
                # Display on canvas
                canvas.delete("all")
                canvas.create_image(canvas_width // 2, canvas_height // 2, 
                                   image=photo, anchor=tk.CENTER)
                
                # Keep reference to prevent garbage collection
                canvas.image = photo
    
    def update_fps(self):
        """Update FPS counter"""
        current_time = time.time()
        elapsed = current_time - self.last_time
        
        if elapsed > 0:
            self.fps = 1.0 / elapsed
        
        self.last_time = current_time
        self.fps_label.config(text=f"FPS: {self.fps:.1f}")
    
    def processing_loop(self):
        """Main processing loop"""
        
        while self.is_running:
            if self.use_webcam and self.camera is not None:
                ret, frame = self.camera.read()
                if ret:
                    self.current_frame = frame
            
            if self.current_frame is not None:
                # Process frame
                original, processed, detected = self.process_frame(self.current_frame)
                
                # Display results
                self.display_images(original, processed, detected)
                
                # Update FPS
                self.update_fps()
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.01)
    
    # ========== File and Camera Operations ==========
    
    def load_image(self):
        """Load an image from file"""
        
        filepath = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                      ("All files", "*.*")]
        )
        
        if filepath:
            image = cv2.imread(filepath)
            if image is not None:
                self.current_frame = image
                self.use_webcam = False
                
                # Start processing if not already running
                if not self.is_running:
                    self.is_running = True
                    self.processing_thread = threading.Thread(target=self.processing_loop, daemon=True)
                    self.processing_thread.start()
                
                self.status_label.config(text=f"Status: Loaded {filepath.split('/')[-1]}")
            else:
                messagebox.showerror("Error", "Failed to load image")
    
    def start_webcam(self):
        """Start webcam capture"""
        
        try:
            self.camera = cv2.VideoCapture(0)
            
            if not self.camera.isOpened():
                messagebox.showerror("Error", "Cannot open webcam")
                return
            
            self.use_webcam = True
            self.is_running = True
            
            self.processing_thread = threading.Thread(target=self.processing_loop, daemon=True)
            self.processing_thread.start()
            
            self.status_label.config(text="Status: Webcam Active")
        
        except Exception as e:
            messagebox.showerror("Error", f"Webcam error: {str(e)}")
    
    def stop_processing(self):
        """Stop processing and release resources"""
        
        self.is_running = False
        
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        
        self.status_label.config(text="Status: Stopped")
    
    def save_results(self):
        """Save processed results"""
        
        if self.current_frame is None:
            messagebox.showwarning("Warning", "No image to save")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"),
                      ("JPEG files", "*.jpg"),
                      ("All files", "*.*")]
        )
        
        if filepath:
            original, processed, detected = self.process_frame(self.current_frame)
            
            # Save all three versions
            base_path = filepath.rsplit('.', 1)[0]
            ext = filepath.rsplit('.', 1)[1]
            
            cv2.imwrite(f"{base_path}_original.{ext}", original)
            cv2.imwrite(f"{base_path}_processed.{ext}", processed)
            cv2.imwrite(f"{base_path}_detected.{ext}", detected)
            
            messagebox.showinfo("Success", 
                              f"Saved 3 images:\n"
                              f"- {base_path}_original.{ext}\n"
                              f"- {base_path}_processed.{ext}\n"
                              f"- {base_path}_detected.{ext}")
    
    def cleanup(self):
        """Cleanup resources on exit"""
        
        self.stop_processing()
        cv2.destroyAllWindows()
        self.root.destroy()


# ========================================
# MAIN ENTRY POINT
# ========================================

def main():
    """Main entry point"""
    
    print("="*60)
    print("🔬 Interactive Computer Vision Demo")
    print("="*60)
    print("\nStarting application...")
    print("\nFeatures:")
    print("  ✓ Mathematical Morphology (8 operations)")
    print("  ✓ Image Filtering (8 filters)")
    print("  ✓ YOLO Object Detection")
    print("  ✓ Real-time Webcam Processing")
    print("  ✓ Interactive Parameter Control")
    print("\nLoading GUI...\n")
    
    root = tk.Tk()
    app = MorphologyYOLOApp(root)
    
    # Handle window close
    root.protocol("WM_DELETE_WINDOW", app.cleanup)
    
    root.mainloop()


if __name__ == "__main__":
    main()
