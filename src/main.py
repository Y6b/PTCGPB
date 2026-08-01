import multiprocessing
import sys
import logging

# Configure basic logging for the main process
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Main")

def run_gui(command_queue, event_queue):
    """
    Entry point for the GUI process.
    It will run the CustomTkinter main loop.
    """
    logger.info("Starting GUI...")

    # CustomTkinter needs to run in the main thread (especially on macOS).
    # Import inside the function to avoid premature initialization issues.
    from src.gui.app import App

    app = App(command_queue=command_queue, event_queue=event_queue)

    # Setup a periodic check of the event_queue so the GUI can respond to bot workers
    def check_events():
        try:
            while not event_queue.empty():
                event = event_queue.get_nowait()
                logger.info(f"GUI received event: {event}")
        except Exception:
            pass
        finally:
            app.after(100, check_events)

    app.after(100, check_events)

    # Simple message router for commands coming from GUI
    from src.bot.manager import BotManager
    bot_manager = BotManager(app.config_manager, event_queue)

    def check_commands():
        try:
            while not command_queue.empty():
                cmd = command_queue.get_nowait()
                if cmd.get("action") == "start":
                    bot_manager.start_all()
                elif cmd.get("action") == "stop":
                    bot_manager.stop_all()
        except Exception:
            pass
        finally:
            app.after(100, check_commands)

    app.after(100, check_commands)

    try:
        app.mainloop()
    except KeyboardInterrupt:
        logger.info("GUI process interrupted.")

def run_bot_worker(instance_id, command_queue, event_queue):
    """
    Entry point for a bot worker process.
    Handles ADB interactions and OpenCV processing for a specific emulator instance.
    """
    logger.info(f"Starting Bot Worker for instance {instance_id}...")
    # TODO: Initialize ADB connection and start bot logic

    import time
    # Placeholder for bot loop
    try:
        while True:
            # Poll for commands from the GUI, perform bot actions, send events back
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info(f"Bot Worker {instance_id} interrupted.")

def main():
    logger.info("Initializing PTCGP Bot (Python Port)...")

    # Multiprocessing context (using spawn for cross-platform compatibility)
    ctx = multiprocessing.get_context('spawn')

    # Queues for IPC between GUI and bot workers
    gui_to_bot_queue = ctx.Queue()
    bot_to_gui_queue = ctx.Queue()

    # In a real scenario, the GUI would spawn bot workers based on configuration.
    # For architectural demonstration, we just define the structure here.

    # For now, we will just launch the GUI. The GUI itself might manage the worker processes later.
    # Or, we can start the GUI in the main thread so macOS/CustomTkinter is happy.

    # NOTE: Tkinter (and CustomTkinter) often requires being on the main thread,
    # especially on macOS. So it's best to run the GUI loop in the main process,
    # and spawn workers from here.

    logger.info("Ready to launch GUI in main thread.")
    run_gui(gui_to_bot_queue, bot_to_gui_queue)

if __name__ == '__main__':
    main()
