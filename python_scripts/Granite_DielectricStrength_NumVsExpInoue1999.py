import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import ndimage
import math
import os
WD    = os.path.expanduser('~/projects/')

#LINE STYLES
# linestyle_tuple = [
#      ('loosely dotted',        (0, (1, 10))),
#      ('dotted',                (0, (1, 1))),
#      ('densely dotted',        (0, (1, 1))),
#
#      ('loosely dashed',        (0, (5, 10))),
#      ('dashed',                (0, (5, 5))),
#      ('densely dashed',        (0, (5, 1))),
#
#      ('loosely dashdotted',    (0, (3, 10, 1, 10))),
#      ('dashdotted',            (0, (3, 5, 1, 5))),
#      ('densely dashdotted',    (0, (3, 1, 1, 1))),
#
#      ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
#      ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
#      ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))]


# Figure dimensions
gs  = gridspec.GridSpec(1,1)
fig = plt.figure(figsize=(12,6))
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
               # ax.plot(g, v, "o", markersize=ms-3, color='white')

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
# 550 kV/cm is the required electric field to induce electric breakdown in 10 um pore under 0.1 MPa pressure

E_EF_Av = 4.5 * 1.75 #The total of the average enhacement factors
# 4.5 is the average at the electrodes from sample simulation.
# calculated from plot_efield_distribution_sample.py
# 1.75 is the average of all pore shapes for air fluid
# calculated from plot_efield_distribution_fluids-shapes.py

numDS10 = 70.8 #From the critical E figures
xmid10     = np.array([0,500/numDS10])
ymid10     = np.array([0,500])
ymid10 = ((ymid10[1]-ymid10[0])/(xmid10[1]-xmid10[0])) * xmid10


DS_Num10  = r"$E_{DS,Num,10\mu m}$"
DS_Num10 += " "
DS_Num10 += r"$\mathrm{=}~%2.0f~\mathrm{kV/cm}$"%numDS10
dsnum10 = ax.plot(xmid10,ymid10, lw=lws, color="blue",  label=numDS10)
ax.text(5.3,400, '$d_P=10\\mathrm{\mu m}$', fontsize=fs-5, rotation=47)


# The numerical dielectric strength calculated by our model
# 130 kV/cm is the required electric field to induce electric breakdown in 50 um pore under 0.1 MPa pressure
numDS50 = 16.5 #From the critical E figures
xmid50     = np.array([0,500/numDS50])
ymid50 = np.array([0,500])
ymid50 = ((ymid50[1]-ymid50[0])/(xmid50[1]-xmid50[0])) * xmid50


DS_Num50  = r"$E_{DS,Num,50\mu m}$"
DS_Num50 += " "
DS_Num50 += r"$\mathrm{=}~%2.0f~\mathrm{kV/cm}$"%numDS50
dsnum50 = ax.plot(xmid50,ymid50, lw=lws, color="green",  label=numDS50)
ax.text(7,125, '$d_P=50\\mathrm{\mu m}$', fontsize=fs-5, rotation=14)


# The numerical dielectric strength calculated by our model
# 550 kV/cm is the required electric field to induce electric breakdown in 100 um pore under 0.1 MPa pressure
numDS100 = 12.3 #From the critical E figures
xmid100     = np.array([0,500/numDS100])
ymid100 = np.array([0,500])
ymid100 = ((ymid100[1]-ymid100[0])/(xmid100[1]-xmid100[0])) * xmid100


DS_Num100  = r"$E_{DS,Num,100\mu m}$"
DS_Num100 += " "
DS_Num100 += r"$\mathrm{=}~%2.0f~\mathrm{kV/cm}$"%numDS100
dsnum100 = ax.plot(xmid100,ymid100, lw=lws, color="red",  label=numDS100)
ax.text(8.4,112, '$d_P=100\\mathrm{\mu m}$', fontsize=fs-5, rotation=10)



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
['$\\mathrm{Damage\;(Exp.)}$', '$\\mathrm{Damage\;Zone}$', '$\\mathrm{No\;Damage\;(Exp.)}$','$\\mathrm{No\;Damage\;Zone}$'],
bbox_to_anchor=(1.04,1), loc="upper left", numpoints = 1, prop={"size":fs-10}
)
plt.gca().add_artist(legenddata)
plt.legend((dsmax[0],dsmin[0],dsnum10[0],dsnum50[0],dsnum100[0]),[DS_Max,DS_Min,DS_Num10,DS_Num50,DS_Num100],
bbox_to_anchor=(1.04,0), loc="lower left", numpoints = 1, prop={"size":fs-8})



# 11.1 for mximum  58
# 12.9 for minmum  47

# plt.legend(numpoints = 1, prop={"size":fs-6})
plt.grid(color="gray")
plt.tight_layout()
plt.savefig(WD+'pore_impact_on_ppgd/figures/Granite_DielectricStrength_NumVsExpInoue1999.png')
plt.savefig(WD+'pore_impact_on_ppgd/figures/Granite_DielectricStrength_NumVsExpInoue1999.eps')

plt.show()
