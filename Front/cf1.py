import os
os.environ['KIVY_GL_BACKEND']='gl'
import kivy
import time
 
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen,NoTransition
from kivy.properties import ObjectProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.config import Config
from kivy.uix.button import Button
from kivy.clock import Clock
from decimal import *
import operator
import json
from pprint import pprint
from kivy.uix.tabbedpanel import TabbedPanel
import threading
import rtmidi
import mido




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
        global nextcall
        global playing
        if self.b001.state=="down":
            self.b001.text="PAUSE"
            nextcall=time.time()
            playing=1
            self.Timing=Timing()
            #self.startTimer()
            self.Timing.Timer()
            Clock.schedule_interval(self.movebar, 0.05)
            #Clock.schedule_interval(self.movebar, 0.01)
            #self.SeqScreen.startTimer()
        else:
            self.b001.text="START"
            playing=0
            Clock.unschedule(self.movebar)

    def stop(self):
        global counter
        global playing
        global count
        global loopstate
        self.b001.state="normal"
        self.b001.text="START"
        Clock.unschedule(self.movebar)
        counter=0
        position=0
        self.b015.pos=50,0
        playing=0
        count=0
        loopstate=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]




    def moveXrgh(self):
        global rangeXs
        if (rangeXs+16)*4<=1021:
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
            print(rangeXs)
           
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
        i=0
        while i <16:
            for elem in song[rangeXs+i]:
                elemY=elem-rangeYs
                elemX=i+1
                #print(i)
                #print(rangeXs)
                print(elemX)
                if elemY <=8:
                    elemY=-(int(elemY)-9)
                    if elemX<10:
                        b="b"+str(elemY)+"0"+str(elemX)
                    else:
                        b="b"+str(elemY)+str(elemX)
                    self.findButton(b)
                else:
                    pass
            i+=1
        self.loopbar()
        self.movebar()


 

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

    def movebar(self, *args):
        #print(counter)
        countbar=count%loopsizeS
        speed=47.5/64
        position=int(50+round((countbar-rangeXs*64)*speed))
        if position<50:
            self.b015.pos=1000,0
        else:
            self.b015.pos=position,0


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
        global buttonpouchedsong
        for key, val in self.ids.items():
            if val==button:
                ID=key
        y=int(ID[1])
        yp=-(y-8)
        x=int(ID[-2:])
        buttonpouchedsong=ID
        if button.state=="normal":
            song[x+rangeXs-1].remove(yp+rangeYs+1)
            print(song)
            #Nmax+=-1
        else:
            song[x+rangeXs-1].append(yp+rangeYs+1)	
            song[x+rangeXs-1]=sorted(song[x+rangeXs-1])
            print(song)
            
            #print(song)

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
        for elem in song:
            if trackselected in elem:
                elem.remove(trackselected)
            print(song)
        self.loadseq()


    def on_enter(self):
        if playing==1:
            self.b001.state="down"
            self.b001.text="PAUSE"
            Clock.schedule_interval(self.movebar, 0.05)
        else: 
            self.b001.state="normal"
            self.b001.text="START"
            self.movebar()

    def on_touch_move(self, touch):
        global buttonpouchedsong
        global sequencepool
        if self.collide_point(*touch.pos):
            #print(touch.pos)
            x=touch.pos[0]-50
            y=touch.pos[1]
            bx=int(x/47+1)
            by=int(y/47+1)
            byc=8-by
            #print(bx,by)
            if (bx>int(buttonpouchedsong[-2:]) and by==int(buttonpouchedsong[1])):
                if bx<=9:
                    b="b"+str(by)+"0"+str(bx)
                else:
                    b="b"+str(by)+str(bx)
                #print(b)
                for val in self.ids.items():
                   # print(val)
                    if val[0]==b:
                        #print("here") 
                        if val[1].state=='normal':
                            val[1].state='down'
                            song[bx+rangeXs-1].append(byc+rangeYs+1) 
                            song[bx+rangeXs-1]=sorted(song[bx+rangeXs-1])
                            print(song)


 


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
            if playing==1:
                self.b001.state="down"
                self.b001.text="PAUSE"
                Clock.schedule_interval(self.movebar, 0.05)
            else: 
                self.b001.state="normal"
                self.b001.text="START"
                self.movebar()
        else:
            start = start +1



    def monitor(self, button):
        global sequencepool
        global buttonpouched
        #print("monitored")

        for key, val in self.ids.items():
            if val==button:
                ID=key
        y=int(ID[1])
        x=int(ID[-2:])
        buttonpouched=ID
        #print(buttonpouched)
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
                    rangeX=128*7
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
        #print(trackselected)
        sequence=sequencepool[trackselected-1]
        #print(sequence)
        i=1
        while i <= len(sequence):
            Xc=sequence[i-1][0]-rangeX
            Yc=sequence[i-1][1]-rangeY+1
            #print(Xc)
            if (Xc>=0 and Xc <= 16*zoom and (sequence[i-1][0]-1)%zoom ==0):
                if (Yc >= 1 and Yc <=8):
                    Xcp=int(Xc/(zoom+0.0000000000001))+1
                    #print(i*100)
                    #print(Xcp)
                    if Xcp<=9:
                        b="b"+str(Yc)+"0"+str(Xcp)
                    else:
                        b="b"+str(Yc)+str(Xcp)
                    #print(b)
                    self.findButton(b)
                else:
                    pass
            i+=1
        self.loopbar()
        self.movebar()

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
        global playing
        if self.b001.state=="down":
            playing=1
            self.b001.text="PAUSE"
            nextcall=time.time()
            self.Timing=Timing()
            #self.startTimer()
            self.Timing.Timer()
            
            Clock.schedule_interval(self.movebar, 0.05)
            
        else:
            self.b001.text="START"
            playing=0
            Clock.unschedule(self.movebar)

    def stop(self):
        global counter
        global count
        global playing
        global loopstate
        self.b001.state="normal"
        self.b001.text="START"
        Clock.unschedule(self.movebar)
        counter=0
        position=0
        self.b015.pos=50,0
        playing=0
        count=0
        loopstate=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

       

    def movebar(self, *args):
        #print(counter)
        countbar=count%loopsize[trackselected-1]
        speed=47.5/zoom
        position=int(50+round((countbar-rangeX)*speed))
        if position<50:
            self.b015.pos=1000,0
        else:
            self.b015.pos=position,0


    def loopbar(self):
        global loopsize
        loopbar_pos=loopsize[trackselected-1]
        #print(loopsize[trackselected])
        #print(rangeX)
        if loopbar_pos<=rangeX+16*zoom:
            if 48+(loopbar_pos-rangeX)/zoom*47>=5:
                self.b017.pos=48+(loopbar_pos-rangeX)/zoom*47,0
            else:
                self.b017.pos=1000,1000
        else:
            self.b017.pos=1000,1000
        self.gridbar()
        
    def gridbar(self):
        #print(rangeX)
        if (rangeX-3*zoom)%(4*zoom)==0:
            self.ids.b018.pos = 94,0
        if (rangeX-2*zoom)%(4*zoom)==0:
            self.ids.b018.pos = 141,0
        if (rangeX-1*zoom)%(4*zoom)==0:
            self.ids.b018.pos = 188,0
        if rangeX%(4*zoom)==0:
            self.ids.b018.pos = 235,0

    def on_touch_move(self, touch):
        global buttonpouched
        global sequencepool
        if self.collide_point(*touch.pos):
            #print(touch.pos)
            x=touch.pos[0]-50
            y=touch.pos[1]
            bx=int(x/47+1)
            by=int(y/47+1)
            #print(bx,by)
            if (bx>int(buttonpouched[-2:]) and by==int(buttonpouched[1])):
                if bx<=9:
                    b="b"+str(by)+"0"+str(bx)
                else:
                    b="b"+str(by)+str(bx)
                #print(b)
                for val in self.ids.items():
                   # print(val)
                    if val[0]==b:
                        #print("here") 
                        if val[1].state=='normal':
                            val[1].state='down'
                            #print(val[1].background_color)
                            #val[1].background_color=[1, 0.7, 0, 1]
                            sequencepool[trackselected-1].append([(bx-1)*zoom+rangeX+1,by+rangeY-1,1])
                            sequencepool[trackselected-1]=sorted(sequencepool[trackselected-1], key=operator.itemgetter(0))
                            print(sequencepool)
                            


    def on_touch_up(self,touch):
        global buttonpouched
        global sequencepool
        if self.collide_point(*touch.pos):
            #print(touch.pos)
            x=touch.pos[0]-50
            y=touch.pos[1]
            bx=int(x/47+1)
            by=int(y/47+1)
            #print(bx,by)
            if (bx>int(buttonpouched[-2:]) and by==int(buttonpouched[1])):
                if bx<=9:
                    b="b"+str(by)+"0"+str(bx)
                else:
                    b="b"+str(by)+str(bx)
                #print(b)
                for val in self.ids.items():
                   # print(val)
                    if val[0]==b:
                        #sequencepool[trackselected-1].append([(bx-1)*zoom+rangeX+1,by+rangeY-1,2])
                        #sequencepool[trackselected-1]=sorted(sequencepool[trackselected-1], key=operator.itemgetter(0))
                        #print(sequencepool)
                        print("released")
        

    




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
        global Nmax
        global n
        nextcall = nextcall+interval

        th=threading.Timer(nextcall - time.time(), self.Timer)
        print(nextcall-time.time())
        self.MIDIsend()

        if playing==1:
            th.start()
            count+=1
        
        if count > 2000:
            count=0
            loopstate=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        print(count)



    def MIDIsend(self):

        global loopstate
        currentstep=count/(16*4)
        i=0
        while i<len(song[currentstep]):
            n=song[currentstep][i]-1
            #n is current track
            if count%loopsize[n]==0:
                loopstate[n]=0
            #print(loopstate)
            if loopstate[n] <= len(sequencepool[n])-1:
                #print(i)
                while sequencepool[n][loopstate[n]][0]==count%loopsize[n]:
                    #print "send" , sequencepool[n][loopstate[n]][1] ,"channel" , n+1
                    if sequencepool[n][loopstate[n]][2]==1:
                        print "send" , sequencepool[n][loopstate[n]][1] ,"channel" , n+1
                        if n < 15:
                            channel=n
                        else:
                            channel=1
                        msg=mido.Message('note_on', note=sequencepool[n][loopstate[n]][1], channel=channel)
                        port.send(msg)
                    else:
                        print "stop" , sequencepool[n][loopstate[n]][1] ,"channel" , n+1

                    if loopstate[n]==len(sequencepool[n])-1:
                        #print("seq over")
                        loopstate[n]=0
                        break
                    else:
                        loopstate[n]+=1

                    
            else:
                pass
                print("pass")
                #print(loopstate)
            i+=1

            
    #def MIDImessages(self):

        
            

            
            




        



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
"16","","","",".","","","",".","","","",".","","","",
"17","","","",".","","","",".","","","",".","","","",
"18","","","",".","","","",".","","","",".","","","",
"19","","","",".","","","",".","","","",".","","","",
"20","","","",".","","","",".","","","",".","","","",
"21","","","",".","","","",".","","","",".","","","",
"22","","","",".","","","",".","","","",".","","","",
"23","","","",".","","","",".","","","",".","","","",
"24","","","",".","","","",".","","","",".","","","",
"25","","","",".","","","",".","","","",".","","","",
"26","","","",".","","","",".","","","",".","","","",
"27","","","",".","","","",".","","","",".","","","",
"28","","","",".","","","",".","","","",".","","","",
"29","","","",".","","","",".","","","",".","","","",
"30","","","",".","","","",".","","","",".","","","",
"31","","","",".","","","",".","","","",".","","","",
"32","","","",".","","","",".","","","",".","","","",
"33","","","",".","","","",".","","","",".","","","",
"34","","","",".","","","",".","","","",".","","","",
"35","","","",".","","","",".","","","",".","","","",
"36","","","",".","","","",".","","","",".","","","",
"37","","","",".","","","",".","","","",".","","","",
"38","","","",".","","","",".","","","",".","","","",
"39","","","",".","","","",".","","","",".","","","",
"40","","","",".","","","",".","","","",".","","","",
"41","","","",".","","","",".","","","",".","","","",
"42","","","",".","","","",".","","","",".","","","",
"43","","","",".","","","",".","","","",".","","","",
"44","","","",".","","","",".","","","",".","","","",
"45","","","",".","","","",".","","","",".","","","",
"46","","","",".","","","",".","","","",".","","","",
"47","","","",".","","","",".","","","",".","","","",
"48","","","",".","","","",".","","","",".","","","",
"49","","","",".","","","",".","","","",".","","","",
"50","","","",".","","","",".","","","",".","","","",
"51","","","",".","","","",".","","","",".","","","",
"52","","","",".","","","",".","","","",".","","","",
"53","","","",".","","","",".","","","",".","","","",
"54","","","",".","","","",".","","","",".","","","",
"55","","","",".","","","",".","","","",".","","","",
"56","","","",".","","","",".","","","",".","","","",
"57","","","",".","","","",".","","","",".","","","",
"58","","","",".","","","",".","","","",".","","","",
"59","","","",".","","","",".","","","",".","","","",
"60","","","",".","","","",".","","","",".","","","",
"61","","","",".","","","",".","","","",".","","","",
"62","","","",".","","","",".","","","",".","","","",
"63","","","",".","","","",".","","","",".","","","",
"64","","","",".","","","",".","","","",".","","","",
"65","","","",".","","","",".","","","",".","","","",
"66","","","",".","","","",".","","","",".","","","",
"67","","","",".","","","",".","","","",".","","","",
"68","","","",".","","","",".","","","",".","","","",
"69","","","",".","","","",".","","","",".","","","",
"70","","","",".","","","",".","","","",".","","","",
"71","","","",".","","","",".","","","",".","","","",
"72","","","",".","","","",".","","","",".","","","",
"73","","","",".","","","",".","","","",".","","","",
"74","","","",".","","","",".","","","",".","","","",
"75","","","",".","","","",".","","","",".","","","",
"76","","","",".","","","",".","","","",".","","","",
]

