from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt

def set_table_contents(records, table):
    table.clearContents()

    for row, ele in enumerate(records):
        column = 0
        table.setItem(row, column, QTableWidgetItem(str(ele[0])))
        item = QTableWidgetItem(ele[1])
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) # set items not editable
        table.setItem(row, column+1, item)
        column += row
