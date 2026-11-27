import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QLineEdit,
    QFileDialog, QLabel, QTableWidget,
    QTableWidgetItem, QComboBox, QFrame,
    QAbstractItemView, QHeaderView,
    QSizePolicy, QGridLayout
)

from PySide6.QtCore import (
    Qt, QSize
)

from PySide6.QtGui import QColor, QIcon, QPixmap, QPainter, QPen


from audio.scanner import scan_folder
from audio.exporter import export_csv as ec

results = []

class InspectorTable(QTableWidget):

    def resizeEvent(self, event):
        super().resizeEvent(event)

        width = self.viewport().width()
        for col, ratio in enumerate([0.34, 0.18, 0.24, 0.24]):
            self.setColumnWidth(col, int(width * ratio))

class ArrowComboBox(QComboBox):
    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor("#A0A8B3"), 1.5))

        center_y = self.height() // 2
        x = self.width() - 16

        if self.view().isVisible():
            # 열린 상태: 위쪽 화살표
            painter.drawLine(x - 4, center_y + 2, x, center_y - 2)
            painter.drawLine(x, center_y - 2, x + 4, center_y + 2)
        else:
            # 닫힌 상태: 아래쪽 화살표
            painter.drawLine(x - 4, center_y - 2, x, center_y + 2)
            painter.drawLine(x, center_y + 2, x + 4, center_y - 2)

        painter.end()

def scan_audio():

    try :
        start_button.setEnabled(False)
        table.setRowCount(0)

        if not browse.text().strip():
            result_label.setText("폴더를 선택해 주세요.")
            return

        folder_path = Path(browse.text())

        if not folder_path.exists():
            result_label.setText("존재하지 않는 경로입니다.")
            return

        elif not folder_path.is_dir():
            result_label.setText("폴더 경로를 입력해 주세요.")
            return

        result_label.setText("검사 중...")
        app.processEvents()

        sample_rate = sample_rate_box.currentData()
        bit_depth = bit_depth_box.currentData()
        results[:] = scan_folder(folder_path, sample_rate, bit_depth)

        if not results:
            result_label.setText("검사할 WAV 파일이 없습니다.")
            return

        table.setRowCount(len(results))


        for row, item in enumerate(results):
            filename_item = QTableWidgetItem(item["filename"])
            filename_item.setToolTip(item["filename"])
            table.setItem(row, 0, filename_item)
            table.setCellWidget(row, 1, make_status_badge(item["status"]))
            table.setItem(row, 2, QTableWidgetItem(f"{item['Sample Rate']} Hz"))

            view_button = QPushButton("View")
            view_button.setIcon(make_search_icon())
            view_button.setIconSize(QSize(14, 14))
            view_button.setFixedSize(84, 26)
            view_button.setStyleSheet("""
                QPushButton {
                    padding: 0px 6px;
                    font-size: 9pt;
                }
            """)
            view_button.clicked.connect(lambda checked=False, r=row: show_file_details(r))

            view_cell = QWidget()
            view_layout = QHBoxLayout(view_cell)
            view_layout.setContentsMargins(4, 0, 4, 0)
            view_layout.addWidget(view_button)
            table.setCellWidget(row, 3, view_cell)

        show_summary()

    except FileNotFoundError as e:
        result_label.setText(f"파일을 찾을 수 없습니다: {e}")

    except Exception as e:
        result_label.setText(f"검사 실패: {e}")
    finally :
        start_button.setEnabled(True)

def show_summary():
    passed = 0
    failed = 0
    error = 0

    for item in results:
        if item["status"] == "PASSED":
            passed += 1
        elif item["status"] == "FAILED":
            failed += 1
        elif item["status"] == "ERROR":
            error += 1
            

    result_label.setText(f"PASSED: {passed}" + " | " + f"FAILED: {failed}" + " | " + f"ERROR: {error}")

    total_value.setText(str(len(results)))
    passed_value.setText(str(passed))
    failed_value.setText(str(failed))
    error_value.setText(f"ERROR: {error}")

