# -*- coding: utf-8 -*-
import random
from numpy import *

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