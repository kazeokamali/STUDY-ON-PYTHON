from PyQt5.QtWidgets.QWidget import window


import sys
import time

from time import ctime
from datetime import datetime, timedelta

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QTextEdit, QMainWindow, QHBoxLayout, \
    QVBoxLayout, QMessageBox


class W_make(QWidget):
    def __init__(self):
        super().__init__()
        self.text = QTextEdit(self)

        self.text.setReadOnly(True)

        self.initUI()

        self.start_time = None
        self.end_time = None
        self.time_past = []
        self.time_left = None
        self.totaltime = timedelta(hours=9)
        self.sum_time = timedelta()
        self.zerotime = timedelta()
        self.current = None
        self.timerecor = None
        self.last_button = None
        self.work_total = timedelta()
        self.get_day = None



    def initUI(self):

        QToolTip.setFont(QFont('sanserif',14))

        self.get_day = datetime.now()

        self.btn1 = QPushButton('start \U0001F622',self)
        self.btn2 = QPushButton('end \U0001F3C3',self)
        self.btn3 = QPushButton('calcu \U0001F553',self)
        self.btn4 = QPushButton('record date \U0001F512',self)

        self.btn1.setToolTip('Work begin')
        self.btn2.setToolTip('take a break')

        self.btn1.resize(self.btn1.sizeHint())
        self.btn2.resize(self.btn2.sizeHint())
        self.btn3.resize(self.btn2.sizeHint())
        self.btn4.resize(self.btn2.sizeHint())


        self.btn1.clicked.connect(self.click_startbtn)
        self.btn2.clicked.connect(self.click_endtime)
        self.btn3.clicked.connect(self.calculate_time)
        self.btn4.clicked.connect(self.record_daily)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.btn1)
        hbox.addWidget(self.btn2)
        hbox.addWidget(self.btn3)
        hbox.addWidget(self.btn4)

        vbox = QVBoxLayout()
        vbox.addWidget(self.text)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(500,500,350,300)
        self.setWindowTitle('丰川祥子模拟器')
        self.text.append(f'Today:{self.get_day.year}-{self.get_day.month}-{self.get_day.day} \n')
        self.show()

# 实现记录start_time，排除12-14点
    def click_startbtn(self):
        self.current = None
        self.last_button = "start"
        self.timerecor = datetime.now()

        delta1 = self.timerecor.hour - 14
        delta2 = self.timerecor.hour - 12

        if delta1 < 0 and delta2 > 0:
            self.start_time =  datetime(year = self.start_time.year, month = self.start_time.month, day = self.start_time.day, hour = 14)
        else:
            self.start_time = self.timerecor

        exact_time = ctime()
        self.text.append('上班work：')
        self.text.append(exact_time)

# 实现计算与start按下后的时间间隔
    def click_endtime(self):
        self.last_button = "end"
        self.end_time = datetime.now()

        delta1 = self.end_time.hour - 14
        delta2 = self.end_time.hour - 12

        if delta1< 0 and delta2 > 0:
            self.end_time = datetime(year = self.end_time.year, month = self.end_time.month, day = self.end_time.day, hour = 12)

        self.time_past.append(self.end_time - self.start_time)
        exact_time = ctime()
        self.text.append('休息rest:')
        self.text.append(exact_time)
        self.text.append(f'下班啦！本次打卡：{self.time_past[-1]} \n')


# 计算剩余时长，总work时长
    def calculate_time(self):
        self.sum_time = timedelta()
        for i in self.time_past:
            self.sum_time += i

        self.current = datetime.now()
        if self.last_button != "end":
            self.sum_time += self.current - self.start_time

        self.work_total = self.sum_time
        self.text.append('总打卡时长：' + str(self.work_total))


        left_time = self.totaltime - self.sum_time
        if left_time >= self.zerotime:
            QMessageBox.information(self, "Time Left", "The left time is: " + str(left_time))
        else:
            QMessageBox.information(self,"time over!", "dont work over time")


# 实现日志
    def record_daily(self):
        lines_set = set()
        try:
            with open('daily_recording.txt','a+',encoding='gbk') as f:
                f.seek(0)
                for line in f:
                    lines_set.add(line.strip())
                if self.text.toPlainText() not in lines_set:
                    f.write(self.text.toPlainText() + '\n')
        except Exception as e:
            print(f"Error occurred: {e}")

# 退出询问
    def closeEvent(self, a0):
        reply = QMessageBox.question(self,'Exit_confirm',"U sure to exit?",
                                     QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            a0.accept()
        else:
            a0.ignore()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = W_make()
    sys.exit(app.exec_())

'''
实现了计时打卡，计算剩余时间，考虑了12-14之间的不计时
未实现打印成表并存储于文本或表格中，无日志功能(已实现）
未实现生成exe运行，需在编译器中run
未实现查找当天最后一次总打卡，每次退出程序需重新计时9hours

'''
