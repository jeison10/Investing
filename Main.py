from Procurador import searcher
#from PyQt5.QtWidgets import QApplication, QPushButton, QTextBrowser, QMainWindow
#from PyQt5.QtCore import QThread
from PyQt5 import uic, QtGui, QtWidgets, QtCore
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time


 
class minhaTarefa2(QtCore.QThread):
    
    valorBTCminEnvia=QtCore.pyqtSignal(str)
    valorBTCmaxEnvia=QtCore.pyqtSignal(str)
    valorBTCatualEnvia=QtCore.pyqtSignal(str)
    msg=QtCore.pyqtSignal(str)


    def __init__(self, user, senha,analise,tempoAnalise):
        super(minhaTarefa2, self).__init__()
        #self.user= user
        #self.senha= senha
        self.user= 'jeison10@msn.com'
        self.senha= 'Je88061149'
        self.analise=analise
        self.tempoAnalise=tempoAnalise
        self.valorBTCmin=float(500000)
        self.valorBTCmax=float(0)

    def run(self):
        
        self.navegador = webdriver.Chrome()
        time.sleep(3)
        os.system('cls') or None

        self.navegador.get("https://www.novadax.com.br/login?return_path=/")
        time.sleep(1)
        self.navegador.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div/div/div[2]/div[1]/div[2]/input').click()
        self.navegador.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div/div/div[2]/div[1]/div[2]/input').send_keys(self.user)
        self.navegador.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div/div/div[3]/div/div[1]/div[2]/input').click()
        self.navegador.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div/div/div[3]/div/div[1]/div[2]/input').send_keys(self.senha)
        self.navegador.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div/div/button').click()
        time.sleep(4)

        # a partir daqui começa monitoramento do bitCoin
        
        self.navegador.find_element_by_xpath('/html/body/div[1]/div[1]/header/div/div[1]/div[1]/div[1]/span').click()
        self.navegador.find_element_by_xpath('/html/body/div[1]/div[1]/header/div/div[1]/div[1]/div[2]/a[2]/div/p[2]').click()
        time.sleep(5)

        cont=0
        if (self.analise==1):
            while (cont<int(self.tempoAnalise)):  
                envia="Iniciando análise dos ativos"
                self.msg.emit(envia)  
                self.precoBTC=self.navegador.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div').text
                self.precoBTC1=str(self.precoBTC).replace(".","")           
                self.precoBTC2=str(self.precoBTC1).replace(",",".")
                print ("O preço atual do BitCoin é:" + (self.precoBTC2))
                if (float(self.precoBTC2) < self.valorBTCmin):
                     self.valorBTCmin =  float(self.precoBTC2)
                if (float(self.precoBTC2) > self.valorBTCmax):
                     self.valorBTCmax = float(self.precoBTC2)

                self.porcBTCdif=round(100-((self.valorBTCmin*100)/self.valorBTCmax),2)


                print (f"O preço minimo do durante a análise é:" + str(self.valorBTCmin))
                print (f"O preço máximo do BitCoin é:" + str(self.valorBTCmax))
                print (f"A diferença entre o maximo e o mínimo é:"+ str(self.porcBTCdif) + "%")

                envia=str(self.valorBTCmin)
                self.valorBTCminEnvia.emit(envia)
                envia=str(self.valorBTCmax)
                self.valorBTCmaxEnvia.emit(envia)
                envia=str(self.precoBTC2)
                self.valorBTCatualEnvia.emit(envia)

                time.sleep(2)
                cont=cont + 1
            envia="Análise concluida no tempo programado"
            self.msg.emit(envia)  

        else:
            envia="Site da corretora aberto, análise desabilitada"
            self.msg.emit(envia)
            
     
class minhaTarefa(QtCore.QThread):
    
    valor_preco_ETH=QtCore.pyqtSignal(str)
    valor_porc_ETH=QtCore.pyqtSignal(str)
    valor_preco_BIT=QtCore.pyqtSignal(str)
    valor_porc_BIT=QtCore.pyqtSignal(str)
    msg=QtCore.pyqtSignal(str)


    def run(self):
        proc=searcher()

        cnt=str(proc.precoE)
        self.valor_preco_ETH.emit(cnt)

        cnt=str(proc.percentE)
        self.valor_porc_ETH.emit(cnt)

        cnt=str(proc.precoB)
        self.valor_preco_BIT.emit(cnt)

        cnt=str(proc.percentB)
        self.valor_porc_BIT.emit(cnt)

        cnt=proc.msg
        self.msg.emit(cnt)


             

class ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(ui,self).__init__()
        uic.loadUi("primeiro.ui",self)
        self.botao=self.findChild(QtWidgets.QPushButton,"pushButton")
        self.botao2=self.findChild(QtWidgets.QPushButton,"pushButton_2")
        self.escrev=self.findChild(QtWidgets.QTextBrowser,"textBrowser")
        self.mostraPrecoE=self.findChild(QtWidgets.QLabel,"label_2")
        self.mostraPorcE=self.findChild(QtWidgets.QLabel,"label_3")
        self.mostraPrecoB=self.findChild(QtWidgets.QLabel,"label_4")
        self.mostraPorcB=self.findChild(QtWidgets.QLabel,"label_5")
        self.executaAnaliseSIM=self.findChild(QtWidgets.QCheckBox,"checkBox")
        self.executaAnaliseNAO=self.findChild(QtWidgets.QCheckBox,"checkBox_2")

        self.entraUser=self.findChild(QtWidgets.QLineEdit,"lineEdit")
        self.entraSenha=self.findChild(QtWidgets.QLineEdit,"lineEdit_2")

        self.mostraMinBTC=self.findChild(QtWidgets.QLineEdit,"lineEdit_5")
        self.mostraMaxBTC=self.findChild(QtWidgets.QLineEdit,"lineEdit_4")
        self.mostraAtualBTC=self.findChild(QtWidgets.QLineEdit,"lineEdit_3")
        self.tempoAnalise=self.findChild(QtWidgets.QLineEdit,"lineEdit_6")

        self.botao.clicked.connect(self.botaoFunc)
        self.botao2.clicked.connect(self.botao2Func)

        self.executaAnaliseNAO.toggled.connect(self.analiseNao)
        self.executaAnaliseSIM.toggled.connect(self.analiseSim)
        
        self.show()

    def botaoFunc(self):
        self.escrev.setText('Pesquisando')
        self.thread=minhaTarefa()
        self.thread.start()

        self.thread.valor_preco_ETH.connect(self.setaPrecoE) 
        self.thread.valor_porc_ETH.connect(self.setaPorcE)
        self.thread.valor_preco_BIT.connect(self.setaPrecoB)
        self.thread.valor_porc_BIT.connect(self.setaPorcB)
        self.thread.msg.connect(self.mostraMsg)
        
        self.thread.quit()

        
    def botao2Func(self):
       
                     
        self.escrev.setText('Acessando site da corretora')
        self.thread=minhaTarefa2(self.entraUser.text(),self.entraSenha.text(),self.analise,self.tempoAnalise.text())
        self.thread.start()
        self.thread.valorBTCminEnvia.connect(self.setaPrecoMinBtc)
        self.thread.valorBTCmaxEnvia.connect(self.setaPrecoMaxBtc)
        self.thread.valorBTCatualEnvia.connect(self.setaPrecoAtualBtc)
        self.thread.msg.connect(self.mostraMsg)
      

    def analiseSim(self):
        self.analise=1
        self.executaAnaliseNAO.setChecked(False)
    
    def analiseNao(self):
        self.analise=0
        self.executaAnaliseSIM.setChecked(False)
               
    def setaPrecoE(self,valor):
        self.mostraPrecoE.setText(valor)

    def setaPorcE(self,valor):
        self.mostraPorcE.setText(valor)
    
    def setaPrecoB(self,valor):
        self.mostraPrecoB.setText(valor)

    def setaPorcB(self,valor):
        self.mostraPorcB.setText(valor)

    def mostraMsg(self,valor):
        self.escrev.setText(valor)

    def setaPrecoMinBtc(self,valor):
        self.mostraMinBTC.setText(valor)
    
    def setaPrecoMaxBtc(self,valor):
        self.mostraMaxBTC.setText(valor)

    def setaPrecoAtualBtc(self,valor):
        self.mostraAtualBTC.setText(valor)
      

app = QtWidgets.QApplication(sys.argv)
uiWindow=ui()
app.exec()
#janela.pushButton.clicked.connect(botao1)























