import enum
from importlib import resources
from matplotlib import font_manager
from pathlib import Path

import matplotlib as mpl

mpl.rcParams["axes.unicode_minus"] = False


class Color(enum.StrEnum):
    pheni = "#4c00b0"
    black = "#202127"


font_files = font_manager.findSystemFonts(
    fontpaths=[Path(resources.files("pretty_plot").__str__()) / "fonts"]
)
for font_file in font_files:
    font_manager.fontManager.addfont(font_file)


class Font(enum.StrEnum):
    neo = "Neo Sans Pro"
    julia = "Julia Mono"
