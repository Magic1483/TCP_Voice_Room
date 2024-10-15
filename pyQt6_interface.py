from PyQt6.QtCore import Qt,QSize
from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QHBoxLayout,QLineEdit,QVBoxLayout,QPushButton,QMainWindow,QComboBox,QTextBrowser
import sys
import PyQt6
import threading
from client import TCP_CLIENT
from text_client import TextClient
import queue


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        layout = QHBoxLayout()
        self.setFixedSize(QSize(800, 600))
        self.client = "127.0.0.1:6000"

        self.setWindowTitle('Call TCP system')
        self.is_calling = False
        self.input_message_queue = queue.Queue()

        chat_layout = QVBoxLayout()
        self.chat = QTextBrowser()
        self.chat.setBaseSize(400,30)
        self.chat.setStyleSheet('font-size: 16px')
        self.chat_input = QLineEdit()
        self.chat_input.setFixedHeight(50)
        self.chat_input.setStyleSheet('font-size: 16px')
        send_btn = QPushButton("Send")


        chat_layout.addWidget(QLabel('Chat'))
        chat_layout.addWidget(self.chat)
        ch = QHBoxLayout()
        ch.addWidget(self.chat_input,stretch=3)
        ch.addWidget(send_btn,stretch=1)
        chat_layout.addLayout(ch)

        self.text_style = 'font-size: 20px'
        self.chat_style = 'font-size: 15px'

        # chat_layout.addWidget(chat_input)



        server_layout = QVBoxLayout()
        
        self.server_addr = QLineEdit(self.client)
        
        self.client_name = QLineEdit()
        self.client_name.setPlaceholderText('Your name')
        self.call_button = QPushButton("call")

        server_layout.addWidget(QLabel('Server addr :-D'),alignment=Qt.AlignmentFlag.AlignBottom)
        server_layout.addWidget(self.client_name)
        server_layout.addWidget(self.server_addr)
        server_layout.addWidget(self.call_button)


        send_btn.clicked.connect(self.SendMsg)
        self.call_button.clicked.connect(self.CallHandle)
        
        layout.addLayout(server_layout,stretch=1)
        layout.addLayout(chat_layout,stretch=2)
        

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        #--------------------------
        

        # self.audio_client = AudioClient()
    
    def SendMsg(self):
        if self.chat_input.text() != "" and self.client_name.text() != "":
            self.InsertMessage(self.client_name.text(),self.chat_input.text())
            self.TextChat.Send(self.chat_input.text())
            self.chat_input.clear()
    

    def InsertMessage(self,user,text):
        self.chat.setFontPointSize(20)
        self.chat.insertPlainText(f'{user}:{text}\n')

    def CallHandle(self):
        if self.client_name.text() != "":
            if not self.is_calling:
                self.is_calling = True
                host,port = self.server_addr.text().split(':')
                self.call_client = TCP_CLIENT(host,6000)
                # self.TextChat = TextClient(self.client_name.text(),self.input_message_queue,host,6060)
                # threading.Thread(target=self.TextInputThread,name='TextInputThread').start()
                self.InsertMessage(self.client_name.text(),'Connected to server')
                self.call_button.setText('Hang out :-(')
                
            else:
                self.is_calling = False
                self.call_client.stop()
                # self.TextChat.stop()
                self.call_button.setText('Call')
                


        # call_th = threading.Thread(target=self.audio_client.run)
        # call_th.name = 'call thread'
        # call_th.start()
        # print('try call to',self.client)
    
    def TextInputThread(self):
        while self.is_calling == True:
            
            if not self.input_message_queue.empty():
                data = self.input_message_queue.get()
                print(data)
                self.InsertMessage(data['user'],data['data'])
        print('stop TextThread')
    
    def closeEvent(self,e):
        print('close window')
        self.is_calling = False
        try:
            self.call_client.stop()
            self.TextChat.stop()
        except: pass

        for thread in threading.enumerate(): 
            print(thread.name)

    

        

app = QApplication(sys.argv)

window = MainWindow()
window.setStyleSheet('background-color:#7d4698;color:#fabc23;font-size: 20px')
window.show()

app.exec()
