from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def set_table_contents(records, table):
    table.clearContents()
    
    for i in enumerate(records):
        d = 0
        table.setItem(i[0], d, QTableWidgetItem(str(i[1][0])))
        item = QTableWidgetItem(i[1][1])
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) # set items not editable
        table.setItem(i[0], d+1, item)
        d += i[0]
