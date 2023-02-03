import tkinter

import customtkinter
import subprocess
import os


class StickyClicker(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Predefined variables
        self.sizeX = 320
        self.sizeY = 360
        self.minSizeX = 280
        self.minSizeY = 390

        # CPS slider
        self.CPS_title = None
        self.CPS_amount = None
        self.cps_slider = None

        # Burst slider
        self.BA_title = None
        self.BA_amount = None
        self.ba_slider = None

        # Clicking time slider
        self.CT_title = None
        self.CT_amount = None
        self.ct_slider = None

        # Mouse button dropdown
        self.MB_title = None
        self.mb_box = None

        # Other options
        self.OO_title = None
        self.gs_checkbox = None
        self.cc_checkbox = None

        self.GT_title = None
        self.theme_box = None
        self.color_box = None
        self.restart_button = None

        # Launch / hide button
        self.launch_button = None
        self.save_button = None

        # Settings
        settingsFile = open("settings.dat", 'r')
        self.settings = settingsFile.readline().split("|")

        self.cps = int(self.settings[0].strip())
        self.burst = float(self.settings[1].strip())
        self.clicking_time = int(self.settings[2].strip())

        self.mbutton = self.settings[3].strip()

        self.GUI_settings = int(self.settings[4].strip())
        self.console = int(self.settings[5].strip())

        self.theme = self.settings[6].strip()
        self.color = self.settings[7].strip()

        print(f"Using {self.theme} theme with {self.color}")

        # CustomTkinter setup
        self.geometry(f"{self.sizeX}x{self.sizeY}")
        self.minsize(self.minSizeX, self.minSizeY)

        customtkinter.set_appearance_mode(self.theme)
        customtkinter.set_default_color_theme(self.color)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.attributes('-topmost', True)

        self.title("StickyClicker")

        self.build_gui()

        # Update options to settings
        self.cps_slider.set(self.cps)
        self.update_cps(self.cps)

        self.ba_slider.set(self.burst)
        self.update_ba(self.burst)

        self.ct_slider.set(self.clicking_time)
        self.update_ct(self.clicking_time)

        self.mb_box.set(self.mbutton)

        print(self.GUI_settings)
        if self.GUI_settings == 1:
            self.gs_checkbox.select()
            self.theme_gui_show()
        if self.console == 16:
            self.cc_checkbox.select()

        self.theme_box.set(self.theme)
        self.color_box.set(self.color)

    def update_cps(self, value):
        self.cps = int(value)
        self.CPS_amount.configure(text=f"{self.cps} CPS")

    def update_ba(self, value):
        self.burst = value
        if self.burst == 0:
            self.BA_amount.configure(text="no burst")
        else:
            self.BA_amount.configure(text=f"{round(self.burst, 2)} burst")

    def update_ct(self, value):
        self.ct = value
        if self.ct == 0:
            self.CT_amount.configure(text="Keybinds")
        else:
            self.CT_amount.configure(text=f"{int(self.ct)} seconds")

    def update_mbutton(self, value):
        self.mbutton = value

    def launch(self):
        if os.name == "nt":
            subprocess.Popen(
                ["python", "clicker.py", str(int(self.cps_slider.get())), str(int(self.ba_slider.get())),
                 str(int(self.ct_slider.get())), str(self.mb_box.get())], creationflags=self.cc_checkbox.get(),
                stdout=None, shell=False)
        else:
            subprocess.Popen(
                ["python3", "clicker.py", str(int(self.cps_slider.get())), str(int(self.ba_slider.get())),
                 str(int(self.ct_slider.get())), str(self.mb_box.get())], stdout=None, shell=False)

    def changetheme(self, value):
        self.theme = value

    def changecolor(self, value):
        self.color = value

    def restart(self):
        # TODO: actually restart
        self.destroy()

    def save_config(self):
        self.settings[0] = self.cps
        self.settings[1] = self.burst
        self.settings[2] = self.clicking_time
        self.settings[3] = self.mbutton
        self.settings[4] = self.gs_checkbox.get()
        self.settings[5] = self.cc_checkbox.get()
        self.settings[6] = self.theme
        self.settings[7] = self.color

        print(self.settings)

        with open("settings.dat", "w") as settingsFile:
            settingsFile.write(
                f"{self.settings[0]}|{self.settings[1]}|{self.settings[2]}|{self.settings[3]}|{self.settings[4]}|{self.settings[5]}|{self.settings[6]}|{self.settings[7]}")

    def build_gui(self):
        self.cps_gui()
        self.burst_gui()
        self.clicktime_gui()
        self.mousebutton_gui()
        self.other_options_gui()
        self.theme_gui()
        self.buttons_gui()

    def cps_gui(self):
        self.CPS_title = customtkinter.CTkLabel(master=self, text="CPS")
        self.CPS_title.grid(row=1, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")
        self.CPS_amount = customtkinter.CTkLabel(master=self, text="30 CPS")
        self.CPS_amount.grid(row=1, column=1, columnspan=1, padx=20, pady=5, sticky="nes")

        self.cps_slider = customtkinter.CTkSlider(master=self, from_=1, to=120, command=self.update_cps)
        self.cps_slider.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

    def burst_gui(self):
        self.BA_title = customtkinter.CTkLabel(master=self, text="Burst scaling")
        self.BA_title.grid(row=3, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")
        self.BA_amount = customtkinter.CTkLabel(master=self, text="1.3 burst")
        self.BA_amount.grid(row=3, column=1, columnspan=1, padx=20, pady=5, sticky="nes")

        self.ba_slider = customtkinter.CTkSlider(master=self, from_=0.0, to=2.0, command=self.update_ba)
        self.ba_slider.grid(row=4, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

    def clicktime_gui(self):
        self.CT_title = customtkinter.CTkLabel(master=self, text="Clicking time")
        self.CT_title.grid(row=5, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")
        self.CT_amount = customtkinter.CTkLabel(master=self, text="Keybinds")
        self.CT_amount.grid(row=5, column=1, columnspan=1, padx=20, pady=5, sticky="nes")

        self.ct_slider = customtkinter.CTkSlider(master=self, from_=0, to=100, command=self.update_ct)
        self.ct_slider.grid(row=6, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

    def mousebutton_gui(self):
        self.MB_title = customtkinter.CTkLabel(master=self, text="Click type")
        self.MB_title.grid(row=7, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")

        self.mb_box = customtkinter.CTkComboBox(master=self, values=["left", "right"], command=self.update_mbutton)
        self.mb_box.grid(row=8, column=0, columnspan=2, padx=20, pady=(0, 5), sticky="ew")

    def other_options_gui(self):
        self.OO_title = customtkinter.CTkLabel(master=self, text="Other options")
        self.OO_title.grid(row=9, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")

        self.gs_checkbox = customtkinter.CTkCheckBox(master=self, text="GUI settings", offvalue=0, onvalue=1,
                                                     command=self.theme_gui_show)
        self.gs_checkbox.grid(row=10, column=0, columnspan=1, padx=(20, 10), pady=5, sticky="ew")

        if os.name == "nt":
            self.cc_checkbox = customtkinter.CTkCheckBox(master=self, text="Console",
                                                         offvalue=subprocess.CREATE_NO_WINDOW,
                                                         onvalue=subprocess.CREATE_NEW_CONSOLE)
        else:
            self.cc_checkbox = customtkinter.CTkCheckBox(master=self, text="Console", state=tkinter.DISABLED)
        self.cc_checkbox.grid(row=10, column=1, columnspan=1, padx=(10, 20), pady=5, sticky="ew")

    def theme_gui(self):
        self.GT_title = customtkinter.CTkLabel(master=self, text="GUI theme")

        self.theme_box = customtkinter.CTkComboBox(master=self, values=["dark", "light"], command=self.changetheme)
        self.color_box = customtkinter.CTkComboBox(master=self, values=["blue", "dark-blue", "green"],
                                                   command=self.changecolor)
        self.restart_button = customtkinter.CTkButton(master=self, text="Update GUI", command=self.restart)

    def theme_gui_show(self):
        if self.gs_checkbox.get() == 1:
            self.minsize(280, 490)
            self.GT_title.grid(row=11, column=0, columnspan=2, padx=20, pady=5, sticky="nsw")
            self.theme_box.grid(row=12, column=0, columnspan=1, padx=(20, 10), pady=(0, 5), sticky="nesw")
            self.color_box.grid(row=12, column=1, columnspan=1, padx=(10, 20), pady=(0, 5), sticky="nesw")
            self.restart_button.grid(row=13, column=0, columnspan=2, padx=20, pady=(5, 0), sticky="nesw")
        else:
            self.minsize(280, 380)
            self.GT_title.grid_remove()
            self.theme_box.grid_remove()
            self.color_box.grid_remove()
            self.restart_button.grid_remove()

    def buttons_gui(self):
        self.launch_button = customtkinter.CTkButton(master=self, text="Start clicker", command=self.launch)
        self.launch_button.grid(row=14, column=0, columnspan=1, padx=(20, 10), pady=10, sticky="nesw")

        self.save_button = customtkinter.CTkButton(master=self, text="Save", command=self.save_config)
        self.save_button.grid(row=14, column=1, columnspan=1, padx=(10, 20), pady=10, sticky="nesw")


stickyclicker = StickyClicker()
stickyclicker.mainloop()
