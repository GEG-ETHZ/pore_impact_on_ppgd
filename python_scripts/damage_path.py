import numpy as np
import matplotlib.pyplot as plt

import matplotlib.gridspec as gridspec



hr = 0.25    # the relative penetration depth for 50 mm electrode gap distance from Vazhov et al. 2010
dE = 5       # [cm] the electrode gap distance
h  = dE * hr # [cm]the penetration depth

R  = (h/2.0) + (dE**2/(8.0*h))

XX  =  np.linspace(4, dE+5, 1000)
YY  =  np.sqrt(R**2 - (XX-dE/2-4)**2) - (R-h)

D_depth   = YY




gs = gridspec.GridSpec(2,5)
gs.update(hspace=0.15, wspace=0.1)
fig= plt.figure(figsize=(16,7.5))
s  = 18
lws = 2
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["text.usetex"] =True
plt.rcParams["axes.facecolor"] = 'white'



ax = plt.subplot(gs[0, 0:4])

plt.plot([0,20],[0,0],  lw=lws, color="black", label="Rock surface")
plt.plot(XX, YY, '--', lw=lws, color="black", label="Damage path")

plt.ylim(0,3)
plt.xlim(0,13)
plt.gca().invert_yaxis()

# ax = plt.subplot(gs[0, 4])
#
# XX1  =  np.linspace(-R, R, 100)
# YY1  =  np.sqrt(R**2 - (XX1)**2)
# plt.plot(XX1,YY1, color="black")
# plt.plot(XX1,-YY1, color="black")
# ax.set_xticklabels([])
# ax.set_yticklabels([])
# plt.annotate(text='', xy=(-R,0), xytext=(R,0), arrowprops=dict(arrowstyle='<->'))
# ax.text(0, 3, '$R$', fontsize=fs)
# plt.annotate(text='', xy=(-10,-R+2), xytext=(10,-R+2), arrowprops=dict(arrowstyle='<->'))
# ax.text(0,-R+5, '$c$', fontsize=fs)




plt.show()