def show_file_details(row):
    item = results[row]

    status = item["status"]
    errors = item["errors"]
    channels = item["Channels"]

    filename_detail.setText(item["filename"])
    filename_detail.setToolTip(item["filename"])
    if channels == 1:
        channels_detail.setText("1 (Mono)")
    elif channels == 2:
        channels_detail.setText("2 (Stereo)")
    else:
        channels_detail.setText(str(channels))
    sample_rate_detail.setText(f"{item['Sample Rate']} Hz")
    bit_depth_detail.setText(f"{item['Bit Depth']} bit")

    validation_message.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    validation_message.setWordWrap(True)

    if status == "PASSED":
        status_color = "#70C99A"
        validation_status.setText("✔  No Errors")
        validation_message.setText("All Checks Passed.")

    elif status == "FAILED":
        status_color = "#E87979"
        validation_status.setText("✖  Errors Found")
        validation_message.setText("\n".join(errors))

    else:
        status_color = "#E5A85B"
        validation_status.setText("✖  ERROR")
        validation_message.setText("에러코드를 확인 해 주세요")

    validation_status.setStyleSheet(f"""
        QLabel {{
            color: {status_color};
            font-size: 13pt;
            font-weight: bold;
            padding: 2px;
        }}
    """)
        # 하단 결과 메시지 갱신
    item_status = item["status"]

    if status == "ERROR":
        result_label.setText("\n".join(errors))
    else:
        show_summary()

def csv_export():
    try:
        csv_export_button.setEnabled(False)
        if not csv_export_browse.text().strip():
                    result_label.setText("저장할 CSV 파일을 선택해 주세요")
                    return

        csv_path = Path(csv_export_browse.text())
        
        if not csv_path.parent.is_dir():
            result_label.setText("존재하지 않는 경로입니다.")
            return

        if not csv_path.suffix:
            csv_path = csv_path.with_suffix(".csv")
            csv_export_browse.setText(str(csv_path))

        elif csv_path.suffix.lower() != ".csv":
            result_label.setText("확장자를 확인해 주세요")
            return

        if not results:
            result_label.setText("내보낼 검사 결과가 없습니다.")
            return

        name_paths = {}

        for item in results:
            name = item["filename"]
            path = item["path"]

            if name not in name_paths:
                name_paths[name] = []

            name_paths[name].append(path)

        result_label.setText("CSV Export 중...")
        app.processEvents()
      
        csv_file = ec(results, name_paths, csv_path)
        result_label.setText(f"CSV Export 완료: {csv_file}")
        

    except Exception as e:
        result_label.setText(f"CSV 저장 실패: {e}")

    finally :
        csv_export_button.setEnabled(True)

def make_section(title, subtitle, content_layout):
    card = QFrame()
    card.setObjectName("card")

    v = QVBoxLayout(card)
    v.setContentsMargins(14, 10, 14, 12)
    v.setSpacing(8)

    title_lbl = QLabel(title)
    title_lbl.setObjectName("sectionTitle")
    sub_lbl = QLabel(subtitle)
    sub_lbl.setObjectName("sectionSub")

    v.addWidget(title_lbl)
    v.addWidget(sub_lbl)
    v.addLayout(content_layout)
    return card

def make_status_badge(status):
    colors = {
        "PASSED": ("#24382D", "#70C99A"),
        "FAILED": ("#3A292B", "#E87979"),
    }
    bg, fg = colors.get(status, ("#3A3322", "#E5A85B"))

    badge = QLabel(status)
    badge.setAlignment(Qt.AlignCenter)
    badge.setStyleSheet(
        f"background-color: {bg}; color: {fg}; border-radius: 10px;"
        "padding: 3px 12px; font-weight: bold;"
    )

    wrap = QWidget()
    h = QHBoxLayout(wrap)
    h.setContentsMargins(0, 0, 0, 0)
    h.addStretch()
    h.addWidget(badge)
    h.addStretch()
    return wrap

