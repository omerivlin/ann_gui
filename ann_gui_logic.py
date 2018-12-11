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


class CircleDrawer(QtWidgets.QWidget):

    def __init__(self, radius):
        QtWidgets.QWidget.__init__(self)
        self.radius = radius

    @staticmethod
    def draw_circle(paint_object, x_position, y_position, radius):
        center = QtCore.QPoint(x_position, y_position)
        # optionally fill each circle yellow
        paint_object.setBrush(QtCore.Qt.red)
        paint_object.drawEllipse(center, radius, radius)

    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        # draw red circles
        paint.setPen(QtCore.Qt.blue)
        
        # Draw the circle in the middle of the parent widget
        self.draw_circle(paint, event.rect().width() / 2, event.rect().height() / 2, self.radius)

        paint.end()

    def sizeHint(self):
        return QtCore.QSize(self.radius * 2, self.radius * 2)


class NeuralNetworkMap(QtWidgets.QWidget):
    ''' An example of PySide/PyQt absolute positioning; the main window
        inherits from QWidget, a convenient widget for an empty window. '''

    NODE_SIZE = 7
 
    def __init__(self, layers):
        """
        Initiates and drawes a neural network drawing using the given layers.
        @param layers: a list containing the amount of nodes in each layer.
        for example - [4,7,6,9,2]
        """
        # Initialize the object as a QWidget and
        # set its title and minimum width
        QtWidgets.QWidget.__init__(self)        

        self.setWindowTitle('My Network!')
        self.setMinimumWidth(300)
        self.setMinimumHeight(300)

        # Create the QVBoxLayout that lays out the whole form
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)
        self.columns = []
        self.nodes = {}

        self._layers = []
        self.layers = layers

    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, value):
        if value != self._layers:
            self._layers = value
            self.delete_all_nodes()
            self._create_layers_layout(value)


    def delete_all_nodes(self):
        for column, nodes in self.nodes.items():
            for node in nodes:
                self.columns[column].removeWidget(node)
                node.deleteLater()

        self.nodes = {}
        self.columns = []

        
    def _create_layers_layout(self, layers):
        """
        Creates the circles in the layout.
        :param layers: A list containing amount of circles in each layer.
        :return:
        """
        for layer_index, layer_nodes_amount in enumerate(layers):
            # A column is a verticle box
            current_column = QtWidgets.QVBoxLayout()
            self.columns.append(current_column)
            self.nodes[layer_index] = []

            for node_index in range(layer_nodes_amount):
                # Create a circle
                current_circle = CircleDrawer(self.NODE_SIZE)
                self.nodes[layer_index].append(current_circle)
                # Add the nodes to the column
                current_column.addWidget(current_circle)

            # Add the column to the "network"
            self.main_layout.addLayout(current_column)    

    @staticmethod
    def _get_node_position(node):
        """
        Since each node's circle is in a box - calculate the box's center
        """
        node_x = (node.width() / 2) + node.x()
        node_y = (node.height() / 2) + node.y()
        return node_x, node_y

    def paintEvent(self, event):
        """
        This draws the lines that connects the circles
        """
        paint = QtGui.QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        # draw red circles
        paint.setPen(QtCore.Qt.blue)

        for layer_index, layer_nodes in self.nodes.items():
            for node in layer_nodes:
                # Don't draw lines for the last layer
                if layer_index == len(self.nodes) - 1:
                    continue

                node_x, node_y = self._get_node_position(node)

                # Connect each node with all the nodes in the next layer
                next_layer = layer_index + 1
                for next_node in self.nodes[next_layer]:
                    next_node_x, next_node_y = self._get_node_position(next_node)
                    paint.drawLine(node_x, node_y, next_node_x, next_node_y)

        paint.end()


class MainWindow(QtWidgets.QMainWindow):

    ACTIVATION_FUNCTION_COLUMN_INDEX = 1
    NODES_AMOUNT_COLUMN_INDEX = 0

    ACTIVATION_FUNCTIONS = ['relu', 'coco', 'yaron']
    MAX_NODES_AMOUNT = 10
    NODES_OPTIONS = [str(i) for i in range(1, MAX_NODES_AMOUNT)]

    def __init__(self):
        self.table_rows_count = 0

        QtWidgets.QWidget.__init__(self)
        uic.loadUi("ann_gui.ui", self)
        self.add_layer_button.clicked.connect(self.add_layer)
        self.remove_layer_button.clicked.connect(self.remove_layer)
        self.activation_combos = {}
        self.nodes_amount_combos = {}

        self.network_drawing = NeuralNetworkMap([])
        self.main_grid_layout.addWidget(self.network_drawing, 3, 4)
        self._network_layers = []
        

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

        self.update_network_drawing()


    def remove_layer(self):
        self.tableWidget.removeRow(self.table_rows_count - 1)
        self.table_rows_count -= 1
        self.update_network_drawing()


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
        self.update_network_drawing()


    def insert_value_to_table(self, table_widget, row, column, value):
        table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(value))


    def update_network_drawing(self):
        layers_data = [int(self.tableWidget.cellWidget(row, self.NODES_AMOUNT_COLUMN_INDEX).currentText()) for row in range(self.tableWidget.rowCount())]
        self.network_drawing.layers = layers_data


        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())