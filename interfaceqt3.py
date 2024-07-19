from PyQt5 import QtCore, QtGui, QtWidgets
import time
from Alpha_Burden_based_semantic import alpha_burden_based
from Burden_based_semantic import burden_based
from catergriser_based import categoriser_based_ranking
from discussion_based import discussion_based
from matt_and_toni import mt_ranking
from scoring_aggregation.biased_scoring_aggregation import biased_scoring_aggregation
from scoring_aggregation.borda_count_aggregation import borda_count_aggregation
from scoring_aggregation.consensus import closest_ranking, kendall_closest_ranking
from scoring_aggregation.plurality_aggregation import plurality_aggregation
from scoring_aggregation.top_k_aggregation import topk_aggregation
from scoring_aggregation.veto_aggregation import  minimax_method, veto_aggregation , aggregate_rankings
from tuple_based import tuple_based
import networkx as nx

Gr = nx.DiGraph()

def load_graph_from_file(filename="graph.gml"):
    G = nx.read_gml(filename)
    print(f"Graph loaded from {filename}")
    return G

class Ui_Form(object):
    #****************************************************************************************
    def __init__(self):
        # Création du graphe G
        self.G = load_graph_from_file()

        # Mappage des fonctions spécifiques avec le graphe comme argument
        self.function_map = {
            "categoriser": lambda: categoriser_based_ranking(self.G),
            "discussion": lambda: discussion_based(self.G, 1),
            "burden": lambda: burden_based(self.G, 10),
            "tuple": lambda: tuple_based(self.G),
            "Matt & Toni": lambda: mt_ranking(self.G),
            "alpha burden": self.handle_alpha_burden  # Special case
        }

    def read_agent_count(self):
        while True:
            try:
                with open("agent_count.txt", "r") as f:
                    content = f.read().strip()
                    if content:
                        return int(content)
            except ValueError as e:
                print("Waiting for valid agent count...")
                time.sleep(1)  # Sleep for a short time before retrying
            except Exception as e:
                print("Failed to read agent count:", e)
                return 0

    # Method to handle alpha burden case
    def handle_alpha_burden(self):
        alpha, ok = AlphaDialog.getAlpha()
        if ok:
            return alpha_burden_based(self.G, alpha)
        return None

    #*****************************************************************************************
    def setupUi(self, Form):
        

        Form.setObjectName("Form")
        Form.resize(944, 593)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 920, 569))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Use QVBoxLayout inside the scroll area for dynamic adjustment
        self.verticalLayoutInsideScrollArea = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayoutInsideScrollArea.setObjectName("verticalLayoutInsideScrollArea")

        # Create multiple widgets
        count = self.read_agent_count()
        self.createWidgets(self.scrollAreaWidgetContents, count)

        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def createWidgets(self, parentWidget, count):
        #######
        for i in reversed(range(self.verticalLayoutInsideScrollArea.count())):
            widget_to_remove = self.verticalLayoutInsideScrollArea.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)
        #########

        for i in range(count):
            widget = QtWidgets.QWidget(parentWidget)
            widget.setEnabled(True)
            widget.setMinimumSize(QtCore.QSize(891, 101))  # Ensure each widget keeps its size
            widget.setObjectName(f"widget_{i}")

            backgroundLabel = RoundedLabel(widget)
            backgroundLabel.setGeometry(0, 0, 891, 101)
            backgroundLabel.setPixmap(QtGui.QPixmap('img.jpg'))

            comboBox = QtWidgets.QComboBox(widget)
            comboBox.setGeometry(QtCore.QRect(160, 30, 271, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            comboBox.setFont(font)
            comboBox.setStyleSheet("background-color:white")
            comboBox.setObjectName(f"comboBox_{i}")
            items = ["categoriser", "discussion", "burden", "tuple", "Matt & Toni", "alpha burden"]
            comboBox.addItems(items)
            comboBox.activated.connect(lambda index, line=i: self.apply_function(line))

            label = QtWidgets.QLabel(widget)
            label.setGeometry(QtCore.QRect(10, 30, 121, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            label.setFont(font)
            label.setAutoFillBackground(False)
            label.setStyleSheet("background-color: white")
            label.setFrameShadow(QtWidgets.QFrame.Sunken)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setObjectName(f"label_{i}")
            label.setText(f"agent n° {i + 1}")  # Incrementing by 1 for correct agent numbering

            lineEdit = QtWidgets.QLineEdit(widget)
            lineEdit.setGeometry(QtCore.QRect(460, 31, 391, 31))
            lineEdit.setStyleSheet("background-color:white")
            lineEdit.setObjectName(f"lineEdit_{i}")

            # Add the widget to the vertical layout inside the scroll area
            self.verticalLayoutInsideScrollArea.addWidget(widget)

    def apply_function(self, line):
        # Get the selected function
        comboBox = self.scrollAreaWidgetContents.findChild(QtWidgets.QComboBox, f"comboBox_{line}")
        function_name = comboBox.currentText()
        function_to_apply = self.function_map[function_name]

        # Apply the function and fetch the result
        result = function_to_apply()

        # Display result in the corresponding line edit
        lineEdit = self.scrollAreaWidgetContents.findChild(QtWidgets.QLineEdit, f"lineEdit_{line}")
        lineEdit.setText(str(result))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

class RoundedLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(RoundedLabel, self).__init__(parent)
        self.pixmap = None

    def setPixmap(self, pixmap):
        self.pixmap = pixmap.scaled(self.width(), self.height(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        self.update()  # Update the label to redraw with the new pixmap

    def paintEvent(self, event):
        if self.pixmap:
            painter = QtGui.QPainter(self)
            painter.setRenderHints(QtGui.QPainter.Antialiasing, True)
            path = QtGui.QPainterPath()
            path.addRoundedRect(0, 0, self.width(), self.height(), 15, 15)  # Adjust these values to set the radius
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, self.pixmap)

class AlphaDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AlphaDialog, self).__init__(parent)
        self.setWindowTitle('Alpha Parameter')
        self.setGeometry(400, 200, 300, 100)

        self.layout = QtWidgets.QVBoxLayout()
        
        self.label = QtWidgets.QLabel('Enter the alpha value:')
        self.layout.addWidget(self.label)

        self.alphaEdit = QtWidgets.QDoubleSpinBox()
        self.alphaEdit.setRange(0.0, 1000.0)  # Set the range of acceptable values
        self.alphaEdit.setDecimals(2)  # Set the number of decimal places
        self.layout.addWidget(self.alphaEdit)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    @staticmethod
    def getAlpha(parent=None):
        dialog = AlphaDialog(parent)
        result = dialog.exec_()
        alpha = dialog.alphaEdit.value()
        if result == QtWidgets.QDialog.Accepted:
            return alpha, True
        return None, False


if __name__ == "__main__":
    import sys
    G = load_graph_from_file()
    print(G.edges())
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
