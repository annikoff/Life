#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *
import random
from numpy import *

class MainWindow(QWidget):

    x = 0
    y = 0
    timerId= 0
    step = 2
    delay = 50
    cellsCount = 0

    def __init__(self):
        QWidget.__init__(self)
        self.life = Life(30,30,False)
        self.setGeometry(300,300,750,610)
        self.setWindowTitle('Main window')
        self.edit = QLineEdit("50")
        self.playButton = QPushButton("Play")
        self.resetButton = QPushButton("Reset")
        self.clearButton = QPushButton("Clear") 
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.edit, 5, 3)
        mainLayout.addWidget(self.playButton, 5, 3)
        mainLayout.addWidget(self.resetButton, 5, 3)
        mainLayout.addWidget(self.clearButton, 6, 3)
        self.setLayout(mainLayout)
        self.playButton.clicked.connect(self.play)
        self.resetButton.clicked.connect(self.resetGame)
        self.clearButton.clicked.connect(self.clearField)
        self.resetGame()

    def clearField(self):
        self.update()

    def resetGame(self):
        self.life.reset()
        self.update()

    def paintEvent(self,event):
        qp = QPainter()
        qp.begin(self)
        self.drawField(qp)
        qp.end()

    def play(self):
        if self.edit.text() > 0:
            self.delay = int(self.edit.text())
        else:
            self.delay = 50
        if not self.timerId:
            self.timerId = self.startTimer(self.delay)
            self.playButton.setText('Stop')
        else:
            self.killTimer(self.timerId)
            self.timerId = 0
            self.playButton.setText('Play')
            return 

    def drawField(self,qp):
        qp.setPen('#FFFFFF')
        qp.setBrush(QColor('#FFFFFF'))
        qp.drawRect(5,5,self.life.fieldSize*10,self.life.fieldSize*10)
        qp.setPen('#000000')
        qp.setBrush(QColor(255,0,0))
        for i in range(1,(self.life.fieldSize*self.step)+2,self.step):
            qp.drawLine(5,5*i,(self.life.fieldSize*10)+5,5*i)
            qp.drawLine(5*i,5,5*i,(self.life.fieldSize*10)+5)
        qp.setPen('#000000')
        qp.setBrush(QColor('#FF0000'))
        x = 0
        for cells in self.life.cells:            
            y = 0
            for cell in cells:
                if cell:
                    qp.drawRect((x*10)+5,(y*10)+5,10,10)
                y+=1
            x+=1

    def mousePressEvent(self, event):    
        x,y = self.getMousePos(event.pos())
        x = ((x+5)/10)-1
        y = ((y+5)/10)-1
        if x >= 0 or x < self.life.fieldSize and y >= 0 or y < self.life.fieldSize:
            if self.life.cells[x,y]:
                self.life.cells[x,y] = False
            else:
                self.life.cells[x,y] = True
        self.update()

    def getMousePos(self, position):
        return position.x(),position.y()

    def timerEvent(self, event):
        self.life.simulate()
        self.update()

class Life:

    cells = []

    def __init__(self,width=30,height=30,infinityField = True):
        self.reset(width,height,infinityField)

    def reset(self,width=30,height=30,infinityField = True):
        self.fieldSize = width*height
        self.infinityField = infinityField
        self.cellsCount = self.fieldSize*self.fieldSize
        self.cells = arange(self.cellsCount).reshape(self.fieldSize,self.fieldSize)
        self.cells.fill(False)
        print self.fieldSize

    def simulate(self):
        self.ncells = []
        self.ncells = arange(self.cellsCount).reshape(self.fieldSize,self.fieldSize)
        self.ncells.fill(False)
        x = 0
        for cells in self.cells:            
            y = 0
            for cell in cells:
                self.ncells[x,y] = cell

                tx = x+1
                if tx < self.fieldSize:
                    nextCell = self.cells[tx,y]
                else:
                    if self.infinityField:
                        nextCell = self.cells[0,y]
                    else:
                        nextCell = False

                tx = x-1
                if tx >= 0:
                    prevCell = self.cells[tx,y]
                else:
                    if self.infinityField:
                        prevCell = self.cells[-1,y]
                    else:
                        prevCell = False

                ty = y-1
                if ty >= 0:
                    topCell = self.cells[x,ty]
                else:
                    if self.infinityField:
                        topCell = self.cells[x,-1]
                    else:
                        topCell = False

                ty = y-1
                if ty >= 0:
                    tx = x-1
                    if tx >=0:
                        topprevCell = self.cells[tx,ty]
                    else:
                        if self.infinityField:
                            topprevCell = self.cells[-1,ty]
                        else:
                            topprevCell = False
                else:
                    tx = x-1
                    if tx >=0:
                        topprevCell = self.cells[tx,-1]
                    else:
                        if self.infinityField:
                            topprevCell = self.cells[-1,-1]
                        else:
                            topprevCell = False

                ty = y-1
                if ty >= 0:
                    tx = x+1
                    if tx < self.fieldSize:
                        topnextCell = self.cells[tx,ty]
                    else:
                        if self.infinityField:
                            topnextCell = self.cells[0,ty]
                        else:
                            topnextCell = False
                else:
                    tx = x+1
                    if tx < self.fieldSize:
                        topnextCell = self.cells[tx,-1]
                    else:
                        if self.infinityField:
                            topnextCell = self.cells[0,-1]
                        else:
                            topnextCell = False


                ty = y+1
                if ty < self.fieldSize:
                    btmCell = self.cells[x,ty]
                else:
                    if self.infinityField:
                        btmCell = self.cells[x,0]
                    else:
                        btmCell = False

                ty = y+1
                if ty < self.fieldSize:
                    tx = x+1
                    if tx < self.fieldSize:
                        btmpnexCell = self.cells[tx,ty]
                    else:
                        if self.infinityField:
                            btmpnexCell = self.cells[0,ty]
                        else:
                            btmpnexCell = False
                else:
                    tx = x+1
                    if tx < self.fieldSize:
                        btmpnexCell = self.cells[tx,0]
                    else:
                        if self.infinityField:
                            btmpnexCell = self.cells[0,0]
                        else:
                            btmpnexCell = False

                ty = y+1
                if ty < self.fieldSize:
                    tx = x-1
                    if tx >=0:
                        btmprevCell = self.cells[tx,ty]
                    else:
                        if self.infinityField:
                            btmprevCell = self.cells[-1,ty]
                        else:
                            btmprevCell = False
                else:
                    tx = x-1
                    if tx >=0:
                        btmprevCell = self.cells[tx,0]
                    else:
                        if self.infinityField:
                            btmprevCell = self.cells[-1,0]
                        else:
                            btmprevCell = False

                neighbors = 0
                if nextCell:
                    neighbors+=1
                if prevCell:
                    neighbors+=1
                if topCell:
                    neighbors+=1
                if topprevCell:
                    neighbors+=1
                if topnextCell:
                    neighbors+=1
                if btmCell:
                    neighbors+=1
                if btmpnexCell:
                    neighbors+=1
                if btmprevCell:
                    neighbors+=1

                if neighbors == 3:
                    self.ncells[x,y] = True
                elif neighbors < 2 or neighbors >= 4:
                    self.ncells[x,y] = False
                y+=1
            x+=1
        self.cells = self.ncells
        return self.cells

app = QApplication([])
win = MainWindow()
win.show()
app.exec_()
