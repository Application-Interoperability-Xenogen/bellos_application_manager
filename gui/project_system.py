# Copyright (C) 2024 Bellande Application Interoperability Xenogen Research Innovation Center, Ronaldson Bellande

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from header_imports import *

class ProjectSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.settings_file = "bellos_settings.bellande"
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Project name
        self.project_name = QLineEdit()
        form_layout.addRow("Project Name:", self.project_name)

        # Project path
        self.project_path = QLineEdit()
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_path)
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.project_path)
        path_layout.addWidget(self.browse_button)
        form_layout.addRow("Project Path:", path_layout)

        # Default shell
        self.default_shell = QComboBox()
        self.default_shell.addItems(["bellos", "bash", "sh", "zsh"])
        form_layout.addRow("Default Shell:", self.default_shell)

        # Tab width
        self.tab_width = QSpinBox()
        self.tab_width.setRange(2, 8)
        self.tab_width.setValue(4)
        form_layout.addRow("Tab Width:", self.tab_width)

        # Editor settings
        self.auto_save = QCheckBox()
        form_layout.addRow("Auto Save:", self.auto_save)

        self.auto_indent = QCheckBox()
        self.auto_indent.setChecked(True)
        form_layout.addRow("Auto Indent:", self.auto_indent)

        self.show_line_numbers = QCheckBox()
        self.show_line_numbers.setChecked(True)
        form_layout.addRow("Show Line Numbers:", self.show_line_numbers)

        # Terminal settings
        self.terminal_font_size = QSpinBox()
        self.terminal_font_size.setRange(8, 24)
        self.terminal_font_size.setValue(10)
        form_layout.addRow("Terminal Font Size:", self.terminal_font_size)

        self.terminal_history_size = QSpinBox()
        self.terminal_history_size.setRange(100, 10000)
        self.terminal_history_size.setValue(1000)
        form_layout.addRow("Terminal History Size:", self.terminal_history_size)

        # Bellos script settings
        self.script_extension = QLineEdit(".bellos")
        form_layout.addRow("Script Extension:", self.script_extension)

        self.default_timeout = QSpinBox()
        self.default_timeout.setRange(0, 3600)
        self.default_timeout.setValue(30)
        form_layout.addRow("Default Script Timeout (seconds):", self.default_timeout)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        reset_button = QPushButton("Reset to Defaults")
        reset_button.clicked.connect(self.reset_settings)
        button_layout.addWidget(save_button)
        button_layout.addWidget(reset_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def browse_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if path:
            self.project_path.setText(path)

    def save_settings(self):
        settings = {
            "project_name": self.project_name.text(),
            "project_path": self.project_path.text(),
            "default_shell": self.default_shell.currentText(),
            "tab_width": self.tab_width.value(),
            "auto_save": self.auto_save.isChecked(),
            "auto_indent": self.auto_indent.isChecked(),
            "show_line_numbers": self.show_line_numbers.isChecked(),
            "terminal_font_size": self.terminal_font_size.value(),
            "terminal_history_size": self.terminal_history_size.value(),
            "script_extension": self.script_extension.text(),
            "default_timeout": self.default_timeout.value()
        }

        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
            QMessageBox.information(self, "Success", "Settings saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save settings: {str(e)}")

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                
                self.project_name.setText(settings.get("project_name", ""))
                self.project_path.setText(settings.get("project_path", ""))
                self.default_shell.setCurrentText(settings.get("default_shell", "bellos"))
                self.tab_width.setValue(settings.get("tab_width", 4))
                self.auto_save.setChecked(settings.get("auto_save", False))
                self.auto_indent.setChecked(settings.get("auto_indent", True))
                self.show_line_numbers.setChecked(settings.get("show_line_numbers", True))
                self.terminal_font_size.setValue(settings.get("terminal_font_size", 10))
                self.terminal_history_size.setValue(settings.get("terminal_history_size", 1000))
                self.script_extension.setText(settings.get("script_extension", ".bellos"))
                self.default_timeout.setValue(settings.get("default_timeout", 30))
            except Exception as e:
                QMessageBox.warning(self, "Warning", f"Could not load settings: {str(e)}")

    def reset_settings(self):
        reply = QMessageBox.question(self, "Confirm Reset", 
                                   "Are you sure you want to reset all settings to default?",
                                   QMessageBox.StandardButton.Yes | 
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.default_shell.setCurrentText("bellos")
            self.tab_width.setValue(4)
            self.auto_save.setChecked(False)
            self.auto_indent.setChecked(True)
            self.show_line_numbers.setChecked(True)
            self.terminal_font_size.setValue(10)
            self.terminal_history_size.setValue(1000)
            self.script_extension.setText(".bellos")
            self.default_timeout.setValue(30)
