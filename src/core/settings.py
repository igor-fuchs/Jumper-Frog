"""Global settings and constants for the game."""

import os
import sys

# ── Base directory (supports PyInstaller --onefile) ──────────────────
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS          # pylint: disable=protected-access,no-member
else:
    BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)

# Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Jumper Frog"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 40, 40)
DARK_GREEN = (34, 139, 34)
GREEN = (50, 180, 50)
LIGHT_GREEN = (144, 238, 144)
DARK_GRAY = (60, 60, 60)
GRAY = (100, 100, 100)
LIGHT_GRAY = (180, 180, 180)
BLUE = (30, 100, 200)
LIGHT_BLUE = (70, 140, 240)
