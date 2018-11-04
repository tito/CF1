import kivy
import time
 
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen,NoTransition
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.uix.button import Button
from kivy.clock import Clock
from decimal import *
import operator
import json
from pprint import pprint
from kivy.uix.tabbedpanel import TabbedPanel
import threading




Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480') 

##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


class ParamScreen(Screen):


    def on_enter(self):
        self.b1001.text=paramcf1["midi-map"][0]["port"]
        self.b1002.text=paramcf1["midi-map"][1]["port"]
        self.b1003.text=paramcf1["midi-map"][2]["port"]
        self.b1004.text=paramcf1["midi-map"][3]["port"]
        self.b1005.text=paramcf1["midi-map"][4]["port"]
        self.b1006.text=paramcf1["midi-map"][5]["port"]
        self.b2001.text=paramcf1["midi-map"][0]["channel"]
        self.b2002.text=paramcf1["midi-map"][1]["channel"]
        self.b2003.text=paramcf1["midi-map"][2]["channel"]
        self.b2004.text=paramcf1["midi-map"][3]["channel"]
        self.b2005.text=paramcf1["midi-map"][4]["channel"]
        self.b2006.text=paramcf1["midi-map"][5]["channel"]



    def menu(self):
        pass

    def test(self):
        paramcf1["midi-map"][5]["channel"] = "15"
        with open("param.json", "w") as jsonFile:
            json.dump(paramcf1, jsonFile)
        print('done')

    def midiportselect(self):
        self.b4000.pos=328,120
        self.b4001.pos=329,121
        self.b4002.pos=329,182
        self.b4003.pos=329,243
        self.b3005.pos=0,0

    def midichannelselect(self):
        self.b5017.pos=310,305
        self.b5000.pos=138,31

        self.b5001.pos=139,236
        self.b5005.pos=139,168
        self.b5009.pos=139,100
        self.b5013.pos=139,32
        self.b5002.pos=269,236
        self.b5006.pos=269,168
        self.b5010.pos=269,100
        self.b5014.pos=269,32
        self.b5003.pos=399,236
        self.b5007.pos=399,168
        self.b5011.pos=399,100
        self.b5015.pos=399,32
        self.b5004.pos=529,236
        self.b5008.pos=529,168
        self.b5012.pos=529,100
        self.b5016.pos=529,32

        self.b3005.pos=0,0


    def trackselected(self,button):
        global trackselectedparam
        for key, val in self.ids.items():
            if val==button:
                ID=key
        trackselectedparam=int(ID[-3:])
        print(trackselectedparam)



    def midiport(self,button):
        for key, val in self.ids.items():
            if val==button:
                ID=key
        newport=(ID[-1:])

        paramcf1["midi-map"][trackselectedparam-1]["port"] = newport
        with open("param.json", "w") as jsonFile:
            json.dump(paramcf1, jsonFile)
        self.on_enter()
#on peut surement updater juste le bouton 



    def midichannel(self,button):
        for key, val in self.ids.items():
            if val==button:
                ID=key
        newchannel=(ID[-2:])

        paramcf1["midi-map"][trackselectedparam-1]["channel"] = newchannel
        with open("param.json", "w") as jsonFile:
            json.dump(paramcf1, jsonFile)
        self.on_enter()




    def closemenu(self):
        self.b4000.pos=1328,1120
        self.b4001.pos=1329,1121
        self.b4002.pos=1329,1182
        self.b4003.pos=1329,1243
        self.b5017.pos=1329,305
        self.b5000.pos=1228,61
        self.b5001.pos=1229,245
        self.b5005.pos=1229,184
        self.b5009.pos=1229,123
        self.b5013.pos=1229,62
        self.b5002.pos=1329,245
        self.b5006.pos=1329,184
        self.b5010.pos=1329,123
        self.b5014.pos=1329,62
        self.b5003.pos=1429,245
        self.b5007.pos=1429,184
        self.b5011.pos=1429,123
        self.b5015.pos=1429,62
        self.b5004.pos=1529,245
        self.b5008.pos=1529,184
        self.b5012.pos=1529,123
        self.b5016.pos=1529,62

        self.b3005.pos=1000,0
        self.clear()

    def clearStep(self,button):
        button.state="normal"


    def clear(self):
        for val in self.ids.items():
            if (str(val[0])== str('b001') or val[0]== 'b002' or val[0]== 'b003' or val[0]== 'b004'):
                pass
            else:
                self.clearStep(val[1])







##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################




