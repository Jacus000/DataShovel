from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableView, QLabel,
                             QPushButton, QComboBox, QLineEdit, QMenu)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction

from app.models.pandas_model import PandasModel


class DataTab(QWidget):
    column_dropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.original_data = None
        self.visible_columns = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Toolbar Layout
        self.toolbar_layout = QHBoxLayout()
        
        # Columns Visibility Menu
        self.visibility_btn = QPushButton("Columns Visibility")
        self.visibility_menu = QMenu()
        self.visibility_btn.setMenu(self.visibility_menu)
        self.toolbar_layout.addWidget(self.visibility_btn)
        
        # Search Tool
        self.toolbar_layout.addWidget(QLabel(" Search: "))
        self.search_col_combo = QComboBox()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search value...")
        self.search_input.textChanged.connect(self.on_search_triggered)
        self.toolbar_layout.addWidget(self.search_col_combo)
        self.toolbar_layout.addWidget(self.search_input)
        
        self.toolbar_layout.addStretch()
        
        # Drop Column Tool
        self.drop_col_combo = QComboBox()
        self.drop_btn = QPushButton("Drop Column")
        self.drop_btn.setStyleSheet("color: red; font-weight: bold;")
        self.drop_btn.clicked.connect(self.on_drop_clicked)
        self.toolbar_layout.addWidget(self.drop_col_combo)
        self.toolbar_layout.addWidget(self.drop_btn)
        
        self.toolbar_widget = QWidget()
        self.toolbar_widget.setLayout(self.toolbar_layout)
        self.toolbar_widget.hide()
        
        layout.addWidget(self.toolbar_widget)

        self.data_table = QTableView()
        self.data_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectItems)
        self.data_table.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        self.data_table.setAlternatingRowColors(True)
        self.data_table.hide()

        self.no_data_label = QLabel("No imported data set")
        self.no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.data_table)
        layout.addWidget(self.no_data_label)

    def update_data(self, data):
        """Update the data displayed in the table"""
        if data is not None:
            self.original_data = data
            self.no_data_label.hide()
            self.data_table.show()
            self.toolbar_widget.show()

            model = PandasModel(data)
            self.data_table.setModel(model)
            self.data_table.resizeColumnsToContents()
            
            self.populate_toolbar(data)
            self.on_search_triggered()
        else:
            self.no_data_label.show()
            self.data_table.hide()
            self.toolbar_widget.hide()
            
    def populate_toolbar(self, data):
        # Populate visibility menu
        self.visibility_menu.clear()
        self.visible_columns = list(data.columns)
        for col in data.columns:
            action = QAction(col, self)
            action.setCheckable(True)
            action.setChecked(True)
            action.triggered.connect(lambda checked, c=col: self.on_visibility_action(c, checked))
            self.visibility_menu.addAction(action)
            
        # Populate Search combobox
        self.search_col_combo.blockSignals(True)
        self.search_col_combo.clear()
        self.search_col_combo.addItems(data.columns)
        self.search_col_combo.blockSignals(False)
        
        # Populate Drop combobox
        self.drop_col_combo.clear()
        self.drop_col_combo.addItems(data.columns)

    def on_visibility_action(self, col, checked):
        if checked and col not in self.visible_columns:
            self.visible_columns.append(col)
        elif not checked and col in self.visible_columns:
            self.visible_columns.remove(col)
        self.refresh_visibility()
        
    def refresh_visibility(self):
        self.set_column_visibility(self.visible_columns)

    def on_search_triggered(self):
        if self.original_data is None:
            return
            
        search_text = self.search_input.text()
        search_col = self.search_col_combo.currentText()
        
        if not search_text or not search_col:
            model = PandasModel(self.original_data)
        else:
            try:
                mask = self.original_data[search_col].astype(str).str.contains(search_text, case=False, na=False)
                filtered_df = self.original_data[mask]
                model = PandasModel(filtered_df)
            except Exception:
                model = PandasModel(self.original_data)
                
        self.data_table.setModel(model)
        self.refresh_visibility()
        
    def on_drop_clicked(self):
        col = self.drop_col_combo.currentText()
        if col:
            self.column_dropped.emit(col)

    def set_column_visibility(self, visible_columns):
        """Show or hide columns based on the provided list of visible columns"""
        model = self.data_table.model()
        if not model:
            return
            
        for i in range(model.columnCount()):
            col_name = model.headerData(i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
            if str(col_name) in visible_columns:
                self.data_table.showColumn(i)
            else:
                self.data_table.hideColumn(i)