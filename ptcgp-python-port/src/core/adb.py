import adbutils
import time
from src.utils.logger import logger

class ADBController:
    def __init__(self, serial=None):
        self.adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        self.serial = serial
        self.device = None

        if self.serial:
            self.connect_to_device(self.serial)

    def get_devices(self):
        """Returns a list of connected device serials."""
        return [d.serial for d in self.adb.device_list()]

    def connect_to_device(self, serial):
        """Connects to a specific device."""
        try:
            self.device = self.adb.device(serial=serial)
            self.serial = serial
            logger.info(f"Connected to ADB device: {self.serial}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to device {serial}: {e}")
            self.device = None
            return False

    def click(self, x, y):
        """Simulates a tap at (x, y)."""
        if not self.device:
            return False
        try:
            self.device.click(x, y)
            return True
        except Exception as e:
            logger.error(f"Click failed at ({x}, {y}): {e}")
            return False

    def swipe(self, x1, y1, x2, y2, duration=300):
        """Simulates a swipe from (x1, y1) to (x2, y2)."""
        if not self.device:
            return False
        try:
            self.device.swipe(x1, y1, x2, y2, duration)
            return True
        except Exception as e:
            logger.error(f"Swipe failed: {e}")
            return False

    def get_screenshot(self):
        """Captures a screenshot and returns a PIL Image."""
        if not self.device:
            return None
        try:
            return self.device.screenshot()
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return None

    def send_text(self, text):
        """Inputs text on the device."""
        if not self.device:
            return False
        try:
            self.device.shell(['input', 'text', text])
            return True
        except Exception as e:
            logger.error(f"Send text failed: {e}")
            return False