class SongScreen(Screen):
    
    def menu(self):
        if self.b007.state=="down":
            self.b008.pos= 648,360
            self.b009.pos= 648,301
            self.b011.pos= 496,900
            self.b012.pos= 496,900
            self.b013.pos= 344,900
            self.b014.pos= 344,900
            self.b019.pos=1300,1120
            self.b020.pos=1301,1121
            self.b021.pos=1301,1182
            self.b022.pos=1301,1243
            self.b006.state="normal"
            self.b005.state="normal"
            self.b010.pos= 0,0
            self.b800.state="normal"
            self.b700.state="normal"
            self.b600.state="normal"
            self.b500.state="normal"
            self.b400.state="normal"
            self.b300.state="normal"
            self.b200.state="normal"
            self.b100.state="normal"
        else:
            self.b008.pos= 648,900
            self.b009.pos= 648,900
            self.b010.pos= 1000,0
       
    def seqmode(self):
        if self.b006.state=="down":
            self.b011.pos= 496,360
            self.b012.pos= 496,301
            self.b008.pos= 648,900
            self.b009.pos= 648,900
            self.b013.pos= 344,900
            self.b014.pos= 344,900
            self.b019.pos=1300,1120
            self.b020.pos=1301,1121
            self.b021.pos=1301,1182
            self.b022.pos=1301,1243
            self.b007.state="normal"
            self.b005.state="normal"
            self.b010.pos= 0,0
            self.b800.state="normal"
            self.b700.state="normal"
            self.b600.state="normal"
            self.b500.state="normal"
            self.b400.state="normal"
            self.b300.state="normal"
            self.b200.state="normal"
            self.b100.state="normal"
        else:
            self.b011.pos= 496,900
            self.b012.pos= 496,900
            self.b010.pos= 1000,0

    def file(self):
        if self.b005.state=="down":
            self.b013.pos= 344,360
            self.b014.pos= 344,301
            self.b011.pos= 496,900
            self.b012.pos= 496,900
            self.b008.pos= 648,900
            self.b009.pos= 648,900
            self.b019.pos=1300,1120
            self.b020.pos=1301,1121
            self.b021.pos=1301,1182
            self.b022.pos=1301,1243
            self.b007.state="normal"
            self.b006.state="normal"
            self.b010.pos= 0,0
            self.b800.state="normal"
            self.b700.state="normal"
            self.b600.state="normal"
            self.b500.state="normal"
            self.b400.state="normal"
            self.b300.state="normal"
            self.b200.state="normal"
            self.b100.state="normal"
        else:
            self.b013.pos= 344,900
            self.b014.pos= 344,900
            self.b010.pos= 1000,0

    def closemenus(self):
        if self.b007.state=="down":
            self.b007.state="normal"
            self.menu()
        if self.b006.state=="down":
            self.b006.state="normal"
            self.seqmode()
        if self.b005.state=="down":
            self.b005.state="normal"
            self.file()
        self.b019.pos=1300,1120
        self.b020.pos=1301,1121
        self.b021.pos=1301,1182
        self.b022.pos=1301,1243
        self.b010.pos= 1000,0
        self.b800.state="normal"
        self.b700.state="normal"
        self.b600.state="normal"
        self.b500.state="normal"
        self.b400.state="normal"
        self.b300.state="normal"
        self.b200.state="normal"
        self.b100.state="normal"

    def start(self):
        if self.b001.state=="down":
            self.b001.text="PAUSE"
            self.SeqScreen=SeqScreen()
            global nextcall
            nextcall=time.time()
            #Clock.schedule_interval(self.movebar, 0.01)
            self.SeqScreen.startTimer()
        else:
            self.b001.text="START"
            #Clock.unschedule(self.movebar)

    def stop(self):
        global counter
        self.b001.state="normal"
        self.b001.text="START"
        Clock.unschedule(self.movebar)
        counter=0
        position=0
        self.b015.pos=50,0

    def moveXrgh(self):
        global rangeXs
        if rangeXs+16*(zoom)<=rangeXmax:
            self.b901.text=timerangeS[rangeXs+1]
            self.b902.text=timerangeS[rangeXs+2]
            self.b903.text=timerangeS[rangeXs+3]
            self.b904.text=timerangeS[rangeXs+4]
            self.b905.text=timerangeS[rangeXs+5]
            self.b906.text=timerangeS[rangeXs+6]
            self.b907.text=timerangeS[rangeXs+7]
            self.b908.text=timerangeS[rangeXs+8]
            self.b909.text=timerangeS[rangeXs+9]
            self.b910.text=timerangeS[rangeXs+10]
            self.b911.text=timerangeS[rangeXs+11]
            self.b912.text=timerangeS[rangeXs+12]
            self.b913.text=timerangeS[rangeXs+13]
            self.b914.text=timerangeS[rangeXs+14]
            self.b915.text=timerangeS[rangeXs+15]
            self.b916.text=timerangeS[rangeXs+16]
            rangeXs=rangeXs+1
            #print(rangeX)
           
        else:
            pass
        self.loadseq()
        
    def moveXlft(self):
        global rangeXs
        if rangeXs>=1:
            self.b901.text=timerangeS[rangeXs-1]
            self.b902.text=timerangeS[rangeXs]
            self.b903.text=timerangeS[rangeXs+1]
            self.b904.text=timerangeS[rangeXs+2]
            self.b905.text=timerangeS[rangeXs+3]
            self.b906.text=timerangeS[rangeXs+4]
            self.b907.text=timerangeS[rangeXs+5]
            self.b908.text=timerangeS[rangeXs+6]
            self.b909.text=timerangeS[rangeXs+7]
            self.b910.text=timerangeS[rangeXs+8]
            self.b911.text=timerangeS[rangeXs+9]
            self.b912.text=timerangeS[rangeXs+10]
            self.b913.text=timerangeS[rangeXs+11]
            self.b914.text=timerangeS[rangeXs+12]
            self.b915.text=timerangeS[rangeXs+13]
            self.b916.text=timerangeS[rangeXs+14]
            rangeXs=rangeXs-1
            #print(rangeX)
            
        else:
            pass
        self.loadseq()
        
    def moveYup(self):
        global rangeYs
        if rangeYs<=91:
            self.b100.text=keyrangeS[rangeYs+8]
            self.b200.text=keyrangeS[rangeYs+7]
            self.b300.text=keyrangeS[rangeYs+6]
            self.b400.text=keyrangeS[rangeYs+5]
            self.b500.text=keyrangeS[rangeYs+4]
            self.b600.text=keyrangeS[rangeYs+3]
            self.b700.text=keyrangeS[rangeYs+2]
            self.b800.text=keyrangeS[rangeYs+1]

            rangeYs=rangeYs+1   
        else:
            pass
        #print(rangeYs)
        self.loadseq()

    def moveYdw(self):
        global rangeYs
        #print(rangeYs)
        if rangeYs>=1:
            self.b100.text=keyrangeS[rangeYs+6]
            self.b200.text=keyrangeS[rangeYs+5]
            self.b300.text=keyrangeS[rangeYs+4]
            self.b400.text=keyrangeS[rangeYs+3]
            self.b500.text=keyrangeS[rangeYs+2]
            self.b600.text=keyrangeS[rangeYs+1]
            self.b700.text=keyrangeS[rangeYs]
            self.b800.text=keyrangeS[rangeYs-1]
            rangeYs=rangeYs-1  
        else:
            pass
        self.loadseq()


    def loadseq(self):
        self.clear()
        i=1
        while i <= len(song):
            Xc=song[i-1][0]-rangeXs
            Yc=song[i-1][1]-rangeYs
            #print(Xc)
            if (Xc>=1 and Xc <= 16):
                if (Yc >= 1 and Yc <=8):
                    Xcp=int(Xc)
                    #print(i*100)
                    #print(Xcp)
                    Ycp=-(int(Yc)-9)
                    if Xcp<=9:
                        b="b"+str(Ycp)+"0"+str(Xcp)
                    else:
                        b="b"+str(Ycp)+str(Xcp)
                    self.findButton(b)
                else:
                    pass
            i+=1
        self.loopbar()

    def findButton(self,button):
        for val in self.ids.items():
            if button==val[0]:
                buttonfound=val[1]
                buttonfound.state="down"



    def loopbar(self):
        global loopsizeS
        loopbar_pos=loopsizeS
        #print(rangeXs)
        if loopbar_pos<=(rangeXs+16)*4:
            if 48+(loopbar_pos/4-rangeXs)*47>=5:
                self.b017.pos=48+(loopbar_pos/4-rangeXs)*47,0
            else:
                self.b017.pos=1000,1000
        else:
            self.b017.pos=1000,1000
        #self.gridbar()


    def clearStep(self,button):
        button.state="normal"


    def clear(self):
        for val in self.ids.items():
            if (str(val[0])== str('b001') or val[0]== 'b002' or val[0]== 'b003' or val[0]== 'b004'):
                pass
            else:
                self.clearStep(val[1])

    def monitor(self, button):
        global song
        for key, val in self.ids.items():
            if val==button:
                ID=key
        y=int(ID[1])
        yp=-(y-8)
        x=int(ID[-2:])
        if button.state=="normal":
            song.remove([(x-1)+rangeXs+1,yp+rangeYs+1])
            print(song)
        else:
            song.append([(x-1)+rangeXs+1,yp+rangeYs+1])
            song=sorted(song, key=operator.itemgetter(0))
            print(song)

    def trackmenu(self,button):
        global trackselected
        for key, val in self.ids.items():
            if val==button:
                ID=key
        trackselected=-(int(ID[1])-9)+rangeYs
        print(trackselected)

        self.b019.pos=300,120
        self.b020.pos=301,121
        self.b021.pos=301,182
        self.b022.pos=301,243
        self.b010.pos=0,0

    def cleartrack(self):
        toclear=[]
        for elem in song:
            if elem[1]==trackselected:
                toclear.append(elem)
        i=0
        if len(toclear)>0:
            while i<=len(toclear)-1: 
                song.remove(toclear[i])
                i+=1
        self.loadseq()


 


