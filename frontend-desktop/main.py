import sys
import requests
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFileDialog, QTableWidget, 
                             QTableWidgetItem, QTabWidget, QMessageBox, QDialog, QFormLayout)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000/api/"

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Chemical Visualizer")
        self.setFixedSize(300, 150)
        
        layout = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        
        layout.addRow("Username:", self.username)
        layout.addRow("Password:", self.password)
        
        self.btn_login = QPushButton("Login")
        self.btn_login.clicked.connect(self.check_login)
        layout.addRow(self.btn_login)
        
        self.setLayout(layout)
        
    def check_login(self):
        if self.username.text() == 'Admin' and self.password.text() == 'Admin':
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials! Please use 'Admin' / 'Admin'")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 1000, 700)
        
        # Tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Dashboard Tab
        self.dashboard_tab = QWidget()
        self.setup_dashboard_tab()
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        
        # Data View Tab
        self.data_tab = QWidget()
        self.setup_data_tab()
        self.tabs.addTab(self.data_tab, "Data Visualization")
        
        self.current_dataset = None

    def setup_dashboard_tab(self):
        layout = QVBoxLayout()
        
        # Upload Section
        upload_layout = QHBoxLayout()
        self.btn_upload = QPushButton("Upload New CSV Dataset")
        self.btn_upload.clicked.connect(self.upload_file)
        upload_layout.addWidget(self.btn_upload)
        layout.addLayout(upload_layout)
        
        # History Section
        layout.addWidget(QLabel("Recent Uploads (Last 5)"))
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["ID", "Uploaded At", "Action"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.history_table)
        
        self.btn_refresh = QPushButton("Refresh History")
        self.btn_refresh.clicked.connect(self.load_history)
        layout.addWidget(self.btn_refresh)
        
        self.dashboard_tab.setLayout(layout)
        self.load_history()

    def setup_data_tab(self):
        layout = QVBoxLayout()
        
        self.data_label = QLabel("No Dataset Selected")
        self.data_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.data_label)
        
        # Stats Cards Layout
        stats_layout = QHBoxLayout()
        self.lbl_count = QLabel("Count: -")
        self.lbl_flow = QLabel("Avg Flow: -")
        self.lbl_press = QLabel("Avg Press: -")
        self.lbl_temp = QLabel("Avg Temp: -")
        
        for lbl in [self.lbl_count, self.lbl_flow, self.lbl_press, self.lbl_temp]:
            lbl.setStyleSheet("""
                QLabel {
                    background-color: #ffffff;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 15px;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)
            lbl.setAlignment(Qt.AlignCenter)
            stats_layout.addWidget(lbl)
            
        layout.addLayout(stats_layout)
        
        
        # Matplotlib Figure
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.btn_pdf = QPushButton("Download PDF Report")
        self.btn_pdf.clicked.connect(self.download_pdf)
        layout.addWidget(self.btn_pdf)
        
        self.data_tab.setLayout(layout)

    def download_pdf(self):
        if not self.current_dataset:
            return
        
        try:
            url = f"{API_URL}pdf/{self.current_dataset['dataset_id']}/"
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                fname, _ = QFileDialog.getSaveFileName(self, 'Save PDF', f"report_{self.current_dataset['dataset_id']}.pdf", "PDF Files (*.pdf)")
                if fname:
                    with open(fname, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    QMessageBox.information(self, "Success", "PDF Saved Successfully!")
            else:
                QMessageBox.warning(self, "Error", "Could not generate PDF")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def load_history(self):
        try:
            response = requests.get(f"{API_URL}history/")
            if response.status_code == 200:
                data = response.json()
                self.history_table.setRowCount(len(data))
                for i, row in enumerate(data):
                    self.history_table.setItem(i, 0, QTableWidgetItem(str(row['id'])))
                    self.history_table.setItem(i, 1, QTableWidgetItem(str(row['uploaded_at'])))
                    
                    btn_view = QPushButton("View")
                    btn_view.clicked.connect(lambda checked, r=row['id']: self.load_dataset(r))
                    self.history_table.setCellWidget(i, 2, btn_view)
        except Exception as e:
            print(f"Error loading history: {e}")

    def upload_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open CSV', 'c:\\', "CSV Files (*.csv)")
        if fname:
            try:
                files = {'file': open(fname, 'rb')}
                response = requests.post(f"{API_URL}upload/", files=files)
                if response.status_code == 201:
                    data = response.json()
                    QMessageBox.information(self, "Success", "File uploaded successfully!")
                    self.load_history()
                    self.load_dataset(data['id'])
                else:
                    QMessageBox.warning(self, "Error", "Upload failed")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def load_dataset(self, dataset_id):
        try:
            response = requests.get(f"{API_URL}summary/{dataset_id}/")
            if response.status_code == 200:
                data = response.json()
                self.current_dataset = data
                self.update_data_view(data)
                self.tabs.setCurrentIndex(1)
            else:
                QMessageBox.warning(self, "Error", "Could not load dataset details")
        except Exception as e:
            print(f"Error loading dataset: {e}")

    def update_data_view(self, data):
        self.data_label.setText(f"Dataset: {data['file_name']}")
        
        self.lbl_count.setText(f"Count: {data['total_count']}")
        self.lbl_flow.setText(f"Avg Flow: {data['averages']['flowrate']}")
        self.lbl_press.setText(f"Avg Press: {data['averages']['pressure']}")
        self.lbl_temp.setText(f"Avg Temp: {data['averages']['temperature']}")
        
        # Plots
        self.figure.clear()
        
        # Subplot 1: Pie Chart (Type Distribution)
        ax1 = self.figure.add_subplot(121)
        type_dist = data['type_distribution']
        labels = [d['equipment_type'] for d in type_dist]
        counts = [d['count'] for d in type_dist]
        ax1.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Equipment Types')
        
        # Subplot 2: Bar Chart (Averages)
        ax2 = self.figure.add_subplot(122)
        params = ['Flowrate', 'Pressure', 'Temp']
        values = [data['averages']['flowrate'], data['averages']['pressure'], data['averages']['temperature']]
        ax2.bar(params, values, color=['#334155', '#64748b', '#94a3b8'])
        ax2.set_title('Average Parameters')
        
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Modern B&W QSS Style
    app.setStyle('Fusion')
    
    qss = """
    QWidget {
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        color: #374151; /* Gray 700 */
        background-color: #f8fafc; /* Slate 50 */
    }
    
    /* Main Window & Tabs */
    QMainWindow {
        background-color: #ffffff;
    }
    
    QTabWidget::pane {
        border: 1px solid #e2e8f0; /* Slate 200 */
        background: #ffffff;
        border-radius: 6px;
    }
    
    QTabBar::tab {
        background: #f1f5f9; /* Slate 100 */
        color: #64748b; /* Slate 500 */
        padding: 10px 20px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 4px;
        font-weight: 500;
    }
    
    QTabBar::tab:selected {
        background: #ffffff;
        color: #1e293b; /* Slate 800 */
        border: 1px solid #e2e8f0;
        border-bottom: 2px solid #ffffff; /* Seamless blend */
        font-weight: bold;
    }
    
    /* Buttons */
    QPushButton {
        background-color: #334155; /* Slate 700 - Lighter than black */
        color: #ffffff;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 600;
    }
    
    QPushButton:hover {
        background-color: #475569; /* Slate 600 */
    }
    
    QPushButton:pressed {
        background-color: #1e293b; /* Slate 800 */
    }
    
    /* Tables */
    QTableWidget {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        gridline-color: #f1f5f9;
        selection-background-color: #f1f5f9;
        selection-color: #0f172a; /* Slate 900 */
    }
    
    QHeaderView::section {
        background-color: #f8fafc;
        padding: 8px;
        border: none;
        border-bottom: 2px solid #e2e8f0;
        font-weight: 600;
        color: #475569;
    }
    
    /* Labels & Cards substitute */
    QLabel {
        color: #334155;
    }
    
    QLineEdit {
        padding: 8px;
        border: 1px solid #cbd5e1; /* Slate 300 */
        border-radius: 6px;
        background-color: #fff;
        color: #1e293b;
    }
    
    QLineEdit:focus {
        border: 2px solid #334155; /* Slate 700 */
    }
    """
    app.setStyleSheet(qss)
    
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
