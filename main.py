﻿from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebChannel import QWebChannel
import time, threading
import os,sys;  sys.path.append('data')

import moban, data, user, config

#————————————————————————————
#接受gui回传的信息
class CallHandler(QObject):
    @pyqtSlot(str)
    def rec(self,x):
        view.page().runJavaScript(
            '''
            data=['%s','%s','%s','%s','%s','%d','%s'];
            set_data();
            all_kiri=%d;
            更新切数()
            '''
            %
            (data.gen_ques()   +   (len(data.kiri),)  )
            # ('じょうか','恐惧','净化','三','四',2(正解位置),'浄化'(写法))
        )
    @pyqtSlot(str)
    def kiri(self,s):
        data.kiri[s]=1
        view.page().runJavaScript(
            '''
            all_kiri=%d;
            更新切数()
            '''
            %
            len(data.kiri)
        )
        
#————————————————————————————
#窗口界面
class my_view(QWebEngineView):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        moban.tp('index.html','final.html',bg=data.gen_bg(),user=user.name,word_dict=config.word_dict)
        self.p=self.page()
        self.p.setWebChannel(channel)
        self.load(QUrl('file:///html/final.html'))
        self.resize(1366,768)
        self.show()
        # self.showFullScreen()
        t = threading.Thread(target=self.size_fix)
        t.setDaemon(True)
        t.start()
        
    def size_fix(self):
        while True:
            self.p.setZoomFactor(self.width()/1366)
            time.sleep(0.15)
pass
pass
pass
pass
'nya'
pass

if __name__=='__main__':
    app = QApplication([])
    
    channel = QWebChannel()
    handler = CallHandler()
    channel.registerObject('handler', handler)
    
    view = my_view()
    
    app.exec_()
    
    data.kiri_save()