keyrangeS=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20",
"21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40",
"41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60",
"61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80",
"81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100"]


timerangeS=["1","5","9","13","17","21","25","29","33","37","41","45","49","53","57","61",
"65","69","73","77","81","85","89","93","97","101","105","109","113","117","121","125",
"129","133","137","141","145","149","153","157","161","165","169","173","177","181","185","189",
"193","197","201","205","209","213","217","221","225","229","233","237","241","245","249","253",
"257","261","265","269","273","277","281","285","289","293","297","301","305","309","313","317",
"321","325","329","333","337","341","345","349","353","357","361","365","369","373","377","381",
"385","389","393","397","401","405","409","413","417","421","425","429","433","437","441","445",
"449","453","457","461","465","469","473","477","481","485","489","493","497","501","505","509",
"513","517","521","525","529","533","537","541","545","549","553","557","561","565","569","573",
"577","581","585","589","593","597","601","605","609","613","617","621","625","629","633","637",
"641","645","649","653","657","661","665","669","673","677","681","685","689","693","697","701",
"705","709","713","717","721","725","729","733","737","741","745","749","753","757","761","765",
"769","773","777","781","785","789","793","797","801","805","809","813","817","821","825","829",
"833","837","841","845","849","853","857","861","865","869","873","877","881","885","889","893",
"897","901","905","909","913","917","921","925","929","933","937","941","945","949","953","957",
"961","965","969","973","977","981","985","989","993","997","1001","1005","1009","1013","1017","1021"]


