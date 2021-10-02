from netCDF4 import Dataset as ns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle
import os
import math


gs  = gridspec.GridSpec(1,1)
fig = plt.figure(figsize=(13,3))
fs = 18
fsIns = fs - 6
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

Hs = 3  #[cm] the sample height
Ws = 13 #[cm] the sample width


Voltage        = 380.0 #kV
Electrode_gap  = 5.0 #cm
EField_Applied = (Voltage/Electrode_gap) * 1e-1 #MV/m


EField_x = EField_x[1] * 1e-6 / EField_Applied #V/m to MV/m and Normalized
EField_y = EField_y[1] * 1e-6 / EField_Applied #V/m to MV/m and Normalized

EField = np.sqrt(EField_x**2 + EField_y ** 2)

ax1 = plt.subplot(gs[0,0])

n   = -2
color_array = np.sqrt(((EField_x-n)/2)**2 + ((EField_y-n)/2)**2)

# plt.quiver(X, Y, EField_x, EField_y, color_array, alpha=0.7)

LEy      = round(EField_y.min(),-1)
HEy      = round(EField_y.max(),-1)+10
LevelsEy = np.linspace(0, 7, 200)
CS       = plt.tricontourf(X,Y,EField, levels=LevelsEy, cmap="jet")
cb       = plt.colorbar( orientation='horizontal', pad=0.2)
labels   = np.arange(0, 8, 1)
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
ax1.text(6.5, -0.4, "$W_S=\mathrm{%2.0f~cm}$"%Ws, ha="center", va="center", bbox=bbox, fontsize=fs)

ax1.annotate("", xy=(0.5, 0), xycoords='axes fraction',  xytext=(0.5, 1),   arrowprops=dict(arrowstyle='<->', color="white"))
# ax1.annotate("", xy=(0.5, 0), xycoords='axes fraction',  xytext=(0.5, 1),  arrowprops=dict(arrowstyle='|-|'))
bbox=dict(fc="white", ec="none", alpha=0)
ax1.text(6.2, 1.5, "$H_S=\mathrm{%2.0f~cm}$"%Hs, ha="center", va="center", bbox=bbox, fontsize=fs, color="white", rotation=90)



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

axins2.annotate("", xy=(0.5, 0), xycoords='axes fraction',  xytext=(0.5, 1),   arrowprops=dict(arrowstyle='<->', color="black"))
bbox=dict(fc="white", ec="none", alpha=0)
axins2.text(3.99, 2.95, "$\mathrm{%2.0f~mm}$"%((y2-y1)*10), ha="center", va="center", bbox=bbox, fontsize=fs-4, color="black", rotation=90)

axins2.annotate("", xy=(-0.004, -0.09), xycoords='axes fraction',  xytext=(1.005, -0.09),  arrowprops=dict(arrowstyle='<->'))
axins2.annotate("", xy=(-0.004, -0.09), xycoords='axes fraction',  xytext=(1.005, -0.09),  arrowprops=dict(arrowstyle='|-|'))
bbox=dict(fc="white", ec="none")
axins2.text(4., 2.885, "$\mathrm{%2.0f~mm}$"%((x2-x1)*10), ha="center", va="center", bbox=bbox, fontsize=fs-4)

# Weighting the mean:
dxg = 0.01
dyg = 0.01
xg     = np.arange(x1+dxg, x2, dxg)
yg     = np.arange(y1+dyg, y2, dyg)
Xg,Yg = np.meshgrid(xg,yg)


gix = np.vstack([Xg.ravel(), Yg.ravel()])[0]
giy = np.vstack([Xg.ravel(), Yg.ravel()])[1]

boxes = []
for n in np.arange(len(gix)):
        boxes.append([gix[n]-dxg, gix[n]+dxg, giy[n]-dyg, giy[n]+dyg])

boxes = np.array(boxes)
dict_weight = {}
for i in np.arange(len(X)):
      for n, coori in enumerate(boxes):
            if X[i] >= coori[0] and X[i] <= coori[1] and Y[i] >= coori[2] and Y[i] <= coori[3]:
                if EField[i] >=0.1: #To mask zeros and infinite values
                    key="%s"%n
                    if key not in dict_weight:
                        dict_weight.update({key: [EField[i]]})
                    dict_weight[key].append(EField[i])

mean_per_pexel = []
for key in dict_weight:
    mean_per_pexel.append(np.mean(np.array(dict_weight.get(key))))


mean_per_pexel = np.mean(np.array(mean_per_pexel))
print(mean_per_pexel)


E_Tip=ax1.indicate_inset_zoom(axins2, edgecolor="red")
E_TipLabel="$\mathrm{\\overline{E_{EF,S,E}}=%3.1f}$"%mean_per_pexel



# Plot the damage path from Ezzat et al. 2021 (Energies)
hr = 0.5    # the relative penetration depth for 50 mm electrode gap distance from Vazhov et al. 2010
dE = 1      # [cm] the electrode gap distance
h  = dE * hr # [cm]the penetration depth
R  = (h/2.0) + (dE**2/(8.0*h)) # The radius of the circle


XStart = 3.75
# Coordinated to plot the arc of the damage path
XX  =  np.linspace(XStart,XStart+dE, 1000)
YY  =  -np.sqrt(R**2 - (XX-dE/2-XStart)**2)+ R+Hs-h

# Weighting the mean:
dxg = 0.1
dyg = 0.1
xg     = np.arange(XStart+dxg, XStart+dE, dxg)
yg     = np.arange(3-h+dyg, 3, dyg)
Xg,Yg  = np.meshgrid(xg,yg)


gix = np.vstack([Xg.ravel(), Yg.ravel()])[0]
giy = np.vstack([Xg.ravel(), Yg.ravel()])[1]

def in_radius(c_x, c_y, r, x, y):
    return math.hypot(c_x-x, c_y-y) <= r

in_radius(XStart+dE,R+Hs-h,R,1,1)

boxes = []
for n in np.arange(len(gix)):
        if (in_radius(XStart+dE,R+Hs-h,R,gix[n],giy[n])):
            boxes.append([gix[n]-dxg, gix[n]+dxg, giy[n]-dyg, giy[n]+dyg])

boxes = np.array(boxes)
dict_weight = {}
for i in np.arange(len(X)):
      for n, coori in enumerate(boxes):
            if X[i] >= coori[0] and X[i] <= coori[1] and Y[i] >= coori[2] and Y[i] <= coori[3]:
                if EField[i] >=0.1: #To mask zeros and infinite values
                    key="%s"%n
                    if key not in dict_weight:
                        dict_weight.update({key: [EField[i]]})
                    dict_weight[key].append(EField[i])

mean_per_pexel = []
for key in dict_weight:
    mean_per_pexel.append(np.mean(np.array(dict_weight.get(key))))

mean_per_pexel = np.mean(np.array(mean_per_pexel))
print(mean_per_pexel)

NE_Region=ax1.plot(XX, YY, '--', color="black")
NE_RegionLabel = "$\mathrm{\\overline{E_{EF,S,NE}}=%3.1f}$"%mean_per_pexel

plt.legend((E_Tip[0], NE_Region[0]),[E_TipLabel, NE_RegionLabel],bbox_to_anchor=(-0.5,-0.65), loc="lower left", numpoints = 1, prop={"size":fs-4})

plt.tight_layout()

# Save the figures
plt.savefig(WD+'pore_impact_on_ppgd/figures/sample_efield.png')
plt.savefig(WD+'pore_impact_on_ppgd/figures/sample_efield.eps')

plt.show()
