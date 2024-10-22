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

import os
from PyQt6.QtWidgets import QTreeView, QAbstractItemView
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from typing import Optional

class FileExplorer(QTreeView):
    file_selected = pyqtSignal(str)
    _model: Optional[QStandardItemModel]

    def __init__(self):
        super().__init__()
        self._model = None
        self.current_path = ""
        self.setup_ui()

    def setup_ui(self):
        # Create and set up the model
        self._model = QStandardItemModel(parent=self)
        self._model.setHorizontalHeaderLabels(['Name'])
        
        # Set up the tree view
        super().setModel(self._model)
        self.setAnimated(False)
        self.setIndentation(20)
        self.setSortingEnabled(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        
        # Connect signals
        self.clicked.connect(self.on_item_clicked)

    def populate_tree(self, path: str, parent_item: Optional[QStandardItem] = None) -> None:
        if parent_item is None and self._model is not None:
            self._model.clear()
            self._model.setHorizontalHeaderLabels(['Name'])
            parent_item = self._model.invisibleRootItem()
            
        try:
            # List directory contents
            items = os.listdir(path)
            
            # Sort items: directories first, then files
            dirs = sorted([item for item in items if os.path.isdir(os.path.join(path, item))])
            files = sorted([item for item in items if os.path.isfile(os.path.join(path, item))])
            
            # Add directories
            for dir_name in dirs:
                dir_path = os.path.join(path, dir_name)
                try:
                    item = QStandardItem(dir_name)
                    item.setData(dir_path, Qt.ItemDataRole.UserRole)
                    if parent_item:
                        parent_item.appendRow(item)
                except Exception:
                    continue
            
            # Add files
            for file_name in files:
                file_path = os.path.join(path, file_name)
                try:
                    item = QStandardItem(file_name)
                    item.setData(file_path, Qt.ItemDataRole.UserRole)
                    if parent_item:
                        parent_item.appendRow(item)
                except Exception:
                    continue
                    
        except PermissionError:
            pass
        except Exception:
            pass

    def on_item_clicked(self, index):
        if self._model is None:
            return
            
        item = self._model.itemFromIndex(index)
        if item:
            path = item.data(Qt.ItemDataRole.UserRole)
            if os.path.isdir(path):
                if self.isExpanded(index):
                    self.collapse(index)
                else:
                    item.removeRows(0, item.rowCount())
                    self.populate_tree(path, item)
                    self.expand(index)
            else:
                self.file_selected.emit(path)

    def set_root_path(self, path: str) -> None:
        if os.path.exists(path):
            self.current_path = path
            self.populate_tree(path)

    def refresh(self) -> None:
        if self.current_path:
            self.populate_tree(self.current_path)
