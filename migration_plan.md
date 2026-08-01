# Cross-Platform Python Migration Plan for PTCGP Bot

## Overview
The goal is to port the PTCGP Bot from AutoHotkey (AHK) to a modern, cross-platform Python application. This will allow the bot to run on Windows, macOS, and Linux, supporting various Android emulators like MuMu Player and Waydroid.

## 1. Phase 1: Project Setup & Architecture Design
- **Project Structure**: Initialize the Python project with modular directories (`src/gui`, `src/bot`, `src/core`, `src/utils`).
- **Dependencies**: Define standard libraries and third-party dependencies in `requirements.txt`:
  - `customtkinter` (Modern, lightweight GUI)
  - `opencv-python` & `numpy` (High-performance image recognition)
  - `adbutils` (ADB wrapper for emulator interaction)
  - `requests` (Discord webhooks & API interactions)
- **Concurrency Model**: Design a unified, non-blocking architecture using `multiprocessing` or `asyncio`. The CustomTkinter GUI will run on the main thread, while bot instances run as separate background workers, communicating via thread-safe queues or event loops.

## 2. Phase 2: Core Utilities & Wrappers (The Foundation)
- **ADB Controller**: Translate `ADB.ahk` to Python. Use `adbutils` (or fallback to standard `subprocess` calls) for multi-device support, handling taps, swipes, text input, and screenshots natively.
- **Computer Vision Engine**: Translate `Gdip_Imagesearch.ahk`. Utilize OpenCV (`cv2.matchTemplate`) and numpy arrays for fast, robust template matching and screen reading.
- **Configuration Management**: Port `Config.ahk`, `Session.ahk`, and `Data.ahk`. Use Python's `json` or `configparser` modules to manage user settings and bot metadata.
- **Logging & Webhooks**: Recreate the discord logging and local heartbeat functions using Python's built-in `logging` and the `requests` library.

## 3. Phase 3: GUI Development (CustomTkinter)
- **Framework Setup**: Recreate the AHK `PTCGPB.ahk` interface using `customtkinter`, maintaining the dark-mode aesthetic and lightweight footprint.
- **Components**: Build tabs, scrollable frames, and option menus to handle:
  - Instance Settings (Multi-emulator configuration)
  - Bot Settings (Wonderpick, Rerolling, Pack Selection)
  - Save for Trade (S4T) configuration
  - Heartbeat & Discord Integration
  - Tools & System Settings
- **Binding**: Connect GUI inputs to the Configuration Management system, saving state synchronously or asynchronously.

## 4. Phase 4: Core Bot Logic Implementation
- **Routine Translation**: Port the main bot flow previously handled by `Main.ahk` and `1.ahk` scripts.
- **Modularization**: Break down tasks into distinct Python classes/functions:
  - `RerollManager`: Handles the pack opening logic.
  - `WonderpickInjector`: Manages 13P/96P specific flows.
  - `TradeManager`: Implements S4T detection and sorting.
  - `EventManager`: Handles Special Events logic.
- **Worker Integration**: Wire these routines into the concurrency model designed in Phase 1, allowing the GUI to start, pause, and stop instances gracefully.

## 5. Phase 5: Cross-Platform & Emulator Support
- **Emulator Abstraction Layer**: Build classes to handle specific emulator quirks natively:
  - MuMu Player (Primary Windows/macOS target)
  - Waydroid (Primary Linux target)
  - Android Studio AVDs / Genymotion (Fallbacks)
- **Window Management**: Implement OS-specific window arrangement (porting the `ArrangeWindows` functionality) using libraries like `pygetwindow` (Windows) or standard X11/Wayland utilities (Linux).

## 6. Phase 6: Testing & Pre-Commit Validation
- **Unit Testing**: Add `pytest` test suites for core utilities (ADB operations, Config Management).
- **Integration Testing**: Verify computer vision and UI interactions in mocked environments.
- **Pre-commit Hooks**: Run formatters (`black`), linters (`flake8`), and checks before final code submissions.

## 7. Phase 7: Final Documentation & Rollout
- **README Update**: Revamp `README.md` to guide users on installing Python, creating virtual environments, and installing dependencies.
- **Platform Guides**: Include OS-specific emulator setup guides (e.g., how to enable ADB on Waydroid vs MuMu).
- **Release Automation**: (Optional) Set up PyInstaller or GitHub Actions to compile standalone executables for Windows, macOS, and Linux to mimic the current easy-to-use distribution.