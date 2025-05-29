# bdf file class
from biosemipy import bdf
from biosemipy import dataviewer

file = "1.Dados_Anteriores\Raw Empirical EEG Data\EEG_Cat_Study4_Resting_S1.bdf"
dat1 = bdf.BDF(file)


dataviewer.run(file)

#from biosemipy.topo import Topo

#topo_plt = Topo()
#topo_plt.plot()
#topo_plt.show()