###################################
PrinterIp="10.254.252.101" 
UserId=1276029666168582146#LOL Thats Mine ID)))))# Twitter id
###################################
from requests_oauthlib.oauth1_session import urldecode
from SRP350IIAPI import WebPrinter 
from SRP350IIAPI import QRcode
import tweepy
import time
import datetime
import cv2
import numpy
import requests
import os
acess_token="1393004984669638659-TMyhvjffqzxMzWfBQHdUZBkofnZJks"
acess_token_secret="nUDafFTuRfy9KxtzmBsmDQlgVGugOXCFmdqCfw8D9RAH1"
api_key="opEjUdyhEYhvZkWyeEK5baPKG"
api_secret="2CBo35kQZr9OlY5BdOCxhRpZrkdhx7f4tFFHZqXd5yXefZ4JrO"
def putImage(xB,yB,xE,yE,img,imgToPut):
                    placement=[256,256,256,256]
                    sy,sx=imgToPut.shape[0],imgToPut.shape[1]
                    sizeX=xE-xB
                    sizeY=yE-yB
                    xC=(xB+xE)/2
                    yC=(yB+yE)/2
                    if ((sx/sy)>(sizeX/sizeY)):
                        sy=int((sizeX/sx)*sy)
                        sx=sizeX
                    else:
                        sx=int((sizeY/sy)*sx)
                        sy=sizeY
                    placement[0],placement[1]=int(xC-(sx/2)),int(xC+(sx/2))
                    placement[2],placement[3]=int(yC-(sy/2)),int(yC+(sy/2))
                    img[placement[2]:placement[3],placement[0]:placement[1]]=cv2.resize(imgToPut,(int(sx),int(sy)))
                    return img
def formDTS():
    
    # Local time without timezone information printed in ISO 8601 format
    dateTime = datetime.datetime.today()

    # Date time separator is a "#" symbol
    print(dateTime.isoformat("#"))

    # Create a timedelta object for CST time zone
    cstTimeDelta    = datetime.timedelta(hours=-6) 

    # Create a timezone instance for CST time zone
    tzObject        = datetime.timezone(cstTimeDelta, name="CST")

    # Replace the time zone with CST
    cstTimeNow = dateTime.replace(tzinfo=tzObject)

    P.fontSelector(bytearray([0b00000000]))
    return cstTimeNow.isoformat("|","seconds")
# auth = tweepy.OAuthHandler(api_key,api_secret)
# auth.set_access_token(acess_token,acess_token_secret)
# apiV1=tweepy.API(auth)
api = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAADXxVwEAAAAAxFoFlav7iKvz11Gnn5lcsYO3yzQ%3DjrGo1wssP71KWzyXBD8RuU4fNxwMRLX1NC6wL7TnBzDZCw9KYg")
print("Shit Post Starting")
P=WebPrinter(PrinterIp)
P.fontSelector(bytearray([0b00000000]))
P.printR(f"==========================================")
P.lineFeed()
P.fontSelector(bytearray([0b00010000]))
P.printR("ShitPost")
P.fontSelector(bytearray([0b00000000]))
P.printR(" logger system")
P.lineFeed()
P.printR("By ")
P.fontSelector(bytearray([0b00000001]))
P.printR("OkunElya")
P.fontSelector(bytearray([0b00000000]))
P.emphrazeMode(False)
P.printR(" and ")
P.fontSelector(bytearray([0b00000001]))
P.underline(False)
P.printR("Edventy")
P.lineFeed()
P.fontSelector(bytearray([0b00000000]))
P.printR("=   =   =   =   =   =   =   =   =   =   =")
P.lineFeed()
P.fontSelector(bytearray([0b00000000]))
P.printR("Starting......")
P.lineFeed()
P.printR(f"==========================================")
for i in range(5):
    P.carrigeReturn()
    P.lineFeed()
P.cut()
P.lineFeed()
P.fontSelector(bytearray([0b00000001]))

P.printR("Establishing connection with Twitter...")
P.fontSelector(bytearray([0b00000000]))
P.lineFeed()

P.printR(formDTS())
P.lineFeed()

uID=UserId
tweets=api.get_users_tweets(uID,max_results=5)
api.get_tweet(tweets[0][0].id)
user=api.get_user(id=uID)
ltt=tweets[0][0].text+" "
# img=P.prepareImg(cv2.imread("C:/Users/OkunElya/Desktop/rabotaet.png"),512,512)
# P.printRastrImage(img)

