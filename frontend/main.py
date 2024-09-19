import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QListWidget, QStackedWidget, QListWidgetItem, \
    QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QSize

# Direct imports since all files are in the same directory
from userLogins import UserManagement
from dashboard import Dashboard
from configuration import AuditConfiguration
from executionControl import ExecutionControl
from result import ResultsDisplay
from issues import IssueManagement

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up splitter for left and right window areas
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(self.splitter)

        # Create list widget for tab navigation (left window)
        self.tab_list = QListWidget()
        self.tab_list.setIconSize(QSize(48, 48))
        self.is_minimized = False  # State to track if the tab list is minimized or not
        self.expanded_width = 250
        self.minimized_width = 60

        # Dictionary to store original tab names
        self.tab_names = {}

        # Add tabs with icons
        self.add_tab("Profile", "../icons/profile.png", 0)
        self.add_tab("Dashboard", "../icons/dashboard.png", 1)
        self.add_tab("Audit Configuration", "../icons/configuration.png", 2)
        self.add_tab("Execution Control", "../icons/execution.png", 3)
        self.add_tab("Results Display", "../icons/results.png", 4)
        self.add_tab("Issue Management", "../icons/issues.png", 5)

        self.tab_list.setFixedWidth(self.expanded_width)

        # Create stacked widget to display the selected tab's content (right window)
        self.tab_content = QStackedWidget()

        # Add the list and the tab content area to the splitter
        self.splitter.addWidget(self.tab_list)
        self.splitter.addWidget(self.tab_content)

        # Control the stretch factor to make the right side expand more
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)

        # Create the tabs and add them to the stacked widget
        self.user_management_tab = UserManagement()
        self.tab_content.addWidget(self.user_management_tab)

        self.dashboard_tab = Dashboard()
        self.tab_content.addWidget(self.dashboard_tab)

        self.audit_config_tab = AuditConfiguration()
        self.tab_content.addWidget(self.audit_config_tab)

        self.execution_control_tab = ExecutionControl()
        self.tab_content.addWidget(self.execution_control_tab)

        self.results_display_tab = ResultsDisplay()
        self.tab_content.addWidget(self.results_display_tab)

        self.issue_management_tab = IssueManagement()
        self.tab_content.addWidget(self.issue_management_tab)

        # Disable all tabs except User Management by default
        self.enable_tabs(False)

        # Connect user management login signal
        self.user_management_tab.user_logged_in.connect(self.on_user_logged_in)

        # Connect the list widget to change the tab content when clicked
        self.tab_list.currentRowChanged.connect(self.switch_tab)

        # Set default selection to the User Management tab
        self.tab_list.setCurrentRow(0)

        # Add a toggle button to minimize/expand the tab list
        self.minimize_button = QPushButton(self)
        self.minimize_button.setFixedWidth(150)
        self.minimize_button.clicked.connect(self.toggle_minimize_tabs)

        # Set initial icon (right arrow for expand)
        self.minimize_button.setIcon(QIcon("../icons/Left_arrow.png"))
        self.minimize_button.setIconSize(QSize(24, 24))

        # Add dark mode toggle button
        self.toggle_button = QPushButton("Toggle Theme", self)
        self.toggle_button.setFixedWidth(150)
        self.toggle_button.clicked.connect(self.toggle_dark_mode)

        # Add toggle buttons to the layout
        self.layout = QVBoxLayout()
        # Create a horizontal layout to place toggle and minimize buttons side by side
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.toggle_button)  # Add dark mode button
        self.button_layout.addWidget(self.minimize_button)  # Add minimize button
        # Add the horizontal button layout to the main vertical layout
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.splitter)  # Add the splitter below the buttons
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.is_dark_mode = False

    def add_tab(self, name, icon_path, index):
        """Add a tab with an icon and name to the QListWidget"""
        item = QListWidgetItem(QIcon(icon_path), name)
        item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.tab_list.addItem(item)

        # Store the original tab names
        self.tab_names[index] = name

    def enable_tabs(self, enable):
        """Enable or disable all tabs except User Management (index 0)"""
        for i in range(1, self.tab_list.count()):
            item = self.tab_list.item(i)
            if enable:
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEnabled)
            else:
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)

    def on_user_logged_in(self):
        """Enable other tabs when a user is logged in"""
        self.enable_tabs(True)

    def switch_tab(self, index):
        """Switch to the corresponding tab content based on the index"""
        self.tab_content.setCurrentIndex(index)

    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        if self.is_dark_mode:
            self.set_light_mode()
        else:
            self.set_dark_mode()
        self.is_dark_mode = not self.is_dark_mode

    def set_light_mode(self):
        """Set the light mode stylesheet"""
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
            }
            QListWidget {
                font-size: 20px;
                color: black;
            }
            QListWidget::item:selected {
                background-color: lightgray;
                color: black;
            }
        """)

    def set_dark_mode(self):
        """Set the dark mode stylesheet"""
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
            }
            QListWidget {
                font-size: 20px;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #505050;
                color: white;
            }
        """)

    def toggle_minimize_tabs(self):
        """Minimize or expand the tab list to show only icons or both icons and names"""
        if self.is_minimized:
            # Restore the tab names when expanded
            self.tab_list.setFixedWidth(self.expanded_width)
            for i in range(self.tab_list.count()):
                self.tab_list.item(i).setText(self.tab_names[i])  # Restore text
            self.minimize_button.setIcon(QIcon("../icons/Left_arrow.png"))  # Set expand icon
        else:
            # Minimize the tab list and remove tab names
            self.tab_list.setFixedWidth(self.minimized_width)
            for i in range(self.tab_list.count()):
                self.tab_list.item(i).setText("")  # Hide text
            self.minimize_button.setIcon(QIcon("../icons/Right_arrow.png"))  # Set minimize icon

        self.minimize_button.setIconSize(QSize(24, 24))
        self.is_minimized = not self.is_minimized


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Ageis Audit")

    logo_path = os.path.abspath("../icons/logo.png")
    if os.path.exists(logo_path):
        app.setWindowIcon(QIcon(logo_path))
    else:
        print(f"Logo file not found at {logo_path}")


    app_font = QFont("Palatino Linotype", 12)
    app.setFont(app_font)

    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
