
# Numerical calculations
import numpy as np
# Matplotlib as plot library
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# import niceplotlib and initialize
import niceplotlib as nipl
nipl.init()

# previous plot script
a = [0,1];
b = [2, 1];

fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(a,b)

# Stylize your plot
fig = nipl.stylizePlot(fig)

fig.savefig('testSplit.pdf')