from src.logger import Colour

BANNER_PATH = "assets/banner.txt"
def print_banner():
    with open(BANNER_PATH, "r") as b:
        banner = b.read()
    banner = banner.format(
        G=Colour.GREEN,
        R=Colour.RED,
        E=Colour.ENDC,
        B=Colour.BOLD
    )
    print(banner)
