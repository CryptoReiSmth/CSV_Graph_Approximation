import sys
import csv
import pyqtgraph as pg
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QVBoxLayout, QSlider, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QMenuBar, QMainWindow, QAction, QFileDialog
from PyQt5.QtCore import Qt
import numpy as np
from pathlib import Path

def sign(n):
  if n < 0: return " "
  else: return " +"

def enter_correct_file_path():
    file_name = input("Введите полный путь .csv файла:\n")
    if file_name[-4::] not in ".csv":
        print("Введен неверный типа файл! Попробуйте еще раз.")
        exit(1)
    else:
        try:
            open(file_name, "r")
        except (FileNotFoundError, IsADirectoryError):
            print("Указанный файл не существует!")
            exit(1)
        else:
            return file_name


class Window(QMainWindow):
    def __init__(self, file_name: str):
        super(QMainWindow, self).__init__()
        self.setGeometry(100, 50, 1400, 950)
        self.dialog = CsvGraph(file_name)
        self.setCentralWidget(self.dialog)

        #Add menu
        self.menuBar = QMenuBar()
        self.setMenuBar(self.menuBar)

        self.file_menu = self.menuBar.addMenu("Файл")
        self.help_menu = self.menuBar.addMenu("Справка")

        # Create actions
        self.open_action = QAction("Открыть")
        self.save_action = QAction("Сохранить")
        self.save_as_action = QAction("Сохранить как")
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)

        self.open_action.setShortcut("Ctrl+O")
        self.save_action.setShortcut("Ctrl+S")
        self.save_as_action.setShortcut("Ctrl+Shift+S")

        self.exit_action = QAction("Выход")
        self.help_action = QAction("О программе")
        self.help_menu.addAction(self.help_action)
        self.help_menu.addAction(self.exit_action)

        self.open_action.triggered.connect(self.open)
        self.save_action.triggered.connect(self.save)
        self.save_as_action.triggered.connect(self.save_as)
        self.exit_action.triggered.connect(self.exit)
        self.help_action.triggered.connect(self.help)


    def open(self):
        home_dir = str(Path.home())
        open_file = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
        if open_file[0][-4::] not in ".csv":
            dialog = QDialog()
            dialog.setWindowTitle("Неверный тип файла")
            label = QLabel("Введен неверный типа файл! Попробуйте еще раз.")
            layout = QHBoxLayout()
            layout.addWidget(label)
            dialog.setLayout(layout)
            dialog.exec()
        else:
            dialog = CsvGraph(open_file[0])

    def save(self):
        pass

    def save_as(self):
        pass

    def help(self):
        pass

    def exit(self):
        self.exec()




