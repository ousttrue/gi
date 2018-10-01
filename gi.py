'''
gi: gltf inspector
'''
import sys
import pathlib
import json
import struct
from logging import getLogger
from typing import Tuple
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QStyle, QFileDialog
#from PyQt5.QtGui import QIcon

LOGGER = getLogger(__name__)


class Reader:
    def __init__(self, data: bytes)->None:
        self.data = data
        self.pos = 0

    def read_str(self, size):
        result = self.data[self.pos: self.pos + size]
        self.pos += size
        return result.strip()

    def read(self, size):
        result = self.data[self.pos: self.pos + size]
        self.pos += size
        return result

    def read_uint(self):
        result = struct.unpack('I', self.data[self.pos:self.pos + 4])[0]
        self.pos += 4
        return result


def parse_glb(data: bytes)->Tuple[dict, bytes]:
    reader = Reader(data)
    magic = reader.read_str(4)
    if  magic != b'glTF':
        raise Exception(f'magic not found: #{magic}')

    version = reader.read_uint()
    if version != 2:
        raise Exception(f'version:#{version} is not 2')

    size = reader.read_uint()
    size -= 12

    json_str = None
    body = None
    while size > 0:
        #print(size)

        chunk_size = reader.read_uint()
        size -= 4

        chunk_type = reader.read_str(4)
        size -= 4

        chunk_data = reader.read(chunk_size)
        size -= chunk_size

        if chunk_type == b'BIN\x00':
            body = chunk_data
        elif chunk_type == b'JSON':
            json_str = chunk_data
        else:
            raise Exception(f'unknown chunk_type: {chunk_type}')

    return json.loads(json_str), body


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

    def on_open(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 'Open file', None, 'Model Files(*.gltf *.glb)' ';;All Files(*.*)')
        self.load(pathlib.Path(path))

    def load(self, path: pathlib.Path):
        ext = path.suffix.lower()
        if ext == '.gltf':
            with path.open(encoding='utf-8') as r:
                gltf = json.loads(r.read())
                self.set_gltf(gltf)
        elif ext == '.glb':
            with path.open('rb') as r:
                gltf, _  = parse_glb(r.read())
                self.set_gltf(gltf)
        else:
            LOGGER.error('unknwon type: %s', path)

    def set_gltf(self, gltf: dict):
        print(gltf['asset']['version'])


def main()->None:
    LOGGER.debug('before')
    from logging import basicConfig, DEBUG
    basicConfig(
        level=DEBUG,
        datefmt='%H:%M:%S',
        format='%(asctime)s[%(levelname)s][%(name)s.%(funcName)s] %(message)s'
    )

    app = QApplication(sys.argv)

    window = MainWindow()

    style = QApplication.style()
    open_action = QAction(style.standardIcon(
        QStyle.SP_DialogOpenButton), '&Open', window)
    open_action.setShortcut('Ctrl+O')
    open_action.setStatusTip('Exit application')
    open_action.triggered.connect(window.on_open)
    window.file_menu_add_action(open_action)

    # main window
    window.show()

    # execute
    app.exec_()


if __name__ == '__main__':
    main()
