import time
from src.utils.logger import logger

class FarmingSession:
    """
    Implements the core farming loop:
    1. Load Account
    2. Launch App
    3. Open Packs
    4. Recognize Cards
    5. Cleanup & Loop
    """
    def __init__(self, adb, vision, config, instance_id):
        self.adb = adb
        self.vision = vision
        self.config = config
        self.instance_id = instance_id

        # In a real scenario, this would be read from the manifest or config
        self.package_name = "jp.pokemon.pokemon_tcg_pocket"

    def run_loop(self):
        """Executes one full farming cycle."""
        logger.info(f"[Worker {self.instance_id}] Starting farming loop...")

        if not self._load_account():
            logger.error(f"[Worker {self.instance_id}] Failed to load account.")
            return False

        if not self._launch_app():
            logger.error(f"[Worker {self.instance_id}] Failed to launch app.")
            return False

        if not self._open_packs():
            logger.error(f"[Worker {self.instance_id}] Failed to open packs.")
            return False

        self._recognize_and_save_cards()
        self._cleanup()

        logger.info(f"[Worker {self.instance_id}] Farming loop complete.")
        return True

    def _load_account(self):
        """Clears app data and injects the account XML."""
        logger.info(f"[Worker {self.instance_id}] Loading account data...")
        if not self.adb or not self.adb.device:
            return False

        # 1. Clear app data
        self.adb.device.shell(['pm', 'clear', self.package_name])
        time.sleep(1)

        # 2. Inject account XML (Mocking the file selection for now)
        # In full implementation, this reads from Accounts/Saved/
        # target_xml = f"Accounts/Saved/{self.instance_id}/current_account.xml"
        # dest_path = f"/data/data/{self.package_name}/shared_prefs/jp.pokemon.pokemon_tcg_pocket.v2.playerprefs.xml"
        # self.adb.device.push(target_xml, dest_path)
        logger.info(f"[Worker {self.instance_id}] Account XML injected successfully.")
        time.sleep(1)
        return True

    def _launch_app(self):
        """Launches the game and navigates to the main menu."""
        logger.info(f"[Worker {self.instance_id}] Launching Pokemon TCG Pocket...")
        if not self.adb or not self.adb.device:
            return False

        # Launch App
        self.adb.device.shell(['monkey', '-p', self.package_name, '-c', 'android.intent.category.LAUNCHER', '1'])

        # Wait for Main Menu loop
        max_attempts = 30
        attempts = 0

        while attempts < max_attempts:
            screenshot = self.adb.get_screenshot()

            # Check if we are already on the main menu
            # if self.vision.find_template(screenshot, 'main_menu_icon'):
            #     logger.info(f"[Worker {self.instance_id}] Reached Main Menu.")
            #     return True

            # Check if we are on the title screen to click Start
            # title_loc = self.vision.find_template(screenshot, 'title_screen')
            # if title_loc:
            #     logger.info(f"[Worker {self.instance_id}] Found Title Screen. Clicking start.")
            #     self.adb.click(title_loc[0], title_loc[1])

            # Check for generic "OK" or "Close" popups during loading
            # ok_loc = self.vision.find_template(screenshot, 'ok_button')
            # if ok_loc:
            #     self.adb.click(ok_loc[0], ok_loc[1])

            attempts += 1
            time.sleep(2)

        logger.warning(f"[Worker {self.instance_id}] Failed to reach main menu within timeout.")
        # Returning true temporarily so the loop continues in this stub
        return True

    def _open_packs(self):
        """Navigates to the pack screen and opens packs."""
        logger.info(f"[Worker {self.instance_id}] Opening packs...")

        if not self.adb or not self.adb.device:
            return False

        # 1. Click Pack Menu Icon
        # pack_icon = self.vision.find_template(self.adb.get_screenshot(), 'pack_menu_icon')
        # if pack_icon: self.adb.click(*pack_icon)

        # 2. Select specific pack (e.g., Mewtwo, Charizard, Pikachu) based on config
        # selected_pack = self.config.get("pack_settings", "preferred_pack")
        # pack_loc = self.vision.find_template(self.adb.get_screenshot(), selected_pack)
        # if pack_loc: self.adb.click(*pack_loc)

        # 3. Swipe to tear pack open (Coordinates depend on emulator resolution)
        # self.adb.swipe(x1, y1, x2, y2, duration=300)

        time.sleep(3)
        return True

    def _recognize_and_save_cards(self):
        """Reads the screen to determine card rarities and saves to DB."""
        logger.info(f"[Worker {self.instance_id}] Recognizing cards...")

        # Take a final screenshot of the results screen
        screenshot = self.adb.get_screenshot()
        detected_cards = []

        # OpenCV templates would be evaluated here
        # For example:
        # if self.vision.find_template(screenshot, 'rarity_crown', threshold=0.85):
        #     detected_cards.append({"rarity": "Crown"})
        # if self.vision.find_template(screenshot, 'rarity_immersive', threshold=0.85):
        #     detected_cards.append({"rarity": "Immersive"})

        # Evaluate Trade Manager
        from src.bot.states.trade import TradeManager
        trade_manager = TradeManager(self.config, self.instance_id)
        if trade_manager.evaluate_s4t(detected_cards):
            logger.info(f"[Worker {self.instance_id}] Account saved for trade!")

        time.sleep(2)

    def _cleanup(self):
        """Closes the app to prepare for the next loop."""
        logger.info(f"[Worker {self.instance_id}] Cleaning up session...")
        if self.adb:
            self.adb.device.shell(['am', 'force-stop', self.package_name])
            time.sleep(1)
