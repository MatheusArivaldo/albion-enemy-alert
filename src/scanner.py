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

    def filter_red_color(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 100, 100])   # Ajuste esses valores para a faixa exata da cor vermelha
        upper_red = np.array([10, 255, 255])  # Pode precisar de ajustes
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        lower_red2 = np.array([170, 100, 100])  # Tons mais escuros de vermelho
        upper_red2 = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

        mask = mask1 | mask2
        result = cv2.bitwise_and(image, image, mask=mask)
        return result

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

                screenshot_filtered = self.filter_red_color(screenshot)
                reference_image_filtered = self.filter_red_color(reference_image)

                result = cv2.matchTemplate(screenshot_filtered, reference_image_filtered, cv2.TM_CCOEFF_NORMED)

                # draw the rectangle on the screenshot
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                top_left = max_loc
                bottom_right = (top_left[0] + reference_image.shape[1], top_left[1] + reference_image.shape[0])
                cv2.rectangle(reference_image_filtered, top_left, bottom_right, (0, 255, 0), 2)

                cv2.imshow("Result", screenshot_filtered)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                print(f"Scanned")

                locations = np.where(result >= 0.7)

                if locations[0].size > 0:
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
