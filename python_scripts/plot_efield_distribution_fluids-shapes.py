from netCDF4 import Dataset as ns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib
from mpl_toolkits.axisartist.axislines import SubplotZero
import os



shapes = ['ellipse_x', 'circle', 'square', 'ellipse_y']
#shapes = ['ellipse_x', 'circle']
#shapes = ['square', 'ellipse_y']
# shapes = ['circle']

fluids = ['geometry', 'air', 'water']
# fluids = ['air']

EmaxAir = []
EminWat = []

gs  = gridspec.GridSpec(len(fluids), len(shapes), wspace=0.01, hspace=0.05)

if len(shapes) == 1:
   fig = plt.figure(figsize=(16,3.5))
   bottomspace = 0.2
if len(shapes) == 2:
   fig = plt.figure(figsize=(16,5))
   bottomspace = 0.15
if len(shapes) == 4:
   fig = plt.figure(figsize=(11,7))
   bottomspace = 0.1
fs = 24

# Working directory is the directory where you locate the simulating_pore_impact directory
# Usually is the project directory
WD    = os.path.expanduser('~/projects/')

for f, fluid in enumerate(fluids):
    for n, shape in enumerate(shapes):
        if fluid == "geometry":
            file  = 'laplace_air_%s_p01_out.e'%(shape)
        else:
            file  = 'laplace_%s_%s_p01_out.e'%(fluid, shape)
        data  = ns(WD+'pore_impact_on_ppgd/simulation_files/pore-scale/'+file)
        # GET THE X-Coord of nodes
        X = data.variables["coordx"]
        X.set_auto_mask(False)
        X = X [:]
        # GET THE Y-Coord of nodes
        Y = data.variables["coordy"]
        Y.set_auto_mask(False)
        Y = Y [:]
        print(f,n)


        # GET THE NAMES OF THE NODE VARIABLES
        variable_node_names = data.variables["name_nod_var"]
        variable_node_names.set_auto_mask(False)
        point_data_names = [b"".join(c).decode("UTF-8") for c in variable_node_names[:]]
        print(point_data_names)

        for i in np.arange(len(point_data_names)):
            if point_data_names[i] == "EField_x":
               EField_x = data.variables["vals_nod_var%s"%(i+1)]
               EField_x.set_auto_mask(False)
               # This minus (-) sign to adapt the positive gradient calcluated by MOOSE as standard.
               # However, the electric field defintion is - grad (V).
               EField_x = -1*EField_x [:][1]
            if point_data_names[i] == "EField_y":
               EField_y = data.variables["vals_nod_var%s"%(i+1)]
               EField_y.set_auto_mask(False)
               # This minus (-) sign to adapt the positive gradient calcluated by MOOSE as standard.
               # However, the electric field defintion is - grad (V).
               EField_y = -1*EField_y [:][1]
            if point_data_names[i] == "voltage":
               voltage = data.variables["vals_nod_var%s"%(i+1)]
               voltage.set_auto_mask(False)
               voltage = voltage [:][1]


        voltage  = voltage

        EField_x = EField_x
        EField_y = EField_y
        EField   = np.sqrt(EField_x**2 + EField_y**2)



        # GET THE NAMES OF THE ELEMENT VARIABLES
        variable_element_names = data.variables["name_elem_var"]
        variable_element_names.set_auto_mask(False)
        element_data_names = [b"".join(c).decode("UTF-8") for c in variable_element_names[:]]
        print(element_data_names)


        for i in np.arange(len(element_data_names)):
            if element_data_names[i] == "electric_permittivity":
               electric_permittivity_rock = data.variables["vals_elem_var%seb1"%(i+1)]
               # electric_permittivity_rock.set_auto_mask(False)

               electric_permittivity_rock = electric_permittivity_rock [:][1]
               electric_permittivity_pore = data.variables["vals_elem_var%seb2"%(i+1)]
               # electric_permittivity_pore.set_auto_mask(False)
               electric_permittivity_pore = electric_permittivity_pore [:][1]








        ax  = plt.subplot(gs[f,n])

        if fluid != "geometry":
            LE = 0
            HE = 2.5

            LevelsE = np.linspace(LE, HE, 200)
            labelsE = np.arange(LE,HE+0.5,0.5)
            locE = labelsE
            CS = plt.tricontourf(X,Y,EField, levels=LevelsE, cmap="jet")
            connect2 = data.variables['connect2']
            ExEy = np.array([EField_x[:], EField_y[:]]).T
            EFieldPore = []
            print(ExEy[connect2[:]-1])
            for ExEyPore in ExEy[connect2[:]-1]:
                    EFieldPoreNode1 = np.sqrt(ExEyPore[0][0]**2 + ExEyPore[0][1]**2)
                    EFieldPoreNode2 = np.sqrt(ExEyPore[1][0]**2 + ExEyPore[1][1]**2)
                    EFieldPoreNode3 = np.sqrt(ExEyPore[2][0]**2 + ExEyPore[2][1]**2)
                    print(EFieldPoreNode1,EFieldPoreNode2,EFieldPoreNode3)
                    MeanEFieldPoreNode = np.mean(np.array([EFieldPoreNode1,EFieldPoreNode2,EFieldPoreNode3]))
                    EFieldPore.append(MeanEFieldPoreNode)
            EFFieldPoreMean = np.mean(np.array(EFieldPore))
            ax.text(0.5, 0.7, "$\\overline{E_{EF,P}}=%3.1f$"%EFFieldPoreMean, ha="center", va="center", bbox=bbox, fontsize=fsIns)

        else:
            connect = data.variables['connect1']
            xy = np.array([X[:], Y[:]]).T
            patches = []
            for coords in xy[connect[:]-1]:
                quad = Polygon(coords, True)
                patches.append(quad)


            # colors = 100 * np.random.rand(len(patches))
            # p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.5)
            p = PatchCollection(patches, color="lightgrey")

            # p.set_array(np.array(colors))
            ax.add_collection(p)

            if n ==0:
                fsIns = fs-8
                ax.annotate("$\mathrm{Pore}$",
                xy=(0.5, 0.5), xycoords='data',
                xytext=(0.5, 0.3), textcoords='data',
                arrowprops=dict(arrowstyle="->",
                        connectionstyle="arc3, rad=0.3"), fontsize=fsIns
                )

                ax.annotate("$\mathrm{Rock}$", (0.4, 0.8), fontsize=fsIns)

                ax.annotate("", xy=(0, 0.2), xycoords='axes fraction',  xytext=(0.4, 0.2),  arrowprops=dict(arrowstyle='<->'))
                bbox=dict(fc="white", ec="none", alpha=0)
                ax.text(0.45, 0.2, "$x$", ha="center", va="center", bbox=bbox, fontsize=fsIns)
                ax.annotate("", xy=(0.2, 0), xycoords='axes fraction',  xytext=(0.2, 0.4),  arrowprops=dict(arrowstyle='<->'))
                bbox=dict(fc="white", ec="none", alpha=0)
                ax.text(0.2, 0.45, "$y$", ha="center", va="center", bbox=bbox, fontsize=fsIns)

            if n==1:
                ax.annotate("", xy=(0, 0.2), xycoords='axes fraction',  xytext=(1, 0.2),  arrowprops=dict(arrowstyle='<->'))
                bbox=dict(fc="white", ec="none", alpha=0)
                ax.text(0.5, 0.25, "$W_P=1$", ha="center", va="center", bbox=bbox, fontsize=fsIns)
                ax.annotate("", xy=(0.2, 0), xycoords='axes fraction',  xytext=(0.2, 1),  arrowprops=dict(arrowstyle='<->'))
                bbox=dict(fc="white", ec="none", alpha=0)
                ax.text(0.15, 0.5, "$H_P=1$", ha="center", va="center", bbox=bbox, fontsize=fsIns, rotation=90)

            if n==2:
                 ax.annotate("$V_P$=1",
                 xy=(0, 0.5), xycoords='data',
                 xytext=(0.1, 0.6), textcoords='data',
                 arrowprops=dict(arrowstyle="->",
                         connectionstyle="arc3, rad=0.3"), fontsize=fsIns
                 )

                 ax.annotate("$V_P$=0",
                 xy=(1, 0.5), xycoords='data',
                 xytext=(0.7, 0.6), textcoords='data',
                 arrowprops=dict(arrowstyle="->",
                         connectionstyle="arc3, rad=0.3"), fontsize=fsIns
                 )




        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.set_aspect('equal')

        if f == 0:
            if shape == "ellipse_x":
               shape = "ellipse_\parallel"
            if shape == "ellipse_y":
               shape = "ellipse_\perp"
            plt.title("$\\mathrm{%s}$"%shape.capitalize() , fontsize=fs)
            for axis in ['top','bottom']:
               ax.spines[axis].set_linewidth(3)
               ax.spines[axis].set_linestyle("--")
               ax.spines[axis].set_color("grey")
            for axis in ['left']:
               ax.spines[axis].set_linewidth(3)
               ax.spines[axis].set_color("black")
            for axis in ['right']:
               ax.spines[axis].set_linewidth(3)
               ax.spines[axis].set_color("black")

        if n == 0:
            ax.set_ylabel('$\\mathrm{%s}$'%fluid.capitalize(), fontsize=fs)


        ax.set_yticks([])
        ax.set_xticks([])



fig.subplots_adjust(bottom=0.05,left=0.05, right=0.9)

cbar_ax = fig.add_axes([0.92, 0.05, 0.02, 0.55])
cb =  fig.colorbar(CS, cax=cbar_ax)

cb.set_ticks(locE)
cb.set_ticklabels(labelsE)
cb.ax.tick_params(labelsize=fs)
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.usetex"] =True

plt.savefig(WD+'pore_impact_on_ppgd/figures/pore_efield_shape_fluid.png')
plt.savefig(WD+'pore_impact_on_ppgd/figures/pore_efield_shape_fluid.eps')

plt.show()
