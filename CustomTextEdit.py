from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys

class DropableTextEdit(QtWidgets.QTextEdit):
    def __init__(self,parent = None):
        QtWidgets.QTextEdit.__init__(self,parent)
        #super(DropableTextEdit, self).__init__()
        self.setAcceptDrops(True)
        self.setText(" Accept Drops")
        self.setStyleSheet("QLabel { background-color : #ccd; color : blue; font-size: 20px;}")
    
    def dropEvent(self, e):
        self.setText(e.mimeData().text())
        dropText = e.mimeData().text()
        if 'file:///' in dropText:
            #dropText = str()
            file =  dropText.lstrip('file:///')
            if os.path.isfile(file):
                fileRef  = open(file,'r')
                inputText = fileRef.read()
                self.setText(inputText)
                fileRef.close()
                e.accept()