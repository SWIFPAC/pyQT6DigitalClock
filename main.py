import sys
import socket
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

HOST = '192.168.63.128'  # The server's hostname or IP address
PORT = 6532  # The port used by the server
clock = Clock()


class Clock(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PyQt6 Digital Clock')
        self.setGeometry(100, 100, 250, 100)

        font = QFont('Arial', 36)
        self.label = QLabel(self)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.live_current_time = ""

    def update_time(self):
        current_time = self.live_current_time
        self.label.setText(current_time)

    def receive_data(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            while True:
                data = s.recv(1024)
                if not data:
                    break
                self.live_current_time = data.decode()

            # close the connection
            s.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = Clock()
    clock.receive_data()
    clock.show()
    sys.exit(app.exec())
