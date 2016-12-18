#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
from PySide import QtCore, QtGui, QtOpenGL
from numpy import *

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
                            "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.glWidget = GLWidget()
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.glWidget)
        self.setLayout(mainLayout)
        self.setWindowTitle(self.tr('Life 3D'))




class GLWidget(QtOpenGL.QGLWidget,QtGui.QWidget):
    cells = []
    timerId= 0
    fieldSize = 20
    step = 2
    delay = 500
    cellsCount = 0

    def __init__(self,parent=None):
        QtOpenGL.QGLWidget.__init__(self,parent)
        self.object = 0
        self.xRot = 2440
        self.yRot = 2160
        self.zRot = 0
        self.lastPos = QtCore.QPoint()
        self.trolltechGreen = QtGui.QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QtGui.QColor.fromCmykF(0.0, 0.0, 0.0, 0.0)

    def resetGame(self):
        self.cellsCount = self.fieldSize*self.fieldSize*self.fieldSize
        self.cells = arange(self.cellsCount).reshape(self.fieldSize,self.fieldSize,self.fieldSize)
        self.cells.fill(False)
        for i in range(150):
            x = random.randint(0, self.fieldSize-1)
            y = random.randint(0, self.fieldSize-1)
            z = random.randint(0, self.fieldSize-1)
            if self.cells[x,y,z]:
                i-=1
            else:
                self.cells[x,y,z] = True

        self.cells[10,11,10] = True
        self.cells[10,12,10] = True
        self.cells[10,13,10] = True
        self.cells[10,14,10] = True

        self.cells[11,11,10] = True
        self.cells[11,12,10] = True
        self.cells[11,13,10] = True
        self.cells[11,14,10] = True

        self.cells[12,11,10] = True
        self.cells[12,12,10] = True
        self.cells[12,13,10] = True
        self.cells[12,14,10] = True

        self.cells[13,11,10] = True
        self.cells[13,12,10] = True
        self.cells[13,13,10] = True
        self.cells[13,14,10] = True

        self.cells[10,11,11] = True
        self.cells[10,12,11] = True
        self.cells[10,13,11] = True
        self.cells[10,14,11] = True

        self.cells[11,11,11] = True
        self.cells[11,12,11] = True
        self.cells[11,13,11] = True
        self.cells[11,14,11] = True

        self.cells[12,11,11] = True
        self.cells[12,12,11] = True
        self.cells[12,13,11] = True
        self.cells[12,14,11] = True

        self.cells[13,11,11] = True
        self.cells[13,12,11] = True
        self.cells[13,13,11] = True
        self.cells[13,14,11] = True


        self.cells[10,11,12] = True
        self.cells[10,12,12] = True
        self.cells[10,13,12] = True
        self.cells[10,14,12] = True

        self.cells[11,11,12] = True
        self.cells[11,12,12] = True
        self.cells[11,13,12] = True
        self.cells[11,14,12] = True

        self.cells[12,11,12] = True
        self.cells[12,12,12] = True
        self.cells[12,13,12] = True
        self.cells[12,14,12] = True

        self.cells[13,11,12] = True
        self.cells[13,12,12] = True
        self.cells[13,13,12] = True
        self.cells[13,14,12] = True

        self.cells[10,11,13] = True
        self.cells[10,12,13] = True
        self.cells[10,13,13] = True
        self.cells[10,14,13] = True

        self.cells[11,11,13] = True
        self.cells[11,12,13] = True
        self.cells[11,13,13] = True
        self.cells[11,14,13] = True

        self.cells[12,11,13] = True
        self.cells[12,12,13] = True
        self.cells[12,13,13] = True
        self.cells[12,14,13] = True

        self.cells[13,11,13] = True
        self.cells[13,12,13] = True
        self.cells[13,13,13] = True
        self.cells[13,14,13] = True

    def sizeRotation(self):
        return self.xRot

    def sizeRotation(self):
        return self.yRot

    def sizeRotation(self):
        return self.zRot

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.updateGL()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.updateGL()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.updateGL()

    def initializeGL(self):
        self.resetGame()
        self.qglClearColor(self.trolltechPurple)
        #self.object = self.makeObject()
        GL.glShadeModel(GL.GL_FLAT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_ALPHA_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA,GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glEnable(GL.GL_LIGHT0)
        lightPosition = ( 2.0, 3.0, 3.0, 1.0 )
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, lightPosition)
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, (1.0,1.0,1.0,1.0));
        GL.glMaterialf(GL.GL_FRONT, GL.GL_SHININESS, 128.0);


    def paintGL(self):
        self.object = self.makeObject()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()
        GL.glTranslated(0.0, 0.0, -10.0)
        GL.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        GL.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        GL.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        GL.glCallList(self.object)

    def resizeGL(self, width, height):
        side = min(width, height)
        GL.glViewport((width - side) / 2, (height - side) / 2, side, side)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(-2, 2, 2, -2, 4.0, 25.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)


    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())
        if event.buttons() & QtCore.Qt.RightButton:
            self.play()

    def mouseMoveEvent(self,event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & QtCore.Qt.MiddleButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)
        self.lastPos = QtCore.QPoint(event.pos())

    def play(self):
        if not self.timerId:
            self.timerId = self.startTimer(self.delay)
        else:
            self.killTimer(self.timerId)
            self.timerId = 0
            return

    def makeObject(self):
        genList = GL.glGenLists(1)
        GL.glNewList(genList, GL.GL_COMPILE)
        self.axis()
        x = 0
        for c1 in self.cells:
            y = 0
            for c2 in c1:
                z = 0
                for c3 in c2:
                    if c3:
                        self.cube(0.1,float(x)/10,float(y)/10,float(z)/10)
                    z+=1

                y+=1
            x+=1
        GL.glEndList()
        return genList

    def timerEvent(self, event):
        self.ncells = arange(self.cellsCount).reshape(self.fieldSize,self.fieldSize,self.fieldSize,)
        self.ncells.fill(False)
        x = 0
        for c1 in self.cells:
            y = 0
            for c2 in c1:
                z = 0
                for c3 in c2:
                    self.ncells[x,y,z] = c3
                    neighbors = self.checkCells(x,y,z)
                    if neighbors == 6:
                        self.ncells[x,y,z] = True
                    elif neighbors < 4 or neighbors >= 8:
                        self.ncells[x,y,z] = False
                    z+=1
                y+=1
            x+=1
        self.cells = self.ncells
        self.updateGL()

    def checkCells(self,x,y,z):
        z-=1
        if z<0:
            z=-1
        neighbors = 0
        for i in range(3):
            if z>=self.fieldSize:
                z=0

            if i == 0:
                if x >= 0:
                    nCell = self.cells[x,y,z]
                else:
                    nCell = self.cells[x,y,-1]
            elif i == 2:
                if x < self.fieldSize:
                    nCell = self.cells[x,y,z]
                else:
                    nCell = self.cells[x,y,0]
            else:
                nCell = False

            tx = x+1
            if tx < self.fieldSize:
                nextCell = self.cells[tx,y,z]
            else:
                nextCell = self.cells[0,y,z]

            tx = x-1
            if tx >= 0:
                prevCell = self.cells[tx,y,z]
            else:
                prevCell = self.cells[-1,y,z]

            ty = y-1
            if ty >= 0:
                topCell = self.cells[x,ty,z]
            else:
                topCell = self.cells[x,-1,z]

            ty = y-1
            if ty >= 0:
                tx = x-1
                if tx >=0:
                    topprevCell = self.cells[tx,ty,z]
                else:
                    topprevCell = self.cells[-1,ty,z]
            else:
                tx = x-1
                if tx >=0:
                    topprevCell = self.cells[tx,-1,z]
                else:
                    topprevCell = self.cells[-1,-1,z]

            ty = y-1
            if ty >= 0:
                tx = x+1
                if tx < self.fieldSize:
                    topnextCell = self.cells[tx,ty,z]
                else:
                    topnextCell = self.cells[0,ty,z]
            else:
                tx = x+1
                if tx < self.fieldSize:
                    topnextCell = self.cells[tx,-1,z]
                else:
                    topnextCell = self.cells[0,-1,z]

            ty = y+1
            if ty < self.fieldSize:
                btmCell = self.cells[x,ty,z]
            else:
                btmCell = self.cells[x,0,z]

            ty = y+1
            if ty < self.fieldSize:
                tx = x+1
                if tx < self.fieldSize:
                    btmpnexCell = self.cells[tx,ty,z]
                else:
                    btmpnexCell = self.cells[0,ty,z]
            else:
                tx = x+1
                if tx < self.fieldSize:
                    btmpnexCell = self.cells[tx,0,z]
                else:
                    btmpnexCell = self.cells[0,0,z]

            ty = y+1
            if ty < self.fieldSize:
                tx = x-1
                if tx >=0:
                    btmprevCell = self.cells[tx,ty,z]
                else:
                    btmprevCell = self.cells[-1,ty,z]
            else:
                tx = x-1
                if tx >=0:
                    btmprevCell = self.cells[tx,0,z]
                else:
                    btmprevCell = self.cells[-1,0,z]

            if nCell:
                neighbors+=1
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
            z+=1
        return neighbors

    def axis(self):
        self.qglColor(self.trolltechGreen)
        GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_NICEST)
        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glEnable(GL.GL_BLEND)
        GL.glLineWidth(1)
        GL.glColor4f(0.5,0.5,0.5,0.3)
        GL.glBegin(GL.GL_LINES)
        for j in range(self.fieldSize+1):
            break
            for i in range(self.fieldSize+1):
                GL.glVertex3f((float(i)/10),0,(float(j)/10))
                GL.glVertex3f((float(i)/10),self.fieldSize/10,(float(j)/10))
            for i in range(self.fieldSize+1):
                GL.glVertex3f(0,(float(i)/10),(float(j)/10))
                GL.glVertex3f(self.fieldSize/10,(float(i)/10),(float(j)/10))
            for i in range(self.fieldSize+1):
                GL.glVertex3f((float(i)/10),0,(float(j)/10))
                GL.glVertex3f((float(i)/10),self.fieldSize/10,(float(j)/10))
        for i in range(self.fieldSize*4):
            GL.glVertex3f(-4,0,(float(i)/10)-4)
            GL.glVertex3f((self.fieldSize/10)+4,0,(float(i)/10)-4)
        for i in range(self.fieldSize*8):
            GL.glVertex3f((float(i)/10)-4,0,-4)
            GL.glVertex3f((float(i)/10)-4,0,4)
        GL.glEnd()
        GL.glDisable(GL.GL_BLEND)
        GL.glDisable(GL.GL_LINE_SMOOTH)
        GL.glColor3f(1,0,0)
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(0,0,0.01)
        GL.glVertex3f(0,10,0.01)
        GL.glEnd()

        GL.glColor3f(0,0.96,0.11)
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(0,0,0)
        GL.glVertex3f(10,0,0)
        GL.glEnd()

        GL.glColor3f(0,0,1)
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(0,0,0)
        GL.glVertex3f(0,0,10)
        GL.glEnd()

    def cube (self,size,x=0,y=0,z=0):
        GL.glLineWidth(1.5)
        GL.glColor3f(1,0,0)
        GL.glBegin(GL.GL_QUADS)
        size = size
        GL.glVertex3f(x,y,z)
        GL.glVertex3f(x+size,y,z)
        GL.glVertex3f(x+size,y+size,z)
        GL.glVertex3f(x,y+size,z)

        GL.glVertex3f(x,y,z+size)
        GL.glVertex3f(x+size,y,z+size)
        GL.glVertex3f(x+size,y+size,z+size)
        GL.glVertex3f(x,y+size,z+size)

        GL.glVertex3f(x,y,z)
        GL.glVertex3f(x,y,z+size)
        GL.glVertex3f(x+size,y,z+size)
        GL.glVertex3f(x+size,y,z)

        GL.glVertex3f(x,y+size,z)
        GL.glVertex3f(x,y+size,z+size)
        GL.glVertex3f(x+size,y+size,z+size)
        GL.glVertex3f(x+size,y+size,z)

        GL.glVertex3f(x,y,z)
        GL.glVertex3f(x,y+size,z)
        GL.glVertex3f(x,y+size,z+size)
        GL.glVertex3f(x,y,z+size)

        GL.glVertex3f(x+size,y,z)
        GL.glVertex3f(x+size,y+size,z)
        GL.glVertex3f(x+size,y+size,z+size)
        GL.glVertex3f(x+size,y,z+size)

        GL.glEnd()

        GL.glColor3d(0,0,0)
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3f(x,y,z)
        GL.glVertex3f(x+size,y,z)
        GL.glVertex3f(x+size,y+size,z)
        GL.glVertex3f(x,y+size,z)

        GL.glVertex3f(x,y,z+size)
        GL.glVertex3f(x+size,y,z+size)
        GL.glVertex3f(x+size,y+size,z+size)
        GL.glVertex3f(x,y+size,z+size)

        GL.glVertex3f(x,y,z)
        GL.glVertex3f(x,y,z+size)
        GL.glVertex3f(x+size,y,z+size)
        GL.glVertex3f(x+size,y,z)

        GL.glVertex3f(x,y+size,z)
        GL.glVertex3f(x,y+size,z+size)
        GL.glVertex3f(x+size,y+size,z+size)
        GL.glVertex3f(x+size,y+size,z)

        GL.glVertex3f(x,y,z)
        GL.glVertex3f(x,y+size,z)
        GL.glVertex3f(x,y+size,z+size)
        GL.glVertex3f(x,y,z+size)

        GL.glVertex3f(x+size,y,z)
        GL.glVertex3f(x+size,y+size,z)
        GL.glVertex3f(x+size,y+size,z+size)
        GL.glVertex3f(x+size,y,z+size)
        GL.glEnd()

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
