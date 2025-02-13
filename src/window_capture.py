from PIL import Image
import mss

class WindowCapture():
    def __init__(self, monitor):
        self.monitor = monitor

    def get_screenshot(self):
        with mss.mss() as sct:
            screenshot = sct.grab(sct.monitors[1])  # Capture first monitor
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)  # Convert to PIL Image
            print("Captured screenshot")
            return img
