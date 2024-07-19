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
from scoring_aggregation.veto_aggregation import minimax_method, veto_aggregation, aggregate_rankings
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
        }

    # Méthode pour gérer le cas alpha burden
    def handle_alpha_burden(self, alpha_value):
        if alpha_value == 0:
            return ""
        return alpha_burden_based(self.G, alpha_value)

    #*****************************************************************************************
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(968, 593)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setStyleSheet("""
        QScrollArea {
            border: 2px solid #2E2E2E; 
            border-radius: 5px; 
        }
    """)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 920, 569))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Utiliser QVBoxLayout à l'intérieur de la zone de défilement pour un ajustement dynamique
        self.verticalLayoutInsideScrollArea = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayoutInsideScrollArea.setObjectName("verticalLayoutInsideScrollArea")

        # Créer 6 widgets
        self.createWidgets(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # Ajouter le bouton "Aggregate" en bas
        self.aggregateButton = QtWidgets.QPushButton("Aggregate")
        self.aggregateButton.setObjectName("aggregateButton")
        self.aggregateButton.setFixedSize(130, 50)  # Définir une taille fixe pour le bouton
        self.aggregateButton.setStyleSheet("background-color: green; color: white; font-size: 16px; font-weight: bold;border-radius: 15px;")

        # Créer une mise en page horizontale pour centrer le bouton
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.addStretch()
        self.horizontalLayout.addWidget(self.aggregateButton)
        self.horizontalLayout.addStretch()

        self.verticalLayout.addLayout(self.horizontalLayout)

    def createWidgets(self, parentWidget):
        function_names = ["categoriser", "discussion", "burden", "tuple", "Matt & Toni", "alpha burden"]

        for i, function_name in enumerate(function_names):
            widget = QtWidgets.QWidget(parentWidget)
            widget.setEnabled(True)
            widget.setMinimumSize(QtCore.QSize(891, 101))  # S'assurer que chaque widget garde sa taille
            widget.setObjectName(f"widget_{i}")
            widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

            backgroundLabel = RoundedLabel(widget)
            if function_name == "alpha burden":
                backgroundLabel.setGeometry(0, 0, 891, 230)
            else:
                backgroundLabel.setGeometry(0, 0, 891, 101)
            backgroundLabel.setObjectName(f"backgroundLabel_{i}")
            backgroundLabel.setPixmap(QtGui.QPixmap('img.jpg'))

            spinBox = QtWidgets.QSpinBox(widget)
            spinBox.setGeometry(QtCore.QRect(160, 30, 100, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            spinBox.setFont(font)
            spinBox.setStyleSheet("""
                background-color:white;
                border: 1px solid #2E2E2E;
                border-radius: 10px;
            """)
            spinBox.setObjectName(f"spinBox_{i}")
            spinBox.setMinimum(0)
            spinBox.setMaximum(100)

            if function_name == "alpha burden":
                # Container widget to hold multiple alphaWidgets
                self.alphaContainer = QtWidgets.QWidget(widget)
                self.alphaContainer.setGeometry(QtCore.QRect(299, 16, 550, 200))  # Adjust initial height
                self.alphaContainer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.alphaContainer.setVisible(False)  # Initially hide the alphaContainer
                
                # Create a scroll area inside the alphaContainer
                self.alphaScrollArea = QtWidgets.QScrollArea(self.alphaContainer)
                self.alphaScrollArea.setGeometry(QtCore.QRect(0, 0, 550, 200))  # Adjust initial height
                self.alphaScrollArea.setWidgetResizable(True)
                self.alphaScrollArea.setVisible(False)  # Initially hide the alphaScrollArea
                self.alphaScrollArea.setStyleSheet("""
                                                        background-color: transparent;
                                                        border-radius: 15px;
                                                    
                                                """)
                # Create a widget and layout for the scroll area
                self.alphaScrollAreaWidgetContents = QtWidgets.QWidget()
                self.alphaScrollAreaLayout = QtWidgets.QVBoxLayout(self.alphaScrollAreaWidgetContents)
                self.alphaScrollAreaLayout.setContentsMargins(0, 0, 0, 0)

                self.alphaScrollArea.setWidget(self.alphaScrollAreaWidgetContents)

                spinBox.valueChanged.connect(lambda value, w=widget: self.create_alpha_widgets(value, w))
                self.alpha_spinBox = spinBox

                # Connect the resize event of alphaContainer to the custom slot
                self.alphaContainer.resizeEvent = self.on_alpha_container_resized

                # Store widget_5 reference to update its size later
                self.widget_5 = widget
            else:
                lineEdit = QtWidgets.QLineEdit(widget)
                lineEdit.setGeometry(QtCore.QRect(460, 31, 391, 31))
                lineEdit.setStyleSheet("""
                    background-color:white;
                    border: 1px solid #2E2E2E;
                    border-radius: 10px;
                """)
                lineEdit.setObjectName(f"lineEdit_{i}")

            label = QtWidgets.QLabel(widget)
            label.setGeometry(QtCore.QRect(10, 30, 121, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            label.setFont(font)
            label.setAutoFillBackground(False)
            label.setStyleSheet("""
                background-color: white;
                border: 1px solid #2E2E2E;
                border-radius: 10px;
            """)
            label.setFrameShadow(QtWidgets.QFrame.Sunken)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setObjectName(f"label_{i}")
            label.setText(function_name)  # Set function name as label text

            # Add the widget to the vertical layout inside the scroll area
            self.verticalLayoutInsideScrollArea.addWidget(widget)

            # Apply the function and display the result
            if function_name != "alpha burden":
                spinBox.valueChanged.connect(lambda value, le=lineEdit, fn=self.function_map[function_name]: self.update_line_edit(le, fn(), value))
                result = self.function_map[function_name]()
                if spinBox.value() == 0:
                    lineEdit.clear()
                else:
                    lineEdit.setText(str(result))

    def create_alpha_widgets(self, count, parent_widget):
        max_height = 200  # Maximum height for alphaScrollArea
        widget_height = 45  # Height of each alpha widget
        total_height = count * widget_height

        # Clear existing widgets
        for i in reversed(range(self.alphaScrollAreaLayout.count())):
            widget = self.alphaScrollAreaLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        for _ in range(count):
            alphaWidget = QtWidgets.QWidget(self.alphaScrollAreaWidgetContents)
            alphaWidget.setFixedSize(520, widget_height)
            alphaWidgetLayout = QtWidgets.QHBoxLayout(alphaWidget)
            alphaWidgetLayout.setContentsMargins(0, 0, 0, 0)

            font = QtGui.QFont()
            font.setPointSize(10)


            doubleSpinBox = QtWidgets.QDoubleSpinBox(alphaWidget)
            doubleSpinBox.setFont(font)
            doubleSpinBox.setStyleSheet("""
                background-color:white;
                border: 1px solid #2E2E2E;
                border-radius: 10px;
            """)
            doubleSpinBox.setMinimum(0.01)
            doubleSpinBox.setMaximum(1000.0)
            doubleSpinBox.setFixedSize(100, 31)
            doubleSpinBox.setDecimals(2)
            alphaWidgetLayout.addWidget(doubleSpinBox)

            lineEdit = QtWidgets.QLineEdit(alphaWidget)
            lineEdit.setStyleSheet("""
                background-color:white;
                border: 1px solid #2E2E2E;
                border-radius: 10px;
            """)
            lineEdit.setFixedSize(391, 31)
            alphaWidgetLayout.addWidget(lineEdit)

            self.alphaScrollAreaLayout.addWidget(alphaWidget)

        # Update visibility and geometry of alphaContainer and parent widget
        if count > 0:
            self.alphaContainer.setVisible(True)
            self.alphaScrollArea.setVisible(True)
            self.alphaContainer.setFixedHeight(min(total_height + 45, max_height))
            self.alphaScrollAreaWidgetContents.setFixedHeight(total_height + 45)
            self.alphaScrollArea.setFixedHeight(min(total_height+ 45, max_height))
            parent_widget.adjustSize()
            self.widget_5.setFixedHeight(self.alphaContainer.height() + 30)  # Adjust widget_5's height
        else:
            self.alphaContainer.setVisible(False)
            self.alphaScrollArea.setVisible(False)
            self.widget_5.setFixedHeight(101)  # Reset to initial height if no widgets

    def update_line_edit(self, line_edit, result, spinbox_value):
        if spinbox_value == 0:
            line_edit.clear()
        else:
            line_edit.setText(str(result))

    def update_line_edit_for_alpha(self, line_edit, double_spinbox_value, spinbox_value):
        if spinbox_value == 0:
            line_edit.clear()
        else:
            result = self.handle_alpha_burden(double_spinbox_value)
            line_edit.setText(str(result))

    def on_alpha_container_resized(self, event):
        new_height = self.alphaContainer.height()
        self.widget_5.setFixedHeight(new_height + 10 )  # Adjust widget_5's height
        # Print the size of widget_5 after resizing
        print(f"widget_5 resized: {self.widget_5.size()}")
        QtWidgets.QWidget.resizeEvent(self.alphaContainer, event)  # Ensure the event is still processed

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Semantics rankings"))

class RoundedLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(RoundedLabel, self).__init__(parent)
        self.pixmap = None

    def setPixmap(self, pixmap):
        self.pixmap_original = pixmap
        self.update_pixmap()

    def resizeEvent(self, event):
        self.update_pixmap()
        super(RoundedLabel, self).resizeEvent(event)

    def update_pixmap(self):
        if self.pixmap_original:
            self.pixmap = self.pixmap_original.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            self.update()

    def paintEvent(self, event):
        if self.pixmap:
            painter = QtGui.QPainter(self)
            painter.setRenderHints(QtGui.QPainter.Antialiasing, True)
            path = QtGui.QPainterPath()
            path.addRoundedRect(0, 0, self.width(), self.height(), 15, 15)  # Ajuster ces valeurs pour définir le rayon
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, self.pixmap)

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
