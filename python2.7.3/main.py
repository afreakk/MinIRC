import sys
import PyQt5.QtWidgets
from window import MyWindow

def main():
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