##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################







class SeqScreen(Screen):
 
   


    def on_enter(self):
        #print("changed")
        global start
        global rangeY
        global rangeX
        global zoom

        if start > 0:
            rangeY=36
            rangeX=0
            zoom=4
            self.loadseq()
            self.b901.text=timerange[rangeX]
            self.b902.text=timerange[rangeX+1*(zoom)]
            self.b903.text=timerange[rangeX+2*(zoom)]
            self.b904.text=timerange[rangeX+3*(zoom)]
            self.b905.text=timerange[rangeX+4*(zoom)]
            self.b906.text=timerange[rangeX+5*(zoom)]
            self.b907.text=timerange[rangeX+6*(zoom)]
            self.b908.text=timerange[rangeX+7*(zoom)]
            self.b909.text=timerange[rangeX+8*(zoom)]
            self.b910.text=timerange[rangeX+9*(zoom)]
            self.b911.text=timerange[rangeX+10*(zoom)]
            self.b912.text=timerange[rangeX+11*(zoom)]
            self.b913.text=timerange[rangeX+12*(zoom)]
            self.b914.text=timerange[rangeX+13*(zoom)]
            self.b915.text=timerange[rangeX+14*(zoom)]
            self.b916.text=timerange[rangeX+15*(zoom)]
            self.b100.text=keyrange[rangeY][0]
            self.b200.text=keyrange[rangeY+1][0]
            self.b300.text=keyrange[rangeY+2][0]
            self.b400.text=keyrange[rangeY+3][0]
            self.b500.text=keyrange[rangeY+4][0]
            self.b600.text=keyrange[rangeY+5][0]
            self.b700.text=keyrange[rangeY+6][0]
            self.b800.text=keyrange[rangeY+7][0]     
        else:
            start = start +1



    def monitor(self, button):
        global sequencepool
        for key, val in self.ids.items():
            if val==button:
                ID=key
        y=int(ID[1])
        x=int(ID[-2:])

        if button.state=="normal":
            sequencepool[trackselected-1].remove([(x-1)*zoom+rangeX+1,y+rangeY-1,1])
            #print(sequence)
        else:
            sequencepool[trackselected-1].append([(x-1)*zoom+rangeX+1,y+rangeY-1,1])
            sequencepool[trackselected-1]=sorted(sequencepool[trackselected-1], key=operator.itemgetter(0))
            #print(x)
            #print(rangeX)
            #print((x-1)*zoom+rangeX+1)
            #print(sorted(sequencepool[trackselected-1], key=operator.itemgetter(0)))
        print(sequencepool)
            
    def clearsequence(self):
        global sequencepool
        #TO DO clear only this channel sequence not all
        sequencepool[trackselected-1]=[]

    def clearStep(self,button):
        button.state="normal"

    def clear(self):
        for val in self.ids.items():
            if (str(val[0])== str('b001') or val[0]== 'b002' or val[0]== 'b003' or val[0]== 'b004'):
                pass
            else:
                self.clearStep(val[1])              
    
    def zoomstep(self,button,text):
        button.text=text

    def zoom(self):
        global rangeX
        print("zoom")
        for val in self.ids.items():
            bty=int(val[0][1])
            btx=int(val[0][-2:])
            if bty ==9:
                if rangeX+16*(zoom)<=rangeXmax:
                    if rangeX%zoom == 0:
                        #print(rangeX)
                        btn=(btx-1)*zoom+rangeX
                        #print(btn)
                        self.zoomstep(val[1],timerange[btn])
                    else:
                        rangeX = rangeX-(rangeX%zoom)
                        btn=(btx-1)*zoom+rangeX
                        print("not multiple")
                        #print(rangeX)
                        self.zoomstep(val[1],timerange[btn])
                else:
                    rangeX=128
                    btn=(btx-1)*zoom+rangeX
                    print("resized")
                    #print(btn)
                    self.zoomstep(val[1],timerange[btn])
        print(rangeX)
        self.loadseq()
         
    def zoomout(self):
        global zoom
        global rangeX
        if zoom <8:
            zoom = 2*zoom
            #print(zoom)
            self.zoom()

    def zoomin(self):
        global zoom
        global rangeX
        if zoom >1:
            zoom = zoom/2
            #print(zoom)
            self.zoom()

    def moveXrgh(self):
        global rangeX
        if rangeX+16*(zoom)<=rangeXmax:
            self.b901.text=timerange[rangeX+1*(zoom)]
            self.b902.text=timerange[rangeX+2*(zoom)]
            self.b903.text=timerange[rangeX+3*(zoom)]
            self.b904.text=timerange[rangeX+4*(zoom)]
            self.b905.text=timerange[rangeX+5*(zoom)]
            self.b906.text=timerange[rangeX+6*(zoom)]
            self.b907.text=timerange[rangeX+7*(zoom)]
            self.b908.text=timerange[rangeX+8*(zoom)]
            self.b909.text=timerange[rangeX+9*(zoom)]
            self.b910.text=timerange[rangeX+10*(zoom)]
            self.b911.text=timerange[rangeX+11*(zoom)]
            self.b912.text=timerange[rangeX+12*(zoom)]
            self.b913.text=timerange[rangeX+13*(zoom)]
            self.b914.text=timerange[rangeX+14*(zoom)]
            self.b915.text=timerange[rangeX+15*(zoom)]
            self.b916.text=timerange[rangeX+16*(zoom)]
            rangeX=rangeX+zoom
            #print(rangeX)
           
        else:
            pass
        self.loadseq()

    def moveXlft(self):
        global rangeX
        if rangeX>=1:
            self.b901.text=timerange[rangeX-1*(zoom)]
            self.b902.text=timerange[rangeX]
            self.b903.text=timerange[rangeX+1*(zoom)]
            self.b904.text=timerange[rangeX+2*(zoom)]
            self.b905.text=timerange[rangeX+3*(zoom)]
            self.b906.text=timerange[rangeX+4*(zoom)]
            self.b907.text=timerange[rangeX+5*(zoom)]
            self.b908.text=timerange[rangeX+6*(zoom)]
            self.b909.text=timerange[rangeX+7*(zoom)]
            self.b910.text=timerange[rangeX+8*(zoom)]
            self.b911.text=timerange[rangeX+9*(zoom)]
            self.b912.text=timerange[rangeX+10*(zoom)]
            self.b913.text=timerange[rangeX+11*(zoom)]
            self.b914.text=timerange[rangeX+12*(zoom)]
            self.b915.text=timerange[rangeX+13*(zoom)]
            self.b916.text=timerange[rangeX+14*(zoom)]
            rangeX=rangeX-zoom
            #print(rangeX)
            
        else:
            pass
        self.loadseq()

    def moveYup(self):
        global rangeY
        if rangeY<=87:
            self.b100.text=keyrange[rangeY+1][0]
            self.b200.text=keyrange[rangeY+2][0]
            self.b300.text=keyrange[rangeY+3][0]
            self.b400.text=keyrange[rangeY+4][0]
            self.b500.text=keyrange[rangeY+5][0]
            self.b600.text=keyrange[rangeY+6][0]
            self.b700.text=keyrange[rangeY+7][0]
            self.b800.text=keyrange[rangeY+8][0]
            if keyrange[rangeY+1][1]==0:
                self.b100.background_color= (0,0,0,0.7)
                self.b100.color= 1,1,1,1
            else:
                self.b100.background_color= 255,255,255,0.8
                self.b100.color= 0,0,0,1
            if keyrange[rangeY+2][1]==0:
                self.b200.background_color= (0,0,0,0.7)
                self.b200.color= 1,1,1,1
            else:
                self.b200.background_color= 255,255,255,0.8
                self.b200.color= 0,0,0,1
            if keyrange[rangeY+3][1]==0:
                self.b300.background_color= (0,0,0,0.7)
                self.b300.color= 1,1,1,1
            else:
                self.b300.background_color= 255,255,255,0.8
                self.b300.color= 0,0,0,1
            if keyrange[rangeY+4][1]==0:
                self.b400.background_color= (0,0,0,0.7)
                self.b400.color= 1,1,1,1
            else:
                self.b400.background_color= 255,255,255,0.8
                self.b400.color= 0,0,0,1
            if keyrange[rangeY+5][1]==0:
                self.b500.background_color= (0,0,0,0.7)
                self.b500.color= 1,1,1,1
            else:
                self.b500.background_color= 255,255,255,0.8
                self.b500.color= 0,0,0,1
            if keyrange[rangeY+6][1]==0:
                self.b600.background_color= (0,0,0,0.7)
                self.b600.color= 1,1,1,1
            else:
                self.b600.background_color= 255,255,255,0.8
                self.b600.color= 0,0,0,1
            if keyrange[rangeY+7][1]==0:
                self.b700.background_color= (0,0,0,0.7)
                self.b700.color= 1,1,1,1
            else:
                self.b700.background_color= 255,255,255,0.8
                self.b700.color= 0,0,0,1
            if keyrange[rangeY+8][1]==0:
                self.b800.background_color= (0,0,0,0.7)
                self.b800.color= 1,1,1,1
            else:
                self.b800.background_color= 255,255,255,0.8
                self.b800.color= 0,0,0,1
            rangeY=rangeY+1
            
        else:
            pass
        self.loadseq()

    def moveYdw(self):
        global rangeY
        if rangeY>=1:
            self.b100.text=keyrange[rangeY-1][0]
            self.b200.text=keyrange[rangeY][0]
            self.b300.text=keyrange[rangeY+1][0]
            self.b400.text=keyrange[rangeY+2][0]
            self.b500.text=keyrange[rangeY+3][0]
            self.b600.text=keyrange[rangeY+4][0]
            self.b700.text=keyrange[rangeY+5][0]
            self.b800.text=keyrange[rangeY+6][0]
            if keyrange[rangeY-1][1]==0:
                self.b100.background_color= (0,0,0,0.7)
                self.b100.color= 1,1,1,1
            else:
                self.b100.background_color= 255,255,255,0.8
                self.b100.color= 0,0,0,1
            if keyrange[rangeY][1]==0:
                self.b200.background_color= (0,0,0,0.7)
                self.b200.color= 1,1,1,1
            else:
                self.b200.background_color= 255,255,255,0.8
                self.b200.color= 0,0,0,1
            if keyrange[rangeY+1][1]==0:
                self.b300.background_color= (0,0,0,0.7)
                self.b300.color= 1,1,1,1
            else:
                self.b300.background_color= 255,255,255,0.8
                self.b300.color= 0,0,0,1
            if keyrange[rangeY+2][1]==0:
                self.b400.background_color= (0,0,0,0.7)
                self.b400.color= 1,1,1,1
            else:
                self.b400.background_color= 255,255,255,0.8
                self.b400.color= 0,0,0,1
            if keyrange[rangeY+3][1]==0:
                self.b500.background_color= (0,0,0,0.7)
                self.b500.color= 1,1,1,1
            else:
                self.b500.background_color= 255,255,255,0.8
                self.b500.color= 0,0,0,1
            if keyrange[rangeY+4][1]==0:
                self.b600.background_color= (0,0,0,0.7)
                self.b600.color= 1,1,1,1
            else:
                self.b600.background_color= 255,255,255,0.8
                self.b600.color= 0,0,0,1
            if keyrange[rangeY+5][1]==0:
                self.b700.background_color= (0,0,0,0.7)
                self.b700.color= 1,1,1,1
            else:
                self.b700.background_color= 255,255,255,0.8
                self.b700.color= 0,0,0,1
            if keyrange[rangeY+6][1]==0:
                self.b800.background_color= (0,0,0,0.7)
                self.b800.color= 1,1,1,1
            else:
                self.b800.background_color= 255,255,255,0.8
                self.b800.color= 0,0,0,1
            rangeY=rangeY-1
            
        else:
            pass
        self.loadseq()

    def findButton(self,button):
        for val in self.ids.items():
            if button==val[0]:
                buttonfound=val[1]
                buttonfound.state="down"



    def loadseq(self):
        global sequencepool
        self.clear()
        print(trackselected)
        sequence=sequencepool[trackselected-1]
        print(sequence)
        i=1
        while i <= len(sequence):
            Xc=sequence[i-1][0]-rangeX
            Yc=sequence[i-1][1]-rangeY+1
            print(Xc)
            if (Xc>=0 and Xc <= 16*zoom and (sequence[i-1][0]-1)%zoom ==0):
                if (Yc >= 1 and Yc <=8):
                    Xcp=int(Xc/(zoom+0.0000000000001))+1
                    print(i*100)
                    print(Xcp)
                    if Xcp<=9:
                        b="b"+str(Yc)+"0"+str(Xcp)
                    else:
                        b="b"+str(Yc)+str(Xcp)
                    print(b)
                    self.findButton(b)
                else:
                    pass
            i+=1
        self.loopbar()

    def menu(self):
        if self.b007.state=="down":
            self.b008.pos= 648,360
            self.b009.pos= 648,301
            self.b011.pos= 496,900
            self.b012.pos= 496,900
            self.b013.pos= 344,900
            self.b014.pos= 344,900
            self.b016.pos= 344,900
            self.b006.state="normal"
            self.b005.state="normal"
            self.b010.pos= 0,0
        else:
            self.b008.pos= 648,900
            self.b009.pos= 648,900
            self.b010.pos= 1000,0
       

    def seqmode(self):
        if self.b006.state=="down":
            self.b011.pos= 496,360
            self.b012.pos= 496,301
            self.b008.pos= 648,900
            self.b009.pos= 648,900
            self.b013.pos= 344,900
            self.b014.pos= 344,900
            self.b016.pos= 344,900
            self.b007.state="normal"
            self.b005.state="normal"
            self.b010.pos= 0,0
        else:
            self.b011.pos= 496,900
            self.b012.pos= 496,900
            self.b010.pos= 1000,0

    def file(self):
        if self.b005.state=="down":
            self.b013.pos= 344,360
            self.b014.pos= 344,301
            self.b016.pos= 344,242
            self.b011.pos= 496,900
            self.b012.pos= 496,900
            self.b008.pos= 648,900
            self.b009.pos= 648,900
            self.b007.state="normal"
            self.b006.state="normal"
            self.b010.pos= 0,0
        else:
            self.b013.pos= 344,900
            self.b014.pos= 344,900
            self.b016.pos= 344,900
            self.b010.pos= 1000,0

    def closemenus(self):
        if self.b007.state=="down":
            self.b007.state="normal"
            self.menu()
        if self.b006.state=="down":
            self.b006.state="normal"
            self.seqmode()
        if self.b005.state=="down":
            self.b005.state="normal"
            self.file()

    def start(self):
        global nextcall
        if self.b001.state=="down":
            self.b001.text="PAUSE"
            nextcall=time.time()
            self.Timing=Timing()
            #self.startTimer()
            self.Timing.Timer()
            #Clock.schedule_interval(self.movebar, 0.0125)
            
        else:
            self.b001.text="START"
            Clock.unschedule(self.movebar)

    def stop(self):
        global counter
        self.b001.state="normal"
        self.b001.text="START"
        Clock.unschedule(self.movebar)
        counter=0
        position=0
        self.b015.pos=50,0





    def myPeriodicFunction(self):
        print '{0:.16f}'.format(time.time())
        global counter
        global stopsignal
        counter = counter +1
        bpm=120
        nbpulse=bpm/60*100
        pulse=Decimal(750)/Decimal(nbpulse)
        position=int(50+counter*pulse)
        if position>800:
            position=50
            counter=1
        print("here")
        self.b015.pos=position,0
        

    def startTimer(self):
        global nextcall
        global count
        nextcall = nextcall+interval
        threading.Timer(nextcall - time.time(), self.startTimer).start()
        self.myPeriodicFunction()
        count+=1
        print(count)
        
        
        
        
        

    def movebar(self, *args):
        #print(counter)
        global counter2
        global stopsignal2
        counter2 = counter2 +1
        bpm=120
        nbpulse=bpm/60*100
        pulse=Decimal(750)/Decimal(nbpulse)
        position=int(50+counter2*pulse)
        if position>800:
            position=50
            counter2=1
        self.b015.pos=position,0


    def loopbar(self):
        global loopsize
        loopbar_pos=loopsize*16
        print(rangeX)
        if loopbar_pos<=rangeX+16*zoom:
            if 48+(loopbar_pos-rangeX)/zoom*47>=5:
                self.b017.pos=48+(loopbar_pos-rangeX)/zoom*47,0
            else:
                self.b017.pos=1000,1000
        else:
            self.b017.pos=1000,1000
        self.gridbar()
        
    def gridbar(self):
        print(rangeX)
        if (rangeX-3*zoom)%(4*zoom)==0:
            self.ids.b018.pos = 94,0
        if (rangeX-2*zoom)%(4*zoom)==0:
            self.ids.b018.pos = 141,0
        if (rangeX-1*zoom)%(4*zoom)==0:
            self.ids.b018.pos = 188,0
        if rangeX%(4*zoom)==0:
            self.ids.b018.pos = 235,0


