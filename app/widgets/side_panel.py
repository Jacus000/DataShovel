from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QLabel, QPushButton,
                             QHBoxLayout, QLineEdit, QComboBox, QGroupBox, QWidget, QScrollArea, QListWidget, QListWidgetItem)
from PyQt6.QtCore import pyqtSignal, Qt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class SidePanel(QFrame):
    """Container for FilterWidget, PlotWidget"""
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # Create both panels
        self.filter_widget = FilterWidget()
        self.plot_widget = PlotWidget()
        self.plot_widget.hide()

        self.layout.addWidget(self.filter_widget)
        self.layout.addWidget(self.plot_widget)

    def toggle_panels(self):
        """Switch between filter and plot panels"""
        if self.filter_widget.isVisible():
            self.filter_widget.hide()
            self.plot_widget.show()
        else:
            self.filter_widget.show()
            self.plot_widget.hide()

    def update_data(self, data):
        """Update both panels with new data"""
        self.filter_widget.update_controls(data)
        self.plot_widget.update_controls(data)


class FilterWidget(QFrame):
    filters_applied = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        self.scroll_content = QWidget()
        self.scroll_main_layout = QVBoxLayout(self.scroll_content)
        
        # Filters Group Box
        self.filter_group = QGroupBox("Filter Data")
        self.filter_controls_layout = QVBoxLayout()
        self.filter_group.setLayout(self.filter_controls_layout)
        self.scroll_main_layout.addWidget(self.filter_group)

        self.filter_placeholder = QLabel("Filters will appear here after loading data")
        self.filter_controls_layout.addWidget(self.filter_placeholder)
        
        # Overview Group Box
        self.overview_group = QGroupBox("Column Viewer & Statistics")
        self.overview_layout = QVBoxLayout()
        self.overview_group.setLayout(self.overview_layout)
        self.scroll_main_layout.addWidget(self.overview_group)
        
        # Column Stats UI
        self.overview_layout.addWidget(QLabel("Column Statistics:"))
        self.stats_combo = QComboBox()
        self.stats_combo.currentTextChanged.connect(self.on_stats_column_changed)
        self.overview_layout.addWidget(self.stats_combo)
        
        self.stats_label = QLabel("Select a column to see stats")
        self.stats_label.setWordWrap(True)
        self.stats_label.setStyleSheet("color: gray;")
        self.overview_layout.addWidget(self.stats_label)

        # Add the vertical stretch to push everything up
        self.scroll_main_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        apply_btn = QPushButton("Apply filters")
        apply_btn.clicked.connect(self.on_apply_filters)
        layout.addWidget(apply_btn)

    def update_controls(self, data):
        """Update filter controls based on data"""
        self.filter_placeholder.hide()
        for i in reversed(range(self.filter_controls_layout.count())):
            item = self.filter_controls_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
            else:
                self.filter_controls_layout.removeItem(item)

        self.filter_controls = {}

        if data is None:
            return

        self.current_data = data

        for column in data.columns:
            label = QLabel(column)
            self.filter_controls_layout.addWidget(label)

            if pd.api.types.is_numeric_dtype(data[column]):
                min_val = data[column].min()
                max_val = data[column].max()

                min_edit = QLineEdit(str(min_val))
                max_edit = QLineEdit(str(max_val))

                hbox = QHBoxLayout()
                hbox.addWidget(QLabel("Min:"))
                hbox.addWidget(min_edit)
                hbox.addWidget(QLabel("Max:"))
                hbox.addWidget(max_edit)

                self.filter_controls_layout.addLayout(hbox)
                self.filter_controls[column] = (min_edit, max_edit)
            else:
                unique_values = data[column].unique()
                combo = NoScrollCBox()
                combo.addItem("(All)")
                combo.addItems(map(str, unique_values))
                self.filter_controls_layout.addWidget(combo)
                self.filter_controls[column] = combo
                
        # Populate stats combobox
        self.stats_combo.blockSignals(True)
        self.stats_combo.clear()
        self.stats_combo.addItems(data.columns)
        self.stats_combo.blockSignals(False)
        
        if len(data.columns) > 0:
            self.on_stats_column_changed(data.columns[0])
            
        # self.filter_controls_layout no longer gets stretch, as scroll_main_layout has it


    def on_apply_filters(self):
        """Collect filter values and emit signal"""
        if not hasattr(self, 'filter_controls'):
            return

        filters = {}

        for column, control in self.filter_controls.items():
            if isinstance(control, tuple):
                min_edit, max_edit = control
                try:
                    min_val = float(min_edit.text()) if min_edit.text() else None
                    max_val = float(max_edit.text()) if max_edit.text() else None
                    filters[column] = (min_val, max_val)
                except ValueError:
                    pass
            else:
                filters[column] = control.currentText()

        self.filters_applied.emit(filters)
        
    def on_stats_column_changed(self, column_name):
        if not hasattr(self, 'current_data') or self.current_data is None or not column_name:
            return
            
        if column_name not in self.current_data.columns:
            return
            
        col_data = self.current_data[column_name]
        dtype = str(col_data.dtype)
        total_rows = len(col_data)
        missing = col_data.isnull().sum()
        missing_pct = (missing / total_rows) * 100 if total_rows > 0 else 0
        unique_vals = col_data.nunique()
        
        stats_text = f"<b>Type:</b> {dtype}<br>"
        stats_text += f"<b>Missing:</b> {missing} ({missing_pct:.1f}%)<br>"
        stats_text += f"<b>Unique Values:</b> {unique_vals}<br>"
        
        if pd.api.types.is_numeric_dtype(col_data):
            stats_text += f"<b>Mean:</b> {col_data.mean():.2f}<br>"
            stats_text += f"<b>Min:</b> {col_data.min()}<br>"
            stats_text += f"<b>Max:</b> {col_data.max()}<br>"
        else:
            if not col_data.mode().empty:
                stats_text += f"<b>Mode:</b> {col_data.mode().iloc[0]}"
                
        self.stats_label.setText(stats_text)
        self.stats_label.setStyleSheet("color: white;")


