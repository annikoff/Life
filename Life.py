#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
import random
from numpy import *

import Resources

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.mdiArea = QtGui.QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QtCore.QSignalMapper(self)
        self.windowMapper.mapped.connect(self.setActiveSubWindow)

        self.playIcon = self.style().standardIcon(QtGui.QStyle.SP_MediaPlay)
        self.pauseIcon = self.style().standardIcon(QtGui.QStyle.SP_MediaPause)

        self.createActions()
        self.createMenus()
        self.createStatusBar()
        self.createToolBars()
        self.updateMenus()

        self.setWindowTitle("The Game of Life")
        self.setUnifiedTitleAndToolBarOnMac(True)

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.activeSubWindow():
            event.ignore()
        else:
            #self.writeSettings()
            event.accept()

    def new(self):
        activeSubWindow = self.createSubWindow()
        activeSubWindow.new()
        activeSubWindow.show()

    def open(self):
        fileName, filtr = QtGui.QFileDialog.getOpenFileName(self)
        if fileName:
            existing = self.findSubWindow(fileName)
            if existing:
                self.mdiArea.setActiveSubWindow(existing)
                return
            activeSubWindow = self.createSubWindow()
            if activeSubWindow.loadFile(fileName):
                self.statusBar().showMessage("Game loaded", 2000)
                activeSubWindow.show()
            else:
                activeSubWindow.close()

    def save(self):
        pass

    def saveAs(self):
        pass

    def play(self):
        activeSubWindow = self.activeSubWindow()
        if activeSubWindow:
            activeSubWindow.play()
        if activeSubWindow.isSimulate():
            self.playStopAct.setIcon(self.pauseIcon)
            self.playStopAct.setText('Sto&p')
        else:            
            self.playStopAct.setIcon(self.playIcon)
            self.playStopAct.setText('&Play')

    def reset(self):
        activeSubWindow = self.activeSubWindow()
        if activeSubWindow:
            if self.confirmMessage("Alert ", "Reset game?"):
                activeSubWindow.reset()
                self.playStopAct.setIcon(self.playIcon)

    def confirmMessage(self, title, message):    
        reply = QtGui.QMessageBox.question(self, title, message,
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            return True
        return False

    def setActiveSubWindow(self, activeSubWindow):
        if activeSubWindow:
            self.mdiArea.setActiveSubWindow(activeSubWindow)

    def createSubWindow(self):
        subWindow = SubWindow()
        self.mdiArea.addSubWindow(subWindow)
        subWindow.installEventFilter(self)
        return subWindow

    def eventFilter(self, subWindow, event):
        # if event.type() is QtCore.QEvent.Timer and subWindow is self.activeSubWindow():
        #     self.statusBar().showMessage("Generation number: "+str(subWindow.life.getGenNumber()))
        # else:
        #     self.statusBar().clear()
        return QtGui.QMainWindow.eventFilter(self, subWindow, event)

    def findSubWindow(self, fileName):
        canonicalFilePath = QtCore.QFileInfo(fileName).canonicalFilePath()

        for window in self.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None

    def activeSubWindow(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def createActions(self):
        self.newAct = QtGui.QAction(QtGui.QIcon(":/images/new.png"), "&New", 
                self, shortcut=QtGui.QKeySequence.New,
                statusTip="Create a new game", triggered=self.new)

        self.openAct = QtGui.QAction(QtGui.QIcon(":/images/open.png"), 
                "&Open...", self, shortcut=QtGui.QKeySequence.Open,
                statusTip="Open an saved game", triggered=self.open)

        self.saveAct = QtGui.QAction(QtGui.QIcon(":/images/save.png"), 
                "&Save", self, shortcut=QtGui.QKeySequence.Save,
                statusTip="Save the game to disk", triggered=self.save)

        self.saveAsAct= QtGui.QAction("Save &As...", self,
                shortcut=QtGui.QKeySequence.SaveAs,
                statusTip="Save the game under a new name",
                triggered=self.saveAs)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application",
                triggered=QtGui.qApp.closeAllWindows)

        self.playStopAct = QtGui.QAction(self.playIcon, "&Play", 
                self, shortcut="Space",
                statusTip="Play or stop the game", triggered=self.play)

        self.resetAct = QtGui.QAction(self.style().standardIcon(QtGui.QStyle.SP_DialogResetButton),"&Reset", 
                self, shortcut="Esc",
                statusTip="Reset the game", triggered=self.reset)


        self.closeAct = QtGui.QAction("Cl&ose", self, shortcut="Ctrl+F4",
                statusTip="Close the active window",
                triggered=self.mdiArea.closeActiveSubWindow)

        self.closeAllAct = QtGui.QAction("Close &All", self,
                statusTip="Close all the windows",
                triggered=self.mdiArea.closeAllSubWindows)

        self.tileAct = QtGui.QAction("&Tile", self,
                statusTip="Tile the windows",
                triggered=self.mdiArea.tileSubWindows)

        self.cascadeAct = QtGui.QAction("&Cascade", self,
                statusTip="Cascade the windows",
                triggered=self.mdiArea.cascadeSubWindows)

        self.nextAct = QtGui.QAction("Ne&xt", self,
                shortcut=QtGui.QKeySequence.NextChild,
                statusTip="Move the focus to the next window",
                triggered=self.mdiArea.activateNextSubWindow)

        self.previousAct = QtGui.QAction("Pre&vious", self,
                shortcut=QtGui.QKeySequence.PreviousChild,
                statusTip="Move the focus to the previous window",
                triggered=self.mdiArea.activatePreviousSubWindow)

        self.separatorAct = QtGui.QAction(self)
        self.separatorAct.setSeparator(True)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.fileMenu = self.menuBar().addMenu("&Game")
        self.fileMenu.addAction(self.playStopAct)
        self.fileMenu.addAction(self.resetAct)

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)
        self.resetAct.setEnabled(False)
        self.playStopAct.setEnabled(False)

    def updateMenus(self):
        activeSubWindow = self.activeSubWindow()
        hasSubWindow = (activeSubWindow is not None)
        self.saveAct.setEnabled(hasSubWindow)
        self.saveAsAct.setEnabled(hasSubWindow)
        self.closeAct.setEnabled(hasSubWindow)
        self.closeAllAct.setEnabled(hasSubWindow)
        self.tileAct.setEnabled(hasSubWindow)
        self.cascadeAct.setEnabled(hasSubWindow)
        self.nextAct.setEnabled(hasSubWindow)
        self.previousAct.setEnabled(hasSubWindow)
        self.separatorAct.setVisible(hasSubWindow)
        self.resetAct.setEnabled(hasSubWindow)
        self.playStopAct.setEnabled(hasSubWindow)
        self.speedSlider.setEnabled(hasSubWindow)
        if hasSubWindow:
            self.speedSlider.setValue(activeSubWindow.delay)
            if activeSubWindow.isSimulate():
                self.playStopAct.setIcon(self.pauseIcon)
                self.playStopAct.setText('Sto&p')
            else:
                self.playStopAct.setIcon(self.playIcon)
                self.playStopAct.setText('&Play')
        else:
            self.speedSlider.setValue(self.speedSlider.minimum())
            self.playStopAct.setIcon(self.playIcon)
            self.playStopAct.setText('&Play')

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            activeSubWindow = window.widget()

            text = "%d %s" % (i + 1, activeSubWindow.userFriendlyCurrentFile())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(activeSubWindow == self.activeSubWindow())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)

        self.gameToolBar = self.addToolBar("Game")
        self.gameToolBar.addAction(self.playStopAct)
        self.gameToolBar.addAction(self.resetAct)
        self.gameToolBar.addSeparator()

        self.speedLabel = QtGui.QLabel()
        self.speedLabel.setText("Speed: 50 ")
        self.gameToolBar.addWidget(self.speedLabel)

        self.speedSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.speedSlider.setRange(50, 2000)
        self.speedSlider.setSingleStep(1)
        self.gameToolBar.addWidget(self.speedSlider)
        self.mdiArea.connect(self.speedSlider, QtCore.SIGNAL("valueChanged(int)"), self.changeSpeed)
  
    def changeSpeed(self,speed):
        activeSubWindow = self.activeSubWindow()
        if activeSubWindow:
            activeSubWindow.changeSpeed(speed)
        self.speedLabel.setText("Speed: %d " % speed)

    def activeSubWindow(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

class SubWindow(QtGui.QScrollArea):
    sequenceNumber = 1
    x = 0
    y = 0
    timerId = 0
    step = 2
    delay = 50
    cellsCount = 0

    def __init__(self):
        super(SubWindow, self).__init__()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.isUntitled = True
        widget = QtGui.QScrollArea()
        self.qp = QtGui.QPainter()
        self.field = Field()
        self.setWidget(self.field)
        self.life = Life(30, 30, False)
        self.reset()
        self.field.cells = self.life.cells

    def isSimulate(self):
        if self.timerId:
            return True
        return False

    def reset(self):
        self.life.reset()
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
            QtGui.QMessageBox.warning(self, "MDI",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return False
        instr = QtCore.QTextStream(file)
        y=15
        start = False
        while not instr.atEnd():
            line = instr.readLine()
            if line[0] != '#':
                start = True
                x = 0
                for char in line:
                    if char == '*':
                        self.life.cells[x,y] = True
                    else:
                        self.life.cells[x,y] = False
                    x += 1
                y += 1
            if line[0] == '#' and start:
                break
        self.field.update()        
        self.setCurrentFile(fileName)
        return True

    def setCurrentFile(self, fileName):
        self.curFile = QtCore.QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.curFile)

    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()

class Field(QtGui.QLabel):
    cells = []
    step = 2
    cellsCount = 0
    buttonFlag = True

    def __init__(self):
        QtGui.QLabel.__init__(self)
        self.fieldSize = 60
        self.setGeometry(0,0,(self.fieldSize*10)+10,(self.fieldSize*10)+10)

    def paintEvent(self,event):
        painter = QtGui.QPainter(self)
        self.drawField(painter)
        

    def drawField(self,painter):
        painter.setPen('#FFFFFF')
        painter.setBrush(QtGui.QColor('#FFFFFF'))
        painter.drawRect(5,5,self.fieldSize*10,self.fieldSize*10)
        painter.setPen('#000000')
        painter.setBrush(QtGui.QColor(255,0,0))
        for i in range(1,(self.fieldSize*self.step)+2,self.step):
            painter.drawLine(5,5*i,(self.fieldSize*10)+5,5*i)
            painter.drawLine(5*i,5,5*i,(self.fieldSize*10)+5)
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
        if x >= 0 or x < self.fieldSize and y >= 0 or y < self.fieldSize:
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
        if x >= 0 or x < self.fieldSize and y >= 0 or y < self.fieldSize:
            if self.cells[x,y]:
                self.cells[x,y] = False
            else:
                self.cells[x,y] = True
        self.update()

    def getMousePos(self, position):
        return position.x(),position.y()

class Life:

    cells = []

    def __init__(self,width=30,height=30,infinityField = True):
        self.reset(width,height,infinityField)
        self.genNumber = 0;

    def getGenNumber(self):
        return self.genNumber

    def reset(self,width=30,height=30,infinityField = True):
        self.fieldSize = width+height
        self.infinityField = infinityField
        self.cellsCount = self.fieldSize*self.fieldSize
        self.cells = arange(self.cellsCount).reshape(self.fieldSize,self.fieldSize)
        self.cells.fill(False)
        return self.cells

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
                    neighbors += 1
                if prevCell:
                    neighbors += 1
                if topCell:
                    neighbors += 1
                if topprevCell:
                    neighbors += 1
                if topnextCell:
                    neighbors += 1
                if btmCell:
                    neighbors += 1
                if btmpnexCell:
                    neighbors += 1
                if btmprevCell:
                    neighbors += 1

                if neighbors == 3:
                    self.ncells[x,y] = True
                elif neighbors < 2 or neighbors >= 4:
                    self.ncells[x,y] = False
                y += 1
            x += 1
        self.cells = self.ncells
        self.genNumber += 1
        return self.cells

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())