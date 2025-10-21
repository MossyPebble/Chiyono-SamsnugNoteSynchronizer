import sys, os, json
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFontDialog, QDialog, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont, QAction, QIcon, QPixmap
from PyQt6.QtCore import QTimer
from utils.SamsungNoteAccess import extract_from_dotnote

currentDir = os.path.dirname(os.path.abspath(__file__))

dotNotePath = r"C:\Users\LG\AppData\Local\Packages\SAMSUNGELECTRONICSCoLtd.SamsungNotes_wyx1vj98g3asy\LocalState\wdoc\46976171-1965-ebf8-0000-017f178d5877\note.note"

settingsPath = os.path.join(currentDir, "settings.json")

class NoteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Note")
        self.setWindowIcon(QIcon(os.path.join(currentDir, "img", "sakurachiyonoo_list.ico")))
        self.setGeometry(100, 100, 600, 1000)

        # 중앙 위젯 설정
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.setCentralWidget(self.textEdit)

        # 주기적으로 파일 확인
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.extract_and_update)
        self.timer.start(500)

        # 초기 텍스트 로드
        self.extract_and_update()

        # 메뉴바 생성
        self.create_menu_bar()

    def create_menu_bar(self):

        """메뉴바 생성 및 설정"""

        menu_bar = self.menuBar()
        self.loadSettings()

        # "File" 메뉴
        file_menu = menu_bar.addMenu("File")

        # "Exit" 액션
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # "Edit" 메뉴
        edit_menu = menu_bar.addMenu("Edit")

        # "Change Font" 액션
        change_font_action = QAction("Change Font", self)
        change_font_action.triggered.connect(self.change_font)
        edit_menu.addAction(change_font_action)

        # "Force Refresh" 액션
        refresh_action = QAction("Force Refresh", self)
        refresh_action.triggered.connect(self.extract_and_update)
        edit_menu.addAction(refresh_action)

        # "Chiyono" 메뉴
        chiyono_menu = menu_bar.addMenu("Chiyono")

        # "About Chiyono" 액션
        about_action = QAction("About Chiyono", self)
        about_action.triggered.connect(self.show_about_dialog)
        chiyono_menu.addAction(about_action)

    def extract_and_update(self):

        """파일에서 텍스트를 추출하고 QTextEdit를 업데이트하는 함수"""

        texts = extract_from_dotnote(dotNotePath)
        if texts == self.textEdit.toPlainText(): return
        self.textEdit.setPlainText(texts)

    def change_font(self):
        font, ok = QFontDialog.getFont(self.textEdit.font(), self, "Select Font")
        if ok:
            self.textEdit.setFont(font)
            self.saveSettings()

    def loadSettings(self):
        try:
            with open(settingsPath, "r") as f:
                settings = json.load(f)
                font_name = settings.get("font_name", "Arial")
                font_size = int(settings.get("font_size", 12))
            
                font = QFont(font_name, font_size)
                self.textEdit.setFont(font)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass

    def saveSettings(self):
        font = self.textEdit.font()
        settings = {
            "font_name": font.family(),
            "font_size": font.pointSize()
        }
        with open(settingsPath, "w") as f:
            json.dump(settings, f)

    def show_about_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About Chiyono")
        dialog.setGeometry(200, 200, 400, 400)

        # 레이아웃 설정
        layout = QVBoxLayout(dialog)

        # 상단 라벨
        title_label = QLabel("Chiyono - Samsnug Note Synchronizer", dialog)
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        layout.addWidget(title_label)

        # QLabel에 이미지 추가
        label = QLabel(dialog)
        pixmap = QPixmap(os.path.join(currentDir, "img", "sakurachiyonoo_01.png"))
        pixmap = pixmap.scaled(563, 990)
        label.setPixmap(pixmap)
        label.setScaledContents(True)  # 이미지 크기를 창 크기에 맞게 조정
        layout.addWidget(label)

        dialog.setLayout(layout)
        dialog.exec()  # 다이얼로그 실행

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoteApp()
    window.show()
    sys.exit(app.exec())