sequence=[]
sequencepool=[[[12,41,1],[17,42,1],[25,42,1],[25,40,1],[26,45,1],[29,42,1],[29,45,1],[70,48,1]],[[17,42,1]],[[12,41,1],[17,42,1],[70,42,1]],[[17,42,1]],[[17,42,1]],[[5,39,1],[13,40,1]],[],[],[],[[17,42,1]],
[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[]
]
#[Step number,Note number, Note length]
#song=[[1,2,3,5,6,10],[1,5],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#song=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
song=[[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

rangeX=0
rangeXs=0
zoom=4
rangeXmax=64*16-1
rangeYs=0
rangeY=36 #C0=0, 8 octaves
q=16
start=0
bom=120
trackselected=1
#loopsize=6
loopsizeS=3000
counter=0
counter2=0
trackselectedparam=1
delta=0
interval = 0.03125
count=0
loopstate=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
print(loopstate)
loopsize=[64,64,64,64,64,32,64,64,64,64,64,64,64,64,64,32,64,64,64,64,64,64,64,64,64,32,64,64,64,64,
64,64,64,64,64,32,64,64,64,64,64,64,64,64,64,32,64,64,64,64,64,64,64,64,64,32,64,64,64,64,
64,64,64,64,64,32,64,64,64,64,64,64,64,64,64,32,64,64,64,64,64,64,64,64,64,32,64,64,64,64,
64,64,64,64,64,32,64,64,64,64]
playing=0
buttonpouched="b000"
buttonpouchedsong="b000"
with open('param.json') as f:
    paramcf1 = json.load(f)

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)
port = available_ports[0]
port = mido.open_output(port)
seq= SequencerApp()
seq.run()

 