class CsvGraph (QDialog):
    def __init__(self, file_name: str):
        super(QDialog, self).__init__()


        # Create cool window
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        self.graphWidget.setTitle("Approximate", color="b", size="25pt")
        styles = {"color": "#f00", "font-size": "20px"}
        self.graphWidget.setLabel("left", "y", **styles)
        self.graphWidget.setLabel("bottom", "x", **styles)
        self.graphWidget.addLegend()
        self.graphWidget.showGrid(x=True, y=True)
        self.setWindowTitle(file_name)

        # Graphic data
        self.y = []
        self.x = []
        self.degree = 2

        # Read data from csv-file
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:      #TODO: add header handling
                self.x.append(int(row[0].split(";")[0]))
                self.y.append(int(row[0].split(";")[1]))

        # Add points from csv-file
        self.scatter = pg.ScatterPlotItem(size=7, brush=pg.mkBrush(color="blue"))
        self.scatter.addPoints(self.x, self.y)
        self.graphWidget.addItem(self.scatter)

        # Draw approximate line
        self.line_coefficients = np.polyfit(self.x, self.y, self.degree)
        self.approximate_y = np.polyval(self.line_coefficients, self.x)
        self.approximate_line = self.graphWidget.plot(self.x, self.approximate_y, pen = pg.mkPen(color =  "red"), symbol='+', symbolSize=5, symbolBrush="red")

        # Show line equation
        self.approximate_line_equation = "    Уравнение линии аппроксимации:  "
        for degree in range(len(self.line_coefficients) - 1, 0, -1):
            self.approximate_line_equation += '%.4f' % self.line_coefficients[degree]
            self.approximate_line_equation += f" x^{degree}"
            self.approximate_line_equation += sign(float(self.line_coefficients[degree - 1]))
        self.approximate_line_equation += '%.4f' % self.line_coefficients[0]
        self.equation_label = QLabel(self.approximate_line_equation)

        # Add slider
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setTickPosition(QSlider.TicksBelow)
        self.sld.setRange(2, 6)
        self.sld.setTickInterval(1)
        self.sld.valueChanged.connect(self.slider_value_change)
        self.degree_label = QLabel(f"Степень полинома: {self.degree}")

        # Add values table
        self.data_table = QTableWidget()
        self.data_table.setRowCount(len(self.x))
        self.data_table.setColumnCount(2)
        self.data_table.setHorizontalHeaderLabels(["x", "y"])
        self.data_table.verticalHeader().setVisible(False)
        self.data_table.resizeColumnsToContents()
        for i in range(self.data_table.rowCount()):
            self.data_table.setItem(i, 0, QTableWidgetItem(str(self.x[i])))
            self.data_table.setItem(i, 1, QTableWidgetItem(str(self.y[i])))

        # Add apply button
        self.apply_button = QPushButton("Применить")
        self.apply_button.clicked.connect(self.apply_table_changes)

        # Set layout
        layout_h = QHBoxLayout()
        layout_v1 = QVBoxLayout()
        layout_v2 = QVBoxLayout()
        sub_layout_h = QHBoxLayout()
        sub_layout_h.setAlignment(Qt.AlignRight)
        layout_v1.addWidget(self.graphWidget)
        layout_v2.addWidget(self.data_table)
        layout_v2.addWidget(self.apply_button)
        sub_layout_h.addWidget(self.sld, 2)
        sub_layout_h.addWidget(self.degree_label, 1)
        sub_layout_h.addWidget(self.equation_label, 7)
        layout_v1.addLayout(sub_layout_h)
        layout_h.addLayout(layout_v1, 10)
        layout_h.addLayout(layout_v2, 1)
        self.setLayout(layout_h)

    def slider_value_change(self, value):
        self.degree = value
        self.degree_label.setText(f"Степень полинома: {self.degree}")
        self.update_line_coefficients()
        self.update_approximate_line()
        self.update_approximate_line_equation()

    def update_approximate_line_equation(self):
        self.approximate_line_equation = "    Уравнение линии аппроксимации:  "
        for degree in range(len(self.line_coefficients) - 1, 0, -1):
            self.approximate_line_equation += '%.4f' % self.line_coefficients[degree]
            self.approximate_line_equation += f" x^{degree}"
            self.approximate_line_equation += sign(float(self.line_coefficients[degree - 1]))
        self.approximate_line_equation += '%.4f' % self.line_coefficients[0]
        self.equation_label.setText(self.approximate_line_equation)

    def update_approximate_line(self):
        self.approximate_y = np.polyval(self.line_coefficients, self.x)
        self.approximate_line.setData(self.x, self.approximate_y)

    def update_drawn_points(self):
        self.scatter.setData(self.x, self.y)

    def update_line_coefficients(self):
        self.line_coefficients = np.polyfit(self.x, self.y, self.degree)

    def apply_table_changes(self):
        #TODO: check entered type
        for x_row in range(self.data_table.rowCount()):
            self.x[x_row] = int(self.data_table.item(x_row, 0).text())
        for y_row in range(self.data_table.rowCount()):
            self.y[y_row] = int(self.data_table.item(y_row, 1).text())
        self.update_line_coefficients()
        self.update_drawn_points()
        self.update_approximate_line()
        self.update_approximate_line_equation()


if __name__ == '__main__':
    #TODO: убрать коммент!!!!!!!
    #file_path = enter_correct_file_path()
    app = QApplication(sys.argv)
    w = Window("check.csv")
    w.show()
    sys.exit(app.exec_())