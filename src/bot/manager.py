import multiprocessing
from src.utils.logger import logger
from src.bot.worker import BotWorker

class BotManager:
    """Orchestrates multiple bot worker processes."""
    def __init__(self, config_manager, event_queue):
        self.config_manager = config_manager
        self.event_queue = event_queue

        self.workers = {}          # instance_id -> BotWorker instance
        self.worker_queues = {}    # instance_id -> Queue for sending commands to that worker

        self.ctx = multiprocessing.get_context('spawn')

    def start_all(self):
        """Starts workers based on the current configuration."""
        instances = int(self.config_manager.get("general", "instances") or 1)
        config_snapshot = self.config_manager.config # Pass a snapshot to avoid pickling issues

        logger.info(f"BotManager starting {instances} instances...")

        for i in range(1, instances + 1):
            if i in self.workers and self.workers[i].is_alive():
                logger.warning(f"Worker {i} is already running.")
                continue

            cmd_queue = self.ctx.Queue()
            worker = BotWorker(
                instance_id=i,
                config=config_snapshot,
                command_queue=cmd_queue,
                event_queue=self.event_queue
            )

            self.workers[i] = worker
            self.worker_queues[i] = cmd_queue
            worker.start()

    def stop_all(self):
        """Sends stop commands to all running workers."""
        logger.info("BotManager stopping all instances...")
        for i, q in self.worker_queues.items():
            q.put({"action": "stop"})

        # Optional: join them
        for i, worker in self.workers.items():
            worker.join(timeout=5)
            if worker.is_alive():
                logger.warning(f"Worker {i} did not stop gracefully. Terminating.")
                worker.terminate()

        self.workers.clear()
        self.worker_queues.clear()
