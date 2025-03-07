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

#!/usr/bin/env python3

import sys

from PyQt6.QtWidgets import QApplication
from gui.bellos_main_window import BellosMainWindow

def main():
    app = QApplication(sys.argv)
    window = BellosMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