def make_field(title, icon_text, combo):
    frame = QFrame()
    frame.setObjectName("field")

    v = QVBoxLayout(frame)
    v.setContentsMargins(10, 8, 10, 10)
    v.setSpacing(6)

    head = QLabel(f"{icon_text}  {title}")
    head.setObjectName("fieldTitle")

    # 콤보 자체의 테두리와 드롭다운 칸 구분선을 없애서 바깥 박스 하나만 보이게 함
    combo.setStyleSheet("""
        QComboBox {
            background-color: #252930;
            color: #E5E9EF;
            border: 1px solid #363A40;
            border-radius: 7px;
            padding: 7px 10px;
        }
        QComboBox::drop-down {
            border: none;
            width: 28px;
        }

        QComboBox QAbstractItemView {
        background-color: #15171B;
        color: #E5E9EF;
        border: 1px solid #2E333B;
        outline: none;
        selection-background-color: #394957;
        selection-color: white;
        }

        QComboBox QAbstractItemView::item:selected {
            background-color: #394957;
            color: white;
            border-left: 3px solid #70C99A;
        }

    """)
    v.addWidget(head)
    v.addWidget(combo)

    return frame


def make_search_icon(color="#E5E9EF", size=16):
    pix = QPixmap(size, size)
    pix.fill(QColor(0, 0, 0, 0))

    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)
    pen = QPen(QColor(color))
    pen.setWidthF(1.8)
    p.setPen(pen)
    p.drawEllipse(2, 2, 9, 9)      # 돋보기 렌즈
    p.drawLine(10, 10, 14, 14)     # 손잡이
    p.end()

    return QIcon(pix)


app = QApplication(sys.argv)

#창 크기 설정
window = QWidget()
window.setObjectName("mainWindow")
window.setWindowTitle("POCKET QA - Audio Asset Inspector")
window.resize(1215, 650)
window.setMinimumSize(680, 420) #최소 창 크기 설정
window.setObjectName("mainWindow") #배경 색 설정

#스타일 추가
window.setStyleSheet("""
    
    QWidget#mainWindow {
        background-color: #17191D;
    }

    QLineEdit, QComboBox {
        background-color: #252930;
        color: #E5E9EF;
        border: 1px solid #363A40;
        border-radius: 9px;
        padding: 9px 11px;
    }

    QLineEdit:focus, QComboBox:focus {
        border: 1px solid #8295A8;
    }

    QPushButton {
        background-color: #303740;
        color: #E5E9EF;
        border: none;
        border-radius: 9px;
        padding: 10px 14px;
        font-weight: 600;
    }

    QPushButton:hover {
        background-color: #414B57;
    }

    QPushButton:pressed {
        background-color: #252930;
    }

    QTableWidget {
        background-color: #202329;
        alternate-background-color: #252930;
        color: #E5E9EF;
        gridline-color: #363A40;
        border: 1px solid #363A40;
        border-radius: 9px;
        selection-background-color: #394957;
        selection-color: white;
    }

    QTableWidget::item {
        border-bottom: 1px solid #303640;
        padding: 6px;
    }
    QHeaderView {
        background-color: #252930;
    }
    QTableCornerButton::section {
        background-color: #252930;
        border: none;
    }

    QHeaderView::section {
        background-color: #252930;
        color: #AAB2BD;
        border: none;
        border-bottom: 1px solid #3A404A;
        padding: 9px;
        font-size: 10pt;
        font-weight: 600;
    }
    
    QLabel {
        color: #E5E9EF;
        background: transparent;
    }

    QFrame#card {
        background-color: #1E2228;
        border: 1px solid #2C313A;
        border-radius: 12px;
    }

    QFrame#totalCard  { background-color: #252B36; border: 1px solid #363E4B; border-radius: 12px; }
    QFrame#passedCard { background-color: #1F2A24; border: 1px solid #2F5A44; border-radius: 12px; }
    QFrame#failedCard { background-color: #2A1F22; border: 1px solid #5A2F36; border-radius: 12px; }

    QLabel#sectionTitle {
        font-size: 12pt;
        font-weight: bold;
    }

    QLabel#sectionSub {
        color: #7D8794;
        font-size: 9pt;
    }
    QFrame#field {
        background-color: #1B1E24;
        border: 1px solid #4A515C;
        border-radius: 10px;
    }

    QLabel#fieldTitle {
        color: #AAB2BD;
        font-size: 9pt;
        font-weight: 600;
    }
    
""")


