import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("PyQt Window")
window.setGeometry(200, 200, 400, 200)

label = QLabel("Hello from PyQt!", window)
label.move(100, 80)

window.show()
sys.exit(app.exec_())
