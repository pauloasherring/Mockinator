import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
import mockinator
from mockMe import mockFile



class impl(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = mockinator.Ui_mw()
        self.ui.setupUi(self)
        postSetup(self.ui)

        #print('init')
        pass
    def onSave(self):
        #print('cb')
        pass
    def onMockMe(self):
        inputData = self.ui.teInputCode.toPlainText()
        headerf, implf = mockFile(inputData)
        self.ui.teOutputHeader.setText(headerf)
        self.ui.teOutputImpl.setText(implf)
        #print('cb')
    def onOpenFile(self):
        fileName,selectedFilter = QtWidgets.QFileDialog.getOpenFileName(self, "Open File")
        if os.path.isfile(fileName):
            fileRef  = open(fileName,'r')
            inputText = fileRef.read()
            self.ui.teInputCode.setText(inputText)
            fileRef.close()
        #print('cb ' + fileName)

def postSetup(uio):
    uio.teInputCode.setAcceptDrops(True)
    pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mw = impl()
    mw.show()
    sys.exit(app.exec_())


##pyuic5 -x -o mockinator.py mockinator.ui
##pyinstaller --onefile --windowed --icon=icon.ico mockinatorimpl.py
##pyinstaller --onefile -c mockinatorimpl.py
#pyinstaller mockinatorimpl.py --onefile --hidden-import win32gui, win32con
# import tempfile
# import codecs
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

# import win32gui, win32con

# the_program_to_hide = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)