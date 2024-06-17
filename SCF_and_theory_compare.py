import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

X1 = np.loadtxt(f"VAK\\Nb1000n0m10sigma0.01chi0.0.txt")
X2 = np.loadtxt(f"VAK\\Nb1000n0m10sigma0.01chi0.3.txt")
X3 = np.loadtxt(f"VAK\\Nb1000n0m10sigma0.01chi0.5.txt")
X4 = np.loadtxt(f"VAK\\Nb1000n0m10sigma0.01chi0.6.txt")

#Overlapping zone
fig, ax = plt.subplots()
fig.set_size_inches(8, 6)
ax.plot(X1[0][:], 0.45*X1[0][:]**(-1/3), "--", color="black")
ax.text(30, 0.15, "$-1/3$", fontsize=13) 

ax.loglog(X1[0][1:-60:2], X1[1][1:-60:2]/((1000 + 1 + (1000//10-1)*0)**(2/3)),  color = "red",     label ="Атермический р-ль")
ax.loglog(X2[0][1:-160:2], X2[1][1:-160:2]/((1000 + 1 + (1000//10-1)*0)**(2/3)),  color = "blue",  label ="Хороший р-ль")
ax.loglog(X3[0][1:-260:2], X3[1][1:-260:2]/((1000 + 1 + (1000//10-1)*0)**(2/3)),  color = "green", label ="Тета р-ль")
ax.loglog(X4[0][1:-300:2], X4[1][1:-300:2]/((1000 + 1 + (1000//10-1)*0)**(2/3)),  color = "gold",  label ="Плохой р-ль")

# ax.loglog(X1[0][1::2], X1[3][1::2], marker="^",  fillstyle='none', color = "red")
# ax.loglog(X2[0][1::2], X2[3][1::2], marker="^",  fillstyle='none', color = "blue")
# ax.loglog(X3[0][1::2], X3[3][1::2], marker="^",  fillstyle='none', color = "green")
# ax.loglog(X4[0][1::2], X4[3][1::2], marker="^",  fillstyle='none', color = "gold")

ax.scatter(323,  0.656*10**-1, c='red', s=70, zorder=3)
ax.text(323+70,  .68*10**-1, f"{323.0}", ha='center', va='bottom', color='black', fontsize=12)

ax.scatter(244.7, .72*10**-1, c='b', s=70, zorder=3)
ax.text(244.7+15, .75*10**-1, f"{244.7}", ha='center', va='bottom', color='black', fontsize=12)

ax.scatter(140.6, .883*10**-1, c='green', s=80, zorder=3)
ax.text(140.6-10, .77*10**-1, f"{140.6}", ha='center', va='bottom', color='black', fontsize=12)

ax.scatter(98, 1.435*10**-1, c='gold', s=80, zorder=3)
ax.text(98-10, 1.45*10**-1, f"{98}", ha='center', va='bottom', color='black', fontsize=12)

ax.scatter(np.sqrt(1000), .1165, c='none', s=60, zorder=3, edgecolors='black')
ax.text(np.sqrt(1000)+8, .106, f"${round(np.sqrt(1000), 1)}$", ha='center', va='bottom', color='black', fontsize=11)

ax.axvline(x=2*1000*0.01, linestyle='-.', linewidth = "0.9", color="black")
ax.text(18,  0.55*10**-1, f"${int(2*1000*0.01)}$", fontsize=13)
ax.text(22, 0.065, "$2\cdot N\sigma$", fontsize=13, 
        bbox=dict(facecolor='white', edgecolor='grey', boxstyle='round,pad=0.2'))

ax.axvline(x=2*(1000-10), linestyle='-.', linewidth = "0.9", color="black")
ax.text(2*(1000)-380, 0.55*10**-1, f"${1980}$", fontsize=13)
ax.text(600, 0.065, "$2\cdot(N_b-m+n)$", fontsize=13, 
        bbox=dict(facecolor='white', edgecolor='grey', boxstyle='round,pad=0.2'))


ax.set_title("$N = 1000$", fontsize=15)
ax.set_ylabel(r"$L(D) \cdot \eta^{4/3} /~N^{2/3}$", fontsize=15)
ax.set_xlabel(r"$D$", fontsize=17)
plt.legend(loc="upper right", fontsize=15)
plt.savefig("L.png", bbox_inches='tight')


#OmegaL
fig, ax = plt.subplots()
fig.set_size_inches(8, 6)

plt.loglog(X1[0][::2], 7.7*10**3* X1[0][::2] ** (-7 / 3), "--", color="black")

ax.loglog(X1[0][1::2], X1[4][1::2],  color = "red",  label ="Атермический р-ль")
ax.loglog(X2[0][1::2], X2[4][1::2],  color = "blue",  label ="Хороший р-ль")
ax.loglog(X3[0][1::2], X3[4][1::2],  color = "green", label ="Тета р-ль")
ax.loglog(X4[0][1::2], X4[4][1::2],  color = "gold",  label ="Плохой р-ль")

plt.loglog()

ax.axvline(x=2*1000*0.01, linestyle='-.', linewidth = "0.9", color="black")
ax.text(18,  0.8*10**-1, f"${int(2*1000*0.01)}$", fontsize=13)
ax.text(22, 0.12, "$2\cdot N\sigma$", fontsize=13, 
        bbox=dict(facecolor='white', edgecolor='grey', boxstyle='round,pad=0.2'))

ax.axvline(x=2*(1000-10), linestyle='-.', linewidth = "0.9", color="black")
ax.text(2*(1000)-380, 0.8*10**-1, f"${2*(1000-10)}$", fontsize=13)
ax.text(600, 0.12, "$2\cdot(N_b-m+n)$", fontsize=13, 
        bbox=dict(facecolor='white', edgecolor='grey', boxstyle='round,pad=0.2'))

ax.set_ylabel("$\Omega(D) \cdot L(D)$", fontsize = 15)
ax.set_xlabel(r"$D$", fontsize=17)
ax.set_ylim(10**-1, 4*10**0)
ax.set_title("$N = 1000,~наклон=-7/3$", fontsize=15)
plt.legend(loc="upper right", fontsize=15)
plt.savefig("OmegaL.png", bbox_inches='tight')

#Spreading Pressure
fig, ax = plt.subplots()
fig.set_size_inches(8, 6)

ax.plot(X1[0][0::2], -X1[5][0::2]-np.log(1-X1[5][0::2])-0.0*X1[5][0::2]**2,  color = "red",  label ="Атермический р-ль")
ax.plot(X2[0][0::2], -X2[5][0::2]-np.log(1-X2[5][0::2])-0.3*X2[5][0::2]**2,  color = "blue",  label ="Хороший р-ль")
ax.plot(X3[0][0::2], -X3[5][0::2]-np.log(1-X3[5][0::2])-0.5*X3[5][0::2]**2,  color = "green", label ="Тета р-ль")
ax.plot(X4[0][0::2], -X4[5][0::2]-np.log(1-X4[5][0::2])-0.6*X4[5][0::2]**2,  color = "gold",  label ="Плохой р-ль")


ax.plot(X1[0, 1::2] - 0.5 * (X1[0, 1::2] - X1[0, 0:-1:2]), -np.diff(X1[7][::2]) / np.diff(X1[0][::2]), marker="o",  fillstyle='none', linestyle = "none",color = "red")
ax.plot(X2[0, 1::2] - 0.5 * (X2[0, 1::2] - X2[0, 0:-1:2]), -np.diff(X2[7][::2]) / np.diff(X2[0][::2]), marker="o",  fillstyle='none', linestyle = "none",color = "blue")
ax.plot(X3[0, 1::2] - 0.5 * (X3[0, 1::2] - X3[0, 0:-1:2]), -np.diff(X3[7][::2]) / np.diff(X3[0][::2]), marker="o",  fillstyle='none', linestyle = "none",color = "green")
ax.plot(X4[0, 1::2] - 0.5 * (X4[0, 1::2] - X4[0, 0:-1:2]), -np.diff(X4[7][::2]) / np.diff(X4[0][::2]), marker="o",  fillstyle='none', linestyle = "none",color = "gold")

plt.loglog()

ax.axvline(x=2*1000*0.01, linestyle='-.', linewidth = "0.9", color="black")
ax.text(18,  0.7*10**-3, f"${int(2*1000*0.01)}$", fontsize=13)
ax.text(22, 0.0025, "$2\cdot N\sigma$", fontsize=13, 
        bbox=dict(facecolor='white', edgecolor='grey', boxstyle='round,pad=0.2'))

ax.axvline(x=2*(1000-10), linestyle='-.', linewidth = "0.9", color="black")
ax.text(2*(1000)-380, 0.7*10**-3, f"${2*(1000-10)}$", fontsize=13)
ax.text(600, 0.0025, "$2\cdot(N_b-m+n)$", fontsize=13, 
        bbox=dict(facecolor='white', edgecolor='grey', boxstyle='round,pad=0.2'))

plt.ylabel("$\Pi(D)$", fontsize = 15)
plt.ylim(10**-3, 2*10**0)
# plt.xlim(2*10**1, 3*10**2)
plt.title("$N=1000$", fontsize = 15)
plt.xlabel("D", fontsize = 15)
plt.legend(fontsize = 15, loc='upper right')
plt.savefig("PreSsure.png", bbox_inches='tight')

# Friction Force
fig, ax = plt.subplots()
fig.set_size_inches(8, 6)

ff1 = ((np.pi-2)/4)*X1[5][::2]
ff2 = ((np.pi-2)/4)*X2[5][::2]
ff3 = ((np.pi-2)/4)*X3[5][::2]
ff4 = ((np.pi-2)/4)*X4[5][::2]

ax.plot((-X1[5][0::2]-np.log(1-X1[5][0::2])-0.0*X1[5][0::2]**2), ff1,  color = "red",  label ="Атермический р-ль")
ax.plot((-X2[5][0::2]-np.log(1-X2[5][0::2])-0.3*X2[5][0::2]**2), ff2,  color = "blue",  label ="Хороший р-ль")
ax.plot((-X3[5][0::2]-np.log(1-X3[5][0::2])-0.5*X3[5][0::2]**2), ff3,  color = "green", label ="Тета р-ль")
ax.plot((-X4[5][0::2]-np.log(1-X4[5][0::2])-0.6*X4[5][0::2]**2), ff4,  color = "gold",  label ="Плохой р-ль")


# ax.plot(-X1[5][0::2]-np.log(1-X1[5][0::2])-0.0*X1[5][0::2]**2, X1[10][0::2],  marker="o",  fillstyle='none', linestyle = "none", color = "red")
# ax.plot(-X2[5][0::2]-np.log(1-X2[5][0::2])-0.3*X2[5][0::2]**2, X2[10][0::2],  marker="o",  fillstyle='none', linestyle = "none", color = "blue")
# ax.plot(-X3[5][0::2]-np.log(1-X3[5][0::2])-0.5*X3[5][0::2]**2, X3[10][0::2],  marker="o",  fillstyle='none', linestyle = "none", color = "green")
# ax.plot(-X4[5][0::2]-np.log(1-X4[5][0::2])-0.6*X4[5][0::2]**2, X4[10][0::2],  marker="o",  fillstyle='none', linestyle = "none", color = "gold")

# ax.plot(-np.diff(X1[7][0::2]) / np.diff(X1[0][0::2]), X1[10][0:-2:2],  marker="^",  fillstyle='none', linestyle = "none", color = "red")
# ax.plot(-np.diff(X2[7][0::2]) / np.diff(X2[0][0::2]), X2[10][0:-2:2],  marker="^",  fillstyle='none', linestyle = "none", color = "blue")
# ax.plot(-np.diff(X3[7][0::2]) / np.diff(X3[0][0::2]), X3[10][0:-2:2],  marker="^",  fillstyle='none', linestyle = "none", color = "green")
# ax.plot(-np.diff(X4[7][0::2]) / np.diff(X4[0][0::2]), X4[10][0:-2:2],  marker="^",  fillstyle='none', linestyle = "none", color = "gold")

plt.ylabel("$F_{тр}$", fontsize=16)
plt.xlabel("$\Pi(D)$", fontsize=16)
plt.xlim(0.0, 1.25)
plt.ylim(0.0, 1.5)
plt.legend(fontsize=15)
plt.savefig("FF.png", bbox_inches='tight')

#Friction coefficient

ff1 = ((np.pi-2) / 4) * X1[5][0::2]
ff2 = ((np.pi-2) / 4) * X2[5][0::2]
ff3 = ((np.pi-2) / 4) * X3[5][0::2]
ff4 = ((np.pi-2) / 4) * X4[5][0::2]

fig, ax = plt.subplots()
fig.set_size_inches(8, 6)
ax.plot(-X1[5][0::2]-np.log(1-X1[5][0::2])-0.0*X1[5][0::2]**2, X1[10][0::2]/  (-X1[5][0::2]-np.log(1-X1[5][0::2])-0.0*X1[5][0::2]**2), color = "red", label ="Атермический р-ль")
ax.plot(-X2[5][0::2]-np.log(1-X2[5][0::2])-0.3*X2[5][0::2]**2, X1[10][0::2] / (-X2[5][0::2]-np.log(1-X2[5][0::2])-0.3*X2[5][0::2]**2), color = "blue",label ="Хороший р-ль")
ax.plot(-X3[5][0::2]-np.log(1-X3[5][0::2])-0.5*X3[5][0::2]**2, X1[10][0::2] / (-X3[5][0::2]-np.log(1-X3[5][0::2])-0.5*X3[5][0::2]**2), color = "green", label ="Тета р-ль")
ax.plot(-X4[5][0::2]-np.log(1-X4[5][0::2])-0.6*X4[5][0::2]**2, X1[10][0::2] / (-X4[5][0::2]-np.log(1-X4[5][0::2])-0.6*X4[5][0::2]**2), color = "gold", label ="Плохой р-ль")

ax.plot(-np.diff(X1[7][::2]) / np.diff(X1[0][::2]), X1[10][0:-2:2] / (-X1[5][0:-2:2]-np.log(1-X1[5][0:-2:2])-0.0*X1[5][0:-2:2]**2), 
        marker="o",  fillstyle='none', linestyle = "none", color = "red")
ax.plot(-np.diff(X2[7][::2]) / np.diff(X2[0][::2]), X2[10][0:-2:2] / (-X2[5][0:-2:2]-np.log(1-X2[5][0:-2:2])-0.3*X2[5][0:-2:2]**2), 
        marker="o",  fillstyle='none', linestyle = "none", color = "blue")
ax.plot(-np.diff(X3[7][::2]) / np.diff(X3[0][::2]), X3[10][0:-2:2] / (-X3[5][0:-2:2]-np.log(1-X3[5][0:-2:2])-0.5*X3[5][0:-2:2]**2), 
        marker="o",  fillstyle='none', linestyle = "none", color = "green")
ax.plot(-np.diff(X4[7][::2]) / np.diff(X4[0][::2]), X4[10][0:-2:2] / (-X4[5][0:-2:2]-np.log(1-X4[5][0:-2:2])-0.6*X4[5][0:-2:2]**2),
        marker="o",  fillstyle='none', linestyle = "none", color = "gold")

plt.ylabel("$\mu$", fontsize=15)
plt.title("$N = 1000$", fontsize=14)
plt.xlabel("$\Pi(D)$", fontsize=16)
plt.ylim(0, 15)
plt.xlim(0.0, 1.)
plt.legend(fontsize=15)
plt.savefig("mu.png", bbox_inches='tight')