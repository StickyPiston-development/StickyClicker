import tkinter

import customtkinter
import subprocess
import os
import sys

settingsFile = open("settings.dat", 'r')
settings = settingsFile.readline().split("|")
print(settings)
theme = settings[0].strip()
color = settings[1].strip()
print(theme, color)

customtkinter.set_appearance_mode(theme)
customtkinter.set_default_color_theme(color)  # blue, dark-blue, green

app = customtkinter.CTk()
app.geometry("320x360")
app.minsize(280, 390)
# app.maxsize(300, 240)

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure((0, 1), weight=1)

app.title("StickyClicker")


# Sliders
def update_cps(value):
    cps = int(value)
    CPS_amount.configure(text=f"{cps} CPS")
    app.update_idletasks()


def update_ba(value):
    burst = value
    if burst == 0:
        BA_amount.configure(text="no burst")
    else:
        BA_amount.configure(text=f"{round(burst, 1)} burst")


def update_ct(value):
    ct = value
    if ct == 0:
        CT_amount.configure(text="Keybinds")
    else:
        CT_amount.configure(text=f"{int(ct)} seconds")
    app.update_idletasks()


def theme(value):
    settings[0] = value
    with open("settings.dat", "w") as settingsFile:
        output = []
        for i in range(len(settings)):
            output.append("|" + settings[i])
        settingsFile.write("".join(output).strip("|"))
    customtkinter.CTkInputDialog(text="Changed ...", title="Test")


def color(value):
    settings[1] = value
    with open("settings.dat", "w") as settingsFile:
        output = []
        for i in range(len(settings)):
            output.append("|" + settings[i])
        settingsFile.write("".join(output).strip("|"))
    customtkinter.CTkInputDialog(text="Changed ...", title="Test")


def restart():
    app.destroy()


# Buttons
def launch():
    if os.name == "windows":
        subprocess.Popen(
            ["python", "clicker.py", str(int(cps_slider.get())), str(int(ba_slider.get())), str(int(ct_slider.get())),
             str(mb_box.get())], creationflags=cc_checkbox.get(), stdout=None, shell=False)
    else:
        subprocess.Popen(
            ["python3", "clicker.py", str(int(cps_slider.get())), str(int(ba_slider.get())), str(int(ct_slider.get())),
             str(mb_box.get())], stdout=None, shell=False)


def hide():
    app.withdraw()


def show():
    app.deiconify()


def setup():
    theme_box.set(settings[0])
    color_box.set(settings[1])


def GUI_settings():
    if gs_checkbox.get():
        app.minsize(280, 490)
        GT_title.grid(row=11, column=0, columnspan=2, padx=20, pady=5, sticky="nsw")
        theme_box.grid(row=12, column=0, columnspan=1, padx=(20, 10), pady=(0, 5), sticky="nesw")
        color_box.grid(row=12, column=1, columnspan=1, padx=(10, 20), pady=(0, 5), sticky="nesw")
        restart_button.grid(row=13, column=0, columnspan=2, padx=20, pady=(5, 0), sticky="nesw")
    else:
        app.minsize(280, 380)
        GT_title.grid_remove()
        theme_box.grid_remove()
        color_box.grid_remove()
        restart_button.grid_remove()


# Clicks per second
CPS_title = customtkinter.CTkLabel(master=app, text="CPS")
CPS_title.grid(row=1, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")
CPS_amount = customtkinter.CTkLabel(master=app, text="30 CPS")
CPS_amount.grid(row=1, column=1, columnspan=1, padx=20, pady=5, sticky="nes")

cps_slider = customtkinter.CTkSlider(master=app, from_=1, to=120, command=update_cps)
cps_slider.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

# Burst
BA_title = customtkinter.CTkLabel(master=app, text="Burst scaling")
BA_title.grid(row=3, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")
BA_amount = customtkinter.CTkLabel(master=app, text="1.3 burst")
BA_amount.grid(row=3, column=1, columnspan=1, padx=20, pady=5, sticky="nes")

ba_slider = customtkinter.CTkSlider(master=app, from_=0.0, to=2.0, command=update_ba)
ba_slider.grid(row=4, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

# Click duration
CT_title = customtkinter.CTkLabel(master=app, text="Clicking time")
CT_title.grid(row=5, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")
CT_amount = customtkinter.CTkLabel(master=app, text="Keybinds")
CT_amount.grid(row=5, column=1, columnspan=1, padx=20, pady=5, sticky="nes")

ct_slider = customtkinter.CTkSlider(master=app, from_=0, to=100, command=update_ct)
ct_slider.grid(row=6, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

# mouse button menu
MB_title = customtkinter.CTkLabel(master=app, text="Click type")
MB_title.grid(row=7, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")

mb_box = customtkinter.CTkComboBox(master=app, values=["left", "right"])
mb_box.grid(row=8, column=0, columnspan=2, padx=20, pady=(0, 5), sticky="ew")

# other options
OO_title = customtkinter.CTkLabel(master=app, text="Other options")
OO_title.grid(row=9, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")

gs_checkbox = customtkinter.CTkCheckBox(master=app, text="GUI settings", offvalue=False, onvalue=True, command=GUI_settings)
gs_checkbox.grid(row=10, column=0, columnspan=1, padx=(20, 10), pady=5, sticky="ew")

if os.name == "windows":
    cc_checkbox = customtkinter.CTkCheckBox(master=app, text="Console", offvalue=subprocess.CREATE_NO_WINDOW,
                                            onvalue=subprocess.CREATE_NEW_CONSOLE)
else:
    cc_checkbox = customtkinter.CTkCheckBox(master=app, text="Console", state=tkinter.DISABLED)
cc_checkbox.grid(row=10, column=1, columnspan=1, padx=(10, 20), pady=5, sticky="ew")

# theme
GT_title = customtkinter.CTkLabel(master=app, text="GUI theme")

theme_box = customtkinter.CTkComboBox(master=app, values=["dark", "ligth"], command=theme)
color_box = customtkinter.CTkComboBox(master=app, values=["blue", "dark-blue", "green"], command=color)
restart_button = customtkinter.CTkButton(master=app, text="Update GUI", command=restart)

# launch button
launch_button = customtkinter.CTkButton(master=app, text="Start clicker", command=launch)
launch_button.grid(row=14, column=0, columnspan=1, padx=(20, 10), pady=10, sticky="nesw")

# Hide button
hide_button = customtkinter.CTkButton(master=app, text="Hide GUI", command=hide)
hide_button.grid(row=14, column=1, columnspan=1, padx=(10, 20), pady=10, sticky="nesw")

cps_slider.set(30)
ba_slider.set(1.3)
ct_slider.set(0)

setup()

app.attributes('-topmost', True)
app.mainloop()
