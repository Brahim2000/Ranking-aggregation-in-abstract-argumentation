from PyQt5 import QtCore, QtGui, QtWidgets
import networkx as nx
from Alpha_Burden_based_semantic import alpha_burden_based
from Burden_based_semantic import burden_based
from catergriser_based import categoriser_based_ranking
from discussion_based import discussion_based
from matt_and_toni import mt_ranking
from tuple_based import tuple_based
from scoring_aggregation.borda_count_aggregation import borda_count_aggregation


def load_graph_from_file(filename="graph.gml"):
    G = nx.read_gml(filename)
    print(f"Graph loaded from {filename}")
    return G

def rankings_to_string(rankings):
    """
    Transforms rankings from a list of lists into a ranking string.
    """
    rank_string = ""
    
    for equal_group in rankings:
        if rank_string:
            rank_string += " > "
        rank_string += " , ".join(equal_group)
    
    return rank_string

class Ui_Form(object):
    def __init__(self):
        self.G = load_graph_from_file()
        self.function_map = {
            "categoriser": lambda: categoriser_based_ranking(self.G),
            "discussion": lambda: discussion_based(self.G, 1),
            "burden": lambda: burden_based(self.G, 10),
            "tuple": lambda: tuple_based(self.G),
            "Matt & Toni": lambda: mt_ranking(self.G),
        }
        self.alpha_widgets_values = {}

    def handle_alpha_burden(self, alpha_value):
        if alpha_value == 0:
            return ""
        return alpha_burden_based(self.G, alpha_value)

    def show_error_dialog(self, message):
                error_dialog = QtWidgets.QMessageBox()
                error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
                error_dialog.setText(message)
                error_dialog.setWindowTitle("Error")
                error_dialog.exec_()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(968, 780)
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

        self.verticalLayoutInsideScrollArea = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayoutInsideScrollArea.setObjectName("verticalLayoutInsideScrollArea")

        self.createWidgets(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.aggregateButton = QtWidgets.QPushButton("Aggregate")
        self.aggregateButton.setObjectName("aggregateButton")
        self.aggregateButton.setFixedSize(130, 50)
        self.aggregateButton.setStyleSheet("background-color: green; color: white; font-size: 16px; font-weight: bold;border-radius: 15px;")
        self.aggregateButton.clicked.connect(self.on_aggregate_button_clicked)  # Connect the button click event

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
            widget.setMinimumSize(QtCore.QSize(891, 101))
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
                self.alphaContainer = QtWidgets.QWidget(widget)
                self.alphaContainer.setGeometry(QtCore.QRect(299, 16, 550, 200))
                self.alphaContainer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.alphaContainer.setVisible(False)

                self.alphaScrollArea = QtWidgets.QScrollArea(self.alphaContainer)
                self.alphaScrollArea.setGeometry(QtCore.QRect(0, 0, 550, 200))
                self.alphaScrollArea.setWidgetResizable(True)
                self.alphaScrollArea.setVisible(False)
                self.alphaScrollArea.setStyleSheet("""
                    background-color: transparent;
                    border-radius: 15px;
                """)

                self.alphaScrollAreaWidgetContents = QtWidgets.QWidget()
                self.alphaScrollAreaLayout = QtWidgets.QVBoxLayout(self.alphaScrollAreaWidgetContents)
                self.alphaScrollAreaLayout.setContentsMargins(0, 0, 0, 0)

                self.alphaScrollArea.setWidget(self.alphaScrollAreaWidgetContents)

                spinBox.valueChanged.connect(lambda value, w=widget: self.create_alpha_widgets(value, w))
                self.alpha_spinBox = spinBox

                self.alphaContainer.resizeEvent = self.on_alpha_container_resized

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
            label.setText(function_name)

            self.verticalLayoutInsideScrollArea.addWidget(widget)

            if function_name != "alpha burden":
                spinBox.valueChanged.connect(lambda value, le=lineEdit, fn=self.function_map[function_name]: self.update_line_edit(le, fn(), value))
                result = self.function_map[function_name]()
                if spinBox.value() == 0:
                    lineEdit.clear()
                else:
                    lineEdit.setText(rankings_to_string(result))
#♥##############################################################################################################################################
    def create_alpha_widgets(self, count, parent_widget):
        max_height = 200
        widget_height = 45
        total_height = count * widget_height

        # Store current values
        self.store_alpha_widgets_values()

        for i in reversed(range(self.alphaScrollAreaLayout.count())):
            widget = self.alphaScrollAreaLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        for index in range(count):
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

            doubleSpinBox.valueChanged.connect(lambda value, le=lineEdit: self.update_line_edit_for_alpha(le, value))

            self.alphaScrollAreaLayout.addWidget(alphaWidget)

            # Restore previous values if they exist
            if index in self.alpha_widgets_values:
                doubleSpinBox.setValue(self.alpha_widgets_values[index][0])
                lineEdit.setText(self.alpha_widgets_values[index][1])

        if count > 0:
            self.alphaContainer.setVisible(True)
            self.alphaScrollArea.setVisible(True)
            self.alphaContainer.setFixedHeight(min(total_height + 45, max_height))
            self.alphaScrollAreaWidgetContents.setFixedHeight(total_height + 45)
            self.alphaScrollArea.setFixedHeight(min(total_height + 45, max_height))
            parent_widget.adjustSize()
            self.widget_5.setFixedHeight(self.alphaContainer.height() + 30)
        else:
            self.alphaContainer.setVisible(False)
            self.alphaScrollArea.setVisible(False)
            self.widget_5.setFixedHeight(101)

    def store_alpha_widgets_values(self):
        self.alpha_widgets_values.clear()
        for index in range(self.alphaScrollAreaLayout.count()):
            widget = self.alphaScrollAreaLayout.itemAt(index).widget()
            if widget is not None:
                doubleSpinBox = widget.findChild(QtWidgets.QDoubleSpinBox)
                lineEdit = widget.findChild(QtWidgets.QLineEdit)
                if doubleSpinBox is not None and lineEdit is not None:
                    self.alpha_widgets_values[index] = (doubleSpinBox.value(), lineEdit.text())
#♥##############################################################################################################################################
    def update_line_edit(self, line_edit, result, spinbox_value):
        if spinbox_value == 0:
            line_edit.clear()
        else:
            line_edit.setText(rankings_to_string(result))

    def update_line_edit_for_alpha(self, line_edit, alpha_value):
        result = self.handle_alpha_burden(alpha_value)
        line_edit.setText(rankings_to_string(result))
#♥##############################################################################################################################################
    def on_alpha_container_resized(self, event):
        new_height = self.alphaContainer.height()
        self.widget_5.setFixedHeight(new_height + 10)
        print(f"widget_5 resized: {self.widget_5.size()}")
        QtWidgets.QWidget.resizeEvent(self.alphaContainer, event)

#♥##############################################################################################################################################
   
   
    def on_aggregate_button_clicked(self):
        rankings = []
        all_spinboxes_zero = True  # Flag to check if all spinboxes have value 0

        for i in range(self.verticalLayoutInsideScrollArea.count()):
            widget = self.verticalLayoutInsideScrollArea.itemAt(i).widget()
            if widget:
                label = widget.findChild(QtWidgets.QLabel, f"label_{i}")
                if label:
                    spinbox = widget.findChild(QtWidgets.QSpinBox, f"spinBox_{i}")
                    if spinbox and spinbox.value() > 0:
                        all_spinboxes_zero = False  # Found a spinbox with a value greater than 0
                        if label.text() == "alpha burden":
                            # Handle alpha burden case
                            for j in range(self.alphaScrollAreaLayout.count()):
                                alpha_widget = self.alphaScrollAreaLayout.itemAt(j).widget()
                                if alpha_widget:
                                    doubleSpinBox = alpha_widget.findChild(QtWidgets.QDoubleSpinBox)
                                    if doubleSpinBox and doubleSpinBox.value() > 0:
                                        result = self.handle_alpha_burden(doubleSpinBox.value())
                                        rankings.extend([result])
                        else:
                            function_name = label.text()
                            result = self.function_map[function_name]()
                            rankings.extend([result] * spinbox.value())
        if all_spinboxes_zero:
            self.show_error_dialog("No rankings to aggregate!.")
        else:
            # Aggregate the rankings
            self.borda_result = borda_count_aggregation(rankings)  # Store the result for later use
            print("the rankings are", rankings)
            print("Result:", self.borda_result)

            self.aggregateButton.setVisible(False)

            separator_label = QtWidgets.QLabel("Aggregation Results")
            separator_label.setFixedHeight(100)
            separator_label.setAlignment(QtCore.Qt.AlignCenter)
            separator_label.setStyleSheet("background-color: green; color: white; font-size: 24px; font-weight: bold;border-radius: 15px;")
            self.verticalLayoutInsideScrollArea.addWidget(separator_label)

            aggregate_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
            aggregate_widget.setObjectName("aggregate_widget")

            backgroundLabel = RoundedLabel(aggregate_widget)
            backgroundLabel.setGeometry(0, 0, 891, 420)
            backgroundLabel.setObjectName("backgroundLabel_aggregate")
            backgroundLabel.setPixmap(QtGui.QPixmap('img2.jpg'))

            aggregate_layout = QtWidgets.QVBoxLayout(aggregate_widget)
            aggregate_layout.setContentsMargins(0, 0, 0, 0)
            Method = ["Score", "Sequential Winner", "Sequential Loser", "Kemeny"]
            for i in range(1, 5):
                method_widget = QtWidgets.QWidget(aggregate_widget)
                method_widget.setMinimumSize(QtCore.QSize(891, 80))
                method_widget.setObjectName(f"method_widget_{i}")
                method_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

                method_label = QtWidgets.QLabel(method_widget)
                method_label.setGeometry(QtCore.QRect(10, 30, 160, 31))
                font = QtGui.QFont()
                font.setPointSize(10)
                method_label.setFont(font)
                method_label.setAutoFillBackground(False)
                method_label.setStyleSheet("""
                    background-color: white;
                    border: 1px solid #2E2E2E;
                    border-radius: 10px;
                """)
                method_label.setFrameShadow(QtWidgets.QFrame.Sunken)
                method_label.setAlignment(QtCore.Qt.AlignCenter)
                method_label.setObjectName(f"method_label_{i}")
                method_label.setText(Method[i-1])

                line_edit = QtWidgets.QLineEdit(method_widget)
                if method_label.text() != "Kemeny":
                    combo_box = QtWidgets.QComboBox(method_widget)
                    combo_box.setGeometry(QtCore.QRect(210, 30, 100, 31))
                    font = QtGui.QFont()
                    font.setPointSize(10)
                    combo_box.setFont(font)
                    combo_box.setStyleSheet("""
                        background-color:white;
                        border: 1px solid #2E2E2E;
                        border-radius: 10px;
                    """)
                    combo_box.setObjectName(f"combo_box_{i}")
                    combo_box.addItems(["Method", "Borda", "Plurality", "Veto"])
                    combo_box.setCurrentIndex(0)  # Set the default selection to "Select Method"
                    combo_box.setItemData(0, QtGui.QColor("gray"), QtCore.Qt.ForegroundRole)  # Set the "Method" item to be gray
                if method_label.text() == "Score":
                    if method_label.text() == "Score":
                        combo_box.currentIndexChanged.connect(lambda index, cb=combo_box, le=line_edit: self.on_score_combobox_changed(cb, le))  # Connect the signal for Score
                    line_edit.setGeometry(QtCore.QRect(400, 31, 391, 31))
                else:
                    line_edit.setGeometry(QtCore.QRect(400, 31, 391, 31))

                line_edit.setStyleSheet("""
                    background-color:white;
                    border: 1px solid #2E2E2E;
                    border-radius: 10px;
                """)
                line_edit.setObjectName(f"line_edit_{i}")

                aggregate_layout.addWidget(method_widget)

            self.verticalLayoutInsideScrollArea.addWidget(aggregate_widget)
            self.scrollAreaWidgetContents.adjustSize()
            QtCore.QTimer.singleShot(0, lambda: self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum()))

    def on_score_combobox_changed(self, combobox, line_edit):
        method_widget = combobox.parentWidget()
        method_label = method_widget.findChild(QtWidgets.QLabel, method_widget.objectName().replace("method_widget", "method_label"))

        if method_label.text() == "Score" and combobox.currentText() == "Borda":
            line_edit.setText(rankings_to_string(self.borda_result))  # Set the result to the line edit


#♥##############################################################################################################################################

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
            path.addRoundedRect(0, 0, self.width(), self.height(), 15, 15)
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
