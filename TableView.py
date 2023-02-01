from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QWidget, QTableView, QHBoxLayout, QHeaderView
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt


class TableModel(QAbstractTableModel):
    def __init__(self, in_data: list):
        super().__init__()
        self.in_data = in_data

        self.horizontalHeaders = list(range(1, 10))

    def headerData(self, index, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                return self.horizontalHeaders[index]
            except:
                pass
        return super().headerData(index, orientation, role)

    def setHeaderData(self, index, orientation, data, role=Qt.EditRole):
        if orientation == Qt.Horizontal and role in (Qt.DisplayRole, Qt.EditRole):
            try:
                self.horizontalHeaders[index] = data
                return True
            except:
                return False
        return super().setHeaderData(index, orientation, data, role)

    @staticmethod
    def _in_data_validator(array):
        res = set(map(len, array))
        return len(res) == 1

    @property
    def in_data(self):
        return self._in_data

    @in_data.setter
    def in_data(self, value):
        if type(value) not in (list, tuple):
            raise TypeError('Data type must be tuple or list')
        if not self._in_data_validator(value):
            raise TypeError('Wrong array structure. It must be 2D array')
        self._in_data = value

    def rowCount(self, parent=QModelIndex()):
        return len(self.in_data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.in_data[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            try:
                return self.in_data[index.row()][index.column()]
            except IndexError:
                return ''

    def change_in_data(self, in_data):
        self.in_data = in_data


class TableWindow(QWidget):
    def __init__(self, in_data, headers_list=None):
        super(TableWindow, self).__init__()
        self.setGeometry(600, 300, 500, 400)
        self.setObjectName('ResultTable')

        self.headers_list = headers_list
        if not headers_list:
            self.test_headers = ['Resource', 'Place']

        self.model = TableModel(in_data)
        for i, name in enumerate(self.test_headers):
            try:
                self.model.setHeaderData(i, Qt.Orientation.Horizontal, name)
            except Exception as ex:
                print(ex)

        self.table_view = QTableView(self)
        self.table_view.setModel(self.model)
        self.table_view.resizeColumnsToContents()

        self.table_layout = QHBoxLayout()
        self.table_layout.addWidget(self.table_view)
        self.setLayout(self.table_layout)


if __name__ == '__main__':
    # t = TableWindow([1,3,3])
    # print('test')
    pass
