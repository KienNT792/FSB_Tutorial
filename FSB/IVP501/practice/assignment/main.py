import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QFileDialog, QMessageBox, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QFont

# Import custom modules
from config import GUI_CONFIG, DEFAULT_VALUES
from ui_components import UIComponents
from processing_thread import ProcessingThread
from image_processor import LandmarksVisualizer

class SkinProcessorApp(QMainWindow):
    """
    Ứng dụng chính xử lý da với giao diện PyQt5
    """
    
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.processed_image = None
        self.landmarks = None
        self.processing_thread = None
        self.current_method = DEFAULT_VALUES['method']
        
        self.init_ui()
    
    def init_ui(self):
        """
        Khởi tạo giao diện người dùng
        """
        # Cài đặt window
        self.setWindowTitle(GUI_CONFIG['window_title'])
        self.setGeometry(*GUI_CONFIG['window_geometry'])
        
        # Widget chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout chính
        main_layout = QHBoxLayout()
        
        # Tạo splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel điều khiển (trái)
        control_panel = UIComponents.create_control_panel(self)
        
        # Khu vực hiển thị ảnh (phải)
        image_area = UIComponents.create_image_display_area(self)
        
        # Thêm vào splitter
        splitter.addWidget(control_panel)
        splitter.addWidget(image_area)
        splitter.setSizes(GUI_CONFIG['splitter_sizes'])
        
        # Layout
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        
        # Menu bar
        UIComponents.create_menu_bar(self)
        
        # Status bar
        self.status_bar = UIComponents.create_status_bar(self)
        
        # Kết nối signals
        self.connect_signals()
    
    def connect_signals(self):
        """
        Kết nối các signals với slots
        """
        self.process_btn.clicked.connect(self.process_image)
    
    def open_image(self):
        """
        Mở file ảnh
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn ảnh",
            "",
            "Image files (*.jpg *.jpeg *.png *.bmp *.tiff)"
        )
        
        if file_path:
            # Đọc ảnh
            image = cv2.imread(file_path)
            if image is not None:
                self.original_image = image
                self.processed_image = None
                self.landmarks = None
                
                # Hiển thị ảnh gốc
                self.display_image(self.original_image, self.original_label)
                
                # Reset tab về ảnh gốc
                self.tab_widget.setCurrentIndex(0)
                
                # Clear ảnh đã xử lý
                self.processed_label.clear()
                self.processed_label.setText("✨ Ảnh đã xử lý")
                
                # Clear landmarks
                self.landmarks_label.clear()
                self.landmarks_label.setText("🎯 Landmarks")
                
                # Enable process button
                self.process_btn.setEnabled(True)
                self.save_btn.setEnabled(False)
                
                # Update info
                self.update_image_info()
                self.status_bar.showMessage(f"📂 Đã tải: {file_path}")
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể đọc file ảnh!")
    
    def display_image(self, cv_image, label):
        """
        Hiển thị ảnh OpenCV trên QLabel
        """
        # Chuyển từ BGR sang RGB
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        
        # Tạo QImage
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Scale ảnh để fit label
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(
            label.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        
        label.setPixmap(scaled_pixmap)
    
    def update_image_info(self):
        """
        Cập nhật thông tin ảnh
        """
        if self.original_image is not None:
            h, w, c = self.original_image.shape
            size_mb = (h * w * c) / (1024 * 1024)
            
            info = f"""
Thông tin ảnh:
• Kích thước: {w} × {h}
• Channels: {c}
• Dung lượng: {size_mb:.2f} MB

Phương pháp: {self.current_method.title()}
Cường độ: {self.strength_slider.value()}%
            """
            self.info_text.setText(info)
    
    def process_image(self):
        """
        Xử lý ảnh trong thread riêng
        """
        if self.original_image is None:
            return
        
        # Hiển thị progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.process_btn.setEnabled(False)
        
        # Lấy các tùy chọn nâng cao
        options = {
            'blemish': self.blemish_checkbox.isChecked(),
            'wrinkle': self.wrinkle_checkbox.isChecked(),
            'skin_tone': self.skin_tone_checkbox.isChecked(),
            'eye': self.eye_checkbox.isChecked(),
            'teeth': self.teeth_checkbox.isChecked()
        }
        
        # Tạo và chạy thread xử lý
        strength = self.strength_slider.value() / 100.0
        self.processing_thread = ProcessingThread(
            self.original_image, 
            strength, 
            self.current_method,
            options
        )
        
        self.processing_thread.progress.connect(self.progress_bar.setValue)
        self.processing_thread.finished.connect(self.on_processing_finished)
        self.processing_thread.error.connect(self.on_processing_error)
        self.processing_thread.start()
        
        self.status_bar.showMessage("Đang xử lý ảnh...")
    
    def on_processing_finished(self, result_image, landmarks):
        """
        Xử lý kết quả từ thread
        """
        self.processed_image = result_image
        self.landmarks = landmarks
        
        # Hiển thị ảnh đã xử lý
        self.display_image(self.processed_image, self.processed_label)
        
        # Vẽ và hiển thị landmarks
        if landmarks is not None:
            landmarks_image = LandmarksVisualizer.draw_landmarks(
                self.original_image.copy(), 
                landmarks, 
                show_connections=True,
                show_indices=False
            )
            self.display_image(landmarks_image, self.landmarks_label)
        
        # Chuyển sang tab ảnh đã xử lý
        self.tab_widget.setCurrentIndex(1)
        
        # Ẩn progress bar và enable button
        self.progress_bar.setVisible(False)
        self.process_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        
        # Cập nhật thông tin
        landmarks_count = len(landmarks) if landmarks is not None else 0
        self.info_text.append(f"\n✅ Xử lý hoàn tất!")
        self.info_text.append(f"🎯 Phát hiện {landmarks_count} điểm mốc khuôn mặt")
        
        self.status_bar.showMessage("✅ Xử lý ảnh hoàn tất!")
    
    def on_processing_error(self, error_message):
        """
        Xử lý lỗi từ thread
        """
        self.progress_bar.setVisible(False)
        self.process_btn.setEnabled(True)
        
        QMessageBox.critical(self, "Lỗi xử lý", error_message)
        self.status_bar.showMessage(" Xử lý thất bại!")
    
    def save_image(self):
        """
        Lưu ảnh đã xử lý
        """
        if self.processed_image is None:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Lưu ảnh đã xử lý",
            "processed_image.jpg",
            "Image files (*.jpg *.png *.bmp)"
        )
        
        if file_path:
            success = cv2.imwrite(file_path, self.processed_image)
            if success:
                self.info_text.append(f"\n💾 Đã lưu: {file_path}")
                self.status_bar.showMessage(f"💾 Đã lưu: {file_path}")
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể lưu file!")
    
    def show_info_dialog(self, title, message):
        """
        Hiển thị dialog thông tin
        """
        QMessageBox.information(self, title, message)
    
    def closeEvent(self, event):
        """
        Xử lý khi đóng ứng dụng
        """
        if self.processing_thread and self.processing_thread.isRunning():
            reply = QMessageBox.question(
                self, 'Xác nhận', 
                'Đang có tiến trình xử lý. Bạn có muốn thoát?',
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.processing_thread.terminate()
                self.processing_thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

def main():
    """
    Hàm main khởi chạy ứng dụng
    """
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    
    # Font
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    # Tạo và hiển thị window
    window = SkinProcessorApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
