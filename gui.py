from lzma import is_check_supported
from turtle import update
import db_connect as db
import sys
from PyQt6 import  QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QCheckBox, QComboBox, QListWidgetItem, QPushButton,
                             QTableView, QListWidget, QMessageBox
)
from PyQt6.QtCore import Qt, QSize


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        #'Global variables'
        self.db_klasse= "klasse_5_d"
        self.fach = 1
        print(self.fach)
        self.selected = []

        self.setWindowTitle("HA Vergessen")
        self.setMinimumSize(QSize(400,300))
        
        lable_klassen = QLabel('Klasse:')
        
        #Combobox klassen
        self.comboBox_klassen = QComboBox()
        self.comboBox_klassen.setPlaceholderText('')
        self.comboBox_klassen.addItems(db.show_tables())
        self.comboBox_klassen.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        self.comboBox_klassen.setEditable(False)
        
        #Combobox fach
        self.comboBox_fach = QComboBox()
        self.comboBox_fach.setPlaceholderText('')
        
        print(db.get_faecher_ls(self.db_klasse))
        self.comboBox_fach.addItems(db.get_faecher_ls(self.db_klasse))
        self.comboBox_fach.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)
        self.comboBox_fach.setEditable(False)
        
        #Buttons
        button_klasse_create = QPushButton('Hinzufügen')
        button_klasse_delete = QPushButton('Entfernen')
        button_selected_apply = QPushButton('Abschicken')
        
        #CheckBox
        self.checkbox_klassen = QCheckBox()
        self.checkbox_klassen.setCheckState(Qt.CheckState.Checked)
        
        #table view
        self.table = QtWidgets.QTableView()
        print(self.fach)
        data = db.query_name_num(self.db_klasse, self.fach)
        self.model = TableModel(data)
        self.table.setModel(self.model)
        
        self.list_widget = QListWidget()
        
        
        #Layouts
        vlayout = QVBoxLayout()
        h1layout = QHBoxLayout()
        h2layout = QHBoxLayout()
        
        h1layout.addWidget(lable_klassen)
        h1layout.addWidget(self.comboBox_klassen)
        h1layout.addWidget(self.comboBox_fach)
        h1layout.addWidget(button_klasse_create)
        h1layout.addWidget(button_klasse_delete)
        h1layout.addStretch()
        h1layout.addWidget(self.checkbox_klassen)
        h1layout.addWidget(button_selected_apply)
        h2layout.addWidget(self.table)
        h2layout.addWidget(self.list_widget)
                
        vlayout.addLayout(h1layout)
        vlayout.addLayout(h2layout)
        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)
        
        #event handlers
        self.comboBox_klassen.activated.connect(self.get_new_table)
        self.comboBox_fach.activated.connect(self.get_new_subject)   
        button_klasse_create.clicked.connect(self.create_button_pressed)
        button_klasse_delete.clicked.connect(self.delete_button_pressed)
        button_selected_apply.clicked.connect(self.show_msg)
        

    
    def create_button_pressed(self):
        double = False
        ls = self.table.selectedIndexes()
        
        if self.selected is None:
            for x in ls:
                id = x.row() + 1
                name = db.search_id_name(self.db_klasse, str(id))
                self.selected.append({
                    'name': name,
                    'id': int(id)
                })
        else:
            for x in ls:
                id = x.row() + 1
                for y in range(len(self.selected)):
                    if id == self.selected[y]['id']:
                        double = True
                if not double:
                    name = db.search_id_name(self.db_klasse, str(id))
                    self.selected.append({
                        'name': name,
                        'id': int(id)
                    })
                double = False
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
    def get_new_subject(self, index):
        self.comboBox_fach.itemText(index)
        ind  = index + 1
        print('Index was %d, the new on is'% self.fach,ind)
        if self.fach is not ind and ind != 0:
            print('Index changed to %d'% ind)
            self.fach = ind
            self.update_table()
    def get_new_table(self, index):
        self.db_klasse = self.comboBox_klassen.itemText(index)
        self.fach = 1
        self.update_table()
    
    def update_table(self):
        db_data = db.query_name_num(self.db_klasse, self.fach)
        self.comboBox_fach.clear()
        sub_names = db.get_faecher_ls(self.db_klasse)
        self.comboBox_fach.addItems(sub_names)
        print("New Data:")
        #print(db_data)
        self.table.setModel(TableModel(db_data))  
    def update_ls(self):
        self.list_widget.clear()
        for x in range(len(self.selected)):
        #for str in self.selected[0]['name']:
            self.list_widget.addItem(self.selected[x]['name'])
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
    def is_checkbox_checked(self):
        return self.checkbox_klassen.isChecked()
        
    

class TableModel(QtCore.QAbstractTableModel):
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

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()