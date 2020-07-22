'''
Created on 22 lip 2020

@author: spasz
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class View(object):

    def __init__(self, t, y):
        ''' Make data preview with matplotlib'''
        # Save data
        self.t = list(t)
        self.y = list(y)

        # Plot Creation
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.25, bottom=0.25)
        self.line, = plt.plot(t, y)

        # Slider creation from 0 to 10% offset
        length = int(0.1*len(t))
        axcolor = 'lightgoldenrodyellow'
        axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
        self.offset = Slider(axfreq, 'Offset', 0, length, valinit=0, valstep=1)
        self.offset.on_changed(self.update)
        plt.show()

    def update(self, val):
        ''' Update offset slider '''
        offset = int(self.offset.val)
        data = self.y[offset:] + self.y[0:offset]
        self.line.set_ydata(data)
        self.fig.canvas.draw_idle()
