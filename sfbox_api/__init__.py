import os

from .composition import Composition
from .frame import Frame
from .lattice import Lat
from .molecule import Mol
from .monomer import Mon
from .newton import Newton
from .system import Sys
from .zoo import barbwire, comb_brush, polyacid

if os.name != "nt":
    target = f"{os.path.dirname(os.path.realpath(__file__))}/data/sfbox"
    os.system(f"chmod +x {target}")

__all__ = [
    "Composition",
    "Lat",
    "Mol",
    "Mon",
    "Sys",
    "Newton",
    "Frame",
    "comb_brush",
    "barbwire",
    "polyacid",
]