while 1:
    tweets=api.get_users_tweets(uID,max_results=5)
    
    if ltt!=tweets[0][0].text:
        P.reconnect()
        lastTweet=api.get_tweet(tweets[0][0].id,expansions="attachments.media_keys",media_fields="media_key,url,type")
        ltt=lastTweet[0].text
        tweetList_=ltt.split("https://t.co/")
        ttp=tweetList_[0]
        tURL=""
        try:
            tURL=tweetList_[1]
        except:
            pass
        tURL="https://t.co/"+tURL
        P.bwReverse(True)
        P.printR(f"{user.data.name}")
        P.bwReverse(False)
        P.print(" ")
        P.fontSelector(bytearray([0b00000001]))
        P.printR(formDTS())
        P.fontSelector(bytearray([0b00000000]))
        P.lineFeed()
        P.printR(ttp)
        P.lineFeed()
        murls=[]
        try:
            mediaS=lastTweet[1]["media"]
            for mediaCounter in range(len(mediaS)):
                if mediaS[mediaCounter].type!='animated_gif':
                    murls.append(mediaS[mediaCounter]["data"]["url"])
                else:
                    P.fontSelector(bytearray([0b00000001]))
                    P.printR("Ахуеть,это гифка")
                    P.fontSelector(bytearray([0b00000000]))
                    P.lineFeed()
                    P.hT()
                    qr=QRcode(P)
                    qr.loadText(tURL)
                    qr.setSize(5)
                    qr.applySize()
                    
                    qr.print()

      
        except:
            P.fontSelector(bytearray([0b00000001]))
            P.printR("Высер без имаги")
            P.fontSelector(bytearray([0b00000000]))
        if len(murls)>0:
            if not ("mTmp" in os.listdir("./")):
                print("creating media dir")
                os.mkdir(f"./mTmp")
            filenames=[]
            for urlCounter,url in enumerate(murls):    
                img_data = requests.get(url).content
                filenames.append(f'./mTmp/{urlCounter}.{url[-3:]}')
                with open(f'./mTmp/{urlCounter}.{url[-3:]}', 'wb') as handler:
                    handler.write(img_data)
            P.fontSelector(bytearray([0b00000001]))

            P.printR(f"Высер содержит {len(murls)} изображени{'е' if len(murls)==1 else 'я' }:")
            P.fontSelector(bytearray([0b00000000]))
            imageToPrint=numpy.zeros([512,512],dtype=numpy.uint8)
            imageToPrint=cv2.rectangle(imageToPrint,(0,0),(512,512),[200],-1)
            imageToPrint=cv2.rectangle(imageToPrint,(0,0),(512,512),[40],4)
            if len(murls)==4:
                sX=0
                sY=0
                for j in range(2):
                    sX+=cv2.imread(filenames[j]).shape[1]
                    sY+=cv2.imread(filenames[j]).shape[0]

                
                if sX>sY:#stack on top
                    imageToPrint=cv2.line(imageToPrint,(0,256),(512,256),[40],4)
                    imageToPrint=putImage(4,4,508,254,imageToPrint,cv2.cvtColor( cv2.imread(filenames[0]),cv2.COLOR_BGR2GRAY))
                    imageToPrint=putImage(4,258,508,508,imageToPrint,cv2.cvtColor( cv2.imread(filenames[1]),cv2.COLOR_BGR2GRAY))
                else:#stack on sides
                    imageToPrint=cv2.line(imageToPrint,(256,0),(256,512),[40],4)
                    imageToPrint=putImage(4,4,254,508,imageToPrint,cv2.cvtColor( cv2.imread(filenames[0]),cv2.COLOR_BGR2GRAY))
                    imageToPrint=putImage(258,4,508,508,imageToPrint,cv2.cvtColor( cv2.imread(filenames[1]),cv2.COLOR_BGR2GRAY))
                #put image 0
                P.printRastrImage(P.prepareImg(imageToPrint,512,512))
                P.lineFeed()
                imageToPrint=numpy.zeros([512,512],dtype=numpy.uint8)
                imageToPrint=cv2.rectangle(imageToPrint,(0,0),(512,512),[200],-1)
                imageToPrint=cv2.rectangle(imageToPrint,(0,0),(512,512),[40],4)
                time.sleep(120)
                sX=0
                sY=0
                for j in range(2,3):
                    sX+=cv2.imread(filenames[j]).shape[1]
                    sY+=cv2.imread(filenames[j]).shape[0]

                
                if sX>sY:#stack on top
                    imageToPrint=cv2.line(imageToPrint,(0,256),(512,256),[40],4)
                    imageToPrint=putImage(4,4,508,254,imageToPrint,cv2.cvtColor( cv2.imread(filenames[2]),cv2.COLOR_BGR2GRAY))
                    imageToPrint=putImage(4,258,508,508,imageToPrint,cv2.cvtColor( cv2.imread(filenames[3]),cv2.COLOR_BGR2GRAY))
                else:#stack on sides
                    imageToPrint=cv2.line(imageToPrint,(256,0),(256,512),[40],4)
                    imageToPrint=putImage(4,4,254,508,imageToPrint,cv2.cvtColor( cv2.imread(filenames[2]),cv2.COLOR_BGR2GRAY))
                    imageToPrint=putImage(258,4,508,508,imageToPrint,cv2.cvtColor( cv2.imread(filenames[3]),cv2.COLOR_BGR2GRAY))
                #put image 0
               

                cv2.imshow("ITP",imageToPrint)
                cv2.waitKey(1)    
            elif len(murls)==3:
                img=cv2.imread(filenames[0])
                imageToPrint=putImage(4,4,508,508,imageToPrint,cv2.cvtColor( cv2.imread(filenames[0]),cv2.COLOR_BGR2GRAY))
                P.printRastrImage(P.prepareImg(imageToPrint,512,512))
                P.lineFeed()

                imageToPrint=numpy.zeros([512,512],dtype=numpy.uint8)
                imageToPrint=cv2.rectangle(imageToPrint,(0,0),(512,512),[200],-1)
                imageToPrint=cv2.rectangle(imageToPrint,(0,0),(512,512),[40],4)
                time.sleep(120)
                time.sleep(120)
                sX=0
                sY=0
                for j in range(1,2):
                    sX+=cv2.imread(filenames[j]).shape[1]
                    sY+=cv2.imread(filenames[j]).shape[0]

                
                if sX>sY:#stack on top
                    imageToPrint=cv2.line(imageToPrint,(0,256),(512,256),[40],4)
                    imageToPrint=putImage(4,4,508,254,imageToPrint,cv2.cvtColor( cv2.imread(filenames[1]),cv2.COLOR_BGR2GRAY))
                    imageToPrint=putImage(4,258,508,508,imageToPrint,cv2.cvtColor( cv2.imread(filenames[2]),cv2.COLOR_BGR2GRAY))
                else:#stack on sides
                    imageToPrint=cv2.line(imageToPrint,(256,0),(256,512),[40],4)
                    imageToPrint=putImage(4,4,254,508,imageToPrint,cv2.cvtColor( cv2.imread(filenames[1]),cv2.COLOR_BGR2GRAY))
                    imageToPrint=putImage(258,4,508,508,imageToPrint,cv2.cvtColor( cv2.imread(filenames[2]),cv2.COLOR_BGR2GRAY))
                #put image 0
               

                cv2.imshow("ITP",imageToPrint)
                cv2.waitKey(1)    
                
            elif len(murls)==2:

                sX=0
                sY=0
                for j in range(2):
                    sX+=cv2.imread(filenames[j]).shape[1]
                    sY+=cv2.imread(filenames[j]).shape[0]

                
                if sX>sY:#stack on top
                    imageToPrint=cv2.line(imageToPrint,(0,256),(512,256),[40],4)
                    imageToPrint=putImage(4,4,508,254,imageToPrint,cv2.cvtColor( cv2.imread(filenames[0]),cv2.COLOR_BGR2GRAY))
                    imageToPrint=putImage(4,258,508,508,imageToPrint,cv2.cvtColor( cv2.imread(filenames[1]),cv2.COLOR_BGR2GRAY))
                else:#stack on sides
                    imageToPrint=cv2.line(imageToPrint,(256,0),(256,512),[40],4)
                    imageToPrint=putImage(4,4,254,508,imageToPrint,cv2.cvtColor( cv2.imread(filenames[0]),cv2.COLOR_BGR2GRAY))
                    imageToPrint=putImage(258,4,508,508,imageToPrint,cv2.cvtColor( cv2.imread(filenames[1]),cv2.COLOR_BGR2GRAY))
                #put image 0
               

                cv2.imshow("ITP",imageToPrint)
                cv2.waitKey(1)    
            else:
                
                img=cv2.imread(filenames[0])
                imageToPrint=putImage(4,4,508,508,imageToPrint,cv2.cvtColor( cv2.imread(filenames[0]),cv2.COLOR_BGR2GRAY))
            
            # cv2.imshow("ITP",imageToPrint)
            # cv2.waitKey(1)
            P.printRastrImage(P.prepareImg(imageToPrint,512,512))
            P.lineFeed()


        for i in range(7):
            P.carrigeReturn()
            P.lineFeed()
        P.cut()
        print("ВЫСЕР ВЫСРАН")
       
    time.sleep(15)
        