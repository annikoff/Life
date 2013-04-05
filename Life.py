# -*- coding: utf-8 -*-
import random
from numpy import *

class Life:

    cells = []

    def __init__(self, width, height, isInfinity=True):
        self.reset(width,height,isInfinity)
        self.genNumber = 0;

    def getGenNumber(self):
        return self.genNumber

    def setInfinity(self, state):
        self.isInfinity = state

    def getInfinity(self):
        return self.isInfinity

    def reset(self, width, height, isInfinity=True):
        self.width = width
        self.height = height
        self.isInfinity = isInfinity
        self.cellsCount = self.width*self.height
        self.cells = arange(self.cellsCount).reshape(self.width,self.height)
        self.cells.fill(False)
        return self.cells

    def simulate(self):
        self.ncells = []
        self.ncells = arange(self.cellsCount).reshape(self.width,self.height)
        self.ncells.fill(False)
        x = 0
        for cells in self.cells:            
            y = 0
            for cell in cells:
                self.ncells[x,y] = cell

                tx = x+1
                if tx < self.width:
                    nextCell = self.cells[tx,y]
                else:
                    if self.isInfinity:
                        nextCell = self.cells[0,y]
                    else:
                        nextCell = False

                tx = x-1
                if tx >= 0:
                    prevCell = self.cells[tx,y]
                else:
                    if self.isInfinity:
                        prevCell = self.cells[-1,y]
                    else:
                        prevCell = False

                ty = y-1
                if ty >= 0:
                    topCell = self.cells[x,ty]
                else:
                    if self.isInfinity:
                        topCell = self.cells[x,-1]
                    else:
                        topCell = False

                ty = y-1
                if ty >= 0:
                    tx = x-1
                    if tx >=0:
                        topprevCell = self.cells[tx,ty]
                    else:
                        if self.isInfinity:
                            topprevCell = self.cells[-1,ty]
                        else:
                            topprevCell = False
                else:
                    tx = x-1
                    if tx >=0:
                        topprevCell = self.cells[tx,-1]
                    else:
                        if self.isInfinity:
                            topprevCell = self.cells[-1,-1]
                        else:
                            topprevCell = False

                ty = y-1
                if ty >= 0:
                    tx = x+1
                    if tx < self.width:
                        topnextCell = self.cells[tx,ty]
                    else:
                        if self.isInfinity:
                            topnextCell = self.cells[0,ty]
                        else:
                            topnextCell = False
                else:
                    tx = x+1
                    if tx < self.width:
                        topnextCell = self.cells[tx,-1]
                    else:
                        if self.isInfinity:
                            topnextCell = self.cells[0,-1]
                        else:
                            topnextCell = False


                ty = y+1
                if ty < self.height:
                    btmCell = self.cells[x,ty]
                else:
                    if self.isInfinity:
                        btmCell = self.cells[x,0]
                    else:
                        btmCell = False

                ty = y+1
                if ty < self.height:
                    tx = x+1
                    if tx < self.width:
                        btmpnexCell = self.cells[tx,ty]
                    else:
                        if self.isInfinity:
                            btmpnexCell = self.cells[0,ty]
                        else:
                            btmpnexCell = False
                else:
                    tx = x+1
                    if tx < self.width:
                        btmpnexCell = self.cells[tx,0]
                    else:
                        if self.isInfinity:
                            btmpnexCell = self.cells[0,0]
                        else:
                            btmpnexCell = False

                ty = y+1
                if ty < self.height:
                    tx = x-1
                    if tx >=0:
                        btmprevCell = self.cells[tx,ty]
                    else:
                        if self.isInfinity:
                            btmprevCell = self.cells[-1,ty]
                        else:
                            btmprevCell = False
                else:
                    tx = x-1
                    if tx >=0:
                        btmprevCell = self.cells[tx,0]
                    else:
                        if self.isInfinity:
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