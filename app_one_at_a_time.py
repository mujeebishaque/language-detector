from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import detectlanguage
import tkinter
import os
import pandas as pd
from tkinter import messagebox
import http.client

class Ui_MainWindow(object):

    def __init__(self):
        detectlanguage.configuration.api_key = 'insert_your_api_key_here'

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Language Detector")
        MainWindow.resize(742, 328)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 20, 241, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(490, 70, 221, 201))
        self.groupBox.setObjectName("groupBox")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setGeometry(QtCore.QRect(20, 20, 181, 161))
        self.textEdit.setObjectName("textEdit")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(100, 100, 171, 141))
        self.groupBox_2.setObjectName("groupBox_2")
        self.change_api = QtWidgets.QPushButton(self.groupBox_2)
        self.change_api.setGeometry(QtCore.QRect(40, 70, 91, 23))
        self.change_api.setObjectName("change_api")
        self.exit = QtWidgets.QPushButton(self.groupBox_2)
        self.exit.setGeometry(QtCore.QRect(40, 100, 91, 23))
        self.exit.setObjectName("exit")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit.setGeometry(QtCore.QRect(10, 40, 151, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 47, 13))
        self.label_2.setObjectName("label_2")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(360, 90, 20, 201))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.get_language = QtWidgets.QPushButton(self.centralwidget)
        self.get_language.setGeometry(QtCore.QRect(560, 280, 81, 23))
        self.get_language.setObjectName("get_language")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.change_api.clicked.connect(self.change_api_function)
        self.get_language.clicked.connect(self.detect_language)
        self.exit.clicked.connect(self.exit_ui)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Language Detector", "Language Detector"))
        self.label.setText(_translate("MainWindow", "Language Detection Software"))
        self.groupBox.setTitle(_translate("MainWindow", "URL List"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Actions"))
        self.change_api.setText(_translate("MainWindow", "Change API Key"))
        self.exit.setText(_translate("MainWindow", "Exit"))
        self.label_2.setText(_translate("MainWindow", "API Key"))
        self.get_language.setText(_translate("MainWindow", "Submit"))

    def change_api_function(self):
        api_key = self.lineEdit.text()
        detectlanguage.configuration.api_key = api_key
        

    def detect_language(self):
        import urllib.request
        num_store = 0
        try:
            if urllib.request.urlopen("http://google.com").getcode() == 200:
                pass
        except Exception:
                self.show_msg("Please Check Internet Connection")
                return

        mytext = self.textEdit.toPlainText()
        data = mytext.splitlines()
        new_data = []
        for x in range(len(data)):
            if not str(data[x]).startswith('https://') or str(data[x]).startswith('Https://'):
                data[x] = 'https://' + str(data[x])
            new_data.append(data[x].strip(' '))

        record = dict()
        filename = os.getcwd() + os.sep + 'records.xlsx'

        if os.path.exists(filename):
            os.remove(filename)
        
        if not os.path.exists(filename):
            import openpyxl
            wb = openpyxl.Workbook()
            wb.save(filename)
        
        
        for i in range(len(new_data)):
            
            print(str(new_data[i]))
            
            if i == len(new_data)-1:
                print('=====> Completed!')
            #get data from web and call the api
            try:
                request = requests.get(str(new_data[i]), headers={"Range": "bytes=0-1200"})
                text    = request.text[:1200]
                text = self.cleanhtml(text)
                record[str(data[i])] = detectlanguage.simple_detect(text)

            except Exception:
                record[str(data[i])] = "Not Working"                
                #record_store.append(str(data[i]))
            finally:
                df = pd.DataFrame(data=record, index=[0])
                df = (df.T)
                df.to_excel(filename, startrow=1)

    def exit_ui(self):
        import sys
        sys.exit()

    
    def show_msg(self, msg=''):
        window = tkinter.Tk()
        window.withdraw()
        messagebox.showinfo('INFORMATION', msg)
    
    def cleanhtml(self, raw_html):
        import re
        cleanr = re.compile('<.*?>')
        #cleanr = re.compile('<[^>]*?>') - not original
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

'''
   def append_df_to_excel(self, df, excel_path):
        if not os.path.exists(excel_path):
            import openpyxl
            wb = openpyxl.Workbook()
            wb.save('records.xlsx')

        df_excel = pd.read_excel(excel_path)
        result = pd.concat([df_excel, df], ignore_index=False)
        print(result)
        result.to_excel(excel_path, index=False)
     
'''
