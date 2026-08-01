import platform
import subprocess
from src.utils.logger import logger

class EmulatorManager:
    """Handles OS-specific emulator discovery and connection."""

    @staticmethod
    def get_default_emulator():
        """Returns the likely emulator based on the host OS."""
        os_name = platform.system()
        if os_name == "Windows" or os_name == "Darwin": # macOS
            return "mumu"
        elif os_name == "Linux":
            return "waydroid"
        return "unknown"

    @staticmethod
    def connect_mumu(instance_id=1):
        """
        Attempts to connect to MuMu Player via its local ADB port.
        Ports typically start at 7555 or 16384 and increment.
        """
        base_port = 16384 # or 7555 depending on MuMu version
        port = base_port + (instance_id - 1)
        address = f"127.0.0.1:{port}"

        try:
            logger.info(f"Attempting to connect to MuMu instance {instance_id} at {address}...")
            # Use subprocess to call adb connect
            result = subprocess.run(["adb", "connect", address], capture_output=True, text=True)
            if "connected" in result.stdout.lower() or "already" in result.stdout.lower():
                logger.info(f"Successfully connected to MuMu {instance_id}")
                return address
            else:
                logger.warning(f"Failed to connect to MuMu: {result.stdout}")
        except FileNotFoundError:
            logger.error("ADB executable not found in PATH.")
        except Exception as e:
            logger.error(f"Error connecting to MuMu: {e}")
        return None

    @staticmethod
    def connect_waydroid():
        """
        Attempts to connect to a running Waydroid session on Linux.
        Typically found at 192.168.240.112:5555
        """
        address = "192.168.240.112:5555"
        try:
            logger.info(f"Attempting to connect to Waydroid at {address}...")
            result = subprocess.run(["adb", "connect", address], capture_output=True, text=True)
            if "connected" in result.stdout.lower() or "already" in result.stdout.lower():
                logger.info("Successfully connected to Waydroid.")
                return address
            else:
                logger.warning(f"Failed to connect to Waydroid: {result.stdout}")
        except FileNotFoundError:
            logger.error("ADB executable not found in PATH.")
        except Exception as e:
            logger.error(f"Error connecting to Waydroid: {e}")
        return None
