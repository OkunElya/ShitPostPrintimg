
import socket
import cv2
import numpy as np
from time import sleep
def minmax(v):
    if v > 255:
        v = 255
    if v < 0:
        v = 0
    return v


def dithering_gray(inMat, samplingF):
   
    h = inMat.shape[0]
    w = inMat.shape[1]
    
    for y in range(0, h-1):
        for x in range(1, w-1):
           
            old_p = inMat[y, x]
            new_p = np.round(samplingF * old_p/255.0) * (255/samplingF)
            inMat[y, x] = new_p
            
            quant_error_p = old_p - new_p
            
            inMat[y, x+1] = minmax(inMat[y, x+1] + quant_error_p * 7 / 16.0)
            inMat[y+1, x-1] = minmax(inMat[y+1, x-1] + quant_error_p * 3 / 16.0)
            inMat[y+1, x] = minmax(inMat[y+1, x] + quant_error_p * 5 / 16.0)
            inMat[y+1, x+1] = minmax(inMat[y+1, x+1] + quant_error_p * 1 / 16.0)

    return inMat
def magic(in_:bytes):
    counter=0
    based=""
    ext=b''
    for b in in_:
        if int(b)>128:
           based+="0"
        else:
            based+="1"
        counter+=1
        if counter==8:
            ext+=bytearray([int(based,base=2)])
            based=""
            counter=0
    return(ext)
