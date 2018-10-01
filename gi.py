from PyQt5 import QtWidgets

# initialize
app = QtWidgets.QApplication([])

# main window
window = QtWidgets.QMainWindow()
window.setCentralWidget(QtWidgets.QLabel('Hello World!'))
window.show()

# execute
app.exec_()