import sys, pyautogui, keyboard
print(f"Starting a new StickyClicker instance with {sys.argv[1]} CPS in {sys.argv[2]} seconds")
print(sys.argv)
print(f"This will take {int(sys.argv[1])*int(sys.argv[2])} clicks")

print(f"""
Clicks per second:	{sys.argv[1]}
Time between clicks	{1/int(sys.argv[1])}
Seconds			{sys.argv[2]}
Total clicks:		{int(sys.argv[1])*int(sys.argv[2])}""")

for i in range(int(int(sys.argv[2])/2)):
	pyautogui.click(clicks=int(sys.argv[1])*2, interval=1/int(sys.argv[1])/2)
