import time
import multiprocessing
from src.utils.logger import logger
from src.core.adb import ADBController
from src.core.vision import VisionEngine

class BotWorker(multiprocessing.Process):
    def __init__(self, instance_id, config, command_queue, event_queue):
        super().__init__()
        self.instance_id = instance_id
        self.config = config
        self.command_queue = command_queue
        self.event_queue = event_queue
        self.running = True

        # We don't initialize ADB/Vision here because multiprocessing
        # requires initialization inside the run() method for fork safety.
        self.adb = None
        self.vision = None

    def setup(self):
        """Initialize resources specific to this worker process."""
        logger.info(f"[Worker {self.instance_id}] Initializing ADB and Vision...")

        from src.core.emulators import EmulatorManager

        # Connect to OS-specific emulator
        emulator_type = EmulatorManager.get_default_emulator()
        serial = None

        if emulator_type == "mumu":
            serial = EmulatorManager.connect_mumu(self.instance_id)
        elif emulator_type == "waydroid":
            serial = EmulatorManager.connect_waydroid()

        self.adb = ADBController(serial=serial)
        self.vision = VisionEngine()
        # TODO: self.vision.load_template('pack_button', 'pack.png')

    def run(self):
        """The main loop for this bot instance."""
        logger.info(f"[Worker {self.instance_id}] Process started.")
        self.setup()

        while self.running:
            # 1. Check for incoming commands (Pause, Stop, etc)
            self._process_commands()
            if not self.running:
                break

            # 2. Execute Bot Logic Iteration
            self._do_bot_iteration()

            # Small sleep to prevent CPU hogging
            time.sleep(1)

        logger.info(f"[Worker {self.instance_id}] Process terminated.")

    def _process_commands(self):
        """Poll the queue for commands from the manager/GUI."""
        try:
            while not self.command_queue.empty():
                cmd = self.command_queue.get_nowait()
                if cmd.get("action") == "stop":
                    logger.info(f"[Worker {self.instance_id}] Received STOP command.")
                    self.running = False
        except Exception as e:
            logger.error(f"[Worker {self.instance_id}] Error reading command: {e}")

    def _do_bot_iteration(self):
        """A single pass of the bot's state machine."""
        # For phase 4 demonstration, we just log and send a heartbeat event.
        logger.debug(f"[Worker {self.instance_id}] Executing bot iteration...")

        # Example of sending data back to the GUI
        self.event_queue.put({
            "source": self.instance_id,
            "type": "heartbeat",
            "message": "Alive and checking packs."
        })

        # TODO: Implement actual state machine:
        # - Check if on main menu
        # - Click pack
        # - Swipe to open
        # - Check for Save For Trade (S4T)
        # - Reroll if needed