##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################



class Manager(ScreenManager):

    screen_one=ObjectProperty(None)
    screen_two=ObjectProperty(None)
    screen_three=ObjectProperty(None)


##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################

class Timing():

    def Timer(self):
        global nextcall
        global count
        global loopstate
        nextcall = nextcall+interval
        threading.Timer(nextcall - time.time(), self.Timer).start()
        print(nextcall-time.time())
        self.MIDIsend()
        count+=1
        if count > 100:
            count=0
        print(count)


    def MIDIsends(self):
        n=0
        while n<15:
            self.MIDIsend(n)
            n+=1


    def MIDIsend(self):
        global i
        global loopstate
        n=0
        while n<7:

            if loopstate[n] <= len(sequencepool[n])-1:
                #print(i)
                while sequencepool[n][loopstate[n]][0]==count:
                    print "send" , n
                    if loopstate[n]==len(sequencepool[n])-1:
                        print("seq over")
                        loopstate[n]=0
                        break
                    else:
                        loopstate[n]+=1
            else:
                #print("No seq")
                pass
            n+=1
            #print(loopstate)
            




        



##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


class SequencerApp(App):
 
    def build(self):
        Config.set('graphics', 'KIVY_CLOCK', 'interrupt')
        Config.write()
        sm = Manager(transition=NoTransition())
        return sm



