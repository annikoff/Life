#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
from Life import Life
from Field import Field
from numpy import *

class SubWindow(QtGui.QScrollArea):
    sequenceNumber = 1
    x = 0
    y = 0
    timerId = 0
    step = 2
    delay = 50
    cellsCount = 0

    def __init__(self, width, height):
        super(SubWindow, self).__init__()
        self.width = width
        self.height = height
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.isUntitled = True
        widget = QtGui.QScrollArea()
        self.qp = QtGui.QPainter()
        if width and height:
            self.field = Field(width, height)
            self.setWidget(self.field)
            self.life = Life(width, height, False)
            self.reset()
            self.field.cells = self.life.cells

    def isSimulate(self):
        if self.timerId:
            return True
        return False

    def reset(self):
        self.life.reset(self.width, self.height)
        self.field.cells = self.life.cells
        self.field.update()
        if self.timerId:
            self.killTimer(self.timerId)
            self.timerId = 0

    def changeSpeed(self, speed):
        self.delay = speed
        if self.timerId:
            self.killTimer(self.timerId)
            self.timerId = self.startTimer(speed)

    def play(self):
        if not self.timerId:
            self.timerId = self.startTimer(self.delay)
        else:
            self.killTimer(self.timerId)
            self.timerId = 0

    def nextStep(self):
        self.field.cells = self.life.simulate()
        self.field.update()

    def timerEvent(self, event):
        self.field.cells = self.life.simulate()
        self.field.update()

    def currentFile(self):
        return self.curFile

    def new(self):
        self.isUntitled = True
        self.curFile = "Game %d" % SubWindow.sequenceNumber
        SubWindow.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')

    def loadFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open( QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Reading error",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return False
        instr = QtCore.QTextStream(file)
        start = False
        width = 0
        lines = []

        while not instr.atEnd():
            line = instr.readLine()
            if width < len(line):
                width = len(line)
            if line[0] != '#':
                start = True
                lines.append(line)
            if line[0] == '#' and start:
                break

        height = len(lines)   
        if not width or not height:
            return False 
        self.width = width
        self.height = height
        self.field = Field(width, height)
        self.setWidget(self.field)
        self.life = Life(width, height, False)
        self.field.cells = self.life.cells
        y=0
        for line in lines:
            x = 0
            for char in line:
                if char == '*':
                    self.life.cells[x,y] = True
                x += 1
            y += 1

        self.field.update()        
        self.setCurrentFile(fileName)
        return True

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName, filtr = QtGui.QFileDialog.getSaveFileName(self, "Save As",
                self.curFile+'.lif')
        if not fileName:
            return False

        return self.saveFile(fileName)

    def saveFile(self, fileName):
        file = QtCore.QFile(fileName)

        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Writing error",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False
        outstr = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        for cells in array(self.life.cells).T:
            for cell in cells:
                if cell:
                    outstr << '*'
                else:
                    outstr << '.'
            outstr << "\n"
        QtGui.QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        return True

    def setCurrentFile(self, fileName):
        self.curFile = QtCore.QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.curFile)

    def currentFile(self):
        return self.curFile

    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()