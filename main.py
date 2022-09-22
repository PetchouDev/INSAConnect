import os
import sys
from functools import partial

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QStyle, \
    QToolButton


class headBar(QWidget):
    clickPos = None

    def __init__(self, parent):
        super(headBar, self).__init__(parent)
        self.setAutoFillBackground(True)

        self.setStyleSheet("margin: 0 0 0 0; background-color: black;")
        # self.setBackgroundRole(QtGui.QPalette.Shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 1, 1, 1)
        title = QLabel("INSA Connect")
        icon = QLabel()
        icon.setFixedWidth(50)
        icon.setPixmap(QtGui.QPixmap("insa.ico").scaled(50, 100, QtCore.Qt.KeepAspectRatio))
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")


        self.title = QLabel("head bar", self, alignment=QtCore.Qt.AlignCenter)


        style = self.style()
        ref_size = self.fontMetrics().height()
        ref_size += style.pixelMetric(style.PM_ButtonMargin) * 2
        self.setMaximumHeight(ref_size + 2)

        btn_size = QtCore.QSize(ref_size, ref_size)
        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addStretch()
        for target in ('min', 'close'):
            btn = QToolButton(self, focusPolicy=QtCore.Qt.NoFocus)
            layout.addWidget(btn)
            btn.setFixedSize(btn_size)

            iconType = getattr(style,
                               'SP_TitleBar{}Button'.format(target.capitalize()))
            btn.setIcon(style.standardIcon(iconType))

            if target == 'close':
                colorNormal = 'red'
                colorHover = 'orangered'
            else:
                colorNormal = 'palette(mid)'
                colorHover = 'palette(light)'
            btn.setStyleSheet('''
                QToolButton {{
                    background-color: {};
                    border-radius: 10px;
                }}
                QToolButton:hover {{
                    background-color: {}
                }}
            '''.format(colorNormal, colorHover))

            signal = getattr(self, target + 'Clicked')
            btn.clicked.connect(signal)

            setattr(self, target + 'Button', btn)

        self.updateTitle("INSA")
        parent.windowTitleChanged.connect(self.updateTitle)

    def updateTitle(self, title=None):
        if title is None:
            title = self.window().windowTitle()
        width = self.title.width()
        width -= self.style().pixelMetric(QStyle.PM_LayoutHorizontalSpacing) * 2
        self.title.setText(self.fontMetrics().elidedText(
            title, QtCore.Qt.ElideRight, width))

    def windowStateChanged(self, state):
        self.normalButton.setVisible(state == QtCore.Qt.WindowMaximized)
        self.maxButton.setVisible(state != QtCore.Qt.WindowMaximized)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clickPos = event.windowPos().toPoint()

    def mouseMoveEvent(self, event):
        if self.clickPos is not None:
            self.window().move(event.globalPos() - self.clickPos)

    def mouseReleaseEvent(self, QMouseEvent):
        self.clickPos = None

    def closeClicked(self):
        self.window().close()

    def maxClicked(self):
        self.window().showMaximized()

    def normalClicked(self):
        self.window().showNormal()

    def minClicked(self):
        self.window().showMinimized()

    def resizeEvent(self, event):
        self.title.resize(self.minButton.x(), self.height())
        self.updateTitle()


class mainView(QMainWindow):
    def __init__(self):
        super(mainView, self).__init__()

        # set window's properties (always on top, only close button)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.FramelessWindowHint
        )

        # create and setup main display area
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        mainWidget = QWidget()
        mainWidget.setStyleSheet("QWidget#mainWidget{"
                                 "background-color: black;"
                                 "border:1px solid black;"
                                 "border-radius: 30px;"
                                 "padding: 5px;"
                                 "}"
                                 "QPushButton{"
                                 "background-color: rgb(30, 30, 30);"
                                 "color: white;"
                                 "font-size: 14px;"
                                 "border-radius: 10px;"
                                 "border: 1.5px solid rgb(150, 150, 150);"
                                 "padding: 5px 10px 5px 10px;"
                                 "}"
                                 "QPushButton:Hover{"
                                 "border-color: white;"
                                 "color: black;"
                                 "background-color: rgb(200, 200, 200);"
                                 "}"
                                 )
        mainWidget.setObjectName("mainWidget")


        self.setCentralWidget(mainWidget)

        # layout gestion
        layout = QVBoxLayout()  # rows
        ligne1 = QHBoxLayout()  # |
        ligne2 = QHBoxLayout()  # |
        ligne3 = QHBoxLayout()  # |columns

        # create and add an action head bar
        self.head = headBar(self)
        layout.addWidget(self.head)

        # layout assignment
        layout.addLayout(ligne1)
        layout.addLayout(ligne2)
        layout.addLayout(ligne3)
        mainWidget.setLayout(layout)

        # open planete
        planete_button = QPushButton("Planete")
        ligne1.addWidget(planete_button)

        # open mailbox
        zmail_button = QPushButton("Mailbox")
        ligne1.addWidget(zmail_button)

        # open intranet
        intranet_fimi_button = QPushButton("Intranet FIMI")
        ligne2.addWidget(intranet_fimi_button)

        # open moodle
        moodle_button = QPushButton("Moodle")
        ligne2.addWidget(moodle_button)

        # vpn button
        vpn_button = QPushButton("Open VPN")
        ligne3.addWidget(vpn_button)

        # files button
        files_button = QPushButton("Home INSA")
        ligne3.addWidget(files_button)

        # assign actions to buttons
        moodle_button.clicked.connect(partial(open_link, "moodle"))
        zmail_button.clicked.connect(partial(open_link, "zmail"))
        intranet_fimi_button.clicked.connect(partial(open_link, 'intranetfimi'))
        planete_button.clicked.connect(partial(open_link, 'planete'))
        vpn_button.clicked.connect(open_vpn)
        files_button.clicked.connect(open_files)

        # show the window once all elements have been set up
        self.show()


def open_files():
    os.system("@start https://planete.insa-lyon.fr/uPortal/f/bv/normal/render.uP?pCt=esup-filemanager-mydoc.u19l1n7"
              "&pCs=normal&pCp")


def open_vpn():
    os.system(r'@start C:\"Program Files (x86)"\Cisco\"Cisco AnyConnect Secure Mobility Client"\vpnui.exe')


def open_link(subdomain):
    os.system(f"@start https://{subdomain}.insa-lyon.fr")


if __name__ == "__main__":
    # change working directory to the script location in temp folder
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # create application
    app = QApplication([])
    app.setApplicationName("INSA Connect")

    # set icon
    icon = "insa.ico"
    app_icon = QtGui.QIcon()
    app_icon.addFile(icon, QtCore.QSize(16, 16))
    app_icon.addFile(icon, QtCore.QSize(24, 24))
    app_icon.addFile(icon, QtCore.QSize(32, 32))
    app_icon.addFile(icon, QtCore.QSize(48, 48))
    app_icon.addFile(icon, QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)

    # add a view
    window = mainView()

    # keep running until app exit
    sys.exit(app.exec())
