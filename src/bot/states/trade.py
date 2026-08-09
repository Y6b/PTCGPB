import time
from src.utils.logger import logger

class TradeManager:
    """
    Handles Save for Trade (S4T) logic.
    Evaluates card rarities (Shinies, Crowns, Immersives)
    and saves the account for trading if criteria are met.
    """
    def __init__(self, config, instance_id):
        self.config = config
        self.instance_id = instance_id

    def evaluate_s4t(self, detected_cards):
        """
        Evaluates a list of detected cards against the S4T configuration.
        detected_cards should be a list of dictionaries with card metadata.
        Returns True if the account should be saved for trading.
        """
        if not self.config.get("save_for_trade", "enabled"):
            return False

        logger.info(f"[Worker {self.instance_id}] Evaluating S4T criteria...")

        # In actual implementation, we check config flags for:
        # s4t1Star, s4t2Star, s4t3Dmnd, s4tCrown, s4tImmersive, etc.

        save_account = False

        for card in detected_cards:
            rarity = card.get("rarity")
            if rarity == "Crown":
                logger.info(f"[Worker {self.instance_id}] Found Crown! Marking for trade.")
                save_account = True
                break
            elif rarity == "Immersive":
                logger.info(f"[Worker {self.instance_id}] Found Immersive! Marking for trade.")
                save_account = True
                break
            elif rarity == "Shiny":
                logger.info(f"[Worker {self.instance_id}] Found Shiny! Marking for trade.")
                save_account = True
                break

        if save_account:
            self._save_account_for_trade()

        return save_account

    def _save_account_for_trade(self):
        """Copies the account XML to the Trades directory and logs it."""
        logger.info(f"[Worker {self.instance_id}] Saving account XML to Trades directory...")
        # TODO: Implement actual file copy from emulator/data to Accounts/Trades
        # TODO: Fire off webhook payload to Discord
        time.sleep(1)
