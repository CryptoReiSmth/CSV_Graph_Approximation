import sys
import csv
import pyqtgraph as pg
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QSlider, QLabel, QLineEdit
from PyQt5.QtCore import Qt
import numpy as np


class CsvGraph (QDialog):
    def __init__(self, file_path: str):
        super(QDialog, self).__init__()
        self.setGeometry(100, 50, 1400, 950)
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
        self.degree = 2

        # Read data from csv-file
        #TODO: read couple of values
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:      #TODO: add header handling
                self.y.append(int(row[0]))
        self.x = [i for i in range (len(self.y))]

        # Add points from csv-file
        self.scatter = pg.ScatterPlotItem(size=7, brush=pg.mkBrush(color="blue"))
        self.scatter.addPoints(self.x, self.y)
        self.graphWidget.addItem(self.scatter)

        # Draw approximate line
        self.approximate_y = np.polyval(np.polyfit(self.x, self.y, self.degree), self.x)
        self.approximate_line = self.graphWidget.plot(self.x, self.approximate_y, pen = pg.mkPen(color =  "red"), symbol='+', symbolSize=5, symbolBrush="red")

        # Add slider
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setTickPosition(QSlider.TicksBelow)
        self.sld.setRange(2, 6)
        self.sld.setTickInterval(1)
        self.sld.valueChanged.connect(self.slider_value_change)
        self.text_degree = QLabel(f"Степень полинома: {self.degree}")

        # Add data input
        self.line_edits = []
        for item in self.y:
            self.line_edits.append(QLineEdit(str(item), self))

        # Add values table
            #TODO: table

        # Set layout
        layout_h = QHBoxLayout()
        layout_v = QVBoxLayout()
        layout_v.addWidget(self.graphWidget)
        layout_v.addWidget(self.sld)
        layout_v.addWidget(self.text_degree)
        layout_h.addLayout(layout_v)
        self.setLayout(layout_h)

    def slider_value_change(self, value):
        self.degree = value
        self.text_degree.setText(f"Степень полинома: {self.degree}")
        self.update_approximate_line()

    def update_approximate_line(self):
        self.approximate_y = np.polyval(np.polyfit(self.x, self.y, self.degree), self.x)
        self.approximate_line.setData(self.x, self.approximate_y)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = CsvGraph("check.csv")
    w.show()
    sys.exit(app.exec_())