# UI Components for Skin Processor Application

from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QSlider, QGroupBox, QGridLayout, QProgressBar,
                             QTabWidget, QTextEdit, QSplitter, QCheckBox,
                             QButtonGroup, QRadioButton, QWidget, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from config import GUI_CONFIG, DEFAULT_VALUES

class UIComponents:
    """
    Lớp quản lý các thành phần giao diện
    """
    
    @staticmethod
    def create_control_panel(parent):
        """
        Tạo panel điều khiển với các slider và checkbox
        """
        # Panel điều khiển chính
        control_panel = QGroupBox("🎛️ Điều khiển")
        control_layout = QVBoxLayout()
        
        # Phương pháp xử lý
        method_group = QGroupBox("Phương pháp xử lý")
        method_layout = QGridLayout()
        
        parent.method_group = QButtonGroup()
        methods = [
            ("bilateral", "Bilateral Filter (Cân bằng)"),
            ("guided", "Guided Filter (Mượt)"),
            ("edge_preserve", "Edge Preserve (Bảo toàn)"),
            ("advanced", "Advanced Blend (Nâng cao)")
        ]
        
        for i, (method, label) in enumerate(methods):
            radio = QRadioButton(label)
            if method == DEFAULT_VALUES['method']:
                radio.setChecked(True)
                parent.current_method = method
            parent.method_group.addButton(radio, i)
            radio.toggled.connect(lambda checked, m=method: 
                                setattr(parent, 'current_method', m) if checked else None)
            method_layout.addWidget(radio, i // 2, i % 2)
        
        method_group.setLayout(method_layout)
        
        # Cường độ
        strength_group = QGroupBox("Cường độ xử lý")
        strength_layout = QVBoxLayout()
        
        parent.strength_slider = QSlider(Qt.Horizontal)
        parent.strength_slider.setRange(0, 100)
        parent.strength_slider.setValue(DEFAULT_VALUES['strength'])
        parent.strength_slider.setTickPosition(QSlider.TicksBelow)
        parent.strength_slider.setTickInterval(10)
        
        parent.strength_label = QLabel(f"{DEFAULT_VALUES['strength']}%")
        parent.strength_slider.valueChanged.connect(
            lambda v: [parent.strength_label.setText(f"{v}%"), parent.update_image_info()]
        )
        
        strength_layout.addWidget(QLabel("🎚️ Cường độ:"))
        strength_layout.addWidget(parent.strength_slider)
        strength_layout.addWidget(parent.strength_label)
        strength_group.setLayout(strength_layout)
        
        # Tính năng nâng cao
        advanced_group = QGroupBox("✨ Tính năng nâng cao")
        advanced_layout = QGridLayout()
        
        # Checkbox features
        parent.blemish_checkbox = QCheckBox("Loại bỏ mụn/tàn nhang")
        parent.wrinkle_checkbox = QCheckBox("Giảm nếp nhăn")
        parent.skin_tone_checkbox = QCheckBox("Điều chỉnh màu da")
        parent.eye_checkbox = QCheckBox("Làm sáng mắt")
        parent.teeth_checkbox = QCheckBox("Làm trắng răng")
        
        # Set default checked
        parent.blemish_checkbox.setChecked(True)
        parent.wrinkle_checkbox.setChecked(True)
        parent.skin_tone_checkbox.setChecked(True)
        
        advanced_layout.addWidget(parent.blemish_checkbox, 0, 0)
        advanced_layout.addWidget(parent.wrinkle_checkbox, 0, 1)
        advanced_layout.addWidget(parent.skin_tone_checkbox, 1, 0)
        advanced_layout.addWidget(parent.eye_checkbox, 1, 1)
        advanced_layout.addWidget(parent.teeth_checkbox, 2, 0, 1, 2)
        
        advanced_group.setLayout(advanced_layout)
        
        # Nút xử lý
        parent.process_btn = QPushButton("Xử lý ảnh")
        parent.process_btn.setEnabled(False)
        parent.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        # Progress bar
        parent.progress_bar = QProgressBar()
        parent.progress_bar.setVisible(False)
        parent.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        
        # Thông tin
        info_group = QGroupBox("📊 Thông tin")
        info_layout = QVBoxLayout()
        
        parent.info_text = QTextEdit()
        parent.info_text.setReadOnly(True)
        parent.info_text.setMaximumHeight(GUI_CONFIG['info_text_height'])
        parent.info_text.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10px;
            }
        """)
        
        info_layout.addWidget(parent.info_text)
        info_group.setLayout(info_layout)
        
        # Assemble control panel
        control_layout.addWidget(method_group)
        control_layout.addWidget(strength_group)
        control_layout.addWidget(advanced_group)
        control_layout.addWidget(parent.process_btn)
        control_layout.addWidget(parent.progress_bar)
        control_layout.addWidget(info_group)
        control_layout.addStretch()
        
        control_panel.setLayout(control_layout)
        control_panel.setFixedWidth(GUI_CONFIG['control_panel_width'])
        
        return control_panel
    
    @staticmethod
    def create_image_display_area(parent):
        """
        Tạo khu vực hiển thị ảnh với tabs
        """
        # Tab widget cho ảnh
        parent.tab_widget = QTabWidget()
        parent.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                padding: 8px 12px;
                margin-right: 2px;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
        """)
        
        # Tab ảnh gốc
        original_tab = UIComponents.create_image_tab("📸 Ảnh gốc")
        parent.original_label = original_tab.findChild(QLabel)
        parent.tab_widget.addTab(original_tab, "📸 Ảnh gốc")
        
        # Tab ảnh đã xử lý
        processed_tab = UIComponents.create_image_tab("✨ Ảnh đã xử lý")
        parent.processed_label = processed_tab.findChild(QLabel)
        parent.tab_widget.addTab(processed_tab, "✨ Ảnh đã xử lý")
        
        # Tab landmarks
        landmarks_tab = UIComponents.create_image_tab("🎯 Landmarks")
        parent.landmarks_label = landmarks_tab.findChild(QLabel)
        parent.tab_widget.addTab(landmarks_tab, "🎯 Landmarks")
        
        return parent.tab_widget
    
    @staticmethod
    def create_image_tab(title):
        """
        Tạo một tab hiển thị ảnh
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Label hiển thị ảnh
        image_label = QLabel(title)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setMinimumSize(*GUI_CONFIG['min_image_size'])
        image_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 2px dashed #dee2e6;
                border-radius: 10px;
                color: #6c757d;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(image_label)
        tab.setLayout(layout)
        
        return tab
    
    @staticmethod
    def create_menu_bar(parent):
        """
        Tạo menu bar
        """
        menubar = parent.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        open_action = file_menu.addAction('Mở ảnh')
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(parent.open_image)
        
        parent.save_btn = file_menu.addAction('Lưu ảnh')
        parent.save_btn.setShortcut('Ctrl+S')
        parent.save_btn.setEnabled(False)
        parent.save_btn.triggered.connect(parent.save_image)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction('Thoát')
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(parent.close)
        
        # Help menu
        help_menu = menubar.addMenu('Trợ giúp')
        
        about_action = help_menu.addAction('ℹVề ứng dụng')
        about_action.triggered.connect(
            lambda: parent.show_info_dialog(
                "Về ứng dụng",
                """
                🌟 Ứng dụng Xử lý Da - Phiên bản Nâng cao
                
                ✨ Tính năng chính:
                • Xử lý da mặt tự động với AI
                • 4 phương pháp lọc khác nhau
                • Loại bỏ mụn và tàn nhang
                • Giảm nếp nhăn
                • Làm sáng mắt và trắng răng
                • Điều chỉnh màu da
                
                🛠️ Công nghệ:
                • OpenCV & MediaPipe
                • PyQt5
                • Computer Vision
                
                👨‍💻 Phiên bản: 2.0
                📅 Cập nhật: 2024
                """
            )
        )
    
    @staticmethod
    def create_status_bar(parent):
        """
        Tạo status bar
        """
        status_bar = parent.statusBar()
        status_bar.showMessage("Sẵn sàng - Chọn ảnh để bắt đầu")
        return status_bar
