import db_connect as db
import sys
from PyQt6.QtWidgets import QMessageBox, QTableView
from PyQt6.QtCore import Qt, QSize, QAbstractTableModel

class Button_comands():
    def create_button_pressed(self):
        is_double = False
        ls = self.table.selectedIndexes()
        
        for item in ls:
            column_id = item.row() + 1 
            if self.selected is None:
                name = db.search_id_name(self.db_klasse, str(column_id))
                self.selected.append({'name': name,'id': int(column_id)})
            else:
                for i in range(len(self.selected)):
                    if column_id == self.selected[i]['id']:
                        is_double = True
                if not is_double:
                    name = db.search_id_name(self.db_klasse, str(column_id))
                    self.selected.append({'name': name,'id': int(column_id)})                            
        self.update_ls()
    def delete_button_pressed(self):
        if self.selected is not None:
            ls = self.table.selectedIndexes()
            for x in ls:
                id = x.row() +1
                for y in range(len(self.selected)):
                    if id == self.selected[y]['id']:
                        print(self.selected[y]['id'])
                        del self.selected[y]
                        break
        self.update_ls()
    def show_msg(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Icon.Question)
        self.msg.setWindowTitle("Bestätigung")    
        self.msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        self.msg.buttonClicked.connect(self.msgbtn)
        
        if self.is_checkbox_checked():
            informative_text = 'Es werden E-Mails an die Schüler verschickt'
        else:
            informative_text = 'Es werden keine E-Mails an die Schüle verschickt'
        self.msg.setInformativeText(informative_text)
        
        detailed_text = 'Schüler:'
        for elm in range(len(self.selected)):
            detailed_text = detailed_text + '\n' + self.selected[elm]['name']
        self.msg.setDetailedText(detailed_text)
        
        retval = self.msg.exec()
        print ("value of pressed message box button:", retval) 
    
    def msgbtn(self, button):
            
        if button == 'Cancle':
            self.msg.close()
        else:
            self.msg.close()
            ls = []
            for i in range(len(self.selected)):
                id = self.selected[i]['id']
                anzahl = db.get_fach_amount_by_id(self.db_klasse, id) + 1
                db.update_row(self.db_klasse, id, self.fach, anzahl)
            self.update_table()
            
class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])      