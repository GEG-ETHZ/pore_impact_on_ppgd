import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import ndimage
import math
import os
WD    = os.path.expanduser('~/projects/')


# Figure dimensions
gs  = gridspec.GridSpec(1,1)
fig = plt.figure(figsize=(9,6))
ax  = plt.subplot(gs[0,0])

# Font sizes and line styles
fs     = 24 #font_size for the plot
ms     = 12 #marker_size
lws    = 3


# Experimental data from Inoue_1999
ElectrodeVoltage    = np.array([240, 300, 390, 480])
ElectrodeGap        = np.array([2, 5, 7, 10]) #cm

# 0 no damage , 1 means damage according to Inoue_1999 (figure 8a)
damage              = np.array([[1,0,0,0],
                                [1,1,0,0],
                                [1,1,0,0],
                                [1,1,1,1]])
# Plot the experimental data
damageEvents   = 0
nodamageEvents = 0
for nv, v in enumerate(ElectrodeVoltage):
    for ng, g in enumerate(ElectrodeGap):
        E = v/g

        # Damage Cases
        if damage[nv][ng] == 0:
            color="black"
            if nodamageEvents ==0:
                nodamagepoint=plt.plot(g, v, "s", markersize=ms, color=color,  label="$\\mathrm{No-Damage_{Exp}}$")
            else:
                ax.plot(g, v, "s", markersize=ms, color=color)
            nodamageEvents += 1

        # No damage cases
        if damage[nv][ng] == 1:
            color="black"
            if damageEvents == 0:
               damagepoint=plt.plot(g, v, "o", markersize=ms,  color=color, label="$\\mathrm{Damage_{Exp}}$")
            else:
               ax.plot(g, v, "o", markersize=ms, color=color)
            damageEvents += 1


# The experimental minimum dielectric strength and the no-damage zone
xmin = np.array([0,500/(47)])
ymin = np.array([0,500])
ymin = ((ymin[1]-ymin[0])/(xmin[1]-xmin[0])) * xmin
nodamagezone = plt.fill_between(xmin,ymin,0,  facecolor='grey', alpha=0.5, label="$\\mathrm{No-Damage~Zone}$")

DS_Min  = r"$E_{DS,Exp,Min}$"
DS_Min += " "
DS_Min += r"$\mathrm{=}~%s~\mathrm{kV/cm}$"%47
dsmin = plt.plot(xmin,ymin,  ":",  lw=lws, color="black",  label=DS_Min)

# The experimental maximum dielectric strength and the damage zone
xmax = np.array([0,500/(58)])
ymax = np.array([0,500])
ymax = ((ymax[1]-ymax[0])/(xmax[1]-xmax[0])) * xmax
damagezone = plt.fill_between(xmax,ymax,500,  facecolor='lightsteelblue', alpha=0.5, label="$\\mathrm{Damage~Zone}$")

DS_Max  = r"$E_{DS,Exp,Max}$"
DS_Max += " "
DS_Max += r"$\mathrm{=}~%s~\mathrm{kV/cm}$"%58
dsmax = plt.plot(xmax,ymax,  "--",  lw=lws, color="black",label=DS_Max)


# The numerical dielectric strength calculated by our model
x = np.array([0,500/(128.0/2.5)])
# 128 kV/cm is the required electric field to induce electric breakdown in 50 um pore under 0.1 MPa pressure
# 2.5  is the enhancement factor (2 the average of sample scale) * (1.25 the average of the pore scale)

y = np.array([0,500])
y = ((y[1]-y[0])/(x[1]-x[0])) * x


DS_Num  = r"$E_{DS,Num}$"
DS_Num += " "
DS_Num += r"$\mathrm{=}~%s~\mathrm{kV/cm}$"%51
dsnum = ax.plot(x,y,  lw=lws, color="black",  label=DS_Num)


ax.set_xlim(0,10.6)
ax.set_xlabel("$d_E~\\mathrm{[cm]}$", fontsize=fs)

ax.set_ylim(0,500)
ax.set_ylabel("$V_E~\\mathrm{[kV]}$",  fontsize=fs)

plt.rcParams['xtick.labelsize']  = fs
plt.rcParams['ytick.labelsize']  = fs
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.usetex"]      = True

legenddata = plt.legend(
(damagepoint[0],damagezone,nodamagepoint[0],nodamagezone),
['Damage (Exp.)','Damage Zone','No Damage (Exp.)','No Damage Zone'],
loc=4, numpoints = 1, prop={"size":fs-10}
)
plt.gca().add_artist(legenddata)
plt.legend((dsmax[0],dsmin[0],dsnum[0]),[DS_Max,DS_Min,DS_Num],
loc=8, numpoints = 1, prop={"size":fs-8})

# plt.legend(numpoints = 1, prop={"size":fs-6})
plt.grid(color="gray")
plt.tight_layout()
plt.savefig(WD+'pore_impact_on_ppgd/figures/Granite_DielectricStrength_NumVsExpInoue1999.png')
plt.savefig(WD+'pore_impact_on_ppgd/figures/Granite_DielectricStrength_NumVsExpInoue1999.eps')

plt.show()
