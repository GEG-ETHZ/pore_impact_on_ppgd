from netCDF4 import Dataset as ns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle

gs  = gridspec.GridSpec(1,1)
fig = plt.figure(figsize=(13,3))
fs = 18
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.usetex"] =True

# Working directory is the directory where you locate the simulating_pore_impact directory
# Usually is the project directory
WD    = os.path.expanduser('~/projects/')

data  = ns(WD+'simulating_pore_impact/simulation_files/sample-scale/laplace_rock_top_out.e')

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
       EField_x = EField_x [:]
    if point_data_names[i] == "EField_y":
       EField_y = data.variables["vals_nod_var%s"%(i+1)]
       EField_y.set_auto_mask(False)
       EField_y = EField_y [:]
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




EField = np.sqrt(EField_x**2 + EField_y ** 2)

ax1 = plt.subplot(gs[0,0])

n   = -2
color_array = np.sqrt(((EField_x-n)/2)**2 + ((EField_y-n)/2)**2)

plt.quiver(X, Y, EField_x, EField_y, color_array, alpha=0.7)

LEy      = round(EField_y.min(),-1)
HEy      = round(EField_y.max(),-1)+10
LevelsEy = np.linspace(0, 7, 200)
CS       = plt.tricontourf(X,Y,EField, levels=LevelsEy, cmap="jet")
cb       = plt.colorbar( orientation='horizontal', pad=0.2)
labels   = np.arange(0,8, 1)
loc      =  labels
cb.set_ticks(loc)
cb.set_ticklabels(labels)
cb.ax.tick_params(labelsize=fs)


plt.xlim([0, 13])
plt.ylim([0, 3])

# ax1.set_xlabel("$S_w$ [cm]", fontsize=fs)
# ax1.set_ylabel("$S_h$ [cm]", rotation=0, fontsize=fs)

# ax1.tick_params(axis='both', which='major', labelsize=fs)
# ax1.tick_params(axis='both', which='minor', labelsize=fs)

# ax1.spines['left'].set_position('center')
ax1.set_xlabel(" ", fontsize=fs)
ax1.set_ylabel(" ",  fontsize=fs)

ax1.set_xticklabels('')
ax1.set_yticklabels('')
ax1.tick_params(axis='x', which='both', top=False, bottom=False, labelsize=fs)
ax1.tick_params(axis='y', which='both', left=False, right=False, labelsize=fs)


ax1.annotate("", xy=(-0.004, -0.15), xycoords='axes fraction',  xytext=(1.005, -0.15),  arrowprops=dict(arrowstyle='<->'))
ax1.annotate("", xy=(-0.004, -0.15), xycoords='axes fraction',  xytext=(1.005, -0.15),  arrowprops=dict(arrowstyle='|-|'))
bbox=dict(fc="white", ec="none")
ax1.text(6.5, -0.4, "$W_S=\mathrm{13~cm}$", ha="center", va="center", bbox=bbox, fontsize=fsIns)

ax1.annotate("", xy=(0.5, 0), xycoords='axes fraction',  xytext=(0.5, 1),   arrowprops=dict(arrowstyle='<->', color="white"))
# ax1.annotate("", xy=(0.5, 0), xycoords='axes fraction',  xytext=(0.5, 1),  arrowprops=dict(arrowstyle='|-|'))
bbox=dict(fc="white", ec="none", alpha=0)
ax1.text(6.2, 1.5, "$H_S=\mathrm{3~cm}$", ha="center", va="center", bbox=bbox, fontsize=fsIns, color="white", rotation=90)



# inset axes....
axins  = ax1.inset_axes([0.8, 0.05, 0.7, 0.8])
axins2 = ax1.inset_axes([-0.5, 0.05, 0.7, 0.8])

for boarder in ['bottom', 'left', 'right', 'top']:
    axins.spines[boarder].set_color('red')

for boarder in ['bottom', 'left', 'right', 'top']:
    axins2.spines[boarder].set_color('red')


plt.subplots_adjust(left=0.26, right=0.74, top=0.95, bottom=0.1)
plt.margins(0,0)


axins.quiver(X, Y, EField_x, EField_y, color_array, alpha=0.7)
# sub region of the original image
x1, x2, y1, y2 = 8.85, 9.15, 2.9, 3
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticklabels('')
axins.set_yticklabels('')
axins.xaxis.set_ticks_position('none')
axins.yaxis.set_ticks_position('none')



ax1.indicate_inset_zoom(axins,  edgecolor="red")


# inset axes....
axins2.quiver(X, Y, EField_x, EField_y, color_array, alpha=0.7)
# sub region of the original image
x1, x2, y1, y2 = 3.85, 4.15, 2.9, 3
axins2.set_xlim(x1, x2)
axins2.set_ylim(y1, y2)
axins2.set_xticklabels('')
axins2.set_yticklabels('')
axins2.xaxis.set_ticks_position('none')
axins2.yaxis.set_ticks_position('none')
ax1.indicate_inset_zoom(axins2,  edgecolor="red")

# plot the near electrodes region
ax1.add_patch(Rectangle((3.3, 1.4), 6.6, 1.6, ls="--", color="white", alpha=1, fill=None))

plt.tight_layout()

# Save the figures
plt.savefig(WD+'simulating_pore_impact/figures/sample_efield.png')
plt.savefig(WD+'simulating_pore_impact/figures/sample_efield.eps')

plt.show()
