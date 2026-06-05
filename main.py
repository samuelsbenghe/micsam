from pystray import Icon, Menu, MenuItem
from PIL import Image


def quit_app(icon, item):
    icon.stop()


image = Image.new("RGB", (64, 64), color="blue")

icon = Icon("MyApp", image, "My Background App", menu=Menu(MenuItem("Quit", quit_app)))

icon.run()
