import kivy
import time
 
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
#from kivy.properties import StringProperty
#from kivy.factory import Factory
from kivy.config import Config
from kivy.uix.button import Button
#from kivy.uix.widget import *
from kivy.clock import Clock
from decimal import *



Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480') 


 

class SeqLayout(GridLayout):
 
   

    def monitor(self, button):
        for key, val in self.ids.items():
            if val==button:
                ID=key
        y=int(ID[1])
        x=int(ID[-2:])
        if button.state=="normal":
            sequence.remove([(x-1)*zoom+rangeX+1,y+rangeY-1,1])
            #print(sequence)
        else:
            sequence.append([(x-1)*zoom+rangeX+1,y+rangeY-1,1])
            print(x)
            print(rangeX)
            print((x-1)*zoom+rangeX+1)
            
        

    def clearStep(self,button):
        button.state="normal"


    def clear(self):
        for val in self.ids.items():
            self.clearStep(val[1])
        
    
    def zoomstep(self,button,text):
        button.text=text

    def zoom(self):
        global rangeX
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
        self.clear()
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

    def menu(self):
        if self.b007.state=="down":
            self.b008.pos= 648,360
            self.b009.pos= 648,301
            self.b011.pos= 496,900
            self.b012.pos= 496,900
            self.b013.pos= 344,900
            self.b014.pos= 344,900
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
        if self.b001.state=="down":
            self.b001.text="PAUSE"
            Clock.schedule_interval(self.movebar, 0.01)
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
        
        

    def movebar(self, *args):
        print(counter)
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
        self.b015.pos=position,0
        






class SequencerApp(App):
 
    def build(self):
        return SeqLayout()





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


sequence=[]
#[12,41,1],[17,42,1],[25,42,1],[33,44,1]]
#[2,36,1],[1,37,1],[4,38,1],[5,39,1],[13,40,1]
#[Step number,Note number, Note length]
rangeX=0
zoom=4
rangeXmax=16*16-1
rangeY=36 #C0=0, 8 octaves
q=16
counter=0
seq= SequencerApp()
seq.run()

 
