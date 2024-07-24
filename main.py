from PyQt5 import QtWidgets
from ui import Ui_Form
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
