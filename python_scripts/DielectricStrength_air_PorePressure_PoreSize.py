"""
Plot the Paschen Law for air at differen pore sizes
"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import ndimage
import os

WD    = os.path.expanduser('~/projects/')

# Choose the x-axis variable, the pore pressure or the pore size
variable = "pressure" # X-Axis
variable = "size"     # X-Axis

# Figure dimensions
gs  = gridspec.GridSpec(1,1)
fig = plt.figure(figsize=(7,4.5))
ax  = plt.subplot(gs[0,0])
ax1 = ax.twinx()

# Font sizes and line styles
fs     = 24 #font_size for the plot
ms     = 16 #marker_size
lws    = 3
lines  = ["-","--","-."]
colors = ["red","blue","black"]

# Paschen law parameters;
A      = 112.50  * 1e-1 #1/(Pa.m)
gamma  = 0.001
B      = 2737.50  * 1e-1 #V/(Pa.m)


if variable == "size":
    # Pore pressures: 0.1, 1, and 2.5 MPa
    # Pore sizes: range from 10 to 150 um
    for n, Pr in enumerate(np.array([1e5, 1e6, 2.5e6])):
        d  = np.arange(10, 150, 0.2) * 1e-6

        # The breakdown voltage threshold by Paschen Law
        V_bd_n = B*Pr*d/np.log(d*A*Pr/ np.log(1./gamma + 1)) #V
        # The air dielectric strenght, divid both sides of Paschen Law by the pore size
        E_bd   = (V_bd_n/d) * 1e-5 #kV/cm (1e-5 factor is to convert from V/um to kV/cm)

        # Plot the air dielectric strength as a fubction of the pore size
        ax.plot(d[0:]*1e6, E_bd[0:],  lines[n], lw=lws, color=colors[n], label="$P_P=%2.1f~\\mathrm{MPa}$"%(Pr*1e-6))

        # Plot the critical electric field required at the electrodes to achieve the air dielectric strength
        E_EF_Av = 4.5 * 1.75 #The total of the average enhacement factors
        # 4.5 is the average at the electrodes from sample simulation.
        # calculated from plot_efield_distribution_sample.py
        # 1.75 is the average of all pore shapes for air fluid
        # calculated from plot_efield_distribution_fluids-shapes.py
        ax1.plot(d[0:]*1e6, E_bd[0:]/E_EF_Av,  lines[n], lw=lws, color=colors[n], label="$P_P=%2.1f~\\mathrm{MPa}$"%(Pr*1e-6))

if variable == "pressure":
    # Pore pressures: 0.1, 1, and 2.5 MPa
    # Pore sizes: range from 10 to 150 um
    for n, dp in enumerate(np.array([20, 50, 150])):
        d       = dp * 1e-6 #m
        Pr = np.linspace(1e5, 2.5e6, 470000)

        # The breakdown voltage threshold by Paschen Law
        V_bd_n = B*Pr*d/np.log(d*A*Pr/ np.log(1./gamma + 1)) #V
        # The air dielectric strenght, divid both sides of Paschen Law by the pore size
        E_bd   = (V_bd_n/d) * 1e-5 #kV/cm (1e-5 factor is to convert from V/um to kV/cm)

        # Plot the air dielectric strength as a fubction of the pore size
        ax.plot(Pr[:]*1e-6, E_bd[:],  lines[n], lw=lws, color=colors[n],  label="$d_P=%s~\\mathrm{\mu m}$"%dp)

        # Plot the critical electric field required at the electrodes to achieve the air dielectric strength
        E_EF_Av = 4.5 * 1.75 #The total of the average enhacement factors
        # 4.5 is the average at the electrodes from sample simulation.
        # calculated from plot_efield_distribution_sample.py
        # 1.75 is the average of all pore shapes for air fluid
        # calculated from plot_efield_distribution_fluids-shapes.py
        ax1.plot(Pr[:]*1e-6, E_bd[:]/E_EF_Av,  lines[n], lw=lws, color=colors[n], label="$d_P=%s~\\mathrm{\mu m}$"%dp)


if variable == "size":
    # X-Axis represnte the pore size
    ax.set_xlabel("$d_P~\\mathrm{[\\mu m]}$", fontsize=fs)
    ax.set_xlim(10,150)
    ax.set_xticks([10,50,100,150])

if variable == "pressure":
    ax.set_xlabel("$P_P~\\mathrm{[MPa]}$", fontsize=fs)
    ax.set_xlim(0.1,2.5)
    ax.set_xticks([0.1,0.5,1,1.5,2,2.5])



# Y-Axis (Left) represnets the dielectric strength
ax.set_ylabel("$E_{DS,P}~\\mathrm{[kV/cm]}$", fontsize=fs)
ax.set_ylim(0,2000)
ax.set_yticks([0,500,1000,1500,2000])

# Y-Axis (Right) represnets the critical electric field at the electrodes
ax1.set_ylabel("$E_{Cr,E}~\\mathrm{[kV/cm]}$", fontsize=fs)
ax1.set_ylim(0,2000/E_EF_Av)
ax1.set_yticks([0, 500/E_EF_Av, 1000/E_EF_Av, 1500/E_EF_Av, 2000/E_EF_Av])

# ax1.set_yticks([0, 500/E_EF_Av, 1000/E_EF_Av, 1500/E_EF_Av, 2000/E_EF_Av])
# ax1.set_yticklabels((0, int(500/E_EF_Av), int(1000/E_EF_Av), int(1500/E_EF_Av), int(2000/E_EF_Av)))

# Use the LaTex text style
plt.rcParams['xtick.labelsize']  = fs
plt.rcParams['ytick.labelsize']  = fs
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.usetex"]      = True

ax.grid()
plt.legend(loc=0, numpoints = 1, prop={"size":fs-6})
plt.tight_layout()
plt.savefig(WD+'pore_impact_on_ppgd/figures/AirDielectricStrength_vs_Pore%s.png'%(variable.title()))
plt.savefig(WD+'pore_impact_on_ppgd/figures/AirDielectricStrength_vs_Pore%s.eps'%(variable.title()))
plt.show()
