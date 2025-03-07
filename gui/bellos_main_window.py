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

class BellosMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.script_manager = ScriptManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Bellos Application Script Manager')
        self.setGeometry(100, 100, 1200, 800)

        # Create central widget with tab support
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        # Create main editor tab
        self.editor = ScriptEditor()
        self.central_widget.addTab(self.editor, "Script Editor")

        # Create and configure dock widgets
        self.setup_file_explorer()
        self.setup_terminal()
        self.setup_menubar()
        
        # Project settings tab
        self.project_settings = ProjectSettings()
        self.central_widget.addTab(self.project_settings, "Project Settings")

    def setup_file_explorer(self):
        self.file_explorer = FileExplorer()
        file_dock = QDockWidget("File Explorer", self)
        file_dock.setWidget(self.file_explorer)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, file_dock)
        
        # Connect file explorer signals
        self.file_explorer.file_selected.connect(self.open_file)

    def setup_terminal(self):
        self.terminal = Terminal()
        terminal_dock = QDockWidget("Terminal", self)
        terminal_dock.setWidget(self.terminal)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, terminal_dock)

    def setup_menubar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        # Add edit actions (undo, redo, cut, copy, paste)
        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)

        # Run menu
        run_menu = menubar.addMenu("Run")
        
        run_action = QAction("Run Script", self)
        run_action.triggered.connect(self.run_script)
        run_menu.addAction(run_action)

    def new_file(self):
        self.editor.clear()
        self.current_file = None

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Bellos Scripts (*.bellos);;All Files (*)")
        if file_name:
            self.open_file(file_name)

    def open_file(self, file_name):
        try:
            with open(file_name, 'r') as f:
                self.editor.setPlainText(f.read())
            self.current_file = file_name
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")

    def save_file(self):
        if not hasattr(self, 'current_file') or not self.current_file:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Bellos Scripts (*.bellos);;All Files (*)")
            if file_name:
                self.current_file = file_name
            else:
                return

        try:
            with open(self.current_file, 'w') as f:
                f.write(self.editor.toPlainText())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")

    def run_script(self):
        script_content = self.editor.toPlainText()
        try:
            output = self.script_manager.run_script(script_content)
            self.terminal.append_output(output)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error running script: {str(e)}")
            self.terminal.append_output(f"Error: {str(e)}")