#전체 레이아웃 생성
layout = QVBoxLayout(window)

#위젯 생성
browse_button = QPushButton("Browse", window)

start_button = QPushButton("▶  START INSPECTION", window)
start_button.setMinimumHeight(44) #스타트 버튼 강조
start_button.setStyleSheet("""
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #2F6BFF, stop:1 #7B4DFF);
        color: white;
        font-size: 11pt;
        font-weight: bold;
        border-radius: 10px;
    }
    QPushButton:disabled {
        background: #3A4150;
    }
""")

result_label = QLabel("검사 결과가 여기에 표시됩니다.", window)

brand_label = QLabel("POCKET QA")
subtitle_label = QLabel("AUDIO ASSET INSPECTOR")
ready_label = QLabel("●  READY")

source_label = QLabel("☷  01.SOURCE DIRECTORY")

settings_title = QLabel("☷  02.INSPECTION SETTINGS")

browse = QLineEdit(window)
browse.setPlaceholderText("Select Audio Folder...")

#Inspection Results 위젯
results_title = QLabel("☷  03.INSPECTION RESULTS")

total_label = QLabel("TOTAL")
passed_label = QLabel("PASSED")
failed_label = QLabel("FAILED")

total_value = QLabel("0")
passed_value = QLabel("0")
failed_value = QLabel("0")
total_caption = QLabel("FILES")
passed_caption = QLabel("FILES")
failed_caption = QLabel("FILES")
for cap in (total_caption, passed_caption, failed_caption):
    cap.setAlignment(Qt.AlignCenter)
total_caption.setStyleSheet("color: #8D9AAE; font-size: 9pt; font-weight: bold;")
passed_caption.setStyleSheet("color: #70C99A; font-size: 9pt; font-weight: bold;")
failed_caption.setStyleSheet("color: #E87979; font-size: 9pt; font-weight: bold;")

error_value = QLabel("ERROR: 0")
error_value.setStyleSheet("""
    QLabel {
        color: #E5A85B;
        font-size: 9pt;
        font-weight: 600;
    }
""")
error_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
#밸류 스타일지정
total_value.setStyleSheet("font-size: 26pt; font-weight: bold;")
passed_value.setStyleSheet("font-size: 26pt; font-weight: bold; color: #8FD6A5;")
failed_value.setStyleSheet("font-size: 26pt; font-weight: bold; color: #E99A9A;")

#가운데 정렬
total_label.setAlignment(Qt.AlignCenter)
total_value.setAlignment(Qt.AlignCenter)
passed_label.setAlignment(Qt.AlignCenter)
passed_value.setAlignment(Qt.AlignCenter)
failed_label.setAlignment(Qt.AlignCenter)
failed_value.setAlignment(Qt.AlignCenter)

#file inspector 위젯
inspector_title = QLabel("☷  04. FILE INSPECTOR")
inspector_subtitle = QLabel("검사된 WAV 파일 목록과 개별 검사 결과입니다.")

#seleted file details 위젯
details_title = QLabel("☷  05. SELECTED FILE DETAILS")
details_subtitle = QLabel("선택한 파일의 상세 정보와 오류 메시지입니다.")

details_frame = QFrame()
details_frame.setStyleSheet("""
    QFrame {
        background-color: #202329;
        border: 1px solid #363A40;
        border-radius: 9px;
    }
""")
details_frame.setFixedHeight(120)

# 왼쪽: 파일 아이콘
file_icon = QLabel("♫")
file_icon.setFixedSize(64, 64)
file_icon.setAlignment(Qt.AlignCenter)
file_icon.setStyleSheet("""
    QLabel {
        background-color: #2B3542;
        color: #7DB8A5;
        border: 1px solid #3B4A59;
        border-radius: 12px;
        font-size: 28pt;
        font-weight: bold;
    }
""")

