from PyQt5 import QtWidgets, uic
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


def get_combo_box(options, select_callback):
    combo = QtWidgets.QComboBox()
    combo.addItems(options)
    combo.activated.connect(select_callback)
    return combo


class MainWindow(QtWidgets.QMainWindow):

    ACTIVATION_FUNCTION_COLUMN_INDEX = 1
    NODES_AMOUNT_COLUMN_INDEX = 0

    ACTIVATION_FUNCTIONS = ['relu', 'coco', 'yaron']
    MAX_NODES_AMOUNT = 10
    NODES_OPTIONS = [str(i) for i in range(MAX_NODES_AMOUNT)]

    def __init__(self):
        self.table_rows_count = 0

        QtWidgets.QWidget.__init__(self)
        uic.loadUi("ann_gui.ui", self)
        self.add_layer_button.clicked.connect(self.add_layer)
        self.remove_layer_button.clicked.connect(self.remove_layer)
        self.activation_combos = {}
        self.nodes_amount_combos = {}

        self.paint_button.clicked.connect(self.paint_something)
        

    def add_layer(self):
        self.tableWidget.insertRow(self.table_rows_count)

        # Making the middle cell combo box
        current_row = self.table_rows_count

        activation_combo_box = get_combo_box(self.ACTIVATION_FUNCTIONS, self.update_activation)
        self.activation_combos[activation_combo_box] = current_row
        self.tableWidget.setCellWidget(current_row, self.ACTIVATION_FUNCTION_COLUMN_INDEX, activation_combo_box)

        nodes_amount_combo_box = get_combo_box(self.NODES_OPTIONS, self.update_nodes_amount)
        self.nodes_amount_combos[nodes_amount_combo_box] = current_row
        self.tableWidget.setCellWidget(current_row, self.NODES_AMOUNT_COLUMN_INDEX, nodes_amount_combo_box)        
        self.table_rows_count += 1


    def remove_layer(self):
        self.tableWidget.removeRow(self.table_rows_count - 1)
        self.table_rows_count -= 1


    def update_activation(self, activation_index):
        sender = self.sender()
        row = self.activation_combos[sender]
        self.insert_value_to_table(self.tableWidget, 
                                   row, 
                                   self.ACTIVATION_FUNCTION_COLUMN_INDEX, 
                                   self.ACTIVATION_FUNCTIONS[activation_index])


    def update_nodes_amount(self, activation_index):
        sender = self.sender()
        row = self.nodes_amount_combos[sender]
        self.insert_value_to_table(self.tableWidget, 
                                   row, 
                                   self.NODES_AMOUNT_COLUMN_INDEX, 
                                   self.NODES_OPTIONS[activation_index])


    def insert_value_to_table(self, table_widget, row, column, value):
        table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(value))


    def paint_something(self):
        import pdb; pdb.set_trace()
        paint = QtGui.QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        # make a white drawing background
        paint.setBrush(Qt.white)
        paint.drawRect(event.rect())
        # for circle make the ellipse radii match
        radx = 100
        rady = 100
        # draw red circles
        paint.setPen(Qt.red)
        for k in range(125, 220, 10):
            center = QtCore.QPoint(k, k)
            # optionally fill each circle yellow
            paint.setBrush(Qt.yellow)
            paint.drawEllipse(center, radx, rady)
        paint.end()


        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())