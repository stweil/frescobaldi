# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008 - 2014 by Wilbert Berendsen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

"""
An Object Editor widget.
"""

from __future__ import unicode_literals

import sys

from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import app
import objecteditor


class Widget(QWidget):
    
# I think we will work with individual editor objects for different types of objects.
# Each one will be shown/hidden on demand, i.e. when an element is activated
# through the SVG view, the music view or the cursor in the source.
# Each editor object handles its own connections to signals.
# (PS: The object editor will also work with the source code directly,
# i.e. independently of graphical SVG editing.)

    def __init__(self, tool):
        super(Widget, self).__init__(tool)
        self.mainwindow = tool.mainwindow()
        
        import panelmanager
        self.svgview = panelmanager.manager(tool.mainwindow()).svgview.widget().view
        
        layout = QVBoxLayout(spacing=1)
        self.setLayout(layout)
        
        self.elemLabel = QLabel()
        
        self.XOffsetBox = QDoubleSpinBox()
        self.XOffsetBox.setRange(-99,99)
        self.XOffsetBox.setSingleStep(0.1)
        self.XOffsetLabel = l = QLabel()
        l.setBuddy(self.XOffsetBox)
 
        self.YOffsetBox = QDoubleSpinBox()
        self.YOffsetBox.setRange(-99,99)
        self.YOffsetBox.setSingleStep(0.1)
        self.YOffsetLabel = l = QLabel()
        l.setBuddy(self.YOffsetBox)
        
        layout.addWidget(self.elemLabel)
        layout.addWidget(self.XOffsetBox)
        layout.addWidget(self.XOffsetLabel)
        layout.addWidget(self.YOffsetBox)
        layout.addWidget(self.YOffsetLabel)
        
        layout.addStretch(1)

        app.translateUI(self)
        self.loadSettings()
        
        self.connectSlots()
    
    def connectSlots(self):
        # On creation we connect to all available signals
        self.connectToSvgView()
    
    def connectToSvgView(self):
        """Register with signals emitted by the
           SVG viewer for processing graphical editing.
        """
        self.svgview.objectStartDragging.connect(self.startDragging)
        self.svgview.objectDragging.connect(self.Dragging)
        self.svgview.objectDragged.connect(self.Dragged)
        self.svgview.selectedObject.connect(self.selected)
        self.svgview.selectedUrl.connect(self.url)
        
    def disconnectFromSvgView(self):
        """Do not process graphical edits when the
           Object Editor isn't visible."""
        self.svgview.objectStartDragging.disconnect()
        self.svgview.objectDragging.disconnect()
        self.svgview.objectDragged.disconnect()
        self.svgview.selectedObject.disconnect()
        self.svgview.selectedUrl.disconnect()
        
    def translateUI(self):
        self.XOffsetLabel.setText(_("X Offset"))
        self.XOffsetBox.setToolTip(_("Display the X Offset"))
        self.YOffsetLabel.setText(_("Y Offset"))
        self.YOffsetBox.setToolTip(_("Display the Y Offset"))

    def hideEvent(self, event):
        """Disconnect from all graphical editing signals
           when the panel isn't visible
        """
        self.disconnectFromSvgView()
        event.accept()
    
    def showEvent(self, event):
        """Connect to the graphical editing signals
           when the panel becomes visible
        """
        self.connectToSvgView()
        event.accept()
        
    def getCurrentLilyObject(self, cursor):
		""" Use cursor from textedit link to get type of object being edited."""
		import ly
		source = ly.document.Source(cursor)
		lilyReader = ly.music.read.Reader(source)
		tree = lilyReader.read()
		for t in tree:
			print(t)
		lilyObj = "still testing"
		self.elemLabel.setText(lilyObj)		
        
    def svg2lily(self, elem):
		""" Translate name of SVG element into name of 
		LilyPond object.
		"""
		svg2lilyDict = {"text": "TextScript"}
		return svg2lilyDict[elem]
    
    @QtCore.pyqtSlot(float, float)
    def setOffset(self, x, y):
        """Display the updated offset."""
        self.XOffsetBox.setValue(x)
        self.YOffsetBox.setValue(y)
    
    @QtCore.pyqtSlot(float, float)
    def startDragging(self, x, y):
        """Set the value of the offset externally."""
        # temporary debug output
        print "Start dragging with offset", x, y
        self.setOffset(x, y)
        
    @QtCore.pyqtSlot(float, float)
    def Dragging(self, x, y):
        """Set the value of the offset externally."""
        # temporary debug output
        # print "Dragging with offset", x, y
        self.setOffset(x, y)
        
    @QtCore.pyqtSlot(float, float)
    def Dragged(self, x, y):
        """Set the value of the offset externally."""
        # temporary debug output
        print "Dragged to", x, y
        self.setOffset(x, y)
        
    @QtCore.pyqtSlot(str)
    def selected(self, elem):
        """Set selected element."""
        # temporary debug output
        lilyObj = self.svg2lily(elem)
        #print(lilyObj)
        self.elemLabel.setText(lilyObj)
        
    @QtCore.pyqtSlot(str)
    def url(self, url):
        """Set selected element."""
        # temporary debug output
        print(url)
        self.getCurrentLilyObject(url)
        
    def loadSettings(self):
        """Called on construction. Load settings and set checkboxes state."""
        s = QSettings()
        s.beginGroup('object_editor')
        
    def saveSettings(self):
        """Called on close. Save settings and checkboxes state."""
        s = QSettings()
        s.beginGroup('object_editor')

