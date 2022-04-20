# -*- coding: utf-8 -*-
"""
Displays a heatmap
"""
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import io, os, struct, sys
from PIL import Image
from PIL.ImageQt import ImageQt

from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set_theme()
from matplotlib.colors import LinearSegmentedColormap 
from matplotlib.colors import Colormap

MSECINSEC=1e3

class HeatMapSNS(object):
    my_dpi=300

    @staticmethod
    def getPixmap(points, w, h, radius, nSubjects=1, colorScale=None):
        # print(points)
        data = np.zeros((h, w))
        for p in points:
            data[p[1]][p[0]] += p[2] # add the time in seconds
        # Standardize data
        # data = (data- data.min())/(data.max()- data.min())        
        data_smooth = gaussian_filter(data, sigma=radius)
        # data_smooth = data
        fig = plt.figure(frameon=False, figsize=(1.0*(w+1)/HeatMapSNS.my_dpi, 1.0*(h+1)/HeatMapSNS.my_dpi), dpi=HeatMapSNS.my_dpi)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # modified colormap with changing alpha
        # color dict
        cdict = {'red':   [(0.0,  0.0, 0.0),
                           (0.5,  0.0, 0.0),
                           (1.0,  1.0, 1.0)],

                 'green': [(0.0,  0.0, 0.0),
                           (0.25, 0.0, 0.0),
                           (0.75, 1.0, 1.0),
                           (1.0,  0.0, 0.0)],
        
                 'blue':  [(0.0,  1.0, 1.0),
                           (0.5,  0.0, 0.0),
                           (1.0,  0.0, 0.0)],
                 'alpha': ((0., 0., 0.),
                           (1.0  , 1.0, 1.0))}        
        myColorMap= LinearSegmentedColormap('mycolormap', cdict)
        # myColorMap = Colormap('coolwarm') 
        
        vmin = data_smooth.min()
        if not colorScale or colorScale == 1.0:
            data_smooth = (data_smooth- data_smooth.min())/(data_smooth.max()- data_smooth.min())
            vmax = 1.0            
        else:
            data_smooth /= nSubjects
            vmax = colorScale*MSECINSEC
        
        # print(f'min={vmin/MSECINSEC} sec, max={vmax/MSECINSEC} sec')
        # fig.text(0.1,0.95,f'min={vmin/MSECINSEC:.2f} sec, max={vmax/MSECINSEC:.2f} sec', fontsize=2) 
        fig.text(0.01,0.95,f'N={nSubjects}', fontsize=3)
        
        sns.heatmap(data_smooth, square=True, cbar=False, vmin=vmin, vmax=vmax, cmap = myColorMap, ax=ax)
        # sns.heatmap(data_smooth, alpha = 0.5, square=True, cbar=False, vmin=data_smooth.min(), vmax=data_smooth.max(), cmap ="coolwarm", ax=ax)
        img_buf = io.BytesIO()
        plt.ioff()
        plt.savefig(img_buf, format='png', dpi=HeatMapSNS.my_dpi)
        im = Image.open(img_buf)
        return QPixmap.fromImage(ImageQt(im))
        
