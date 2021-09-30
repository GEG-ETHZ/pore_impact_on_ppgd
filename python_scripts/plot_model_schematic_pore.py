from   netCDF4 import Dataset as ns
import numpy as np
import matplotlib

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle, Ellipse
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import os


gs  = gridspec.GridSpec(1,1)
fig = plt.figure(figsize=(6,3))
fs  = 18
lws = 2
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.usetex"] =True

# Working directory is the directory where you locate the simulating_pore_impact directory
# Usually is the project directory
WD    = os.path.expanduser('~/projects/')


data  = ns(WD+'pore_impact_on_ppgd/simulation_files/pore-scale/laplace_air_ellipse_p01_out.e')

# GET THE X-Coord of nodes
X = data.variables["coordx"]
X.set_auto_mask(False)
X = X [:]
# GET THE Y-Coord of nodes
Y = data.variables["coordy"]
Y.set_auto_mask(False)
Y = Y [:]

# GET THE NAMES OF THE NODE VARIABLES
variable_node_names = data.variables["name_nod_var"]
variable_node_names.set_auto_mask(False)
point_data_names = [b"".join(c).decode("UTF-8") for c in variable_node_names[:]]
print(point_data_names)

# GET THE NAMES OF THE ELEMENT VARIABLES
variable_element_names = data.variables["name_elem_var"]
variable_element_names.set_auto_mask(False)
element_data_names = [b"".join(c).decode("UTF-8") for c in variable_element_names[:]]
print(element_data_names)

# GET THE VARIABLES AND THE AUXVARIABKES
for i in np.arange(len(point_data_names)):
    if point_data_names[i] == "EField_x":
       EField_x = data.variables["vals_nod_var%s"%(i+1)]
       EField_x.set_auto_mask(False)
       # This minus (-) sign to adapt the positive gradient calcluated by MOOSE as standard.
       # However, the electric field defintion is - grad (V).
       EField_x = -1*EField_x [:]
    if point_data_names[i] == "EField_y":
       EField_y = data.variables["vals_nod_var%s"%(i+1)]
       EField_y.set_auto_mask(False)
       # This minus (-) sign to adapt the positive gradient calcluated by MOOSE as standard.
       # However, the electric field defintion is - grad (V).
       EField_y = -1*EField_y [:]
    if point_data_names[i] == "charge_density":
       charge_density = data.variables["vals_nod_var%s"%(i+1)]
       charge_density.set_auto_mask(False)
       charge_density = charge_density[:]
    if point_data_names[i] == "voltage":
       voltage = data.variables["vals_nod_var%s"%(i+1)]
       voltage.set_auto_mask(False)
       voltage = voltage [:]

for i in np.arange(len(element_data_names)):
    if element_data_names[i] == "electric_permittivity":
       electric_permittivity_rock = data.variables["vals_elem_var%seb1"%(i+1)]
       electric_permittivity_rock.set_auto_mask(False)
       electric_permittivity_rock = electric_permittivity_rock [:]
       # electric_permittivity_pore = data.variables["vals_elem_var%seb2"%(i+1)]
       # electric_permittivity_pore.set_auto_mask(False)
       # electric_permittivity_pore = electric_permittivity_pore [:]


EField_x = EField_x[1]
EField_y = EField_y[1]
voltage  = voltage[1]





EField = np.sqrt(EField_x**2 + EField_y ** 2)

ax1 = plt.subplot(gs[0,0])

connect = data.variables['connect1']
xy = np.array([X[:], Y[:]]).T
patches = []
for coords in xy[connect[:]-1]:
    quad = Polygon(coords, True)
    patches.append(quad)


# colors = 100 * np.random.rand(len(patches))
p = PatchCollection(patches, color="lightgrey")

# p.set_array(np.array(colors))
ax1.add_collection(p)


ax1.tricontour(X, Y, voltage, levels=30, linewidths=0.5, colors='k', zorder=1)

ax1.add_patch(Ellipse((0.5, 0.5), 0.141, 0.090, ls="-", lw=2, color="black",  zorder=3, fill=None))

plt.xlim([0, 1])
plt.ylim([0, 1])

