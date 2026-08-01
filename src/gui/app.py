import customtkinter as ctk
from src.core.config import ConfigManager

class App(ctk.CTk):
    def __init__(self, command_queue=None, event_queue=None):
        super().__init__()

        self.config_manager = ConfigManager()
        self.command_queue = command_queue
        self.event_queue = event_queue

        self.title("PTCGP Bot (Python Port)")
        self.geometry("800x400")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="PTCGP Bot", font=ctk.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.tabview = ctk.CTkTabview(self, width=500)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.tabview.add("Instance Settings")
        self.tabview.add("Bot Settings")
        self.tabview.add("Save for Trade")
        self.tabview.add("System")

        self._build_instance_settings()
        self._build_bot_settings()
        self._build_s4t_settings()
        self._build_system_settings()

        self.start_button = ctk.CTkButton(self.navigation_frame, text="Start Bot", command=self.start_bot)
        self.start_button.grid(row=5, column=0, padx=20, pady=20)

    def _build_instance_settings(self):
        tab = self.tabview.tab("Instance Settings")

        self.instances_label = ctk.CTkLabel(tab, text="Instances:")
        self.instances_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.instances_entry = ctk.CTkEntry(tab)
        self.instances_entry.insert(0, str(self.config_manager.get("general", "instances") or 1))
        self.instances_entry.grid(row=0, column=1, padx=20, pady=10)

        self.columns_label = ctk.CTkLabel(tab, text="Columns:")
        self.columns_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.columns_entry = ctk.CTkEntry(tab)
        self.columns_entry.insert(0, str(self.config_manager.get("general", "columns") or 3))
        self.columns_entry.grid(row=1, column=1, padx=20, pady=10)

        self.save_inst_btn = ctk.CTkButton(tab, text="Save Config", command=self.save_config)
        self.save_inst_btn.grid(row=2, column=0, columnspan=2, pady=20)

    def _build_bot_settings(self):
        tab = self.tabview.tab("Bot Settings")

        self.delete_method_label = ctk.CTkLabel(tab, text="Delete Method:")
        self.delete_method_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.delete_method_opt = ctk.CTkOptionMenu(tab, values=["Create Bots (13P)", "Inject 13P+", "Inject Wonderpick 96P+"])
        self.delete_method_opt.set(self.config_manager.get("general", "delete_method") or "Create Bots (13P)")
        self.delete_method_opt.grid(row=0, column=1, padx=20, pady=10)

        self.extra_pack_cb = ctk.CTkCheckBox(tab, text="Open Extra Pack")
        if self.config_manager.get("general", "open_extra_pack"):
            self.extra_pack_cb.select()
        self.extra_pack_cb.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="w")

    def _build_s4t_settings(self):
        tab = self.tabview.tab("Save for Trade")

        self.s4t_enabled_cb = ctk.CTkCheckBox(tab, text="Enable Save for Trade")
        if self.config_manager.get("save_for_trade", "enabled"):
            self.s4t_enabled_cb.select()
        self.s4t_enabled_cb.grid(row=0, column=0, padx=20, pady=10, sticky="w")

    def _build_system_settings(self):
        tab = self.tabview.tab("System")

        self.debug_cb = ctk.CTkCheckBox(tab, text="Debug Mode")
        if self.config_manager.get("system", "debug_mode"):
            self.debug_cb.select()
        self.debug_cb.grid(row=0, column=0, padx=20, pady=10, sticky="w")

    def save_config(self):
        try:
            instances = int(self.instances_entry.get())
            columns = int(self.columns_entry.get())
            self.config_manager.set("general", "instances", instances)
            self.config_manager.set("general", "columns", columns)
            self.config_manager.set("general", "delete_method", self.delete_method_opt.get())
            self.config_manager.set("general", "open_extra_pack", bool(self.extra_pack_cb.get()))
            self.config_manager.set("save_for_trade", "enabled", bool(self.s4t_enabled_cb.get()))
            self.config_manager.set("system", "debug_mode", bool(self.debug_cb.get()))
        except ValueError:
            pass # Ignore invalid inputs for now

    def start_bot(self):
        self.save_config()
        if self.command_queue:
            self.command_queue.put({"action": "start"})

    def stop_bot(self):
        if self.command_queue:
            self.command_queue.put({"action": "stop"})
