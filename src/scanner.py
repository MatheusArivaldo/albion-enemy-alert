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
        self.debug = False
        self.threshold = 0.8

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

                result = cv2.matchTemplate(screenshot, reference_image, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                if max_val > self.threshold:
                    print("Scanner found")
                    if self.onScannerFound is not None:
                        self.onScannerFound()
                else:
                    print("Scanner not found")
                    if self.onScannerNotFound is not None:
                        self.onScannerNotFound()

                sleep(1)  # Prevent excessive CPU usage

                if debug: # Display the result
                    cv2.rectangle(screenshot, max_loc, (max_loc[0] + reference_image.shape[1], max_loc[1] + reference_image.shape[0]), (0, 255, 0), 2)

                    cv2.imshow("Scanner", screenshot)

                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

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

    def set_threshold(self, threshold):
        self.threshold = threshold