# 가운데: 파일 상세 정보

filename_detail = QLabel("-")
filename_detail.setWordWrap(False)
filename_detail.setMinimumWidth(0)
filename_detail.setSizePolicy(
    QSizePolicy.Ignored,
    QSizePolicy.Preferred
)


channels_detail = QLabel("-")
sample_rate_detail = QLabel("-")
bit_depth_detail = QLabel("-")

# 오른쪽: 검사 결과
validation_title = QLabel("Validation Result")
validation_title.setStyleSheet("""
    QLabel {
        color: #AAB2BD;
        font-size: 9pt;
        font-weight: bold;
        letter-spacing: 1px;
    }
""")
validation_status = QLabel("No File Selected")
validation_status.setMinimumHeight(28)
validation_status.setStyleSheet("""
    QLabel {
        color: #70C99A;
        font-size: 13pt;
        font-weight: bold;
    }
""")
validation_message = QLabel("파일을 선택해 주세요.")
validation_message.setStyleSheet("""
    QLabel {
        color: #AAB2BD;
        font-size: 9pt;
    }
""")
validation_message.setWordWrap(True)

#export 위젯
export_title = QLabel("☷  06. EXPORT REPORT")
export_subtitle = QLabel("검사 결과를 CSV 파일로 저장하세요.")
export_title.setStyleSheet("""
    QLabel {
        color: #E5E9EF;
        font-size: 11pt;
        font-weight: bold;
    }
""")


#헤더 부분

#브랜드 레이아웃
brand_layout = QVBoxLayout()
brand_layout.addWidget(brand_label)
brand_layout.addWidget(subtitle_label)

#헤더 레이아웃 | 브랜드 레이아웃과 레디라벨추가
header_layout = QHBoxLayout()
header_layout.addLayout(brand_layout)
header_layout.addStretch()
header_layout.addWidget(ready_label)

#레이아웃에 헤더 추가
layout.addLayout(header_layout)

#위젯 디자인 설정
brand_label.setStyleSheet("""
    color: #E5E9EF;
    font-size: 18pt;
    font-weight: bold;
""")

subtitle_label.setStyleSheet("""
    color: #929BA7;
    font-size: 8pt;
    letter-spacing: 2px;
""")

ready_label.setStyleSheet("""
    color: #8FD6A5;
    background-color: #24382D;
    border-radius: 8px;
    padding: 6px 12px;
    font-weight: bold;
""")



#중간 부분
sample_rate_box = ArrowComboBox()
sample_rate_box.addItem("44100 Hz", 44100)
sample_rate_box.addItem("48000 Hz", 48000)
sample_rate_box.addItem("96000 Hz", 96000)
sample_rate_label = QLabel("Sample Rate")

bit_depth_box = ArrowComboBox()
bit_depth_box.addItem("16 bit", 16)
bit_depth_box.addItem("24 bit", 24)
bit_depth_box.addItem("32 bit", 32)
bit_depth_label = QLabel("Bit Depth")

csv_browse_button = QPushButton("Browse", window)
# csv_browse_button 스타일
csv_browse_button.setStyleSheet("""
    QPushButton {
        background-color: #303640;
        color: #E5E9EF;
        border: 1px solid #454D59;
        border-radius: 7px;
        padding: 8px 12px;
    }

    QPushButton:hover {
        background-color: #3B4552;
    }
""")

csv_export_button = QPushButton("⬇  Export CSV", window)
# csv_export_button 스타일
csv_export_button.setMinimumHeight(40)
csv_export_button.setStyleSheet("""
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #2F6BFF, stop:1 #7B4DFF);
        color: white;
        font-weight: bold;
        border-radius: 9px;
        padding: 8px 16px;
    }
    QPushButton:disabled {
        background: #3A4150;
    }
""")

