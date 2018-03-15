"""
Overlapping densities ('joy plot')
==================================


"""
from IPython import embed
import time
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

wait_time = sys.argv[1] if len(sys.argv) > 1 else 0
KDE = True if len(sys.argv) > 2 else False

sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

# Read the data
df = pd.read_csv('peroxisome_stats_zoom_raw.csv')
df['g'] = df.ImageNum
df['x'] = df.Distances

# Initialize the FacetGrid object
pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
if KDE:
  g = sns.FacetGrid(df, row="g", hue="g", aspect=15, size=.5, palette=pal, xlim=(-1.1, 30))
else:
  g = sns.FacetGrid(df, row="g", hue="g", aspect=15, size=.5, palette=pal, xlim=(-1.1, 15), ylim=(0, 75))

# Draw the densities in a few steps
if KDE:
  g.map(sns.kdeplot, "x", clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2,cut=0)
  g.map(sns.kdeplot, "x", clip_on=False, color="w", lw=2, bw=.2)
else:
  bins = np.arange(0, 15, 1)
  g.map(plt.hist, "x", bins=bins,edgecolor='white', linewidth=2)
g.map(plt.axhline, y=0, lw=2, clip_on=False)

# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color, 
            ha="left", va="center", transform=ax.transAxes)

g.map(label, "x")

# Set the subplots to overlap
g.fig.subplots_adjust(hspace=-.25)

# Remove axes details that don't play will with overlap
g.set_titles("")
g.set(yticks=[])
g.despine(bottom=True, left=True)

# plt.waitforbuttonpress()
plt.show(block=False)
time.sleep(int(wait_time))
# embed()
