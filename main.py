import sys
import csv
import pyqtgraph as pg
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QSlider, QLabel, QTableWidget, QTableWidgetItem
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
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:      #TODO: add header handling
                self.x.append(int(row[0].split(";")[0]))
                self.y.append(int(row[0].split(";")[1]))

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


        # Add values table
        self.data_table = QTableWidget()
        self.data_table.setRowCount(len(self.x))
        self.data_table.setColumnCount(2)
        self.data_table.setHorizontalHeaderLabels(["x", "y"])
        self.data_table.verticalHeader().setVisible(False)
        self.data_table.resizeColumnsToContents()
        for i in range(len(self.x)):
            self.data_table.setItem(i, 0, QTableWidgetItem(str(self.x[i])))
            self.data_table.setItem(i, 1, QTableWidgetItem(str(self.y[i])))


        # Set layout
        layout_h = QHBoxLayout()
        layout_v1 = QVBoxLayout()
        layout_v2 = QVBoxLayout()
        sub_layout_h = QHBoxLayout()
        layout_v1.addWidget(self.graphWidget)
        layout_v2.addWidget(self.data_table)
        sub_layout_h.addWidget(self.sld, 3)
        sub_layout_h.addWidget(self.text_degree, 7)
        layout_v1.addLayout(sub_layout_h)
        layout_h.addLayout(layout_v1, 9)
        layout_h.addLayout(layout_v2, 1)
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