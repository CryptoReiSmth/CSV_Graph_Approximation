import sys
import csv
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QCheckBox, QDialog, QVBoxLayout, QHBoxLayout
import numpy as np

class CsvGraph (QDialog):
    def __init__(self, filename: str):
        super(QDialog, self).__init__()
        self.dragPoint = None
        self.dragOffset = None
        self.setGeometry(150, 100, 1000, 750)
        # Create cool window
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        self.graphWidget.setTitle("Approximate", color="b", size="25pt")
        styles = {"color": "#f00", "font-size": "20px"}
        self.graphWidget.setLabel("left", "y", **styles)
        self.graphWidget.setLabel("bottom", "x", **styles)
        self.graphWidget.addLegend()
        self.graphWidget.showGrid(x=True, y=True)
        self.setWindowTitle("CsvGraph")

        # Graphic data
        self.y = []
        self.x = []
        degree = 2

        # Read data from csv-file
        with open(r'C:\Users\redko\Desktop\check.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:      #TODO: добавить обработку заголовка
                self.y.append(int(row[0]))
        self.x = [i for i in range (len(self.y))]

        # Add points from csv-file
        self.scatter = pg.ScatterPlotItem(size=7, brush=pg.mkBrush(color="blue"))
        self.scatter.addPoints(self.x, self.y)
        self.graphWidget.addItem(self.scatter)

        # Draw approximate line
        self.approximate_y = np.polyval(np.polyfit(self.x, self.y, degree), self.x)
        self.approximate_line = self.graphWidget.plot(self.x, self.approximate_y, pen = pg.mkPen(color =  "red"), symbol='+', symbolSize=5, symbolBrush="red")
        # Set layout
        layout_h = QHBoxLayout()
        layout_h.addWidget(self.graphWidget)
        self.setLayout(layout_h)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = CsvGraph("check.csv")
    w.show()
    sys.exit(app.exec_())