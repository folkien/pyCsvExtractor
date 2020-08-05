'''
Created on 22 lip 2020

@author: spasz
'''
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class View(object):

    def __init__(self, t, y, xlabel='', ylabel='', label=''):
        ''' Make data preview with matplotlib'''
        # Save data
        self.t = list(t)
        self.y = list(y)

        # Select backend
        matplotlib.use('TkAgg')

        # Plot Creation
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.25, bottom=0.25)
        self.line, = plt.plot(t, y, label=label)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        self.ax.minorticks_on()
        self.ax.grid(b=True, which='major', axis='both', color='k')
        self.ax.grid(b=True, which='minor', axis='both')

        # Slider creation from 0 to 10% offset
        length = int(0.5*len(t))
        axcolor = 'lightgoldenrodyellow'
        axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
        self.offset = Slider(axfreq, 'Offset', 0, length, valinit=0, valstep=1)
        self.offset.on_changed(self.update)

    def Show(self):
        ''' Show whole plot'''
        self.ax.legend(loc='upper left')
        plt.show()

    def AddDataset(self, t, y, label=''):
        ''' Add additional plotted line'''
        self.ax.plot(t, y, label=label)

    def update(self, val):
        ''' Update offset slider '''
        offset = int(self.offset.val)
        data = self.y[offset:] + self.y[0:offset]
        self.line.set_ydata(data)
        self.fig.canvas.draw_idle()
