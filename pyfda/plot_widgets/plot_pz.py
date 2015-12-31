# -*- coding: utf-8 -*-
"""
Widget for plotting poles and zeros

Author: Christian Muenker 2015
"""
from __future__ import print_function, division, unicode_literals, absolute_import

from PyQt4 import QtGui

import pyfda.filterbroker as fb
import pyfda.pyfda_rc as rc

from pyfda.pyfda_lib import zplane

from pyfda.plot_widgets.plot_utils import MplWidget#, MplCanvas

class PlotPZ(QtGui.QMainWindow):

    def __init__(self, parent = None): # default parent = None -> top Window
        super(PlotPZ, self).__init__(parent) # initialize QWidget base class
#        QtGui.QMainWindow.__init__(self) # alternative syntax

        self.layHChkBoxes = QtGui.QHBoxLayout()
        self.layHChkBoxes.addStretch(10)

        self.mplwidget = MplWidget()

        self.mplwidget.layVMainMpl.addLayout(self.layHChkBoxes)

        # make this the central widget, taking all available space:
        self.setCentralWidget(self.mplwidget)
        
        self.initAxes()

        self.draw() # calculate and draw poles and zeros

#        #=============================================
#        # Signals & Slots
#        #=============================================
#        self.btnWhatever.clicked.connect(self.draw)


    def initAxes(self):
        """Initialize and clear the axes
        """
#        self.ax = self.mplwidget.ax
        self.ax = self.mplwidget.fig.add_subplot(111)
        self.ax.clear()
        
#------------------------------------------------------------------------------
    def update_plot(self):
        """
        Draw the figure with new limits, scale etcs without recalculating H(f)
        -- not yet implemented, just use draw() for the moment
        """
        self.draw()

#------------------------------------------------------------------------------
    def draw(self):
        if self.mplwidget.mplToolbar.enable_update:
            self.draw_pz()
            
#------------------------------------------------------------------------------
    def draw_pz(self):
        """
        (re)draw P/Z plot
        """
        p_marker = rc.params['P_Marker']
        z_marker = rc.params['Z_Marker']
        
        zpk = fb.fil[0]['zpk']

        self.ax.clear()

        [z, p, k] = zplane(self.ax, zpk, verbose = False, 
            mps = p_marker[0], mpc = p_marker[1], mzs = z_marker[0], mzc = z_marker[1])

        self.ax.set_title(r'Pole / Zero Plot')
        self.ax.set_xlabel('Real axis')
        self.ax.set_ylabel('Imaginary axis')

        self.ax.axis([-1.1, 1.1, -1.1, 1.1])

        self.mplwidget.redraw()

#------------------------------------------------------------------------------

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    form = PlotPZ()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()