class PlotWidget(QFrame):
    plot_requested = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.current_data = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems(['bar', 'line', 'scatter', 'box', 'violin', 'hist', 'kde', 'heatmap', 'pie', 'area'])
        layout.addWidget(QLabel("Plot Type:"))
        layout.addWidget(self.plot_type_combo)

        self.palette_combo = QComboBox()
        self.palette_combo.addItems(['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'tab10', 'Set1', 'Set2', 'Set3', 'Dark2', 'husl', 'coolwarm'])
        layout.addWidget(QLabel("Color Palette:"))
        layout.addWidget(self.palette_combo)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Optional Title...")
        layout.addWidget(QLabel("Plot Title:"))
        layout.addWidget(self.title_input)

        self.x_axis_combo = QComboBox()
        layout.addWidget(QLabel("X Axis:"))
        layout.addWidget(self.x_axis_combo)

        self.y_axis_combo = QComboBox()
        layout.addWidget(QLabel("Y Axis:"))
        layout.addWidget(self.y_axis_combo)

        self.aggregation_combo = QComboBox()
        self.aggregation_combo.addItems(["None", "sum", "mean", "count", "median", "min", "max"])
        layout.addWidget(QLabel("Aggregation (Y):"))
        layout.addWidget(self.aggregation_combo)

        self.hue_combo = QComboBox()
        self.hue_combo.addItem("None")
        layout.addWidget(QLabel("Hue (color by):"))
        layout.addWidget(self.hue_combo)

        plot_btn = QPushButton("Generate Plot")
        plot_btn.clicked.connect(self.on_plot_requested)
        layout.addWidget(plot_btn)

    def update_controls(self, data):
        """Update the plot controls when new data is loaded"""
        self.x_axis_combo.clear()
        self.y_axis_combo.clear()
        self.hue_combo.clear()

        self.x_axis_combo.addItem("None")
        self.y_axis_combo.addItem("None")
        self.hue_combo.addItem("None")

        if data is not None:
            for column in data.columns:
                self.x_axis_combo.addItem(column)
                self.y_axis_combo.addItem(column)
                self.hue_combo.addItem(column)

    def on_plot_requested(self):
        """Emit signal with plot parameters"""
        agg = self.aggregation_combo.currentText()
        plot_params = {
            'plttype': self.plot_type_combo.currentText(),
            'x': self.x_axis_combo.currentText() if self.x_axis_combo.currentText() != "None" else None,
            'y': self.y_axis_combo.currentText() if self.y_axis_combo.currentText() != "None" else None,
            'hue': self.hue_combo.currentText() if self.hue_combo.currentText() != "None" else None,
            'aggregation': agg if agg != "None" else None,
            'palette': self.palette_combo.currentText(),
            'title': self.title_input.text() if self.title_input.text() else None
        }
        self.plot_requested.emit(plot_params)


class NoScrollCBox(QComboBox):
    """disable changing ComboBox options using scroll"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event):
        event.ignore()