# ax1.set_ylabel("HV")
# ax2 = ax1.twinx()
# ax2.set_ylabel("0")
#

# plt.legend()


#
# ax1.set_ylabel("HV", fontsize=fs)
# ax2.set_ylabel("0",  fontsize=fs)

ax1.tick_params(axis='x', which='both', top=False, bottom=False, labelsize=fs)
ax1.tick_params(axis='y', which='both', left=False, right=False, labelsize=fs)

# ax2.tick_params(axis='x', which='both', top=False, bottom=False, labelsize=fs)
# ax2.tick_params(axis='y', which='both', left=False, right=False, labelsize=fs)


for axis in ['top','bottom']:
   ax1.spines[axis].set_linewidth(3)
   ax1.spines[axis].set_linestyle("--")
   ax1.spines[axis].set_color("gray")
for axis in ['left']:
   ax1.spines[axis].set_linewidth(3)
   ax1.spines[axis].set_color("black")
for axis in ['right']:
   ax1.spines[axis].set_linewidth(3)
   ax1.spines[axis].set_color("black")


plt.yticks(rotation=90)


ax1.set_xticklabels('')
ax1.set_yticklabels('')
ax1.tick_params(color='red', labelcolor='red')

fsIns = fs


ax1.annotate("$\mathrm{Pore}$",
xy=(0.5, 0.5), xycoords='data',
xytext=(1.1, 0.5), textcoords='data',
arrowprops=dict(arrowstyle="->", lw=lws), fontsize=fsIns
)

ax1.annotate("$\mathrm{Granite}$",
xy=(0.88, 0.7), xycoords='data',
xytext=(1.1, 0.7), textcoords='data',
arrowprops=dict(arrowstyle="->", lw=lws), fontsize=fsIns
)


ax1.annotate("$V_P$=1",
xy=(-0.0, 0.8), xycoords='axes fraction',
xytext=(-0.35, 0.8),  arrowprops=dict(arrowstyle='->', lw=lws),
fontsize=fsIns)


ax1.annotate("$V_P$=0",
xy=(1, 0.9), xycoords='data',
xytext=(1.1, 0.9), textcoords='data',
arrowprops=dict(arrowstyle="->", lw=lws), fontsize=fsIns
)

ax1.annotate("", xy=(0, -0.1), xycoords='axes fraction',  xytext=(1, -0.1),  arrowprops=dict(arrowstyle='<->'))
ax1.annotate("", xy=(0, -0.1), xycoords='axes fraction',  xytext=(1, -0.1),  arrowprops=dict(arrowstyle='|-|'))
bbox=dict(fc="white", ec="none")
ax1.text(0.5, -0.1, "$W_P=1$", ha="center", va="center", bbox=bbox, fontsize=fsIns)

ax1.annotate("", xy=(-0.1, 0), xycoords='axes fraction',  xytext=(-0.1, 1),  arrowprops=dict(arrowstyle='<->'))
ax1.annotate("", xy=(-0.1, 0), xycoords='axes fraction',  xytext=(-0.1, 1),  arrowprops=dict(arrowstyle='|-|'))
bbox=dict(fc="white", ec="none")
ax1.text(-0.1, 0.5, "$H_P=1$", ha="center", va="center", bbox=bbox, fontsize=fsIns, rotation=90)

ax1.annotate("", xy=(1.05, 0), xycoords='axes fraction',  xytext=(1.3, 0),  arrowprops=dict(arrowstyle='<-'))
bbox=dict(fc="white", ec="none", alpha=0)
ax1.text(1.25, 0.07, "$x$", ha="center", va="center", bbox=bbox, fontsize=fsIns)

ax1.annotate("", xy=(1.05, 0), xycoords='axes fraction',  xytext=(1.05, 0.25),  arrowprops=dict(arrowstyle='<-'))
bbox=dict(fc="white", ec="none", alpha=0)
ax1.text(1.15 , 0.22, "$y$", ha="center", va="center", bbox=bbox, fontsize=fsIns)

plt.tight_layout()

plt.savefig(WD+'pore_impact_on_ppgd/figures/model_schematic_pore.png')
plt.savefig(WD+'pore_impact_on_ppgd/figures/model_schematic_pore.eps')
plt.show()
