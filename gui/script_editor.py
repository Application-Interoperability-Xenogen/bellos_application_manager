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

from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtGui import QTextCharFormat, QSyntaxHighlighter, QColor, QFont

class BellosSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Define formats for different syntax elements
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = ["if", "else", "while", "for", "in", "do", "done", "echo", "export"]
        
        for word in keywords:
            self.highlighting_rules.append((
                f"\\b{word}\\b",
                keyword_format
            ))

        # String format
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))
        self.highlighting_rules.append((
            r'"[^"\\]*(\\.[^"\\]*)*"',
            string_format
        ))

        # Comment format
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#608B4E"))
        self.highlighting_rules.append((
            r"#[^\n]*",
            comment_format
        ))

    def highlightBlock(self, text):
        from PyQt6.QtCore import QRegularExpression
        
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class ScriptEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setup_editor()

    def setup_editor(self):
        # Set font
        font = QFont("Courier New", 10)
        self.setFont(font)

        # Set tab width
        self.setTabStopDistance(40)  # 4 spaces

        # Enable line numbers
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        # Set syntax highlighter
        self.highlighter = BellosSyntaxHighlighter(self.document())

        # Set placeholder text
        self.setPlaceholderText("Enter your Bellos script here...")

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, new_block_count):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
