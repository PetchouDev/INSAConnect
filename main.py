import os
import sys
from functools import partial


from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QApplication, QVBoxLayout, QHBoxLayout


class mainView(QMainWindow):
    def __init__(self):
        super(mainView, self).__init__()

        # create and setup main display area
        mainWidget = QWidget()
        mainWidget.setStyleSheet("border-radius#mainWidget: 30px; background-color#mainWidget: rgb(255, 255, 255);")
        self.setCentralWidget(mainWidget)

        # set window's properties (always on top, only close button)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint
        )

        # layout gestion
        layout = QVBoxLayout()  # rows
        ligne1 = QHBoxLayout()  # |
        ligne2 = QHBoxLayout()  # |
        ligne3 = QHBoxLayout()  # |columns

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
