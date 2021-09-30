from netCDF4 import Dataset as ns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle

gs  = gridspec.GridSpec(1,1)
fig = plt.figure(figsize=(8,4))
fs = 18
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.usetex"] =True


# Working directory is the directory where you locate the simulating_pore_impact directory
# Usually is the project directory
WD    = os.path.expanduser('~/projects/')

data  = ns(WD+'pore_impact_on_ppgd/simulation_files/sample-scale/laplace_rock_top_out.e')

# GET THE X-Coord of nodes
X = data.variables["coordx"]
X.set_auto_mask(False)
X = X [:] * 1e2 #m to cm
# GET THE Y-Coord of nodes
Y = data.variables["coordy"]
Y.set_auto_mask(False)
Y = Y [:] * 1e2 #m to cm

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

Voltage        = 300.0 #kV
Electrode_gap  = 5.0 #cm
EField_Applied = (300.0/5.0) * 1e-1 #MV/m


EField_x = EField_x[1] * 1e-6 / EField_Applied #V/m to MV/m and Normalized
EField_y = EField_y[1] * 1e-6 / EField_Applied #V/m to MV/m and Normalized
voltage  = voltage[1]  * 1e-3 #V to kV



fsIns = fs

EField = np.sqrt(EField_x**2 + EField_y ** 2)

ax1 = plt.subplot(gs[0,0])

ax1.annotate("", xy=(0, -0.1), xycoords='axes fraction',  xytext=(1, -0.1),  arrowprops=dict(arrowstyle='<->'))
ax1.annotate("", xy=(0, -0.1), xycoords='axes fraction',  xytext=(1, -0.1),  arrowprops=dict(arrowstyle='|-|'))
bbox=dict(fc="white", ec="none")
ax1.text(6.5, -0.3, "$W_S=\mathrm{13~cm}$", ha="center", va="center", bbox=bbox, fontsize=fsIns)

ax1.annotate("", xy=(-0.02, 0), xycoords='axes fraction',  xytext=(-0.02, 1),  arrowprops=dict(arrowstyle='<->'))
ax1.annotate("", xy=(-0.02, 0), xycoords='axes fraction',  xytext=(-0.02, 1),  arrowprops=dict(arrowstyle='|-|'))
bbox=dict(fc="white", ec="none")
ax1.text(-0.3, 1.5, "$H_S=\mathrm{3~cm}$", ha="center", va="center", bbox=bbox, fontsize=fsIns, rotation=90)


ax1.annotate("", xy=(0.31, 0.97), xycoords='axes fraction',  xytext=(0.31, 1.7),  arrowprops=dict(arrowstyle='->'))
ax1.annotate("", xy=(0.69, 0.97), xycoords='axes fraction',  xytext=(0.69, 1.7),  arrowprops=dict(arrowstyle='->'))


#
# ax1.annotate("", xy=(HVEP,0.98), xycoords='axes fraction',  xytext=(HVEP,1.3),  arrowprops=dict(arrowstyle='-'))
# ax1.annotate("", xy=(GEP,0.98), xycoords='axes fraction',  xytext=(GEP,1.3),  arrowprops=dict(arrowstyle='-'))
# ax1.annotate("", xy=(HVEP-0.001,1.285), xycoords='axes fraction',  xytext=(GEP+0.001,1.285),  arrowprops=dict(arrowstyle='-'))
# ax1.annotate("", xy=(HVEP,1.11), xycoords='axes fraction',  xytext=(GEP,1.11),  arrowprops=dict(arrowstyle='<->'))

#
#
# ax1.text(6.5, 3.9, "$\mathrm{Pulse~Generator}~(V_E = \mathrm{380~kV})$", ha="center", va="center", bbox=bbox, fontsize=fsIns)
# ax1.text(6.5, 3.35, "$d_E = \mathrm{5~cm}$", ha="center", va="center", bbox=bbox, fontsize=fsIns)
# ax1.text(3.8, 3.3, "$+$", ha="center", va="center", bbox=bbox, fontsize=fsIns)
# ax1.text(9.2, 3.3, "$-$", ha="center", va="center", bbox=bbox, fontsize=fsIns)



ax1.tricontour(X, Y, voltage, levels=100, linewidths=0.5, colors='k', zorder=1)

plt.xlim([0, 13])
plt.ylim([0, 3])

ax1.set_xlabel(" ", fontsize=fs)
ax1.set_ylabel(" ",  fontsize=fs)

ax1.tick_params(axis='x', which='both', top=False, bottom=False, labelsize=fs)
ax1.tick_params(axis='y', which='both', left=False, right=False, labelsize=fs)

# ax1.add_patch(Rectangle((6.5 - 0.1, 1.5 - 0.1), 0.2, 0.2, ls="-", lw=2, color="red", angle="120", zorder=3, fill=None))
# ax1.add_patch(Rectangle((6.5 - 0.1, 2.2 - 0.1), 0.2, 0.2, ls="-", lw=2, color="red", angle="100", zorder=3, fill=None))

ax1.add_patch(Rectangle((6.5 - 0.1, 1.5 - 0.1), 0.2, 0.2, ls="-", lw=2, color="red", zorder=3, fill=None))
ax1.add_patch(Rectangle((6.5 - 0.1, 2.2 - 0.1), 0.2, 0.2, ls="-", lw=2, color="red", zorder=3, fill=None))


ax1.add_patch(Rectangle((4 - 0.1, 2.8 - 0.1), 0.2, 0.2, ls="-", lw=2, color="red", zorder=3, fill=None))
ax1.add_patch(Rectangle((5.5 - 0.1, 2.1 - 0.1), 0.2, 0.2, ls="-", lw=2, color="red", zorder=3, fill=None))

ax1.add_patch(Rectangle((8.9 - 0.1, 2.8 - 0.1), 0.2, 0.2, ls="-", lw=2, color="red", zorder=3, fill=None))
ax1.add_patch(Rectangle((7.4 - 0.1, 2.1 - 0.1), 0.2, 0.2, ls="-", lw=2, color="red", zorder=3, fill=None))


ax1.set_xticks([0,5,10,13])
ax1.set_yticks([0,3])
plt.yticks(rotation=90)

# LM =
# plt.subplots_adjust(bottom=0.1,top=0.7, left=0.05, right=0.95)
# plt.margins(0,0)

ax1.set_xticklabels('')
ax1.set_yticklabels('')
plt.tight_layout()

plt.savefig(WD+'pore_impact_on_ppgd/figures/model_schematic_sample.png')
plt.savefig(WD+'pore_impact_on_ppgd/figures/model_schematic_sample.eps')


plt.show()
