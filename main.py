import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QPushButton, QLabel, \
    QTreeWidget, QTreeWidgetItem, QDialog, QFormLayout, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QFont

class ApplicantForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.name_edit = QLineEdit(self)
        self.contact_info_edit = QLineEdit(self)
        self.exam_results_edit = QLineEdit(self)
        self.total_score_edit = QLineEdit(self)

        layout = QFormLayout(self)
        layout.addRow("Имя:", self.name_edit)
        layout.addRow("Контактная информация:", self.contact_info_edit)
        layout.addRow("Результаты экзаменов (через запятую):", self.exam_results_edit)
        layout.addRow("Баллы:", self.total_score_edit)

        self.submit_button = QPushButton("Добавить", self)
        self.submit_button.clicked.connect(self.accept)

        layout.addRow(self.submit_button)

class Applicant:
    def __init__(self, name, contact_info, exam_results, total_score):
        self.name = name
        self.contact_info = contact_info
        self.exam_results = exam_results
        self.total_score = total_score

class Dormitory:
    def __init__(self, room_count, amenities, location):
        self.room_count = room_count
        self.amenities = amenities
        self.location = location

class ApplicationSystem:
    def __init__(self):
        self.applicants = []
        self.dormitory = Dormitory(room_count=100, amenities="Wi-Fi, Laundry", location="Central Campus")

    def add_applicant(self, applicant):
        self.applicants.append(applicant)

    def calculate_total_score(self, applicant):
        total_score = sum(applicant.exam_results)
        return total_score

    def update_total_scores(self):
        for applicant in self.applicants:
            applicant.total_score = self.calculate_total_score(applicant)

class ApplicationGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.application_system = ApplicationSystem()

        # Create and set up tabs
        self.tabs = QTabWidget(self)
        self.applicant_tab = QWidget()
        self.dormitory_tab = QWidget()
        self.tabs.addTab(self.applicant_tab, "Абитуриенты")
        self.tabs.addTab(self.dormitory_tab, "Общежитие")
        self.setCentralWidget(self.tabs)

        # Set tab styles
        self.tabs.setStyleSheet("""
            QTabBar::tab:selected {
                background-color: #4CAF50; /* Green */
            }
        """)

        # Applicant tab
        self.applicant_tree = QTreeWidget(self.applicant_tab)
        self.applicant_tree.setColumnCount(4)  # Increased column count for total score
        self.applicant_tree.setHeaderLabels(["ID", "Имя", "Результаты экзаменов", "Баллы"])

        # Apply styles to the tree widget
        self.applicant_tree.setStyleSheet("""
            QTreeWidget {
                border-radius: 10px; /* Rounded corners */
            }
        """)

        self.applicant_tab_layout = QVBoxLayout(self.applicant_tab)
        self.applicant_tab_layout.addWidget(self.applicant_tree)

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()

        self.add_applicant_button = QPushButton("Добавить абитуриента", self.applicant_tab)
        self.add_applicant_button.clicked.connect(self.show_applicant_form)
        button_layout.addWidget(self.add_applicant_button)

        self.update_scores_button = QPushButton("Обновить баллы", self.applicant_tab)
        self.update_scores_button.clicked.connect(self.update_scores)
        button_layout.addWidget(self.update_scores_button)

        # Add the button layout to the main layout
        self.applicant_tab_layout.addLayout(button_layout)

        # Dormitory tab
        self.room_count_label = QLabel(f"Количество комнат: {self.application_system.dormitory.room_count}", self.dormitory_tab)
        self.amenities_label = QLabel(f"Удобства: {self.application_system.dormitory.amenities}", self.dormitory_tab)
        self.location_label = QLabel(f"Расположение: {self.application_system.dormitory.location}", self.dormitory_tab)

        self.dormitory_tab_layout = QVBoxLayout(self.dormitory_tab)
        self.dormitory_tab_layout.addWidget(self.room_count_label)
        self.dormitory_tab_layout.addWidget(self.amenities_label)
        self.dormitory_tab_layout.addWidget(self.location_label)

        self.update_applicant_tree()

        # Apply styles to the buttons
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 20px 40px; /* Increased padding for larger buttons */
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 24px; /* Increased font size for larger text */
                margin: 10px 5px; /* Increased margin */
                cursor: pointer;
                border-radius: 20px; /* Increased border radius for rounded corners */
            }
        """)

        # Increase font size for labels
        font = QFont()
        font.setPointSize(18)
        self.room_count_label.setFont(font)
        self.amenities_label.setFont(font)
        self.location_label.setFont(font)

    def show_applicant_form(self):
        form = ApplicantForm(self)
        result = form.exec_()

        if result == QDialog.Accepted:
            name = form.name_edit.text()
            contact_info = form.contact_info_edit.text()
            exam_results_str = form.exam_results_edit.text()
            total_score_str = form.total_score_edit.text()

            # Convert the comma-separated string to a list of integers
            exam_results = [int(score.strip()) for score in exam_results_str.split(',')]
            total_score = int(total_score_str)

            new_applicant = Applicant(name=name, contact_info=contact_info, exam_results=exam_results, total_score=total_score)
            self.application_system.add_applicant(new_applicant)
            self.update_applicant_tree()

        form.deleteLater()  # Ensure the form is deleted to prevent memory leaks

    def update_scores(self):
        self.application_system.update_total_scores()
        self.update_applicant_tree()

    def update_applicant_tree(self):
        self.applicant_tree.clear()

        for i, applicant in enumerate(self.application_system.applicants, start=1):
            item = QTreeWidgetItem(self.applicant_tree, [str(i), applicant.name, str(applicant.exam_results), str(applicant.total_score)])
            self.applicant_tree.addTopLevelItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationGUI()
    window.resize(1200, 800)  # Установите размер приложения на ваш выбор
    window.show()
    sys.exit(app.exec_())