csv_export_browse = QLineEdit(window)
# csv_export_browse 스타일
csv_export_browse.setStyleSheet("""
    QLineEdit {
        background-color: #202329;
        color: #E5E9EF;
        border: 1px solid #363A40;
        border-radius: 7px;
        padding: 8px;
    }
""")
csv_export_browse.setPlaceholderText("Export Location...")


#브라우즈 레이아웃
controls_layout = QHBoxLayout()
controls_layout.addWidget(browse)
controls_layout.addWidget(browse_button)
controls_layout.setSpacing(8)

# 좌우 두 열
columns = QHBoxLayout()
left_col = QVBoxLayout()
right_col = QVBoxLayout()
columns.addLayout(left_col)
columns.addLayout(right_col)
columns.setSpacing(10)
columns.setStretch(0, 1)
columns.setStretch(1, 1)
layout.addLayout(columns)

left_col.addWidget(make_section(
    "01. Source Directory", "검사할 오디오 폴더를 선택하세요.", controls_layout
))




#인스펙션 레이아웃
sample_rate_field = make_field("Sample Rate", "▂▄▆", sample_rate_box)
bit_depth_field = make_field("Bit Depth", "⠿", bit_depth_box)

settings_layout = QHBoxLayout()
settings_layout.addWidget(sample_rate_field)
settings_layout.addWidget(bit_depth_field)
settings_layout.setSpacing(12)

inspection_layout = QVBoxLayout()
inspection_layout.addLayout(settings_layout)
inspection_layout.addWidget(start_button)
inspection_layout.setSpacing(10)

left_col.addWidget(make_section(
    "02. Inspection Settings", "검사 설정을 지정하세요.", inspection_layout
))

#results 레이아웃
total_frame = QFrame()
total_frame.setObjectName("totalCard")
total_card = QVBoxLayout(total_frame)
total_card.setContentsMargins(12, 12, 12, 12)
total_card.setSpacing(6)
total_card.addWidget(total_label)
total_card.addWidget(total_value)
total_card.addWidget(total_caption)

passed_frame = QFrame()
passed_frame.setObjectName("passedCard")
passed_card = QVBoxLayout(passed_frame)
passed_card.setContentsMargins(12, 12, 12, 12)
passed_card.setSpacing(6)
passed_card.addWidget(passed_label)
passed_card.addWidget(passed_value)
passed_card.addWidget(passed_caption)

failed_frame = QFrame()
failed_frame.setObjectName("failedCard")
failed_card = QVBoxLayout(failed_frame)
failed_card.setContentsMargins(12, 12, 12, 12)
failed_card.setSpacing(6)
failed_card.addWidget(failed_label)
failed_card.addWidget(failed_value)
failed_card.addWidget(failed_caption)

results_card = QHBoxLayout()
results_card.addWidget(total_frame)
results_card.addWidget(passed_frame)
results_card.addWidget(failed_frame)
results_card.setSpacing(10)
# 프레임 너비 비율로 맞추기
results_card.setStretch(0, 1)
results_card.setStretch(1, 1)
results_card.setStretch(2, 1)


result_layout = QVBoxLayout()
result_layout.addLayout(results_card)   # 결과 카드가 남는 높이를 사용
result_layout.addWidget(error_value)
result_layout.setSpacing(8)

left_col.addWidget(make_section(
    "03. Inspection Results", "검사 결과 요약입니다.", result_layout
), 1)   # 남는 높이를 03 카드가 차지

#file inspector 레이아웃
table = InspectorTable(0, 4, window)
table.setMinimumHeight(150)
table_header = table.horizontalHeader()

table.setHorizontalHeaderLabels([
    "Filename",
    "Status",
    "Sample Rate",
    "",
])

table.setEditTriggers(QAbstractItemView.NoEditTriggers)
table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
table.verticalHeader().setDefaultSectionSize(42)
table.setAlternatingRowColors(True)
table.setShowGrid(False)
table.verticalHeader().setVisible(False)
table.setCornerButtonEnabled(False)
table.setSelectionMode(QAbstractItemView.NoSelection)
table.setFocusPolicy(Qt.NoFocus)

