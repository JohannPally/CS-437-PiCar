import argparse
import sys
import time

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

class Vision:
    
    def __init__(self):
        
        model='efficientdet_lite0.tflite'
        camera_id=0
        width=640
        height=480
        num_threads=4
        enable_edgetpu=False
        
        # Variables to calculate FPS
        self.counter, self.fps = 0, 30
        self.start_time = time.time()

        # Start capturing video input from the camera
        self.cap = cv2.VideoCapture(-1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # Visualization parameters
        self.row_size = 20  # pixels
        self.left_margin = 24  # pixels
        self.text_color = (0, 0, 255)  # red
        self.font_size = 1
        self.font_thickness = 1
        self.fps_avg_frame_count = 10

        # Initialize the object detection model
        base_options = core.BaseOptions(
          file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
        detection_options = processor.DetectionOptions(
          max_results=3, score_threshold=0.3)
        options = vision.ObjectDetectorOptions(
          base_options=base_options, detection_options=detection_options)
        self.detector = vision.ObjectDetector.create_from_options(options)

    def check_stop_sign(self):
        time_check = time.time()
        while(time.time()-time_check < 1):
            success, image = self.cap.read()
            if not success:
              sys.exit(
                  'ERROR: Unable to read from webcam. Please verify your webcam settings.'
              )

            self.counter += 1
            image = cv2.flip(image, 1)

            # Convert the image from BGR to RGB as required by the TFLite model.
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Create a TensorImage object from the RGB image.
            input_tensor = vision.TensorImage.create_from_array(rgb_image)

            # Run object detection estimation using the model.
            detection_result = self.detector.detect(input_tensor)

            # Draw keypoints and edges on input image
            image = utils.visualize(image, detection_result)

            #print('detections', detection_result.detections)
            for detection in detection_result.detections:
                object_name = detection.categories[0].category_name
                #print(object_name)
                if object_name == 'stop sign':
                    print('found stop sign')
                    return True

            # Calculate the FPS
            if self.counter % self.fps_avg_frame_count == 0:
              end_time = time.time()
              self.fps = self.fps_avg_frame_count / (end_time - self.start_time)
              self.start_time = time.time()

            # Show the FPS
            self.fps_text = 'FPS = {:.1f}'.format(self.fps)
            text_location = (self.left_margin, self.row_size)
            cv2.putText(image, self.fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                        self.font_size, self.text_color, self.font_thickness)

            # Stop the program if the ESC key is pressed.
            cv2.imshow('object_detector', image)
        return False