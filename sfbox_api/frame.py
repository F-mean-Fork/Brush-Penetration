import os
from typing import Dict, List, Optional

import numpy as np

from .composition import Composition
from .lattice import Lat
from .molecule import Mol
from .monomer import Mon
from .newton import Newton
from .system import Sys

HOME_DIR = os.getcwd()
if os.name != "nt":
    TARGET_DIR = f"{os.path.dirname(os.path.realpath(__file__))}/data"
else:
    TARGET_DIR = f"{os.path.dirname(os.path.realpath(__file__))}\\data"


class Frame:
    def __init__(
        self,
        lat: Lat,
        sys: Sys,
        mols: List[Mol],
        mons: List[Mon],
        chi_list: Dict[str, float] = dict(),
        newton: Newton = Newton(),
    ) -> None:
        self.lat = lat
        self.sys = sys
        self.mols = mols
        self.mons = mons
        self.chi_list = chi_list
        self.newton = newton
        self.profile: Optional[Dict[str, np.ndarray]] = dict()
        self.stats: Optional[Dict[str, float]] = dict()
        self.profile_labels: Optional[List[str]] = []
        self.stats_labels: Optional[List[str]] = []
        self.text = ""

        list_mons_names = []
        for m in mons:
            list_mons_names.append(m.name)

        self.compositions = []
        for mol in mols:
            self.compositions.append(Composition(mol.composition))

        list_mons_compare = []
        for comp in self.compositions:
            list_mons_compare += comp.types_list()

        if set(list_mons_names) != set(list_mons_compare):
            raise ValueError(
                f"Set monomers: {list_mons_names}, but {list_mons_compare} used in molecules"
            )

        for paar in self.chi_list:
            p = paar.split()
            if len(p) != 2:
                raise ValueError(f"Frame: incorrect key in chi_list: {paar}")
            if p[0] not in list_mons_names:
                raise ValueError(f"Frame: unknown type monomer in chi_list: {p[0]}")
            if p[1] not in list_mons_names:
                raise ValueError(f"Frame: unknown type monomer in chi_list: {p[1]}")

    def __str__(self):
        result = ""
        for p in self.lat:
            if p[1] and p[1] != self.lat.name:
                if p[0] == "lambda1":
                    result += f"lat : {self.lat.name} : lambda : {str(p[1])} \n"
                else:
                    result += f"lat : {self.lat.name} : {p[0]} : {str(p[1])} \n"
                if p[0] == "lowerbound" and p[1] == "surface":
                    result += "mon : lower : freedom : frozen \n"
                    result += "mon : lower : frozen_range : lowerbound \n"
                if p[0] == "upperbound" and p[1] == "surface":
                    result += "mon : upper : freedom : frozen \n"
                    result += "mon : upper : frozen_range : upperbound \n"

        for p in self.sys:
            if p[1] and p[1] != self.sys.name:
                result += f"sys : {self.sys.name} : {p[0]} : {str(p[1])} \n"

        for mon in self.mons:
            for p in mon:
                if p[1] and p[1] != mon.name:
                    result += f"mon : {mon.name} : {p[0]} : {str(p[1])} \n"

        for paar in self.chi_list:
            p = paar.split()
            result += f"mon : {p[0]} : chi - {p[1]} : {self.chi_list[paar]} \n"

        for mol in self.mols:
            for p in mol:
                if p[1] and p[1] != mol.name:
                    result += f"mol : {mol.name} : {p[0]} : {str(p[1])} \n"

        for p in self.newton:
            if p[1] and p[1] != self.newton.name:
                result += f"newton : {self.newton.name} : {p[0]} : {str(p[1])} \n"

        result += "output : filename.pro : type : profiles \n"
        result += "output : filename.pro : template : profile.tmp \n"
        result += "output : filename.kal : type : kal \n"
        result += "output : filename.kal : template : kal.tmp \n"
        result += self.text
        result += "\n"
        result += "start"
        return result

    def run(self):
        self.profile = dict()
        self.stats = dict()
        self.profile_labels = []
        self.stats_labels = []

        f = open(f"{os.path.join(TARGET_DIR, 'info.txt')}", "w")
        f.close()
        f = open(f"{os.path.join(TARGET_DIR, 'input.pro')}", "w")
        f.close()
        with open(f"{os.path.join(TARGET_DIR, 'profile.tmp')}", "w") as f:
            f.writelines("mol : * : phi : profile \n")
            f.writelines("mon : * : phi : profile \n")
            f.writelines("state : * : phi : profile")
        with open(f"{os.path.join(TARGET_DIR, 'kal.tmp')}", "w") as f:
            f.writelines("sys : * : free energ* : 1 \n")
            f.writelines("mol : * : ln(G* : 1)")
        with open(f"{os.path.join(TARGET_DIR, 'input.in')}", "w") as f:
            f.write(str(self))
        os.chdir(TARGET_DIR)
        if os.name != "nt":
            os.system(
                f"{os.path.join(TARGET_DIR, 'sfbox')} {os.path.join(TARGET_DIR, 'input.in')} >> info.txt"
            )
        else:
            os.system(
                f"{os.path.join(TARGET_DIR, 'sfbox.exe')} {os.path.join(TARGET_DIR, 'input.in')} >> info.txt"
            )
        with open(f"{os.path.join(TARGET_DIR, 'info.txt')}", "r") as f:
            content = f.read()
        if "Problem solved" not in content:
            os.chdir(HOME_DIR)
            raise TimeoutError("Frame: Calculation process is ruined")
        with open(f"{os.path.join(TARGET_DIR, 'input.pro')}", "r") as f:
            lines = f.readlines()
        labels = lines[0].split()
        pro_data = np.loadtxt(f"{os.path.join(TARGET_DIR, 'input.pro')}", skiprows=1).T
        self.profile[labels[0]] = pro_data[0]
        self.profile_labels.append(labels[0])
        iter = 0
        for data in pro_data[1:]:
            iter += 3
            self.profile[labels[iter]] = data
            self.profile_labels.append(labels[iter])
            iter += 2

        with open(f"{os.path.join(TARGET_DIR, 'input.kal')}", "r") as f:
            lines = f.readlines()
        self.stats_labels = lines[0].split("\t")
        stats_data = np.loadtxt(
            f"{os.path.join(TARGET_DIR, 'input.kal')}", skiprows=1
        ).T
        iter = -1
        for stats in stats_data:
            iter += 1
            self.stats[self.stats_labels[iter]] = stats
        os.chdir(HOME_DIR)
