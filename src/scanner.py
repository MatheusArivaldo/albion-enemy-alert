import cv2
import numpy as np
import threading
from time import sleep
from utils import resource_path
from window_capture import WindowCapture

class Scanner():
    def __init__(self, monitor, reference_image_path, onScannerFound, onScannerNotFound):
        self.window_capture = WindowCapture(monitor)
        self.reference_image_path = reference_image_path
        self.onScannerFound = onScannerFound
        self.onScannerNotFound = onScannerNotFound
        self.running = False
        self.thread = None

    def load_reference_image(self, image_path):
        reference_image = cv2.imread(resource_path(image_path))
        if reference_image is None:
            raise ValueError(f"Could not load image from {image_path}")
        print("Reference image loaded")
        return reference_image

    def scan(self):
        while self.running:
            try:
                print("Scanning...")
                screenshot_image = self.window_capture.get_screenshot()

                screenshot = cv2.cvtColor(np.array(screenshot_image), cv2.COLOR_RGB2BGR)
                reference_image = self.load_reference_image(resource_path(self.reference_image_path))

                orb = cv2.ORB_create()

                kp1, des1 = orb.detectAndCompute(reference_image, None)
                kp2, des2 = orb.detectAndCompute(screenshot, None)

                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(des1, des2)

                matches = sorted(matches, key=lambda x: x.distance)

                if len(matches) > 0:
                    print("Scanner found")
                    self.onScannerFound()
                else:
                    print("Scanner not found")
                    self.onScannerNotFound()

                sleep(1)  # Prevent excessive CPU usage

            except Exception as e:
                print(f"Error during image detection: {str(e)}")

    def start(self):
        """Starts the scanning in a background thread."""
        if self.thread is None or not self.thread.is_alive():
            self.running = True
            self.thread = threading.Thread(target=self.scan, daemon=True)
            self.thread.start()
            print("Scanner started in background thread")

    def stop(self):
        """Stops the scanning thread."""
        self.running = False
        if self.thread:
            self.thread.join()
            print("Scanner stopped")
