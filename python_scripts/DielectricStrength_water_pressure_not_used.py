import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import ndimage





fs     = 24 #font_size for the plot
ms     = 16 #marker_size
lws    = 3

gs  = gridspec.GridSpec(1,1)
fig = plt.figure(figsize=(6,5))

ax  = plt.subplot(gs[0,0])
ax2 = ax.twinx()


lines = ["-","--",":"]
colors = ["red","blue","black"]

for n, dp in enumerate(np.array([20,50,150])):
    S      = (dp * 1e-4)**2       # cm^2
    teff   = 1.5                  # mus
    Pr     = np.linspace(0.1, 2.5, 40)
    E_ds_w = 185.0 * S**(-1/16) * teff**(-1/3) * Pr**(1/8)
    ax.plot(Pr[:], E_ds_w[:], lines[n], lw=lws, color=colors[n], label="$d_p=%s~\\mathrm{\mu m}$"%dp)
    ax2.plot(Pr[:], E_ds_w[:]*10, lines[n], lw=lws, color=colors[n], label="$d_p=%s~\\mathrm{\mu m}$"%dp)

plt.xlim(0.1,2.5)
ax.set_ylim(200,400)
ax2.set_ylim(2000,4000)

ax.set_xlabel("$P_P~\\mathrm{[MPa]}$", fontsize=fs)
ax.set_xticks([0.1,0.5,1,1.5,2,2.5])
ax.set_ylabel("$E_{DS,W}~\\mathrm{[kV/cm]}$", fontsize=fs)
ax2.set_ylabel("$E_{DS,E}~\\mathrm{[kV/cm]}$", fontsize=fs)

plt.rcParams['xtick.labelsize']  = fs
plt.rcParams['ytick.labelsize']  = fs
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.usetex"]      = True

ax.grid()
ax2.grid(None)

ax.legend(loc=0, numpoints = 1, prop={"size":fs-6})

plt.tight_layout()
plt.show()



#
# #%%%%%%%%%%%%%%%%%%%%%%%%%%
# A      = 112.50  * 1e-1 #1/(Pa.m)
#
# gamma  = 0.001
#
# B      = 2737.50  * 1e-1 #V/(Pa.m)
#
#
# # for dp in np.array([20, 50, 150]):
# dp      = 10
# d       = dp * 1e-6 #m
# Pr      = np.linspace(1e5, 1e6, 470000)
# V_bd_n  = B*Pr*d/np.log(d*A*Pr/ np.log(1./gamma + 1)) #V
# E_bd    = (V_bd_n/d) * 1e-5 #kV/cm
# # E_bd2  = abs(B*Pr*(np.log(d*A*Pr/ np.log(1./gamma + 1)) - 1.0) / np.log(d*A*Pr/ np.log(1./gamma + 1))**2.0)
# # plt.plot(Pr[100:]*d, V_bd_n[100:],  lw=lws,  label="$E_{thr}$")
# # ax.plot(Pr[:]*1e-6, E_bd[:],  lw=lws,  label="Air at $d_p=%s~\mu m$"%dp)
# # ax.plot(Pr[200:]*1e-6, V_bd_n[200:],  lw=lws,  label="$d_p=%s~\mu m$"%dp)
#
# # ax.plot(Pr[200:]*1e-6, E_bd[200:],  lw=lws,  label="$d_p=%s~\mu m$"%dp)
#
#
# # plt.yscale('log')
# # plt.xscale('log')
# # plt.xlim(0.1,6)
# # plt.ylim(50,1e4)
# plt.ylabel("$E_{ds,A}~[kV/cm]$",  fontsize=fs)
# plt.xlabel("$P_f[MPa]$", fontsize=fs)
# plt.rcParams['xtick.labelsize']  = fs
# plt.rcParams['ytick.labelsize']  = fs
# plt.rcParams["mathtext.fontset"] = "cm"
# plt.rcParams["text.usetex"]      = True
# plt.legend(loc=0, numpoints = 1, prop={"size":fs})
# plt.grid(color="gray")
# ax.set_xticks([0.1,2,4,6])
#
