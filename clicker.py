import time, threading, sys, random
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import pynput.keyboard

button = Button.left
cps = 10
ct = 0
burst = 1
start_stop_key = KeyCode(char='þ')
exit_key = KeyCode(char='é')

if len(sys.argv) > 4:
    print("Starting a new clicker instance")
    cps = int(sys.argv[1])
    burst = float(sys.argv[2])
    ct = int(sys.argv[3])
    if sys.argv[4] == 'right':
        button = Button.right
    elif sys.argv[5] == 'middle':
        button = Button.middle

delay = 1 / cps


class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False
        exit()

    def getBurst(self):
        return random.uniform(-0.9, 0.5) * burst * self.delay

    def run(self):
        while self.program_running:
            if ct == 0:
                while self.running:
                    mouse.click(self.button)
                    time.sleep(self.delay + self.getBurst())
            else:
                if self.running:
                    for i in range(ct):
                        for i in range(cps):
                            mouse.click(self.button)
                            time.sleep(self.delay + self.getBurst())
                    self.running = False
            time.sleep(0.1)


mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()


def toggle():
    if click_thread.running:
        print("Stopping... ")
        click_thread.stop_clicking()
    else:
        print(f"Starting... ({cps} CPS {button})")
        click_thread.start_clicking()


with pynput.keyboard.GlobalHotKeys({
    '<ctrl>+<alt>+t': toggle,
    '<ctrl>+<alt>+e': click_thread.exit}) as h:
    h.join()