##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################


#Data
keyrange=[['C0',1],['C#0',0],['D0',1],['D#0',0],['E0',1],['F0',1],['F#0',0],['G0',1],['G#0',0],['A0',1],['A#0',0],['B0',1],
        ['C1',1],['C#1',0],['D1',1],['D#1',0],['E1',1],['F1',1],['F#1',0],['G1',1],['G#1',0],['A1',1],['A#1',0],['B1',1],
        ['C2',1],['C#2',0],['D2',1],['D#2',0],['E2',1],['F2',1],['F#2',0],['G2',1],['G#2',0],['A2',1],['A#2',0],['B2',1],
        ['C3',1],['C#3',0],['D3',1],['D#3',0],['E3',1],['F3',1],['F#3',0],['G3',1],['G#3',0],['A3',1],['A#3',0],['B3',1],
        ['C4',1],['C#4',0],['D4',1],['D#4',0],['E4',1],['F4',1],['F#4',0],['G4',1],['G#4',0],['A4',1],['A#4',0],['B4',1],
        ['C5',1],['C#5',0],['D5',1],['D#5',0],['E5',1],['F5',1],['F#5',0],['G5',1],['G#5',0],['A5',1],['A#5',0],['B5',1],
        ['C6',1],['C#6',0],['D6',1],['D#6',0],['E6',1],['F6',1],['F#6',0],['G6',1],['G#6',0],['A6',1],['A#6',0],['B6',1],
        ['C7',1],['C#7',0],['D7',1],['D#7',0],['E7',1],['F7',1],['F#7',0],['G7',1],['G#7',0],['A7',1],['A#7',0],['B7',1]]