# 컬럼 너비는 InspectorTable의 resizeEvent에서 관리
table_header.setSectionResizeMode(QHeaderView.Interactive)
table_header.setFixedHeight(36)
table_header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

inspector_layout = QVBoxLayout()
inspector_layout.addWidget(table)
inspector_layout.setSpacing(8)

# item = QTableWidgetItem(item_data)
# item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

right_col.addWidget(make_section(
    "04. File Inspector", "검사된 WAV 파일 목록과 개별 검사 결과입니다.", inspector_layout
), 1)
# 인덱스: 0 헤더, 1~6 섹션 01~06, 7 result_label
layout.setStretch(0, 0)   # 헤더
layout.setStretch(1, 1)   # 좌우 두 열 (남는 높이 사용)
layout.setStretch(2, 0)   # result_label

# selected file details 위젯
# 왼쪽: 파일 아이콘
icon_layout = QVBoxLayout()
icon_layout.addWidget(file_icon)

# 가운데: 키-값 그리드
details_grid = QGridLayout()
details_grid.setHorizontalSpacing(6)
details_grid.setVerticalSpacing(6)
detail_rows = [
    ("Filename", filename_detail),
    ("Channels", channels_detail),
    ("Sample Rate", sample_rate_detail),
    ("Bit Depth", bit_depth_detail),
]
for r, (key, value_label) in enumerate(detail_rows):
    key_label = QLabel(key)
    key_label.setStyleSheet("color: #7D8794;")
    key_label.setFixedWidth(84)

    colon = QLabel(":")
    colon.setFixedWidth(10)
    colon.setAlignment(Qt.AlignCenter)

    value_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    details_grid.addWidget(key_label, r, 0)
    details_grid.addWidget(colon, r, 1)
    details_grid.addWidget(value_label, r, 2)

# 값 열만 남는 공간을 차지하게 해서 키와 콜론을 붙여 둠
details_grid.setColumnStretch(0, 0)
details_grid.setColumnStretch(1, 0)
details_grid.setColumnStretch(2, 1)
details_grid.setAlignment(Qt.AlignTop)
# 오른쪽: 검사 결과
validation_layout = QVBoxLayout()
validation_layout.addWidget(validation_status)
validation_layout.addWidget(validation_message)
validation_layout.addStretch()

details_content_layout = QHBoxLayout()
details_content_layout.addLayout(icon_layout)
details_content_layout.addLayout(details_grid)
details_content_layout.addLayout(validation_layout)
details_content_layout.setStretch(0, 2)
details_content_layout.setStretch(1, 5)
details_content_layout.setStretch(2, 3)
details_content_layout.setSpacing(16)

right_col.addWidget(make_section(
    "05. Selected File Details", "선택한 파일의 상세 정보와 오류 메시지입니다.", details_content_layout
))

csv_layout = QHBoxLayout()
csv_layout.addWidget(csv_export_browse)
csv_layout.addWidget(csv_browse_button)
csv_layout.addWidget(csv_export_button)
csv_layout.setSpacing(8)

right_col.addWidget(make_section(
    "06. Export Report", "검사 결과를 CSV 파일로 저장하세요.", csv_layout
))

# 메시지 표시용 라벨을 화면에 추가 (현재는 빠져 있음)
layout.addWidget(result_label)


def select_folder(): #브라우즈버튼 누르면 뜨는 함수
    folder = QFileDialog.getExistingDirectory() #폴더지정
    if folder:
        browse.setText(folder)

def select_csv_file(target): #CSV 브라우즈버튼 누르면 뜨는 함수
    file_path, selected_filter = QFileDialog.getSaveFileName(
        window,
        "CSV 저장",
        "",
        "CSV Files (*.csv)"
    )

    if file_path:
        csv_export_browse.setText(file_path)

browse_button.clicked.connect(select_folder)
start_button.clicked.connect(scan_audio)

csv_browse_button.clicked.connect(lambda: select_csv_file(csv_export_browse))
csv_export_button.clicked.connect(csv_export)

# table.itemSelectionChanged.connect(show_error)

window.show()

sys.exit(app.exec())