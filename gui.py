import db_connect as db
import gui_functions as fn
import sys
from PyQt6 import  QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QCheckBox, QComboBox, QListWidgetItem, QPushButton,
                             QTableView, QListWidget, QMessageBox
)
from PyQt6.QtCore import Qt, QSize


class MainWindow(QMainWindow,fn.Button_comands):
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
        button_add_student = QPushButton('ADD Student')
        button_delete_student = QPushButton('DELETE Student')
        
        #CheckBox
        self.checkbox_klassen = QCheckBox()
        self.checkbox_klassen.setCheckState(Qt.CheckState.Checked)
        
        #table view
        self.table = QtWidgets.QTableView()
        print(self.fach)
        data = db.query_name_num(self.db_klasse, self.fach)
        self.model = fn.TableModel(data)
        self.table.setModel(self.model)
        
        self.list_widget = QListWidget()
        
        
        #Layouts
        vlayout = QVBoxLayout()
        h1layout = QHBoxLayout()
        h2layout = QHBoxLayout()
        h3layout = QHBoxLayout()
        
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
         
        h3layout.addWidget(button_add_student)
        h3layout.addWidget(button_delete_student)
        h3layout.addStretch()       
        
        vlayout.addLayout(h1layout)
        vlayout.addLayout(h2layout)
        vlayout.addLayout(h3layout)
        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)
        
        #event handlers
        self.comboBox_klassen.activated.connect(self.get_new_table)
        self.comboBox_fach.activated.connect(self.get_new_subject)   
        button_klasse_create.clicked.connect(self.create_button_pressed)
        button_klasse_delete.clicked.connect(self.delete_button_pressed)
        button_selected_apply.clicked.connect(self.show_msg)
        
    def get_new_subject(self, index):
        self.comboBox_fach.itemText(index)
        ind  = index + 1
        if self.fach is not ind:
            self.fach = ind
            self.update_table()
    def get_new_table(self, index):
        self.db_klasse = self.comboBox_klassen.itemText(index)
        self.fach = 1
        self.update_table() 
    def update_table(self):
        db_data = db.query_name_num(self.db_klasse, self.fach)
        self.comboBox_fach.clear()
        self.comboBox_fach.addItems(db.get_faecher_ls(self.db_klasse))
        self.table.setModel(fn.TableModel(db_data))  
    def update_ls(self):
        self.list_widget.clear()
        for x in range(len(self.selected)):
            self.list_widget.addItem(self.selected[x]['name'])
    def is_checkbox_checked(self):
        return self.checkbox_klassen.isChecked()
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()