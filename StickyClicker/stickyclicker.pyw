import tkinter
import customtkinter
import subprocess

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")  #blue, dark-blue, green

app = customtkinter.CTk()
app.geometry("400x320")
app.minsize(340, 320)
#app.maxsize(300, 240)

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure((0, 1), weight=1)

app.title("StickyClicker")

# Sliders
def update_cps(value):
    CPS_amount.configure(text=str(int(value)) + " CPS")
    app.update_idletasks()
def update_ct(value):
    if value == 0:
        CT_amount.configure(text="Keybinds")
    else:
        CT_amount.configure(text=str(int(value)) + " seconds")
    app.update_idletasks()

# Buttons
def launch():
    subprocess.Popen(["python", "clicker.py", str(int(cps_slider.get())), str(int(ct_slider.get())), str(mb_box.get())], creationflags=cc_checkbox.get(), stdout=None, shell=False)
def hide():
    app.withdraw()
def show():
    app.deiconify()

# Clicks per second
CPS_title = customtkinter.CTkLabel(master=app, text="StickyClicker CPS")
CPS_title.grid(row=1, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")
CPS_amount = customtkinter.CTkLabel(master=app, text="30 CPS")
CPS_amount.grid(row=1, column=1, columnspan=1, padx=20, pady=5, sticky="nes")

cps_slider = customtkinter.CTkSlider(master=app, from_=1, to=120, command=update_cps)
cps_slider.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

# Click duration
CT_title = customtkinter.CTkLabel(master=app, text="StickyClicker ClickTime")
CT_title.grid(row=3, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")
CT_amount = customtkinter.CTkLabel(master=app, text="Keybinds")
CT_amount.grid(row=3, column=1, columnspan=1, padx=20, pady=5, sticky="nes")

ct_slider = customtkinter.CTkSlider(master=app, from_=0, to=100, command=update_ct)
ct_slider.grid(row=4, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

# mouse button menu
MB_title = customtkinter.CTkLabel(master=app, text="StickyClicker click type")
MB_title.grid(row=5, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")

mb_box = customtkinter.CTkComboBox(master=app,values=["left", "right"])
mb_box.grid(row=6, column=0, columnspan=2, padx=20, pady=(0, 5), sticky="ew")

# other options
OO_title = customtkinter.CTkLabel(master=app, text="Other options")
OO_title.grid(row=7, column=0, columnspan=1, padx=20, pady=5, sticky="nsw")

cc_checkbox = customtkinter.CTkCheckBox(master=app, text="Enable console", offvalue=subprocess.CREATE_NO_WINDOW, onvalue=subprocess.CREATE_NEW_CONSOLE)
cc_checkbox.grid(row=8, column=0, columnspan=2, padx=20, pady=5, sticky="ew")

# launch button
launch_button = customtkinter.CTkButton(master=app, text="Start StickyClicker", command=launch)
launch_button.grid(row=9, column=0, columnspan=1, padx=(20, 10), pady=10, sticky="nesw")

# Hide button
hide_button = customtkinter.CTkButton(master=app, text="Hide StickyClicker", command=hide)
hide_button.grid(row=9, column=1, columnspan=1, padx=(10, 20), pady=10, sticky="nesw")

cps_slider.set(30)
ct_slider.set(0)

app.attributes('-topmost',True)
app.mainloop()
