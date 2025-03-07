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

class Terminal(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # Set read-only mode
        self.setReadOnly(True)

        # Set monospace font
        font = QFont("Courier New", 10)
        self.setFont(font)

        # Set background and text colors
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: none;
            }
        """)

    def append_output(self, text):
        self.moveCursor(QTextCursor.MoveOperation.End)
        self.insertPlainText(text + '\n')
        self.moveCursor(QTextCursor.MoveOperation.End)

    def clear_output(self):
        self.clear()