timerange=["1","","","",".","","","",".","","","",".","","","",
"2","","","",".","","","",".","","","",".","","","",
"3","","","",".","","","",".","","","",".","","","",
"4","","","",".","","","",".","","","",".","","","",
"5","","","",".","","","",".","","","",".","","","",
"6","","","",".","","","",".","","","",".","","","",
"7","","","",".","","","",".","","","",".","","","",
"8","","","",".","","","",".","","","",".","","","",
"9","","","",".","","","",".","","","",".","","","",
"10","","","",".","","","",".","","","",".","","","",
"11","","","",".","","","",".","","","",".","","","",
"12","","","",".","","","",".","","","",".","","","",
"13","","","",".","","","",".","","","",".","","","",
"14","","","",".","","","",".","","","",".","","","",
"15","","","",".","","","",".","","","",".","","","",
"16","","","",".","","","",".","","","",".","","",""
]

keyrangeS=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20",
"21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40",
"41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60",
"61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80",
"81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100"]


timerangeS=["1","5","9","13","17","21","25","29","33","37","41","45","49","53","57","61",
"65","69","73","77","81","85","89","93","97","101","105","109","113","117","121","125",
"3","","","",".","","","",".","","","",".","","","",
"4","","","",".","","","",".","","","",".","","","",
"5","","","",".","","","",".","","","",".","","","",
"6","","","",".","","","",".","","","",".","","","",
"7","","","",".","","","",".","","","",".","","","",
"8","","","",".","","","",".","","","",".","","","",
"9","","","",".","","","",".","","","",".","","","",
"10","","","",".","","","",".","","","",".","","","",
"11","","","",".","","","",".","","","",".","","","",
"12","","","",".","","","",".","","","",".","","","",
"13","","","",".","","","",".","","","",".","","","",
"14","","","",".","","","",".","","","",".","","","",
"15","","","",".","","","",".","","","",".","","","",
"16","","","",".","","","",".","","","",".","","",""
]


sequence=[]
sequencepool=[[[12,41,1],[17,42,1],[25,42,1],[25,40,1],[25,45,1],[29,42,1],[29,45,1],[29,48,1]],[],[],[],[],[[5,39,1],[13,40,1]],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[]
]
#[12,41,1],[17,42,1],[25,42,1],[33,44,1]]
#[2,36,1],[1,37,1],[4,38,1],[5,39,1],[13,40,1]
#[Step number,Note number, Note length]
song=[ [1,1], [2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[15,1],[16,1] ]
#song=[[1,3,4,5,8,9],[2,3,6,7],[],[],[],[2,3,4],[],[],[],[],[]]

rangeX=0
rangeXs=0
zoom=4
rangeXmax=16*16-1
rangeYs=0
rangeY=36 #C0=0, 8 octaves
q=16
start=0
trackselected=1
loopsize=6
loopsizeS=64
counter=0
counter2=0
trackselectedparam=1
delta=0
interval = 0.0125
count=0
i=0
loopstate=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
with open('param.json') as f:
    paramcf1 = json.load(f)
#pprint(data)
#print(data)
print(paramcf1["midi-map"][0]["port"])
print(len(sequencepool[0]))
seq= SequencerApp()
seq.run()

 