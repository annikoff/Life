#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
import random
from numpy import *

import Resources
from Life import Life
from Field import Field
from SubWindow import SubWindow

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

        self.playIcon = QtGui.QIcon.fromTheme("media-playback-start")
        self.pauseIcon =  QtGui.QIcon.fromTheme("media-playback-pause")
        self.nextStepIcon = QtGui.QIcon.fromTheme("media-seek-forward")

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
        x, xok = QtGui.QInputDialog.getInteger(self,
                "Enter field width", "X:", 40, 2, 100, 1)
        y, yok = QtGui.QInputDialog.getInteger(self,
                "Enter field height", "Y:", 20, 2, 100, 1)
        if xok and yok:
            activeSubWindow = self.createSubWindow(x, y)
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
                self.statusMessage.setText("Game loaded")
                activeSubWindow.show()
            else:
                activeSubWindow.close()

    def save(self):
        if self.activeSubWindow() and self.activeSubWindow().save():
            self.statusMessage.setText("File saved")

    def saveAs(self):
        if self.activeSubWindow() and self.activeSubWindow().saveAs():
            self.statusMessage.setText("File saved")

    def play(self):
        activeSubWindow = self.activeSubWindow()
        if activeSubWindow:
            activeSubWindow.play()
        else:
            return False;
        if activeSubWindow.isSimulate():
            self.playStopAct.setIcon(self.pauseIcon)
            self.playStopAct.setText('Sto&p')
        else:            
            self.playStopAct.setIcon(self.playIcon)
            self.playStopAct.setText('&Play')
        self.saveAct.setEnabled(not activeSubWindow.isSimulate())
        self.saveAsAct.setEnabled(not activeSubWindow.isSimulate())
        self.nextStepAct.setEnabled(not activeSubWindow.isSimulate())

    def reset(self):
        activeSubWindow = self.activeSubWindow()
        if activeSubWindow:
            if self.confirmMessage("Alert ", "Reset game?"):
                activeSubWindow.reset()
                self.playStopAct.setIcon(self.playIcon)

    def nextStep(self):
        activeSubWindow = self.activeSubWindow()
        if activeSubWindow:
            if not activeSubWindow.isSimulate():
                activeSubWindow.nextStep()

    def confirmMessage(self, title, message):    
        reply = QtGui.QMessageBox.question(self, title, message,
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            return True
        return False

    def setActiveSubWindow(self, activeSubWindow):
        if activeSubWindow:
            self.mdiArea.setActiveSubWindow(activeSubWindow)

    def createSubWindow(self, x, y):
        subWindow = SubWindow(x, y)
        self.mdiArea.addSubWindow(subWindow)
        subWindow.installEventFilter(self)
        return subWindow

    def eventFilter(self, subWindow, event):
        if subWindow is self.activeSubWindow():
            self.statusMessage.setText("%d" % subWindow.life.getGenNumber())
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
        self.newAct = QtGui.QAction(QtGui.QIcon.fromTheme("document-new", QtGui.QIcon(":/images/new.png")), "&New", 
                self, shortcut=QtGui.QKeySequence.New,
                statusTip="Create a new game", triggered=self.new)

        self.openAct = QtGui.QAction(QtGui.QIcon.fromTheme("document-open", QtGui.QIcon(":/images/open.png")), 
                "&Open...", self, shortcut=QtGui.QKeySequence.Open,
                statusTip="Open an saved game", triggered=self.open)

        self.saveAct = QtGui.QAction(QtGui.QIcon.fromTheme("document-save", QtGui.QIcon(":/images/save.png")), 
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

        self.nextStepAct = QtGui.QAction(self.nextStepIcon, "Nex&t", 
                self, shortcut="Right",
                statusTip="Next step", triggered=self.nextStep)

        self.resetAct = QtGui.QAction(QtGui.QIcon.fromTheme("edit-clear"),"&Reset", 
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
        self.fileMenu.addAction(self.nextStepAct)
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
        self.nextStepAct.setEnabled(hasSubWindow)
        if hasSubWindow:
            self.speedSlider.setValue(activeSubWindow.delay)
            if activeSubWindow.isSimulate():
                self.playStopAct.setIcon(self.pauseIcon)
                self.playStopAct.setText('Sto&p')
            else:
                self.playStopAct.setIcon(self.playIcon)
                self.playStopAct.setText('&Play')
            self.setWindowTitle(activeSubWindow.windowTitle()+" - The Game of Life")
        else:
            self.setWindowTitle("The Game of Life")
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
        self.speedLabel = QtGui.QLabel()
        self.speedLabel.setText("Speed: 50 ")
        self.statusBar().addWidget(self.speedLabel,5)

        self.speedSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.speedSlider.setRange(50, 2000)
        self.speedSlider.setSingleStep(1)
        self.statusBar().addWidget(self.speedSlider,15)
        self.mdiArea.connect(self.speedSlider, QtCore.SIGNAL("valueChanged(int)"), self.changeSpeed)

        self.statusMessage = QtGui.QLabel()
        self.statusMessage.setText("Ready")
        self.statusBar().addWidget(self.statusMessage,40)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)

        self.gameToolBar = self.addToolBar("Game")
        self.gameToolBar.addAction(self.playStopAct)
        self.gameToolBar.addAction(self.nextStepAct)
        self.gameToolBar.addAction(self.resetAct)
        self.gameToolBar.addSeparator()
 
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

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())