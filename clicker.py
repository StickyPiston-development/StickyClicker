import random
import threading
import time

import pynput.keyboard
from pynput.mouse import Button, Controller


class ClickMouse(threading.Thread):
    def __init__(self, cps=60, button=Button.left, clicktime=0, burst=1):
        super(ClickMouse, self).__init__()
        self.cps = cps
        self.delay = 1 / cps

        if button == "right":
            self.button = Button.right
        elif button == "middle":
            self.button = Button.middle
        else:
            self.button = Button.left

        self.running = False
        self.program_running = True

        self.ct = clicktime
        self.burst = burst

        self.mouse = Controller()
        self.start()

        self.listener = threading.Thread(target=self.listen_hotkeys)
        self.listener.start()

    def toggle(self):
        if self.running:
            print("Stopping... ")
            self.running = False
        else:
            print(f"Starting... ({self.cps} CPS {self.button})")
            self.running = True

    def exit(self):
        self.running = False
        self.program_running = False

    def getBurst(self):
        return random.uniform(-0.9, 0.5) * self.burst * self.delay

    def run(self):
        while self.program_running:
            if self.ct == 0:
                while self.running:
                    self.mouse.click(self.button)
                    time.sleep(self.delay + self.getBurst())
            else:
                if self.running:
                    for i in range(self.ct):
                        for i in range(self.cps):
                            self.mouse.click(self.button)
                            time.sleep(self.delay + self.getBurst())
                    self.running = False
            time.sleep(0.1)

    def listen_hotkeys(self):
        with pynput.keyboard.GlobalHotKeys({
                                            '<ctrl>+<alt>+t': self.toggle,
                                            '<ctrl>+<alt>+e': self.exit}) as h:
            h.join()


if __name__ == "__main__":
    click_thread = ClickMouse()
