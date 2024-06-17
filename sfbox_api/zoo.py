from .frame import Frame
from .lattice import Lat
from .molecule import Mol
from .monomer import Mon
from .system import Sys


def comb_brush(Nb: int, n: int, m: int, n_layers, sigma: float) -> Frame:
    if n <= 0:
        if m > 1:
            comp = f"(X)1((A){m}){Nb//m-1}(A){m-1}(G)1"
        else:
            comp = f"(X)1((A){m}){Nb//m-1}(G)1"
    else:
        if m > 1:
            comp = f"(X)1((A){m}[(A){n}]){Nb//m-1}(A){m-1}(G)1"
        else:
            comp = f"(X)1((A){m}[(A){n}]){Nb//m-1}(G)1"
    theta = (Nb + 1 + (Nb // m - 1) * n) * sigma
    lat = Lat.model_validate({"n_layers": n_layers, "geometry": "cylindrical"})
    mons = [
        Mon.model_validate({"name": "X", "freedom": "pinned", "pinned_range": "1"}),
        Mon.model_validate({"name": "A", "freedom": "free"}),
        Mon.model_validate({"name": "G", "freedom": "free"}),
        Mon.model_validate({"name": "W", "freedom": "free"}),
    ]
    mols = [
        Mol.model_validate(
            {"name": "Water", "composition": "(W)1", "freedom": "solvent"}
        ),
        Mol.model_validate(
            {
                "name": "pol",
                "composition": comp,
                "freedom": "restricted",
                "theta": theta,
            }
        ),
    ]
    sys = Sys()
    chi = 0.0
    chi_list = {"X W": chi, "A W": chi}

    frame = Frame(lat, sys, mols, mons, chi_list=chi_list)
    frame.run()

    return frame


def barbwire(p, n, m, q, n_layers, sigma):
    comp = f"(X)1(A){m-1}([(A){n}]){q}((A){m}([(A){n}]){q}){p-1}(A){m-1}(G)1"
    N = (m + q * n) * p + m
    theta = N * sigma
    lat = Lat.model_validate({"n_layers": n_layers, "geometry": "cylindrical"})
    mons = [
        Mon.model_validate({"name": "X", "freedom": "pinned", "pinned_range": "1"}),
        Mon.model_validate({"name": "A", "freedom": "free"}),
        Mon.model_validate({"name": "G", "freedom": "free"}),
        Mon.model_validate({"name": "W", "freedom": "free"}),
    ]
    mols = [
        Mol.model_validate(
            {"name": "Water", "composition": "(W)1", "freedom": "solvent"}
        ),
        Mol.model_validate(
            {
                "name": "pol",
                "composition": comp,
                "freedom": "restricted",
                "theta": theta,
            }
        ),
    ]
    sys = Sys()
    chi = 0.0
    chi_list = {"X W": chi, "A W": chi}

    frame = Frame(lat, sys, mols, mons, chi_list=chi_list)
    frame.run()

    return frame


def polyacid(
    N: int,
    sigma: float,
    pK: float,
    ionic_strength: float,
    chi: float,
    n_layers: int = 0,
) -> Frame:
    if N < 3:
        raise ValueError("polyacid: N < 3")
    if pK < 0.0:
        raise ValueError("polyacid: pK < 0.0")
    if ionic_strength < 0.0 or ionic_strength > 1.0:
        raise ValueError("polyacid: ionic_strength < 0.0 or ionic_strength > 1.0")
    if n_layers < 1:
        n_layers = N + 1

    comp = f"(X)1(A){N-2}(G){1}"
    theta = N * sigma

    lat = Lat.model_validate(
        {
            "n_layers": n_layers,
            "geometry": "flat",
            "lowerbound": "surface",
        }
    )
    mons = [
        Mon.model_validate({"name": "W", "freedom": "free"}),
        Mon.model_validate({"name": "X", "freedom": "pinned", "pinned_range": "1"}),
        Mon.model_validate({"name": "A", "freedom": "free"}),
        Mon.model_validate({"name": "G", "freedom": "free"}),
        Mon.model_validate({"name": "P", "freedom": "free", "valence": 1.0}),
        Mon.model_validate({"name": "M", "freedom": "free", "valence": -1.0}),
    ]
    mols = [
        Mol.model_validate(
            {"name": "water", "composition": "(W)1", "freedom": "solvent"}
        ),
        Mol.model_validate(
            {
                "name": "pol",
                "composition": comp,
                "freedom": "restricted",
                "theta": theta,
            }
        ),
        Mol.model_validate(
            {
                "name": "ionp",
                "composition": "(P)1",
                "freedom": "free",
                "phibulk": ionic_strength,
            }
        ),
        Mol.model_validate(
            {
                "name": "ionm",
                "composition": "(M)1",
                "freedom": "free",
                "phibulk": ionic_strength,
            }
        ),
    ]
    sys = Sys()
    chi_list = {
        "X W": chi,
        "A W": chi,
        "G W": chi,
        "X P": chi,
        "A P": chi,
        "G P": chi,
        "X M": chi,
        "A M": chi,
        "G M": chi,
    }

    frame = Frame(lat, sys, mols, mons, chi_list=chi_list)
    frame.text += "state : H3O : valence: 1 \n"
    frame.text += "state : H2O : valence: 0 \n"
    frame.text += "state : OH : valence: -1 \n"

    frame.text += "state : X0 : valence: 0 \n"
    frame.text += "state : X1 : valence: -1 \n"

    frame.text += "state : A0 : valence: 0 \n"
    frame.text += "state : A1 : valence: -1 \n"

    frame.text += "state : G0 : valence: 0 \n"
    frame.text += "state : G1 : valence: -1 \n"

    frame.text += "mon : W : state1: H3O \n"
    frame.text += "mon : W : state2: H2O \n"
    frame.text += "mon : W : state3: OH \n"

    frame.text += "mon : X : state1: X0 \n"
    frame.text += "mon : X : state2: X1 \n"

    frame.text += "mon : A : state1: A0 \n"
    frame.text += "mon : A : state2: A1 \n"

    frame.text += "mon : G : state1: G0 \n"
    frame.text += "mon : G : state2: G1 \n"

    frame.text += "reaction : auto : equation: 2(H2O)=1(H3O)1(OH) \n"
    frame.text += "reaction : auto : pK: 17.5 \n"

    frame.text += "reaction : pdx : equation: 1(X0)1(H2O)=1(X1)1(H3O) \n"
    frame.text += f"reaction : pdx : pK: {pK+1.76} \n"

    frame.text += "reaction : pda : equation: 1(A0)1(H2O)=1(A1)1(H3O) \n"
    frame.text += f"reaction : pda : pK: {pK+1.76} \n"

    frame.text += "reaction : pdg : equation: 1(G0)1(H2O)=1(G1)1(H3O) \n"
    frame.text += f"reaction : pdg : pK: {pK+1.76} \n"

    frame.run()

    return frame
