import numpy as np
from sfbox_api import Composition, Frame, Lat, Mol, Mon, Sys
from sfbox_api import Newton

def brushes(Nb: int, N2: int, n: int, n_layers) -> Frame:
    if N2 >=2 and N2 < Nb:
        comp1 = f'(X1)1(B1){Nb-N2}((B1)1[(S1){n}]){N2-1}(B1)1'
        comp2 = f'(X2)1(B2){Nb-N2}((B2)1[(S2){n}]){N2-1}(B1)1'
    elif N2 == 1:
        comp1 = f'(X1)1(B1){Nb-1}(B1)1[(S1){n}](B1)1'
        comp2 = f'(X2)1(B2){Nb-1}(B2)1[(S2){n}](B2)1'
    elif N2 == Nb:
        comp1 = f'(X1)1((B1)1[(S1){n}]){N2-1}(B1)1'
        comp2 = f'(X2)1((B2)1[(S2){n}]){N2-1}(B2)1'
    # if N2 == 0:
    #     comp1 = f'(X1)1(B1){Nb-1}(B1)1'
    #     comp2 = f'(X2)1(B2){Nb-1}(B2)1'
      
    theta = 6.0   
    lat = Lat(
        **{
            "n_layers": n_layers,
            "geometry": "flat",
            "lowerbound": "surface",
            "upperbound": "surface",
        }
    )
    mons = [
        Mon(**{"name": "X1", "freedom": "pinned", "pinned_range": "1"}),
        Mon(**{"name": "B1", "freedom": "free"}),
        Mon(**{"name": "S1", "freedom": "free"}),
        Mon(**{"name": "X2", "freedom": "pinned", "pinned_range": str(n_layers)}),
        Mon(**{"name": "B2", "freedom": "free"}),
        Mon(**{"name": "S2", "freedom": "free"}),
        Mon(**{"name": "W", "freedom": "free"}),
    ]
    mols = [
        Mol(**{"name": "Water", "composition": "(W)1", "freedom": "solvent"}),
        Mol(
            **{
                "name": "pol1",
                "composition": comp1,
                "freedom": "restricted",
                "theta": theta,
            }
        ),
        Mol(
            **{
                "name": "pol2",
                "composition": comp2,
                "freedom": "restricted",
                "theta": theta,
            }
        ),
    ]
    sys = Sys()
    chi = 0.0

    # chi_list = {"X1 W": chi, "B1 W": chi,"X2 W": chi, "B2 W": chi}
    chi_list = {"X1 W": chi, "B1 W": chi, "S1 W": chi, "X2 W": chi, "B2 W": chi, "S2 W": chi}        
    frame = Frame(lat, sys, mols, mons, chi_list=chi_list)
    frame.text += "sys : name : overflow_protection : true"
    frame.run()
    print(frame.profile_labels)
    return frame


if __name__ == "__main__":
    Nb = 60
    n = 6
    theta = 6.0
    for N2 in range(59, 60, 1):
        data = []
        for n_layers in range(int(2*theta)+2, 2*Nb+1, 1):
            frame = brushes(Nb, N2, n, n_layers)
            phi1 = frame.profile["pol1"][1:-1]
            phi2 = frame.profile["pol2"][1:-1]
            z = frame.profile["layer"][1:-1]
            z_mean = 0.5 * (z[0] + z[-1])

            if len(z) % 2 == 0:
                z0 = len(z) // 2 + 1
            else:
                z0 = len(z) // 2

            L1 = 2.0 * np.sum(phi1[z0:] * (z[z0:] + 0.5 - z_mean)) / np.sum(phi1[z0:])
            # L2 = np.sum(phi1[:] * phi2[:] * np.square(z[:] + 0.5 - z_mean)) / np.sum(phi1[:] * phi2[:])
            # L2 = 2.0 * L2**0.5
            phi_mean = phi1[z0] + phi2[z0]

            L_Omega = np.sum(phi1[:] * phi2[:])

            F = frame.stats["sys : name : free energy"]

            F_int = np.sum((1 - phi1[:] - phi2[:]) * np.log(1 - phi1[:] - phi2[:]))

            F_f = np.sum((phi1[:]**2 * phi2[:]**2) / (phi1[:]**2 + phi2[:]**2))

            print(n_layers, L1, F_int)

            data.append([n_layers, L1, L_Omega, phi_mean, F_int, F, F_f])
        np.savetxt(f"N2_{N2}n{n}theta{theta}.txt", np.array(data).T)