class WebPrinter():
    def __init__(self,address) -> None:
        super().__init__()
        self.printerSocket=socket.socket()
        self.address=address
        self.printerSocket.connect((self.address,9100))
        self.esc=bytes.fromhex('1B')
    def reconnect(self):
        print("reconecting")
        try:
            self.printerSocket.close()
        except:
            print("socket is closed already")
        self.printerSocket=socket.socket()
        self.printerSocket.connect((self.address,9100))
        sleep(1)
        
    def send(self,text:bytes):
        self.printerSocket.send(text)
    def hT(self):
        '''Horisontal tab'''
        self.send(bytes.fromhex("09"))
    def lineFeed(self):
        self.send(bytes.fromhex('0A'))
    def formFeed(self):
        '''This commands prints all data collected in the printer buffer In page mode. After completion of printing, the printer is
returned to standard mode.'''
        self.send(bytes.fromhex('0C'))
    def cut(self):
        self.send(bytes.fromhex('1B69'))
    def carrigeReturn(self):
        '''This command prints the data. With auto line feed enabled, it performs printing and one line feeding same as LF.
'''
        self.send(bytes.fromhex('0D'))
    def can(self):
        '''This command clears the receive buffer and print buffers in page mode'''
        self.send(bytes.fromhex('18'))
    def transmitRtStatus(self,n:int):
        self.send(bytes.fromhex('1004'))
        self.send(bytearray([n]))
    def generatePulse(self,pin:int,time:int):
        '''time from 1 to 8     pin 0 is 2 and 1 is 5 Upon receiving this command, the printer outputs the drive pulse to the specified connector pin ■ The real time command is stored into the receive buffer and executed with higher priority than other commands'''
        self.send(bytes.fromhex('1014'))
        self.send(bytearray([1]))
        self.send(bytearray([pin]))
        self.send(bytearray([time]))
    def underline(self,mode:bool):
        mode=int(mode)
        self.send(bytes.fromhex("1B2D"))
        self.send(bytearray([mode]))
    def bwReverse(self,mode:bool):
        mode=int(mode)
        self.send(bytes.fromhex("1D42"))
        self.send(bytearray([mode]))
    def emphrazeMode(self,mode:bool):
        mode=int(mode)
        self.send(bytes.fromhex("1B45"))
        self.send(bytearray([mode]))
    def doubleStrike(self,mode:bool):
        mode=int(mode)
        self.send(bytes.fromhex("1B47"))
        self.send(bytearray([mode]))
    def aFontB(self,mode:bool):
        mode=int(mode)
        self.send(bytes.fromhex("1B4D"))
        self.send(bytearray([mode]))
    def fontSelector(self,fontType):
        '''
            0b00000000
            fontA fontB|
            NE EBU|
            NE EBu|
            Emode OFF Emode ON|
            DH OFF DH ON| 
            DW OFF DW ON| 
            Reverse NE EBU| 
            UnderlineOFF UnderlineONN|
        '''
        
        self.send(bytes.fromhex('1B21'))
        self.send(fontType)
    def print(self,text:str):
        self.send(text.encode("ASCII"))
    def printR(self,text:str):
        self.send(text.encode("CP866"))
    def prepareImg(self,imgArr,sizeX,sizeY,F=1):
        img=cv2.resize(imgArr,[sizeX,sizeY])
        #_,img= cv2.threshold(img,128,255,cv2.THRESH_BINARY_INV)
        img=dithering_gray(img,F)
        img=bytearray(img.flatten())
        img=magic(img)
        return img,sizeX,sizeY
    def initialize(self):
        self.send(bytes.fromhex("1B40"))
    def setLineSpacing(self,spacing:int):
        self.send(self.esc)
        self.send(bytearray([spacing]))
    def printRastrImage(self,sugoma):
        img,sizeX,sizeY=sugoma
        sizeX//=8
        Wl=sizeX%256
        Wh=(sizeX-(sizeX%256))/256
        Hl=sizeY%256
        Hh=(sizeY-(sizeY%256))/256

        self.send(bytes.fromhex("1D763030"))
        self.send(bytearray([Wl]))
        self.send(bytearray([int(Wh)]))
        self.send(bytearray([Hl]))
        self.send(bytearray([int(Hh)]))
        self.send(img)
    def loadImage(self,sugoma):
        #[xSize 0 Ysize 0 ]
        img,sizeX,sizeY=sugoma
        sizeX//=8
        
        Nl=sizeX%256
        Nh=(len(img)-(len(img)%256))/256
        Wl=sizeX%256
        Wh=(sizeX-(sizeX%256))/256
        Hl=sizeY%256
        Hh=(sizeY-(sizeY%256))/256
        self.send(bytes.fromhex("1B2A"))#selext bit-image specefying mode
        self.send(bytearray([0]))
        self.send(bytearray([Nl]))
        self.send(bytearray([int(Nh)]))
        
        self.send(bytes.fromhex("1C71"))
        self.send(bytearray([1]))
        self.send(bytearray([Wl]))
        self.send(bytearray([int(Wh)]))
        self.send(bytearray([Hl]))
        self.send(bytearray([int(Hh)]))
        self.send(img)
        # self.initialize()
        # self.setLineSpacing(24)
        
        
        # self.send(bytearray([33]))#density selection
        # self.send(sizeX)#send image dimensions
        # self.send(sizeY)#YES
        # self.send(bytes.fromhex("1C71"))#load image command
        # self.send(bytearray([1]))#bytearray([2])
        # self.send(sizeX)
        # self.send(sizeY)
        # self.send(img)
    def printImage(self):
        self.send(bytes.fromhex("1C70"))
        self.send(bytearray([1]))
        self.send(bytearray([0]))
    
    def __del__(self):
        self.printerSocket.close()
class QRcode():
    def __init__(self,P):
        self.size=3
        self.model=50#49
        self.errorCorrectionLevel=49
        self.P=P
    def setSize(self,size=3):
        self.size=size
    
    def applyModel(self):
        self.P.send(bytes.fromhex("1D286B04003141"))#GS ( k pL pH cn fn 
        self.P.send(bytearray([self.model]))
        self.P.send(bytearray([0]))
    def applySize(self):
        '''size is variating from 1 to 8'''
        self.P.send(bytes.fromhex("1D286B03003143"))#GS ( k pL pH cn fn 
        self.P.send(bytearray([self.size]))
    def applyErrorCorrectionLevel(self):
        ''' variating from 48 to 51'''
        self.P.send(bytes.fromhex("1D286B03003145"))#GS ( k pL pH cn fn 
        self.P.send(bytearray([self.errorCorectionLevel]))
    def loadText(self,text:str):
        tl=len(text)+3
        pl=tl%256
        ph=(tl-(tl%256))/256
        self.P.send(bytes.fromhex("1D286B"))
        self.P.send(bytearray([pl]))
        self.P.send(bytearray([int(ph)]))
        self.P.send(bytes.fromhex("315030"))
        self.P.print(text)
    def print(self):
        self.P.send(bytes.fromhex("1D286B0300315130"))




