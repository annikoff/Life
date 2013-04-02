# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
import random
from numpy import *

class Field(QtGui.QLabel):
    cells = []
    step = 2
    cellsCount = 0
    buttonFlag = True

    def __init__(self, x, y):
        QtGui.QLabel.__init__(self)
        self.fieldSize = 60
        self.xSize = x
        self.ySize = y
        self.setGeometry(0,0,(self.xSize*10)+10,(self.ySize*10)+10)

    def paintEvent(self,event):
        painter = QtGui.QPainter(self)
        self.drawField(painter)
        

    def drawField(self,painter):
        painter.setPen('#FFFFFF')
        painter.setBrush(QtGui.QColor('#FFFFFF'))
        painter.drawRect(5,5,self.xSize*10,self.ySize*10)
        painter.setPen('#000000')
        painter.setBrush(QtGui.QColor(255,0,0))
        for i in range(1,(self.xSize*self.step)+2,self.step):
            painter.drawLine(5,5*i,(self.xSize*10)+5,5*i)
            painter.drawLine(5*i,5,5*i,(self.ySize*10)+5)
        painter.setPen('#000000')
        painter.setBrush(QtGui.QColor('#FF0000'))
        x = 0
        for cells in self.cells:            
            y = 0
            for cell in cells:
                if cell:
                    painter.drawRect((x*10)+5,(y*10)+5,10,10)
                y += 1
            x += 1
        painter.end()

    def mouseMoveEvent(self, event):    
        x,y = self.getMousePos(event.pos())
        x = ((x+5)/10)-1
        y = ((y+5)/10)-1
        if x >= 0 or x < self.xSize and y >= 0 or y < self.ySize:
            if self.buttonFlag:
                self.cells[x,y] = True
            else:
                self.cells[x,y] = False
        self.update()

    def mousePressEvent(self, event):    
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.buttonFlag = True
        else:
            self.buttonFlag = False
        x,y = self.getMousePos(event.pos())
        x = ((x+5)/10)-1
        y = ((y+5)/10)-1
        if x >= 0 or x < self.xSize and y >= 0 or y < self.ySize:
            if self.cells[x,y]:
                self.cells[x,y] = False
            else:
                self.cells[x,y] = True
        self.update()

    def getMousePos(self, position):
        return position.x(),position.y()