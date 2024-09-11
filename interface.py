# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaceqt.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import networkx as nx
import matplotlib.pyplot as plt
import warnings
import interface2  # Add this import statement


warnings.filterwarnings("ignore", category=DeprecationWarning)


class Ui_Form(object):
    def reset_text(self):
        self.zone_texte.clear()

    def __init__(self):
        self.G = nx.DiGraph()
    
    def save_graph_to_file(self, filename="graph.gml"):
        nx.write_gml(self.G, filename)
        print(f"Graph saved to {filename}")

    def open_file(self):
        # Open a QFileDialog to select a file
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(Form, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            # Open and read the file, then set its contents to the textEdit widget
            with open(fileName, 'r') as file:
                self.zone_texte.setText(file.read())


    def show_error_dialog(self, message):
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec_()

    def save_graph(self):
        self.G.clear()
        graph_text = self.zone_texte.toPlainText().strip().split('\n')
        for line in graph_text:
            if line:
                if line[0] == '#':
                    continue
                else:
                    content = line.split()
                    if len(content) == 2:
                        try:
                            self.G.add_edge(int(content[0]), int(content[1]))
                        except ValueError:
                            print(f"Skipping invalid line: {line}")
                    else:
                        print(f"Skipping invalid line: {line}")
        self.save_graph_to_file()
        print("Graph saved:", self.G.edges())

    def show_graph(self):
        self.save_graph()
        plt.figure(figsize=(7, 7))
        nx.draw_networkx(self.G, with_labels=True, node_color='#6fb3b8')
        plt.show()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(787, 643)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 0, 771, 641))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(9, 20, 761, 631))
        self.label.setStyleSheet("border-image: url(img.jpg);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.display = QtWidgets.QPushButton(self.widget)
        self.display.setGeometry(QtCore.QRect(460, 340, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.display.setFont(font)
        self.display.setObjectName("display")
        self.zone_texte = QtWidgets.QTextEdit(self.widget)
        self.zone_texte.setGeometry(QtCore.QRect(40, 60, 371, 481))
        self.zone_texte.setObjectName("zone_texte")
        self.zone_texte.setPlaceholderText("Enter your graph here \n\n Please adhere to the format:\n Each line should contain exactly two integers separated by whitespace. These integers represent the nodes of the directed edge in the graph.   \n\n Note: Any line that does not conform to the format will be ignored.")  # Adding placeholder text

        self.reset = QtWidgets.QPushButton(self.widget)
        self.reset.setGeometry(QtCore.QRect(460, 420, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.reset.setFont(font)
        self.reset.setObjectName("reset")
        self.Open = QtWidgets.QPushButton(self.widget)
        self.Open.setGeometry(QtCore.QRect(530, 110, 221, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(False)
        self.Open.setFont(font)
        self.Open.setObjectName("Open")
        self.labe_1 = QtWidgets.QLabel(self.widget)
        self.labe_1.setEnabled(True)
        self.labe_1.setGeometry(QtCore.QRect(450, 140, 55, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.labe_1.setFont(font)
        self.labe_1.setAutoFillBackground(False)
        self.labe_1.setStyleSheet("color: white")
        self.labe_1.setTextFormat(QtCore.Qt.PlainText)
        self.labe_1.setAlignment(QtCore.Qt.AlignCenter)
        self.labe_1.setObjectName("labe_1")
        self.apply = QtWidgets.QPushButton(self.widget)
        self.apply.setGeometry(QtCore.QRect(40, 570, 281, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.apply.setFont(font)
        self.apply.setObjectName("apply")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(622, 577, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
#---------------------------------------------------------------------
        self.reset.clicked.connect(self.reset_text)
        self.Open.clicked.connect(self.open_file)
        self.pushButton.clicked.connect(Form.close)
        self.apply.clicked.connect(self.save_graph)  # Connect the apply button to save the graph

        self.apply.clicked.connect(self.on_apply_clicked)  # Connect the apply button to custom slot

        self.display.clicked.connect(self.show_graph)  # Connect the display button to show the graph
#-----------------------------------------------------------------------
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.display.setText(_translate("Form", "Display"))
        self.reset.setText(_translate("Form", "Reset"))
        self.Open.setText(_translate("Form", "Open from file"))
        self.labe_1.setText(_translate("Form", "OR"))
        self.apply.setText(_translate("Form", "Validate"))
        self.pushButton.setText(_translate("Form", "Exit"))

    def on_apply_clicked(self):
        self.save_graph()
        if self.G.number_of_nodes() == 0 or self.G.number_of_edges() == 0:
            self.show_error_dialog("No graph has been entered.")
        else:
            self.open_interface2()  # Open the new interface instead of the dialog

    def open_interface2(self):
        self.interface2_window = QtWidgets.QWidget()
        self.ui_interface2 = interface2.Ui_Form()
        self.ui_interface2.setupUi(self.interface2_window)
        self.interface2_window.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()

    sys.exit(app.exec_())
