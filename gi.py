'''
gi: gltf inspector
'''
import sys
import pathlib
from logging import getLogger
#from typing import Tuple, Any
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QStyle, QFileDialog
#from PyQt5.QtGui import QIcon

LOGGER = getLogger(__name__)


class Scene:
    def __init__(self):
        pass

    def load(self, path: pathlib.Path):
        ext = path.suffix.lower()
        if ext == '.gltf':
            print('.gltf')
        elif ext == '.glb':
            print('.glb')
        else:
            LOGGER.error(f'unknwon type: {path}')


class MainWindow(QMainWindow):
    def __init__(self)->None:
        super().__init__()

        self.root_menu = self.menuBar()
        self.file_menu = self.root_menu.addMenu('&File')

        self.toolbar = self.addToolBar('Exit')

        self.statusBar().showMessage('Ready')
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('gi')
        self.setCentralWidget(QLabel('Hello World!'))

    def file_menu_add_action(self, action: QAction)->None:
        self.toolbar.addAction(action)
        self.file_menu.addAction(action)


def main()->None:
    LOGGER.debug('before')
    from logging import basicConfig, DEBUG
    basicConfig(
        level=DEBUG,
        datefmt='%H:%M:%S',
        format='%(asctime)s[%(levelname)s][%(name)s.%(funcName)s] %(message)s'
    )

    scene = Scene()

    app = QApplication(sys.argv)

    window = MainWindow()

    style = QApplication.style()

    open_action = QAction(style.standardIcon(
        QStyle.SP_DialogOpenButton), '&Open', window)
    open_action.setShortcut('Ctrl+O')
    open_action.setStatusTip('Exit application')

    def on_open():
        path, _ = QFileDialog.getOpenFileName(
            window, 'Open file', None, 'Model Files(*.gltf *.glb)' ';;All Files(*.*)')
        scene.load(pathlib.Path(path))
    open_action.triggered.connect(on_open)
    window.file_menu_add_action(open_action)

    # main window
    window.show()

    # execute
    app.exec_()


if __name__ == '__main__':
    main()
