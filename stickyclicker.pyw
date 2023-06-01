import sys
import tkinter

import customtkinter
import os

from pynput.mouse import Button

import clicker


class StickyClicker(customtkinter.CTk):
    """The stickyclicker main class that builds the GUI and can edit the config."""

    def __init__(self):
        """Initializes the GUI and registers the required variables."""
        super().__init__()

        # Predefined variables
        self.sizeX = 320
        self.sizeY = 425
        self.minSizeX = 280
        self.minSizeY = 425

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

        self.GT_title = None
        self.theme_box = None
        self.color_box = None
        self.restart_button = None

        # Launch / hide button
        self.exit_button = None
        self.save_button = None

        # Settings
        settingsFile = open("settings.dat", 'r')
        self.settings = settingsFile.readline().split("|")

        self.cps = int(self.settings[0].strip())
        self.burst = float(self.settings[1].strip())
        self.clicking_time = int(self.settings[2].strip())

        self.mbutton = self.settings[3].strip()

        self.GUI_settings = int(self.settings[4].strip())

        self.theme = self.settings[6].strip()
        self.color = self.settings[7].strip()

        print(
            f"\nUsing {self.color} {self.theme} theme\nCPS:\t\t\t{self.cps}\nBurst scaling:\t{self.burst}\nClicking time:\t{self.clicking_time}\nMouse button:\t{self.mbutton}\n\nGUI settings:\t{self.GUI_settings}\n")

        self.click_thread = clicker.ClickMouse(cps=self.cps, button=self.mbutton, clicktime=self.clicking_time,
                                               burst=self.burst)

        # CustomTkinter setup
        self.geometry(f"{self.sizeX}x{self.sizeY}")
        self.minsize(self.minSizeX, self.minSizeY)

        customtkinter.set_appearance_mode(self.theme)
        customtkinter.set_default_color_theme(self.color)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.attributes('-topmost', True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

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

        if self.GUI_settings == 1:
            self.gs_checkbox.select()
            self.theme_gui_show()

        self.theme_box.set(self.theme)
        self.color_box.set(self.color)

    def on_closing(self):
        """Hook for closing. We don't want to close, but minimize.
        close with self.exit() instead"""
        self.iconify()

    def update_cps(self, value):
        """Hook for CPS slider"""
        self.cps = int(value)
        self.click_thread.cps = self.cps
        self.CPS_amount.configure(text=f"{self.cps} CPS")

    def update_ba(self, value):
        """Hook for burst slider"""
        self.burst = value
        self.click_thread.burst = self.burst
        if self.burst == 0:
            self.BA_amount.configure(text="no burst")
        else:
            self.BA_amount.configure(text=f"{round(self.burst, 2)} burst")

    def update_ct(self, value):
        """Hook for clicking time slider"""
        self.clicking_time = value
        self.click_thread.burst = self.burst
        if self.clicking_time == 0:
            self.CT_amount.configure(text="Keybinds")
        else:
            self.CT_amount.configure(text=f"{int(self.clicking_time)} seconds")

    def update_mbutton(self, value):
        """hook for the mouse button box"""
        self.mbutton = value
        if self.mbutton == "right":
            self.click_thread.button = Button.right
        elif self.mbutton == "middle":
            self.click_thread.button = Button.middle
        else:
            self.click_thread.button = Button.left

    def exit(self):
        """Exit the script."""
        self.destroy()
        try:
            self.click_thread.exit()

            print("Successfully closed the subprocess")
        except Exception:
            print("No subprocess active > not stopping a subprocess")
        os.kill(os.getpid(), 1)
        sys.exit()

    def changetheme(self, value):
        """Hook for the theme box"""
        self.theme = value

    def changecolor(self, value):
        """Hook for the color box"""
        self.color = value

    def restart(self):
        """Restart the GUI. Does not restart the whole script."""
        self.save_config()
        try:
            self.click_thread.exit()
            print("Successfully closed the subprocess")
        except Exception:
            print("No active subprocess > not closing it")
        self.destroy()
        print("Restarting the GUI... (Dont mind the errors)")
        main()

    def save_config(self):
        """Writes the config to a file in value|value|value format.
        Other options can be added by adding a list entry."""
        self.settings[0] = self.cps
        self.settings[1] = self.burst
        self.settings[2] = self.clicking_time
        self.settings[3] = self.mbutton
        self.settings[4] = self.gs_checkbox.get()
        self.settings[6] = self.theme
        self.settings[7] = self.color

        print(f"Saving settings:\n{self.settings}")

        with open("settings.dat", "w") as settingsFile:
            settingsFile.write(
                f"{self.settings[0]}|{self.settings[1]}|{self.settings[2]}|{self.settings[3]}|{self.settings[4]}|NULL|{self.settings[6]}|{self.settings[7]}")

    def build_gui(self):
        """Builds the stickyclicker GUI.
        Always call this in the init, else you will see a empty box."""
        self.cps_gui()
        self.burst_gui()
        self.clicktime_gui()
        self.mousebutton_gui()
        self.other_options_gui()
        self.theme_gui()
        self.buttons_gui()

    def cps_gui(self):
        """Slider for CPS.
        CPS is short for clicks per second
        The official limit is 120 to avoid issues on low-end PC's,
        but it can be as high as you want. (Using config)"""
        self.CPS_title = customtkinter.CTkLabel(master=self, text="CPS")
        self.CPS_title.grid(row=1, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")
        self.CPS_amount = customtkinter.CTkLabel(master=self, text="30 CPS")
        self.CPS_amount.grid(row=1, column=1, columnspan=1, padx=20, pady=5, sticky="nes")

        self.cps_slider = customtkinter.CTkSlider(master=self, from_=1, to=120, command=self.update_cps)
        self.cps_slider.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

    def burst_gui(self):
        """Slider for burst.
        burst is the randomness that makes it look more human like
        Works the best at 1.0"""
        self.BA_title = customtkinter.CTkLabel(master=self, text="Burst scaling")
        self.BA_title.grid(row=3, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")
        self.BA_amount = customtkinter.CTkLabel(master=self, text="1.3 burst")
        self.BA_amount.grid(row=3, column=1, columnspan=1, padx=20, pady=5, sticky="nes")

        self.ba_slider = customtkinter.CTkSlider(master=self, from_=0.0, to=2.0, command=self.update_ba)
        self.ba_slider.grid(row=4, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

    def clicktime_gui(self):
        """Slider for clicking time.
        Clicking time is the time the clicker will be clicking.
        When it is zero, it is 100% keybind dependant"""
        self.CT_title = customtkinter.CTkLabel(master=self, text="Clicking time")
        self.CT_title.grid(row=5, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")
        self.CT_amount = customtkinter.CTkLabel(master=self, text="Keybinds")
        self.CT_amount.grid(row=5, column=1, columnspan=1, padx=20, pady=5, sticky="nes")

        self.ct_slider = customtkinter.CTkSlider(master=self, from_=0, to=100, command=self.update_ct)
        self.ct_slider.grid(row=6, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

    def mousebutton_gui(self):
        """A selection box that has two values:
        left - for left-clicking (Default)
        right - for right-clicking
        middle - for middle-clicking (But who uses that?)"""
        self.MB_title = customtkinter.CTkLabel(master=self, text="Click type")
        self.MB_title.grid(row=7, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")

        self.mb_box = customtkinter.CTkComboBox(master=self, values=["left", "right", "middle"],
                                                command=self.update_mbutton)
        self.mb_box.grid(row=8, column=0, columnspan=2, padx=20, pady=(0, 5), sticky="ew")

    def other_options_gui(self):
        """A multiple choice menu that lets you choose additional options.
        GUI settings - shows the additional GUI and theme settings.
        Console - Show the console when enabled. Only nt (windows) support"""
        self.OO_title = customtkinter.CTkLabel(master=self, text="Other options")
        self.OO_title.grid(row=9, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")

        self.gs_checkbox = customtkinter.CTkCheckBox(master=self, text="Show GUI settings", offvalue=0, onvalue=1,
                                                     command=self.theme_gui_show)
        self.gs_checkbox.grid(row=10, column=0, columnspan=1, padx=(20, 10), pady=5, sticky="ew")

    def theme_gui(self):
        """Initialize the theme settings.
        The theme settings are hidden by default.
        Show / hide using theme_gui_show()"""
        self.GT_title = customtkinter.CTkLabel(master=self, text="GUI theme")

        self.theme_box = customtkinter.CTkComboBox(master=self, values=["dark", "light"], command=self.changetheme)
        self.color_box = customtkinter.CTkComboBox(master=self, values=["blue", "dark-blue", "green"],
                                                   command=self.changecolor)
        self.restart_button = customtkinter.CTkButton(master=self, text="Update GUI", command=self.restart)

    def theme_gui_show(self):
        """Checks the checkbox to decide whether to show or not to show the theme settings"""
        if self.gs_checkbox.get() == 1:
            self.minsize(self.minSizeX, self.minSizeY + 110)
            self.GT_title.grid(row=11, column=0, columnspan=2, padx=20, pady=5, sticky="nsw")
            self.theme_box.grid(row=12, column=0, columnspan=1, padx=(20, 10), pady=(0, 5), sticky="nesw")
            self.color_box.grid(row=12, column=1, columnspan=1, padx=(10, 20), pady=(0, 5), sticky="nesw")
            self.restart_button.grid(row=13, column=0, columnspan=2, padx=20, pady=(5, 0), sticky="nesw")
        else:
            self.minsize(self.minSizeX, self.minSizeY)
            self.GT_title.grid_remove()
            self.theme_box.grid_remove()
            self.color_box.grid_remove()
            self.restart_button.grid_remove()

    def buttons_gui(self):
        """Renders the start, the save config and the exit button."""
        self.save_button = customtkinter.CTkButton(master=self, text="Save config", command=self.save_config)
        self.save_button.grid(row=15, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="nesw")

        self.exit_button = customtkinter.CTkButton(master=self, text="Exit", command=self.exit)
        self.exit_button.grid(row=16, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="nesw")


def main():
    stickyclicker = StickyClicker()
    stickyclicker.mainloop()


if __name__ == "__main__":
    main()
