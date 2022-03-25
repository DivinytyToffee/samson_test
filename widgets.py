import sys
from math import sqrt

from PyQt4.QtCore import Qt, QModelIndex, QVariant, QAbstractTableModel
from PyQt4.QtGui import QPen, QWidget, QLineEdit, QLabel, QGridLayout, QAbstractItemDelegate, QStyle, QBrush, \
    QTableView, QApplication, QFont

from reverse import reverse_string


class ReverseStringWidget(QWidget):
    """
    Class describing widget for reversing input string.
    """

    def __init__(self):
        super(ReverseStringWidget, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Reverse Form')
        input_string = QLineEdit()
        input_string.textChanged.connect(self.reverse_string_event)
        self.reversed_string = QLabel()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(input_string, 1, 0)
        grid.addWidget(self.reversed_string, 2, 0)

        self.setLayout(grid)

        self.show()

    def reverse_string_event(self, text):
        rev = reverse_string(text)
        self.reversed_string.setText(rev)


class TableDelegate(QAbstractItemDelegate):

    def __init__(self, parent=None, *args):
        QAbstractItemDelegate.__init__(self, parent, *args)

    def paint(self, QPainter, QStyleOptionViewItem, QModelIndex):
        QPainter.save()
        QPainter.setPen(QPen(Qt.NoPen))
        value = QModelIndex.data(Qt.DisplayRole)
        int_val = value.toInt()[0]
        if self.is_fib(int_val):
            QPainter.setBrush(QBrush(Qt.yellow))
        elif self.is_prime(int_val):
            QPainter.setBrush(QBrush(Qt.green))
        else:
            QPainter.setBrush(QBrush(Qt.white))
        QPainter.drawRect(QStyleOptionViewItem.rect)

        QPainter.setPen(QPen(Qt.black))
        if int_val % 5 == 0:
            QPainter.setPen(QPen(Qt.blue))
        elif int_val % 2 == 0:
            QPainter.setPen(QPen(Qt.red))

        font = QFont()
        if self.is_prime(int_val):
            font.setUnderline(True)
            QPainter.setFont(font)
        elif int_val % 10 == 0:
            font.setBold(True)
            QPainter.setFont(font)

        if value.isValid():
            text = value.toString()
            QPainter.drawText(QStyleOptionViewItem.rect, Qt.AlignCenter, text)

        QPainter.restore()

    @staticmethod
    def is_prime(number):
        if number % 2 == 0:
            return number == 2
        d = 3
        while d * d <= number and number % d != 0:
            d += 2
        return d * d > number

    @staticmethod
    def is_fib(number):
        return sqrt(5 * (number ** 2) - 4) % 1 == 0 or sqrt(5 * (number ** 2) + 4) % 1 == 0


class TableModel(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        super(TableModel, self).__init__()
        self.datatable = None

    def update(self, dataIn):
        self.datatable = dataIn

    def rowCount(self, parent=QModelIndex()):
        return len(self.datatable)

    def columnCount(self, parent=QModelIndex()):
        return len(self.datatable[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            i = index.row()
            j = index.column()
            return '{0}'.format(self.datatable[i][j])
        else:
            return QVariant()

    def flags(self, index):
        return Qt.ItemIsEnabled


class MultiplicationTable(QTableView):
    def __init__(self):
        super(MultiplicationTable, self).__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 1100, 360)
        self.setWindowTitle('Multiplication table')

        tm = TableModel(self)
        de = TableDelegate(self)
        tm.update(self.multiplication_table())
        self.setModel(tm)
        self.setItemDelegate(de)

        self.show()
        self.raise_()

    @staticmethod
    def multiplication_table():
        return [[x * y for y in range(1, 11)] for x in range(1, 11)]


def run_widget(widget):
    app = QApplication(sys.argv)
    ex = widget()
    sys.exit(app.exec_())
