import os
os.environ['KIVY_GL_BACKEND']='gl'
import kivy
import platform
import time
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.config import Config
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.tabbedpanel import TabbedPanel
from decimal import *
import operator
import json
import multiprocessing
import rtmidi
import mido
import serial
import numpy
from iconfonts import *
from os.path import join, dirname

register('default_font', 'Icons.ttf',
             join(dirname(__file__), 'Icons.fontd'))
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480') 

if platform.system()=='Linux':
	rpi=1
else:
	rpi=0

print("rpi detected:",rpi)
if rpi==1:
	import smbus
	from RPi import GPIO
	ser=serial.Serial('/dev/ttyAMA0', 38400)
	bus = smbus.SMBus(1)
	clk = 16
	dt = 20
	sw = 21
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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
		global rangeMidi
		global rangeCV
		global rangeCVTrack
		rangeCVTrack=0
		rangeMidi=0
		rangeCV=0
		self.midiupdate()
		self.CVupdate()
		self.convert()


    def midiupdate(self):
    	self.b1001.text=paramcf1["midi-map"][rangeMidi]["port"]
        self.b1002.text=paramcf1["midi-map"][rangeMidi+1]["port"]
        self.b1003.text=paramcf1["midi-map"][rangeMidi+2]["port"]
        self.b1004.text=paramcf1["midi-map"][rangeMidi+3]["port"]
        self.b1005.text=paramcf1["midi-map"][rangeMidi+4]["port"]
        self.b1006.text=paramcf1["midi-map"][rangeMidi+5]["port"]
        self.b2001.text=paramcf1["midi-map"][rangeMidi]["channel"]
        self.b2002.text=paramcf1["midi-map"][rangeMidi+1]["channel"]
        self.b2003.text=paramcf1["midi-map"][rangeMidi+2]["channel"]
        self.b2004.text=paramcf1["midi-map"][rangeMidi+3]["channel"]
        self.b2005.text=paramcf1["midi-map"][rangeMidi+4]["channel"]
        self.b2006.text=paramcf1["midi-map"][rangeMidi+5]["channel"]
        self.lbl1.text = 'Track' + str(rangeMidi + 1)+':'
        self.lbl2.text = 'Track' + str(rangeMidi + 2)+':'
        self.lbl3.text = 'Track' + str(rangeMidi + 3)+':'
        self.lbl4.text = 'Track' + str(rangeMidi + 4)+':'
        self.lbl5.text = 'Track' + str(rangeMidi + 5)+':'
        self.lbl6.text = 'Track' + str(rangeMidi + 6)+':'



    def CVupdate(self):
    	self.b10001.text=paramcf1["CV-map"][rangeCV]["Type"]
        self.b10002.text=paramcf1["CV-map"][rangeCV+1]["Type"]
        self.b10003.text=paramcf1["CV-map"][rangeCV+2]["Type"]
        self.b10004.text=paramcf1["CV-map"][rangeCV+3]["Type"]
        self.b10005.text=paramcf1["CV-map"][rangeCV+4]["Type"]
        self.b10006.text=paramcf1["CV-map"][rangeCV+5]["Type"]
        self.b20001.text=paramcf1["CV-map"][rangeCV]["Track"]
        self.b20002.text=paramcf1["CV-map"][rangeCV+1]["Track"]
        self.b20003.text=paramcf1["CV-map"][rangeCV+2]["Track"]
        self.b20004.text=paramcf1["CV-map"][rangeCV+3]["Track"]
        self.b20005.text=paramcf1["CV-map"][rangeCV+4]["Track"]
        self.b20006.text=paramcf1["CV-map"][rangeCV+5]["Track"]
        self.b30001.text=paramcf1["CV-map"][rangeCV]["Voltage"]
        self.b30002.text=paramcf1["CV-map"][rangeCV+1]["Voltage"]
        self.b30003.text=paramcf1["CV-map"][rangeCV+2]["Voltage"]     
        self.b30004.text=paramcf1["CV-map"][rangeCV+3]["Voltage"]
        self.b30005.text=paramcf1["CV-map"][rangeCV+4]["Voltage"]
        self.b30006.text=paramcf1["CV-map"][rangeCV+5]["Voltage"]
     	self.VoltageHide()
        self.lbl10.text = 'CV' + str(rangeCV + 1)+':'
        self.lbl20.text = 'CV' + str(rangeCV + 2)+':'
        self.lbl30.text = 'CV' + str(rangeCV + 3)+':'
        self.lbl40.text = 'CV' + str(rangeCV + 4)+':'
        self.lbl50.text = 'CV' + str(rangeCV + 5)+':'
        self.lbl60.text = 'CV' + str(rangeCV + 6)+':'

    def VoltageHide(self):
    	if self.b10001.text=="PITCH":
        	self.b30001.pos=479,320
        else:
        	self.b30001.pos=1479,320
        if self.b10002.text=="PITCH":
        	self.b30002.pos=479,260
        else:
        	self.b30002.pos=1479,320
        if self.b10003.text=="PITCH":
        	self.b30003.pos=479,200
        else:
        	self.b30003.pos=1479,320        
        if self.b10004.text=="PITCH":
        	self.b30004.pos=479,140
        else:
        	self.b30004.pos=1479,320
        if self.b10005.text=="PITCH":
        	self.b30005.pos=479,80
        else:
        	self.b30005.pos=1479,320
        if self.b10006.text=="PITCH":
        	self.b30006.pos=479,20
        else:
        	self.b30006.pos=1479,320  



    def midiportselect(self):
        self.b4000.pos=328,120
        self.b4001.pos=329,121
        self.b4002.pos=329,182
        self.b4003.text="MIDI PORT:"
        self.b4001.text="2"
        self.b4002.text="1"
        self.b4003.pos=329,243
        self.b3005.pos=0,0


    def midichannelselect(self):
        self.b5017.pos=310,305
        self.b5017.text="MIDI CHANNEL:"
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
    	self.b5001.text="1"
        self.b5005.text="5"
        self.b5009.text="9"
        self.b5013.text="13"
        self.b5002.text="2"
        self.b5006.text="6"
        self.b5010.text="10"
        self.b5014.text="14"
        self.b5003.text="3"
        self.b5007.text="7"
        self.b5011.text="11"
        self.b5015.text="15"
        self.b5004.text="4"
        self.b5008.text="8"
        self.b5012.text="12"
        self.b5016.text="16"

    def CVTypeselect(self):
        self.b4000.pos=328,120
        self.b4001.pos=329,121
        self.b4002.pos=329,182
        self.b4001.text="GATE"
        self.b4002.text="PITCH"
        self.b4003.text="CV TYPE:"
        self.b4003.pos=329,243
        self.b3005.pos=0,0

    def CVTrackselect(self):
    	global rangeCVTrack
    	rangeCVTrack=0
        self.b5017.pos=310,305
        self.b5017.text="TRACK:"
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
        self.b5001.text="1"
        self.b5005.text="5"
        self.b5009.text="9"
        self.b5013.text="13"
        self.b5002.text="2"
        self.b5006.text="6"
        self.b5010.text="10"
        self.b5014.text="14"
        self.b5003.text="3"
        self.b5007.text="7"
        self.b5011.text="11"
        self.b5015.text="15"
        self.b5004.text="4"
        self.b5008.text="8"
        self.b5012.text="12"
        self.b5016.text="16"

    def CVVoltageselect(self):
        self.b4000.pos=328,120
        self.b4001.pos=329,121
        self.b4002.pos=329,182
        self.b4001.text="[ -5V ; 5V ]"
        self.b4002.text="[ 0V ; 10V ]"
        self.b4003.pos=329,243
        self.b4003.text="VOLTAGE:"
        self.b3005.pos=0,0


    def trackselected(self,button):
        global trackselectedparam
        for key, val in self.ids.items():
            if val==button:
                ID=key
        trackselectedparam=int(ID[-3:])+rangeMidi
        print(trackselectedparam)


    def CVselected(self,button):
        global CVselectedparam
        for key, val in self.ids.items():
            if val==button:
                ID=key
        CVselectedparam=int(ID[-2:])+rangeCV
        print(CVselectedparam)



    def port1(self,button):
        global Sendinfo
        for key, val in self.ids.items():
            if val==button:
                ID=key
        new=(ID[-1:])

        if self.b4003.text=="MIDI PORT:":
	        paramcf1["midi-map"][trackselectedparam-1]["port"] = new
	        with open("param.json", "w") as jsonFile:
	            json.dump(paramcf1, jsonFile)
	        self.midiupdate()


        if self.b4003.text=="VOLTAGE:":
			if int(new)==1:
				paramcf1["CV-map"][CVselectedparam-1]["Voltage"] = "[ 0V ; 10V ]"
				#CVassign[CVselectedparam-1][2]=5
			if int(new)==2:
				paramcf1["CV-map"][CVselectedparam-1]["Voltage"] = "[ -5V ; 5V ]"
				#CVassign[CVselectedparam-1][2]=0
			with open("param.json", "w") as jsonFile:
				json.dump(paramcf1, jsonFile)
			self.CVupdate()
			#Sendinfo[CVassign[trackselectedparam-1][1]-1][5]=CVassign[CVselectedparam-1][2]



        if self.b4003.text=="CV TYPE:":
			if int(new)==1:
				paramcf1["CV-map"][CVselectedparam-1]["Type"] = "PITCH"
				i=0
				while i<12:
					if paramcf1["CV-map"][i]["Type"]== "PITCH" and i!=CVselectedparam-1 and paramcf1["CV-map"][i]["Track"]==paramcf1["CV-map"][CVselectedparam-1]["Track"]:
					#old=paramcf1["CV-map"][i]["Track"]
						paramcf1["CV-map"][i]["Track"] = "NONE"
						break
					i+=1
				#CVassign[CVselectedparam-1][0]="PITCH"
				#Sendinfo[CVassign[trackselectedparam-1][1]-1][1]=CVinfo[CVassign[trackselectedparam-1][1]-1][0]
				#Sendinfo[CVassign[trackselectedparam-1][1]-1][2]=CVinfo[CVassign[trackselectedparam-1][1]-1][1]
				#Sendinfo[CVassign[trackselectedparam-1][1]-1][3]=0
				#Sendinfo[CVassign[trackselectedparam-1][1]-1][4]=0
			if int(new)==2:
				paramcf1["CV-map"][CVselectedparam-1]["Type"] = "GATE"
				i=0
				while i<12:
					if paramcf1["CV-map"][i]["Type"]== "GATE" and i!=CVselectedparam-1 and paramcf1["CV-map"][i]["Track"]==paramcf1["CV-map"][CVselectedparam-1]["Track"]:
					#old=paramcf1["CV-map"][i]["Track"]
						paramcf1["CV-map"][i]["Track"] = "NONE"
						break
					i+=1				
				#CVassign[CVselectedparam-1][0]="GATE"
				#Sendinfo[CVassign[trackselectedparam-1][1]-1][1]=0
				#Sendinfo[CVassign[trackselectedparam-1][1]-1][2]=0
				#Sendinfo[CVassign[trackselectedparam-1][1]-1][3]=CVinfo[CVassign[trackselectedparam-1][1]-1][0]
				#Sendinfo[CVassign[trackselectedparam-1][1]-1][4]=CVinfo[CVassign[trackselectedparam-1][1]-1][1]		
			with open("param.json", "w") as jsonFile:
				json.dump(paramcf1, jsonFile)
			self.CVupdate()
			self.convert()
        print(Sendinfo)


    def port2(self,button):
		global Sendinfo
		for key, val in self.ids.items():
			if val==button:
				ID=key
		new=int((ID[-2:]))

		if self.b5017.text=="TRACK:":
			new=int(new)+rangeCVTrack
			paramcf1["CV-map"][CVselectedparam-1]["Track"] = str(new)
			i=0
			while i<12:
				if paramcf1["CV-map"][i]["Track"]== str(new) and i!=CVselectedparam-1 and paramcf1["CV-map"][i]["Type"]==paramcf1["CV-map"][CVselectedparam-1]["Type"]:
					paramcf1["CV-map"][i]["Track"] = "NONE"
					break
				i+=1
			with open("param.json", "w") as jsonFile:
				json.dump(paramcf1, jsonFile)
			self.CVupdate()
			self.convert()


		else:
			paramcf1["midi-map"][trackselectedparam-1]["channel"] = str(new)
			with open("param.json", "w") as jsonFile:
			    json.dump(paramcf1, jsonFile)
			self.midiupdate()
			self.convert()
			print(Sendinfo)

    def convert(self):
		i=0
		j=0
		k=0
		while j<len(Sendinfo):
			Sendinfo[j]=[0,0,0,0,0,0]
			j+=1
		while i<12:

			if paramcf1["CV-map"][i]["Type"]=="PITCH" and paramcf1["CV-map"][i]["Track"]!="NONE":
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][1]=CVinfo[i][0]
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][2]=CVinfo[i][1]
			elif paramcf1["CV-map"][i]["Track"]=="NONE":
				pass
			else:
				#Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][1]=0
				#Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][2]=0
				pass
			
			if paramcf1["CV-map"][i]["Type"]=="GATE" and paramcf1["CV-map"][i]["Track"]!="NONE":
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][3]=CVinfo[i][0]
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][4]=CVinfo[i][1]
			elif paramcf1["CV-map"][i]["Track"]=="NONE":
				pass
			else:
				#Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][3]=0
				#Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][4]=0
				pass
			
			if paramcf1["CV-map"][i]["Voltage"]=="[ 0V ; 10V ]" and paramcf1["CV-map"][i]["Track"]!="NONE":
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][5]=5
			elif paramcf1["CV-map"][i]["Track"]=="NONE":
				pass
			else:
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][5]=0
			i+=1
		
		while k<len(Sendinfo):
			Sendinfo[k][0]=int(paramcf1["midi-map"][k]["channel"])
			k+=1
		if start==1:
			q4.put(Sendinfo)
			r1.put(Sendinfo)
		return Sendinfo


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

    def scrollDownMIDI(self):
        global rangeMidi
        if rangeMidi <  94:
            self.b2001.text = paramcf1['midi-map'][rangeMidi + 1]["channel"]
            self.b2002.text = paramcf1['midi-map'][rangeMidi + 2]["channel"]
            self.b2003.text = paramcf1['midi-map'][rangeMidi + 3]["channel"]
            self.b2004.text = paramcf1['midi-map'][rangeMidi + 4]["channel"]
            self.b2005.text = paramcf1['midi-map'][rangeMidi + 5]["channel"]
            self.b2006.text = paramcf1['midi-map'][rangeMidi + 6]["channel"]
            self.b1001.text = paramcf1['midi-map'][rangeMidi + 1]["port"]
            self.b1002.text = paramcf1['midi-map'][rangeMidi + 2]["port"]
            self.b1003.text = paramcf1['midi-map'][rangeMidi + 3]["port"]
            self.b1004.text = paramcf1['midi-map'][rangeMidi + 4]["port"]
            self.b1005.text = paramcf1['midi-map'][rangeMidi + 5]["port"]
            self.b1006.text = paramcf1['midi-map'][rangeMidi + 6]["port"]
            self.lbl1.text = 'Track' + str(rangeMidi + 2)+':'
            self.lbl2.text = 'Track' + str(rangeMidi + 3)+':'
            self.lbl3.text = 'Track' + str(rangeMidi + 4)+':'
            self.lbl4.text = 'Track' + str(rangeMidi + 5)+':'
            self.lbl5.text = 'Track' + str(rangeMidi + 6)+':'
            self.lbl6.text = 'Track' + str(rangeMidi + 7)+':'
            rangeMidi+= 1   
        else:
            pass

    def scrollUpMIDI(self):
        global rangeMidi
        if rangeMidi >  0:
            self.b2001.text = paramcf1['midi-map'][rangeMidi - 1]["channel"]
            self.b2002.text = paramcf1['midi-map'][rangeMidi]["channel"]
            self.b2003.text = paramcf1['midi-map'][rangeMidi + 1]["channel"]
            self.b2004.text = paramcf1['midi-map'][rangeMidi + 2]["channel"]
            self.b2005.text = paramcf1['midi-map'][rangeMidi + 3]["channel"]
            self.b2006.text = paramcf1['midi-map'][rangeMidi + 4]["channel"]
            self.b1001.text = paramcf1['midi-map'][rangeMidi - 1]["port"]
            self.b1002.text = paramcf1['midi-map'][rangeMidi]["port"]
            self.b1003.text = paramcf1['midi-map'][rangeMidi + 1]["port"]
            self.b1004.text = paramcf1['midi-map'][rangeMidi + 2]["port"]
            self.b1005.text = paramcf1['midi-map'][rangeMidi + 3]["port"]
            self.b1006.text = paramcf1['midi-map'][rangeMidi + 4]["port"]
            self.lbl1.text = 'Track' + str(rangeMidi)+':'
            self.lbl2.text = 'Track' + str(rangeMidi + 1)+':'
            self.lbl3.text = 'Track' + str(rangeMidi + 2)+':'
            self.lbl4.text = 'Track' + str(rangeMidi + 3)+':'
            self.lbl5.text = 'Track' + str(rangeMidi + 4)+':'
            self.lbl6.text = 'Track' + str(rangeMidi + 5)+':'
            rangeMidi-= 1   
        else:
            pass


    def scrollDownCV(self):
        global rangeCV
        if rangeCV <  6:
            self.b20001.text = paramcf1['CV-map'][rangeCV + 1]["Track"]
            self.b20002.text = paramcf1['CV-map'][rangeCV + 2]["Track"]
            self.b20003.text = paramcf1['CV-map'][rangeCV + 3]["Track"]
            self.b20004.text = paramcf1['CV-map'][rangeCV + 4]["Track"]
            self.b20005.text = paramcf1['CV-map'][rangeCV + 5]["Track"]
            self.b20006.text = paramcf1['CV-map'][rangeCV + 6]["Track"]
            self.b10001.text = paramcf1['CV-map'][rangeCV + 1]["Type"]
            self.b10002.text = paramcf1['CV-map'][rangeCV + 2]["Type"]
            self.b10003.text = paramcf1['CV-map'][rangeCV + 3]["Type"]
            self.b10004.text = paramcf1['CV-map'][rangeCV + 4]["Type"]
            self.b10005.text = paramcf1['CV-map'][rangeCV + 5]["Type"]
            self.b10006.text = paramcf1['CV-map'][rangeCV + 6]["Type"]
            self.b30001.text = paramcf1['CV-map'][rangeCV + 1]["Voltage"]
            self.b30002.text = paramcf1['CV-map'][rangeCV + 2]["Voltage"]
            self.b30003.text = paramcf1['CV-map'][rangeCV + 3]["Voltage"]
            self.b30004.text = paramcf1['CV-map'][rangeCV + 4]["Voltage"]
            self.b30005.text = paramcf1['CV-map'][rangeCV + 5]["Voltage"]
            self.b30006.text = paramcf1['CV-map'][rangeCV + 6]["Voltage"]
            self.lbl10.text = 'CV' + str(rangeCV + 2)+':'
            self.lbl20.text = 'CV' + str(rangeCV + 3)+':'
            self.lbl30.text = 'CV' + str(rangeCV + 4)+':'
            self.lbl40.text = 'CV' + str(rangeCV + 5)+':'
            self.lbl50.text = 'CV' + str(rangeCV + 6)+':'
            self.lbl60.text = 'CV' + str(rangeCV + 7)+':'
            rangeCV+= 1   
        else:
            pass
        self.VoltageHide()

    def scrollUpCV(self):
        global rangeCV
        if rangeCV >  0:
            self.b20001.text = paramcf1['CV-map'][rangeCV - 1]["Track"]
            self.b20002.text = paramcf1['CV-map'][rangeCV]["Track"]
            self.b20003.text = paramcf1['CV-map'][rangeCV + 1]["Track"]
            self.b20004.text = paramcf1['CV-map'][rangeCV + 2]["Track"]
            self.b20005.text = paramcf1['CV-map'][rangeCV + 3]["Track"]
            self.b20006.text = paramcf1['CV-map'][rangeCV + 4]["Track"]
            self.b10001.text = paramcf1['CV-map'][rangeCV - 1]["Type"]
            self.b10002.text = paramcf1['CV-map'][rangeCV]["Type"]
            self.b10003.text = paramcf1['CV-map'][rangeCV + 1]["Type"]
            self.b10004.text = paramcf1['CV-map'][rangeCV + 2]["Type"]
            self.b10005.text = paramcf1['CV-map'][rangeCV + 3]["Type"]
            self.b10006.text = paramcf1['CV-map'][rangeCV + 4]["Type"]
            self.b30001.text = paramcf1['CV-map'][rangeCV - 1]["Voltage"]
            self.b30002.text = paramcf1['CV-map'][rangeCV]["Voltage"]
            self.b30003.text = paramcf1['CV-map'][rangeCV + 1]["Voltage"]
            self.b30004.text = paramcf1['CV-map'][rangeCV + 2]["Voltage"]
            self.b30005.text = paramcf1['CV-map'][rangeCV + 3]["Voltage"]
            self.b30006.text = paramcf1['CV-map'][rangeCV + 4]["Voltage"]
            self.lbl10.text = 'CV' + str(rangeCV)+':'
            self.lbl20.text = 'CV' + str(rangeCV + 1)+':'
            self.lbl30.text = 'CV' + str(rangeCV + 2)+':'
            self.lbl40.text = 'CV' + str(rangeCV + 3)+':'
            self.lbl50.text = 'CV' + str(rangeCV + 4)+':'
            self.lbl60.text = 'CV' + str(rangeCV + 5)+':'
            rangeCV-= 1   
        else:
            pass
        self.VoltageHide()

    def scrollDownCVTrack(self):
		global rangeCVTrack
		if rangeCVTrack <  83:
			self.b5001.text=str(rangeCVTrack+1)
			self.b5005.text=str(rangeCVTrack+5)
			self.b5009.text=str(rangeCVTrack+9)
			self.b5013.text=str(rangeCVTrack+13)
			self.b5002.text=str(rangeCVTrack+2)
			self.b5006.text=str(rangeCVTrack+6)
			self.b5010.text=str(rangeCVTrack+10)
			self.b5014.text=str(rangeCVTrack+14)
			self.b5003.text=str(rangeCVTrack+3)
			self.b5007.text=str(rangeCVTrack+7)
			self.b5011.text=str(rangeCVTrack+11)
			self.b5015.text=str(rangeCVTrack+15)
			self.b5004.text=str(rangeCVTrack+4)
			self.b5008.text=str(rangeCVTrack+8)
			self.b5012.text=str(rangeCVTrack+12)
			self.b5016.text=str(rangeCVTrack+16)
			rangeCVTrack+= 1   
		else:
			pass

    def scrollUpCVTrack(self):
		global rangeCVTrack
		if rangeCVTrack >  0:
			self.b5001.text=str(rangeCVTrack-1)
			self.b5005.text=str(rangeCVTrack+3)
			self.b5009.text=str(rangeCVTrack+7)
			self.b5013.text=str(rangeCVTrack+11)
			self.b5002.text=str(rangeCVTrack)
			self.b5006.text=str(rangeCVTrack+4)
			self.b5010.text=str(rangeCVTrack+8)
			self.b5014.text=str(rangeCVTrack+12)
			self.b5003.text=str(rangeCVTrack+1)
			self.b5007.text=str(rangeCVTrack+5)
			self.b5011.text=str(rangeCVTrack+9)
			self.b5015.text=str(rangeCVTrack+13)
			self.b5004.text=str(rangeCVTrack+2)
			self.b5008.text=str(rangeCVTrack+6)
			self.b5012.text=str(rangeCVTrack+10)
			self.b5016.text=str(rangeCVTrack+14)
			rangeCVTrack-= 1   
		else:
			pass



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


    def on_enter(self):
		self.b003.text=str(BPM)
		Clock.schedule_interval(self.listening, 0.002)
		w1.value=0
		self.b004.text=str(loopsizeS/64)
		self.loopbar()	    	
		if playing==1:
			self.b001.state="down"
			self.b001.text="%s"%(icon('icon-pause', 22))
			Clock.schedule_interval(self.movebar, 0.002)
		else: 
			self.b001.state="normal"
			self.b001.text="%s"%(icon('icon-play', 22))
			self.movebarenter()

    
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
        global playing
        if self.b001.state=="down":
            self.b001.text="%s"%(icon('icon-pause', 22))
            playing=1
            v1.value=1
            Clock.schedule_interval(self.movebar, 0.002)
        else:
            self.b001.text="%s"%(icon('icon-play', 22))
            playing=0
            v1.value=2
            Clock.unschedule(self.movebar)

    def stop(self):
        global playing
        self.b001.state="normal"
        self.b001.text="%s"%(icon('icon-play', 22))
        Clock.unschedule(self.movebar)
        position=0
        self.b015.pos=50,0
        playing=0
        v1.value=0
        

    def moveXrgh(self):
        global rangeXs
        if (rangeXs+16)*4<=1021:
            self.b901.text=str((rangeXs+1)*4+1)
            self.b902.text=str((rangeXs+2)*4+1)
            self.b903.text=str((rangeXs+3)*4+1)
            self.b904.text=str((rangeXs+4)*4+1)
            self.b905.text=str((rangeXs+5)*4+1)
            self.b906.text=str((rangeXs+6)*4+1)
            self.b907.text=str((rangeXs+7)*4+1)
            self.b908.text=str((rangeXs+8)*4+1)
            self.b909.text=str((rangeXs+9)*4+1)
            self.b910.text=str((rangeXs+10)*4+1)
            self.b911.text=str((rangeXs+11)*4+1)
            self.b912.text=str((rangeXs+12)*4+1)
            self.b913.text=str((rangeXs+13)*4+1)
            self.b914.text=str((rangeXs+14)*4+1)
            self.b915.text=str((rangeXs+15)*4+1)
            self.b916.text=str((rangeXs+16)*4+1)
            rangeXs=rangeXs+1
            print(rangeXs)  
        else:
            pass
        self.loadseq()
        
    def moveXlft(self):
        global rangeXs
        if rangeXs>=1:
            self.b901.text=str((rangeXs-1)*4+1)
            self.b902.text=str((rangeXs)*4+1)
            self.b903.text=str((rangeXs+1)*4+1)
            self.b904.text=str((rangeXs+2)*4+1)
            self.b905.text=str((rangeXs+3)*4+1)
            self.b906.text=str((rangeXs+4)*4+1)
            self.b907.text=str((rangeXs+5)*4+1)
            self.b908.text=str((rangeXs+6)*4+1)
            self.b909.text=str((rangeXs+7)*4+1)
            self.b910.text=str((rangeXs+8)*4+1)
            self.b911.text=str((rangeXs+9)*4+1)
            self.b912.text=str((rangeXs+10)*4+1)
            self.b913.text=str((rangeXs+11)*4+1)
            self.b914.text=str((rangeXs+12)*4+1)
            self.b915.text=str((rangeXs+13)*4+1)
            self.b916.text=str((rangeXs+14)*4+1)
            rangeXs=rangeXs-1
        else:
            pass
        self.loadseq()
        
    def moveYup(self):
        global rangeYs
        if rangeYs<=91:
            self.b100.text=str(rangeYs+9)
            self.b200.text=str(rangeYs+8)
            self.b300.text=str(rangeYs+7)
            self.b400.text=str(rangeYs+6)
            self.b500.text=str(rangeYs+5)
            self.b600.text=str(rangeYs+4)
            self.b700.text=str(rangeYs+3)
            self.b800.text=str(rangeYs+2)
            rangeYs=rangeYs+1   
        else:
            pass
        self.loadseq()

    def moveYdw(self):
        global rangeYs
        if rangeYs>=1:
            self.b100.text=str(rangeYs+7)
            self.b200.text=str(rangeYs+6)
            self.b300.text=str(rangeYs+5)
            self.b400.text=str(rangeYs+4)
            self.b500.text=str(rangeYs+3)
            self.b600.text=str(rangeYs+2)
            self.b700.text=str(rangeYs+1)
            self.b800.text=str(rangeYs)
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
        loopbar_pos=v3.value/16
        if loopbar_pos<=(rangeXs+16)*4:
            if 48+(loopbar_pos/4-rangeXs)*47>=5:
                self.b017.pos=48+(loopbar_pos/4-rangeXs)*47,0
            else:
                self.b017.pos=1000,1000
        else:
            self.b017.pos=1000,1000

    def movebarenter(self):
    	countbar=v2.value%loopsizeS
        speed=47.1/64
        position=int(50+round((countbar-rangeX*64)*speed))
        position=(position/12)*12
        if position<50:
            self.b015.pos=1000,0
        else:
            self.b015.pos=position,0


    def movebar(self, *args):
        countbar=v2.value%loopsizeS
        speed=47.1/64
        position=int(50+round((countbar-rangeXs*64)*speed))
        if v2.value%16==0:
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
        global buttonpushedsong
        for key, val in self.ids.items():
            if val==button:
                ID=key
        y=int(ID[1])
        yp=-(y-8)
        x=int(ID[-2:])
        buttonpushedsong=ID
        if button.state=="normal":
            song[x+rangeXs-1].remove(yp+rangeYs+1)
        else:
            song[x+rangeXs-1].append(yp+rangeYs+1)	
            song[x+rangeXs-1]=sorted(song[x+rangeXs-1])
        q3.put(song)
            

    def trackmenu(self,button):
        global trackselected
        for key, val in self.ids.items():
            if val==button:
                ID=key
        trackselected=-(int(ID[1])-9)+rangeYs
        r2.put(trackselected)
        self.b019.pos=300,120
        self.b020.pos=301,121
        self.b021.pos=301,182
        self.b022.pos=301,243
        self.b010.pos=0,0


    def cleartrack(self):
        global song
        for elem in song:
            if trackselected in elem:
                elem.remove(trackselected)
        q3.put(song)
        self.loadseq()


    def on_touch_move(self, touch):
        global buttonpushedsong
        if self.collide_point(*touch.pos):
            x=touch.pos[0]-50
            y=touch.pos[1]
            bx=int(x/47+1)
            by=int(y/47+1)
            byc=8-by
            if (bx>int(buttonpushedsong[-2:]) and by==int(buttonpushedsong[1])):
                if bx<=9:
                    b="b"+str(by)+"0"+str(bx)
                else:
                    b="b"+str(by)+str(bx)
                for val in self.ids.items():
                    if val[0]==b:
                        if val[1].state=='normal':
                            val[1].state='down'
                            song[bx+rangeXs-1].append(byc+rangeYs+1) 
                            song[bx+rangeXs-1]=sorted(song[bx+rangeXs-1])
        q3.put(song)

    def leaving(self):
    	Clock.unschedule(self.listening)


    def mode(self,num):
        global seqbuttonmodesong
        if num==2:
            if seqbuttonmodesong==2:
                seqbuttonmodesong=0
                self.b003.state='normal'
            else:
                seqbuttonmodesong=2
                self.b003.state='down'
                w2.value=0
        if num==3:
            if seqbuttonmodesong==3:
                seqbuttonmodesong=0
                self.b004.state='normal'
            else:
                seqbuttonmodesong=3
                self.b004.state='down'
                w2.value=0
        if num==4:
            seqbuttonmodesong=0
            self.b003.state='normal'
            self.b004.state='normal'
            print("here")
        print(seqbuttonmodesong)

    def listening(self,*args):
		global wheel
		global seqbuttonmodesong
		global loopsizeS
		global BPM
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		if seqbuttonmodesong==0:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					if encoderpushed==1:
						self.moveXrgh()
					else:
						self.moveYup()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					if encoderpushed==1:
						self.moveXlft()
					else:
						self.moveYdw()

		if seqbuttonmodesong==2:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM<200:
						BPM+=1
						self.b003.text=str(BPM)
						v4.value=BPM
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM>30:
						BPM-=1
						self.b003.text=str(BPM)
						v4.value=BPM					
			if encoderpushed==1:
				seqbuttonmodesong=0
				self.b003.state='normal'


		if seqbuttonmodesong==3:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsizeS<1024*64:
						loopsizeS+=64
						v3.value=loopsizeS
						self.b004.text=str(loopsizeS/64)
						self.loopbar()				

			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsizeS>64:
						loopsizeS-=64
						v3.value=loopsizeS	
						self.b004.text=str(loopsizeS/64)
						self.loopbar()						
		
			if encoderpushed==1:
				seqbuttonmodesong=0
				self.b004.state='normal'        


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
        global start
        global rangeY
        global rangeX
        global zoom
        w1.value=0
        Clock.schedule_interval(self.listening, 0.002)
        if start > 0:
            rangeY=36
            rangeX=0
            zoom=4
            self.LoopSdisplay()
            self.b003.text=str(BPM)
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
                self.b001.text="%s"%(icon('icon-pause', 22))
                Clock.schedule_interval(self.movebar, 0.002)
            else: 
                self.b001.state="normal"
                self.b001.text="%s"%(icon('icon-play', 22))
                self.movebarenter()
        else:
            start = start +1

    def leaving(self):
    	Clock.unschedule(self.listening)

    def monitor(self, button):
        global sequencepool2
        global buttonpushed
        global xseq
        global yseq

        for key, val in self.ids.items():
            if val==button:
                ID=key
        yseq=int(ID[1])
        xseq=int(ID[-2:])
        buttonpushed=ID

        if button.state=="normal":
            print("x",(xseq-1)*zoom+rangeX+1)
            print("y",yseq+rangeY-1)
            for elem in sequencepool2[trackselected-1]:
                print("a")
                if elem[0]==(xseq-1)*zoom+rangeX+1 and elem[1]==yseq+rangeY-1 and elem[2]==1:
                    duration=elem[3]
                    break
            sequencepool2[trackselected-1].remove([(xseq-1)*zoom+rangeX+1,yseq+rangeY-1,1,duration])
            sequencepool2[trackselected-1].remove([(xseq-1)*zoom+rangeX+1+duration,yseq+rangeY-1,0,duration])
            self.loadseq()

        if button.background_color==[0.3, 0.7, 1, 1]:
            i=0
            for elem in sequencepool2[trackselected-1]:
                if elem[1]==yseq+rangeY-1 and elem[2]==1:
                    result=i
                if elem[0]>(xseq-1)*zoom+rangeX+1:
                    break
                i+=1
            i=result
            removed=sequencepool2[trackselected-1][i]
            sequencepool2[trackselected-1].remove(removed)
            removed[0]=removed[0]+removed[3]
            removed[2]=0
            sequencepool2[trackselected-1].remove(removed)
            self.loadseq()

        if button.state=="down":           
            sequencepool2[trackselected-1].append([(xseq-1)*zoom+rangeX+1+zoom,yseq+rangeY-1,0,zoom])
            sequencepool2[trackselected-1].append([(xseq-1)*zoom+rangeX+1,yseq+rangeY-1,1,zoom])
            sequencepool2[trackselected-1]=sorted(sequencepool2[trackselected-1], key=operator.itemgetter(0,2))
        q1.put(sequencepool2)
            
    def clearsequence(self):
        global sequencepool2
        sequencepool2[trackselected-1]=[]
        q1.put(sequencepool2)
        print(sequencepool2)

    def clearStep(self,button):
        button.state="normal"
        

    def clear(self):
        for val in self.ids.items():
            if (str(val[0])== str('b001') or val[0]== 'b002' or val[0]== 'b003' or val[0]== 'b004' or val[0]=='b020'):
                pass
            else:
                if int(val[0][1])>0 and int(val[0][1])<9 and int(val[0][-2:])>0:
                    self.clearStep(val[1])
                    val[1].background_color= .68,.68,.84,1
                else:
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
                        btn=(btx-1)*zoom+rangeX
                        self.zoomstep(val[1],timerange[btn])
                    else:
                        rangeX = rangeX-(rangeX%zoom)
                        btn=(btx-1)*zoom+rangeX
                        print("not multiple")
                        self.zoomstep(val[1],timerange[btn])
                else:
                    rangeX=128*7
                    btn=(btx-1)*zoom+rangeX
                    print("resized")
                    self.zoomstep(val[1],timerange[btn])
        self.loadseq()
         
    def zoomout(self):
        global zoom
        global rangeX
        if zoom <8:
            zoom = 2*zoom
            self.zoom()

    def zoomin(self):
        global zoom
        global rangeX
        if zoom >1:
            zoom = zoom/2
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

    def findButtonC(self,button):
        for val in self.ids.items():
            if button==val[0]:
                buttonfound=val[1]
                buttonfound.background_color=[0.3, 0.7, 1, 1]

    def findButtonCi(self,button):
        for val in self.ids.items():
            if button==val[0]:
                buttonfound=val[1]
                buttonfound.state="down"


    def loadseq(self):
        global sequencepool2
        self.clear()
        sequence=sequencepool2[trackselected-1]
        i=1
        while i <= len(sequence):
            if sequence[i-1][2]==1:
                Xc=sequence[i-1][0]-rangeX
                Yc=sequence[i-1][1]-rangeY+1
                j=0
                while j < sequence[i-1][3]:
                    if (Xc>=0 and Xc <= 16*zoom and (sequence[i-1][0]-1)%zoom ==0):
                        if (Yc >= 1 and Yc <=8):
                            Xcp=int(Xc/(zoom+0.0000000000001))+1
                            if Xcp<=9:
                                b="b"+str(Yc)+"0"+str(Xcp)
                            else:
                                b="b"+str(Yc)+str(Xcp)
                            if sequence[i-1][3]>zoom:
                                if j==0:
                                    self.findButtonCi(b)
                                else:
                                    self.findButtonC(b)
                            else:
                                self.findButton(b)
                        else:
                            pass
                    Xc+=zoom
                    j+=zoom
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
            self.b020.pos= 344,900
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
            self.b020.pos= 344,900
            self.b007.state="normal"
            self.b005.state="normal"
            self.b010.pos= 0,0
        else:
            self.b011.pos= 496,900
            self.b012.pos= 496,900
            self.b010.pos= 1000,0

    def tools(self):
        if self.b005.state=="down":
            self.b013.pos= 344,360
            self.b014.pos= 344,301
            self.b016.pos= 344,242
            self.b020.pos= 344,183
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
            self.b020.pos= 344,900
            self.b010.pos= 1000,0


    def mode(self,num):
        global seqbuttonmode
        if num==1:
            if seqbuttonmode==1:
                seqbuttonmode=0
                self.b020.state='normal'
            else:
                seqbuttonmode=1
                self.b020.state='down'
                w2.value=0
        if num==2:
            if seqbuttonmode==2:
                seqbuttonmode=0
                self.b003.state='normal'
            else:
                seqbuttonmode=2
                self.b003.state='down'
                w2.value=0
        if num==3:
            if seqbuttonmode==3:
                seqbuttonmode=0
                self.b004.state='normal'
            else:
                seqbuttonmode=3
                self.b004.state='down'
                w2.value=0
        if num==4:
            seqbuttonmode=0
            self.b003.state='normal'
            self.b004.state='normal'
            self.b020.state='normal'
        print(seqbuttonmode)



    def closemenus(self):
        if self.b007.state=="down":
            self.b007.state="normal"
            self.menu()
        if self.b006.state=="down":
            self.b006.state="normal"
            self.seqmode()
        if self.b005.state=="down":
            self.b005.state="normal"
            self.tools()

    def start(self):
        global playing
        if self.b001.state=="down":
            v1.value=1
            playing=1
            self.b001.text="%s"%(icon('icon-pause', 22))
            Clock.schedule_interval(self.movebar, 0.002)
        else:
            self.b001.text="%s"%(icon('icon-play', 22))
            playing=0
            Clock.unschedule(self.movebar)
            v1.value=2



    def stop(self):
        global playing
        self.b001.state="normal"
        self.b001.text="%s"%(icon('icon-play', 22))
        Clock.unschedule(self.movebar)
        v1.value=0
        playing=0
        self.b015.pos=50,0

    def movebarenter(self):
    	countbar=v2.value%loopsize[trackselected-1]
        speed=47.1/zoom
        position=int(50+round((countbar-rangeX)*speed))
        position=(position/189)*189+50
        if position<50:
            self.b015.pos=1000,0
        else:
            self.b015.pos=position,0


    def movebar(self, *args):
        countbar=v2.value%loopsize[trackselected-1]
        speed=47.1/zoom
        position=int(50+round((countbar-rangeX)*speed))
        if v2.value%16==0: 
	        if position<50:
	            self.b015.pos=1000,0
	        else:
	            self.b015.pos=position,0

   

    def loopbar(self):
        global loopsize
        loopbar_pos=loopsize[trackselected-1]
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
        global buttonpushed
        global sequencepool2
        global erased
        if self.collide_point(*touch.pos):
            x=touch.pos[0]-50
            y=touch.pos[1]
            bx=int(x/47+1)
            by=int(y/47+1)
            if (bx>int(buttonpushed[-2:]) and by==int(buttonpushed[1])):
                if bx<=9:
                    b="b"+str(by)+"0"+str(bx)
                if bx==10:
                    b="b"+str(by)+"10"
                if bx>10:
                    print("here")
                    b="b"+str(by)+str(bx)
                for val in self.ids.items():
                    if val[0]==b:
                        if val[1].state=='normal':
                            val[1].background_color=[0.3, 0.7, 1, 1]
                    if val[0]==buttonpushed and erased==0:
                        val[1].state=='normal'
                        sequencepool2[trackselected-1].remove([(xseq-1)*zoom+rangeX+1+zoom,yseq+rangeY-1,0,zoom])
                        sequencepool2[trackselected-1].remove([(xseq-1)*zoom+rangeX+1,yseq+rangeY-1,1,zoom])
                        erased=1
                            


    def on_touch_up(self,touch):
        global buttonpushed
        global erased
        if self.collide_point(*touch.pos):
            x=touch.pos[0]-50
            y=touch.pos[1]
            bx=int(x/47+1)
            by=int(y/47+1)
            if (bx>int(buttonpushed[-2:]) and by==int(buttonpushed[1])):
                if bx<=9:
                    b="b"+str(by)+"0"+str(bx)
                else:
                    b="b"+str(by)+str(bx)
                for val in self.ids.items():
                    if val[0]==b:
                        erased=0
                        binit=int(buttonpushed[-2:])
                        duration=(bx-binit)+1
                        sequencepool2[trackselected-1].append([(xseq-1)*zoom+rangeX+1,yseq+rangeY-1,1,duration*zoom])
                        sequencepool2[trackselected-1].append([(xseq-1)*zoom+rangeX+1+duration*zoom,yseq+rangeY-1,0,duration*zoom])
                        sequencepool2[trackselected-1]=sorted(sequencepool2[trackselected-1], key=operator.itemgetter(0,2))
                        print(sequencepool2)
                        q1.put(sequencepool2)
                        self.loadseq()



  

    def listening(self,*args):
		global wheel
		global seqbuttonmode
		global loopsize
		global BPM
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		if seqbuttonmode==0:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					if encoderpushed==1:
						self.moveXrgh()
					else:
						self.moveYup()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					if encoderpushed==1:
						self.moveXlft()
					else:
						self.moveYdw()
    	
		if seqbuttonmode==1:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.zoomin()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.zoomout()
			if encoderpushed==1:
				seqbuttonmode=0
				self.b020.state='normal'
				self.closemenus()

		if seqbuttonmode==2:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM<200:
						BPM+=1
						self.b003.text=str(BPM)
						v4.value=BPM
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if BPM>30:
						BPM-=1
						self.b003.text=str(BPM)
						v4.value=BPM					
			if encoderpushed==1:
				seqbuttonmode=0
				self.b003.state='normal'


		if seqbuttonmode==3:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsize[trackselected-1]<64*16:
						loopsize[trackselected-1]+=16
						q2.put(loopsize)					
						self.LoopSdisplay()
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					if loopsize[trackselected-1]>16:
						loopsize[trackselected-1]-=16
						q2.put(loopsize)
						self.LoopSdisplay()				
			if encoderpushed==1:
				seqbuttonmode=0
				self.b004.state='normal'				
			

    def LoopSdisplay(self):
		a,b=divmod(loopsize[trackselected-1],16)
		b=b/4
		self.b004.text=str(a) + "." +str(b)
		self.loopbar()	    	



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

class SaveSeq(Screen):

	def on_enter(self):
		global rangeFile
		rangeFile=0
		self.b5001.text=str(rangeFile*4+1)
		self.b5002.text=str(rangeFile*4+2)
		self.b5003.text=str(rangeFile*4+3)
		self.b5004.text=str(rangeFile*4+4)
		self.b5005.text=str(rangeFile*4+5)
		self.b5006.text=str(rangeFile*4+6)
		self.b5007.text=str(rangeFile*4+7)
		self.b5008.text=str(rangeFile*4+8)
		self.b5009.text=str(rangeFile*4+9)
		self.b5010.text=str(rangeFile*4+10)
		self.b5011.text=str(rangeFile*4+11)
		self.b5012.text=str(rangeFile*4+12)
		self.b5013.text=str(rangeFile*4+13)
		self.b5014.text=str(rangeFile*4+14)
		self.b5015.text=str(rangeFile*4+15)
		self.b5016.text=str(rangeFile*4+16)

	def choice(self, chosen):
		print(chosen)
		if self.b001.state=="down":
			with open('savedseq.json', "w") as s:
				saved["savedseq"][chosen+rangeFile*4]["sequence"] = sequencepool2[trackselected-1]
				json.dump(saved, s)

	def up(self):
		global rangeFile
		if rangeFile<10:
			rangeFile+=1
			self.b5001.text=str(rangeFile*4+1)
			self.b5002.text=str(rangeFile*4+2)
			self.b5003.text=str(rangeFile*4+3)
			self.b5004.text=str(rangeFile*4+4)
			self.b5005.text=str(rangeFile*4+5)
			self.b5006.text=str(rangeFile*4+6)
			self.b5007.text=str(rangeFile*4+7)
			self.b5008.text=str(rangeFile*4+8)
			self.b5009.text=str(rangeFile*4+9)
			self.b5010.text=str(rangeFile*4+10)
			self.b5011.text=str(rangeFile*4+11)
			self.b5012.text=str(rangeFile*4+12)
			self.b5013.text=str(rangeFile*4+13)
			self.b5014.text=str(rangeFile*4+14)
			self.b5015.text=str(rangeFile*4+15)
			self.b5016.text=str(rangeFile*4+16)

	def dw(self):
		global rangeFile
		if rangeFile>0:
			rangeFile-=1
			self.b5001.text=str(rangeFile*4+1)
			self.b5002.text=str(rangeFile*4+2)
			self.b5003.text=str(rangeFile*4+3)
			self.b5004.text=str(rangeFile*4+4)
			self.b5005.text=str(rangeFile*4+5)
			self.b5006.text=str(rangeFile*4+6)
			self.b5007.text=str(rangeFile*4+7)
			self.b5008.text=str(rangeFile*4+8)
			self.b5009.text=str(rangeFile*4+9)
			self.b5010.text=str(rangeFile*4+10)
			self.b5011.text=str(rangeFile*4+11)
			self.b5012.text=str(rangeFile*4+12)
			self.b5013.text=str(rangeFile*4+13)
			self.b5014.text=str(rangeFile*4+14)
			self.b5015.text=str(rangeFile*4+15)
			self.b5016.text=str(rangeFile*4+16)
			


class LoadSeq(Screen):

	def on_enter(self):
		global rangeFile
		rangeFile=0
		self.b5001.text=str(rangeFile*4+1)
		self.b5002.text=str(rangeFile*4+2)
		self.b5003.text=str(rangeFile*4+3)
		self.b5004.text=str(rangeFile*4+4)
		self.b5005.text=str(rangeFile*4+5)
		self.b5006.text=str(rangeFile*4+6)
		self.b5007.text=str(rangeFile*4+7)
		self.b5008.text=str(rangeFile*4+8)
		self.b5009.text=str(rangeFile*4+9)
		self.b5010.text=str(rangeFile*4+10)
		self.b5011.text=str(rangeFile*4+11)
		self.b5012.text=str(rangeFile*4+12)
		self.b5013.text=str(rangeFile*4+13)
		self.b5014.text=str(rangeFile*4+14)
		self.b5015.text=str(rangeFile*4+15)
		self.b5016.text=str(rangeFile*4+16)

	def choice(self, chosen):
		print(chosen)
		if self.b001.state=="down":
			with open('savedseq.json') as s:
				saved = json.load(s)
				print(saved["savedseq"][chosen]["sequence"])
				sequencepool2[trackselected-1]=saved["savedseq"][chosen+rangeFile*4]["sequence"]
				q1.put(sequencepool2)
		else:
			from midiconvert import MIDIconvert
			#sequencepool2[trackselected-1]=MIDIconvert('test4.mid')


	def up(self):
		global rangeFile
		if rangeFile<10:
			rangeFile+=1
			self.b5001.text=str(rangeFile*4+1)
			self.b5002.text=str(rangeFile*4+2)
			self.b5003.text=str(rangeFile*4+3)
			self.b5004.text=str(rangeFile*4+4)
			self.b5005.text=str(rangeFile*4+5)
			self.b5006.text=str(rangeFile*4+6)
			self.b5007.text=str(rangeFile*4+7)
			self.b5008.text=str(rangeFile*4+8)
			self.b5009.text=str(rangeFile*4+9)
			self.b5010.text=str(rangeFile*4+10)
			self.b5011.text=str(rangeFile*4+11)
			self.b5012.text=str(rangeFile*4+12)
			self.b5013.text=str(rangeFile*4+13)
			self.b5014.text=str(rangeFile*4+14)
			self.b5015.text=str(rangeFile*4+15)
			self.b5016.text=str(rangeFile*4+16)

	def dw(self):
		global rangeFile
		if rangeFile>0:
			rangeFile-=1
			self.b5001.text=str(rangeFile*4+1)
			self.b5002.text=str(rangeFile*4+2)
			self.b5003.text=str(rangeFile*4+3)
			self.b5004.text=str(rangeFile*4+4)
			self.b5005.text=str(rangeFile*4+5)
			self.b5006.text=str(rangeFile*4+6)
			self.b5007.text=str(rangeFile*4+7)
			self.b5008.text=str(rangeFile*4+8)
			self.b5009.text=str(rangeFile*4+9)
			self.b5010.text=str(rangeFile*4+10)
			self.b5011.text=str(rangeFile*4+11)
			self.b5012.text=str(rangeFile*4+12)
			self.b5013.text=str(rangeFile*4+13)
			self.b5014.text=str(rangeFile*4+14)
			self.b5015.text=str(rangeFile*4+15)
			self.b5016.text=str(rangeFile*4+16)		



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


    def Timer(self,v1,v2,v3,v4,q1,q2,q3,q4,q5,q6):
        nextcall=time.time()
        count=0
        loopstate=loopstate0

        while 1:
            BPM=v4.value
            interval=float(60/Decimal(BPM)/Decimal(16))        	
            v2.value=count
            while q1.empty() is False:
                    sequencepool2=q1.get()
                    print('sequencepool2', sequencepool2)
            while q2.empty() is False:
                    loopsize=q2.get()
                    print('loopsize', loopsize)
            while q3.empty() is False:
                    song=q3.get()
                    print('song', song)
            while q4.empty() is False:
                    Sendinfo=q4.get()
                    print('sendinfo', Sendinfo)
            while q5.empty() is False:
                    #port=q5.get()
                    #print('Port', port)
                    pass
            while q6.empty() is False:
                    #sequencepool2=q1.get()
                    #print('qvalue', q6.get()) 
                    pass


            if rpi==1:
                available_ports = midiout.get_ports()
                port = available_ports[0]            
                if len(available_ports)>1:
                  port = available_ports[1]
                port = mido.open_output(port)
            else:
                port=0

            if v1.value==1:
                count+=1
                if count > v3.value:
                    count=1
                    loopstate=loopstate0
                nextcall = nextcall+interval
                self.send(count,loopstate,sequencepool2,loopsize,song,Sendinfo,port)
                print(nextcall-time.time())
                if nextcall-time.time()>0:
                    time.sleep(nextcall-time.time())
                else:
                    nextcall=time.time()
            elif v1.value==2:
                pass
            else:
                loopstate=loopstate0
                count=0
            time.sleep(0.0005)


    def send(self,count,loopstate,sequencepool2,loopsize,song,Sendinfo,port):
        currentstep=count/(16*4)
        i=0
        print('Count', count)
        while i<len(song[currentstep]):
            n=song[currentstep][i]-1 #n is current track
            if count%loopsize[n]==0:
                loopstate[n]=0
            if loopstate[n] <= len(sequencepool2[n])-1:
                while sequencepool2[n][loopstate[n]][0]==count%loopsize[n]:
                    if Sendinfo[n][3] > 0:
                        self.CVsendGate(n,sequencepool2,loopstate,Sendinfo)
                    if Sendinfo[n][1] > 0:
                        self.CVsendPitch(n,sequencepool2,loopstate,Sendinfo)
                    if Sendinfo[n][0] > 0:
                        channel=Sendinfo[n][0]-1
                        self.MIDIsend(n,channel,sequencepool2,loopstate,Sendinfo,port)
                        self.USBsend(n,channel,sequencepool2,loopstate,port)
                    if loopstate[n]==len(sequencepool2[n])-1:
                        loopstate[n]=0
                        break
                    else:
                        loopstate[n]+=1 
            else:
                pass
                print("pass")
            i+=1


    def CVsendGate(self,n,sequencepool2,loopstate,Sendinfo):
            if sequencepool2[n][loopstate[n]][2]==1:
                print('CV Gate On',Sendinfo[n][3], Sendinfo[n][4], 'Value: 8V')
                if rpi==1:
                    bus.write_i2c_block_data(Sendinfo[n][3], Sendinfo[n][4], [0x09, 0xFF])
            else:
                print('CV Gate Off',Sendinfo[n][3], Sendinfo[n][4], 'Value: 0V')
                if rpi==1:
                    bus.write_i2c_block_data(Sendinfo[n][3], Sendinfo[n][4], [0x05, 0x0])

    def CVsendPitch(self,n,sequencepool2,loopstate,Sendinfo):
            if sequencepool2[n][loopstate[n]][2]==1:
                a,b=divmod(4096*sequencepool2[n][loopstate[n]][1]/15/12+4096/15*Sendinfo[n][5],256)
                print('CV Pitch On',Sendinfo[n][1],Sendinfo[n][2], 'Value',sequencepool2[n][loopstate[n]][1], 'Offset' , Sendinfo[n][5])
                if rpi==1:
                    bus.write_i2c_block_data(Sendinfo[n][1], Sendinfo[n][2], [a, b])

            
    def MIDIsend(self,n,channel,sequencepool2,loopstate,Sendinfo,port):
        if sequencepool2[n][loopstate[n]][2]==1:
            print "send" , sequencepool2[n][loopstate[n]][1] ,"channel" , Sendinfo[n][0]
            byte1=bin(int(128+16+Sendinfo[n][0]-1))
            byte3=bin(100)
        else:
            print "stop" , sequencepool2[n][loopstate[n]][1] ,"channel" , Sendinfo[n][0]
            byte1=bin(int(128+Sendinfo[n][0]-1))
            byte3=bin(0)
        byte2 = bin(int(24+sequencepool2[n][loopstate[n]][1]))
        byte_chr1 = chr(int(byte1,2))
        byte_chr3 = chr(int(byte3,2))         
        byte_chr2 = chr(int(byte2,2))            
        ser.write(byte_chr1)
        ser.write(byte_chr2)
        ser.write(byte_chr3)  

    def USBsend(self,n,channel,sequencepool2,loopstate,port):
        #print(port)
        if sequencepool2[n][loopstate[n]][2]==1:
            msg=mido.Message('note_on', note=sequencepool2[n][loopstate[n]][1]+24, channel=channel)
        else:
            msg=mido.Message('note_off', note=sequencepool2[n][loopstate[n]][1]+24, channel=channel)
        try:
            port.send(msg)  
        except:
            print('Port error')          

          
            
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


class Listen():


	def starting(self,w1,w2,r1,r2):
		global clkLastState
		global swLastState
		

		if rpi==1:
			clkLastState = GPIO.input(clk)
			swLastState = GPIO.input(sw)
			midi_in = rtmidi.MidiIn()

		while 1:

			if rpi==1:
				if len(available_ports)>1:
					midi_in.open_port(1)
				else:
					midi_in.open_port(0)
			while r1.empty() is False:
				Sendinfo=r1.get()
				print('Sendinfo', Sendinfo)
			while r2.empty() is False:
				trackselected=r2.get()
				print('trackselected', trackselected)
			self.encoder()
			self.MIDIdinIn(Sendinfo,trackselected)
			self.MIDIusbIn(Sendinfo,trackselected)
			time.sleep(0.001)


	def encoder(self):
		#print('listening')
		global clkLastState
		global swLastState		
		if rpi==1:
			clkState = GPIO.input(clk)
			dtState = GPIO.input(dt)
			if clkState != clkLastState:
				if dtState != clkState:
					w1.value+=1
				else:
					w1.value+=-1
			clkLastState = clkState
			
			swstate =GPIO.input(sw)
			if swstate != swLastState:			
				if swstate==0:
					if w2.value==1:
						w2.value=0
					else:
						w2.value=1
			swLastState=swstate
		else:
			pass

	def MIDIdinIn(self,Sendinfo,trackselected):
		if rpi==1:
			pass
		else:
			pass

	def MIDIusbIn(self,Sendinfo,trackselected):
		if rpi==1:
			message= midi_in.get_message()
			if message:
				print message[0]
				self.ThroughDin(message[0],Sendinfo,trackselected)
				self.ThroughCV(message[0],Sendinfo,trackselected)


	def ThroughUSB(self,Message,Sendinfo,trackselected):
		pass

	def ThroughDin(self,Message,Sendinfo,trackselected):
		if Message[0]==90:
			print "send" , Message 
			byte1=bin(int(128+16+Sendinfo[trackselected][0]-1))
			byte3=bin(100)
		if Message[0]==80:
			print "stop" , Message
			byte1=bin(int(128+Sendinfo[n][trackselected]-1))
			byte3=bin(0)
		byte2 = bin(int(Message[1]))
		byte_chr1 = chr(int(byte1,2))
		byte_chr3 = chr(int(byte3,2))         
		byte_chr2 = chr(int(byte2,2))            
		ser.write(byte_chr1)
		ser.write(byte_chr2)
		ser.write(byte_chr3) 

	def ThroughCV(self,Message,Sendinfo,trackselected):
		if Sendinfo[3]>0:
			if Message[0]==0x90:
				if rpi==1:
					bus.write_i2c_block_data(Sendinfo[trackselected][3], Sendinfo[trackselected][4], [0x09, 0xFF])
			if Message[0]==0x80:
				if rpi==1:
					bus.write_i2c_block_data(Sendinfo[trackselected][3], Sendinfo[trackselected][4], [0x05, 0x0])
		if Sendinfo[1]>0:
			if Message[0]==0x90 and (Message[1]-24)>0 and (Message[1]-24)<96 :
				a,b=divmod(4096*(Message[1]-24)/15/12+4096/15*Sendinfo[trackselected][5],256)
				if rpi==1:
					bus.write_i2c_block_data(Sendinfo[trackselected][1], Sendinfo[trackselected][2], [a, b])


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

    pass

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


keyrange=[['C0',1],['C#0',0],['D0',1],['D#0',0],['E0',1],['F0',1],['F#0',0],['G0',1],['G#0',0],['A0',1],['A#0',0],['B0',1],
        ['C1',1],['C#1',0],['D1',1],['D#1',0],['E1',1],['F1',1],['F#1',0],['G1',1],['G#1',0],['A1',1],['A#1',0],['B1',1],
        ['C2',1],['C#2',0],['D2',1],['D#2',0],['E2',1],['F2',1],['F#2',0],['G2',1],['G#2',0],['A2',1],['A#2',0],['B2',1],
        ['C3',1],['C#3',0],['D3',1],['D#3',0],['E3',1],['F3',1],['F#3',0],['G3',1],['G#3',0],['A3',1],['A#3',0],['B3',1],
        ['C4',1],['C#4',0],['D4',1],['D#4',0],['E4',1],['F4',1],['F#4',0],['G4',1],['G#4',0],['A4',1],['A#4',0],['B4',1],
        ['C5',1],['C#5',0],['D5',1],['D#5',0],['E5',1],['F5',1],['F#5',0],['G5',1],['G#5',0],['A5',1],['A#5',0],['B5',1],
        ['C6',1],['C#6',0],['D6',1],['D#6',0],['E6',1],['F6',1],['F#6',0],['G6',1],['G#6',0],['A6',1],['A#6',0],['B6',1],
        ['C7',1],['C#7',0],['D7',1],['D#7',0],['E7',1],['F7',1],['F#7',0],['G7',1],['G#7',0],['A7',1],['A#7',0],['B7',1]]


timerange=["1","","","",".","","","",".","","","",".","","","","2","","","",".","","","",".","","","",".","","","","3","","","",".","","","",".","","","",".","","","","4","","","",".","","","",".","","","",".","","","",
"5","","","",".","","","",".","","","",".","","","","6","","","",".","","","",".","","","",".","","","","7","","","",".","","","",".","","","",".","","","","8","","","",".","","","",".","","","",".","","","",
"9","","","",".","","","",".","","","",".","","","","10","","","",".","","","",".","","","",".","","","","11","","","",".","","","",".","","","",".","","","","12","","","",".","","","",".","","","",".","","","",
"13","","","",".","","","",".","","","",".","","","","14","","","",".","","","",".","","","",".","","","","15","","","",".","","","",".","","","",".","","","","16","","","",".","","","",".","","","",".","","","",
"17","","","",".","","","",".","","","",".","","","","18","","","",".","","","",".","","","",".","","","","19","","","",".","","","",".","","","",".","","","","20","","","",".","","","",".","","","",".","","","",
"21","","","",".","","","",".","","","",".","","","","22","","","",".","","","",".","","","",".","","","","23","","","",".","","","",".","","","",".","","","","24","","","",".","","","",".","","","",".","","","",
"25","","","",".","","","",".","","","",".","","","","26","","","",".","","","",".","","","",".","","","","27","","","",".","","","",".","","","",".","","","","28","","","",".","","","",".","","","",".","","","",
"29","","","",".","","","",".","","","",".","","","","30","","","",".","","","",".","","","",".","","","","31","","","",".","","","",".","","","",".","","","","32","","","",".","","","",".","","","",".","","","",
"33","","","",".","","","",".","","","",".","","","","34","","","",".","","","",".","","","",".","","","","35","","","",".","","","",".","","","",".","","","","36","","","",".","","","",".","","","",".","","","",
"37","","","",".","","","",".","","","",".","","","","38","","","",".","","","",".","","","",".","","","","39","","","",".","","","",".","","","",".","","","","40","","","",".","","","",".","","","",".","","","",
"41","","","",".","","","",".","","","",".","","","","42","","","",".","","","",".","","","",".","","","","43","","","",".","","","",".","","","",".","","","","44","","","",".","","","",".","","","",".","","","",
"45","","","",".","","","",".","","","",".","","","","46","","","",".","","","",".","","","",".","","","","47","","","",".","","","",".","","","",".","","","","48","","","",".","","","",".","","","",".","","","",
"49","","","",".","","","",".","","","",".","","","","50","","","",".","","","",".","","","",".","","","","51","","","",".","","","",".","","","",".","","","","52","","","",".","","","",".","","","",".","","","",
"53","","","",".","","","",".","","","",".","","","","54","","","",".","","","",".","","","",".","","","","55","","","",".","","","",".","","","",".","","","","56","","","",".","","","",".","","","",".","","","",
"57","","","",".","","","",".","","","",".","","","","58","","","",".","","","",".","","","",".","","","","59","","","",".","","","",".","","","",".","","","","60","","","",".","","","",".","","","",".","","","",
"61","","","",".","","","",".","","","",".","","","","62","","","",".","","","",".","","","",".","","","","63","","","",".","","","",".","","","",".","","","","64","","","",".","","","",".","","","",".","","","",
"65","","","",".","","","",".","","","",".","","","","66","","","",".","","","",".","","","",".","","","","67","","","",".","","","",".","","","",".","","","","68","","","",".","","","",".","","","",".","","","",
"69","","","",".","","","",".","","","",".","","","","70","","","",".","","","",".","","","",".","","","","71","","","",".","","","",".","","","",".","","","","72","","","",".","","","",".","","","",".","","","",
"73","","","",".","","","",".","","","",".","","","","74","","","",".","","","",".","","","",".","","","","75","","","",".","","","",".","","","",".","","","","76","","","",".","","","",".","","","",".","","",""]

# [step number, note number, on, note length][step number + note length, note number, off, nnote length]
sequencepool2=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

# [Midi channel, Pitch Dac N, Pitch Ch N, Gate Dac N, Gate Ch N, Pitch offeset] 
Sendinfo=numpy.full((100,6),0)
Sendinfo=Sendinfo.tolist()

# Indexed chronologialy ; [Track a,Track b, ...]
song=[[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

# [DAC Adress, Channel Adress]
CVinfo=[[0x60,0x50],[0x60,0x52],[0x60,0x54],[0x60,0x56],[0x61,0x50],[0x61,0x52],[0x61,0x54],[0x61,0x56],[0x62,0x50],[0x62,0x52],[0x62,0x54],[0x62,0x56]]
zoom=4
rangeX=0
rangeXs=0
rangeXmax=64*16-1
rangeFile=0
rangeYs=0
rangeY=36 #C0=0, 8 octaves
rangeMidi=0
rangeCV=0
rangeCVTrack=0
start=0
trackselected=1
wheel=0
loopsizeS=64*16
erased=0
trackselectedparam=1
BPM=120
interval=float(60/Decimal(BPM)/Decimal(16))
count=0
seqbuttonmode=0
seqbuttonmodesong=0

# [[a],[b],...] where a,b.. are the loop from track i iteration number
loopstate0=numpy.full(100,0)
loopstate0=loopstate0.tolist()
loopstate=loopstate0

# size of the loops of each tracks
loopsize=numpy.full(100,64)
loopsize=loopsize.tolist()
playing=0

buttonpushed="b000"
buttonpushedsong="b000"
with open('param.json') as f:
    paramcf1 = json.load(f)
with open('savedseq.json') as s:
    saved = json.load(s)

paramcalc=ParamScreen()
Sendinfo=paramcalc.convert()

midiout = rtmidi.MidiOut()

def outsmp(v1,v2,v3,v4,q1,q2,q3,q4,q5,q6):
    ti=Timing()
    ti.Timer(v1,v2,v3,v4,q1,q2,q3,q4,q5,q6)

#v1: playing ; v2: count ; v3: song size ; v4: BPM
#q1:sequencepool ; q2: loopsize ; q3: song ; q4: Sendinfo

v1=multiprocessing.Value('i',1)
v1.value=0
v2=multiprocessing.Value('i',1)
v3=multiprocessing.Value('i',1)
v3.value=16*4*16
v4=multiprocessing.Value('i',1)
v4.value=BPM

q1=multiprocessing.Queue()
q1.put(sequencepool2)
q2=multiprocessing.Queue()
q2.put(loopsize)
q3=multiprocessing.Queue()
q3.put(song)
q4=multiprocessing.Queue()
q4.put(Sendinfo)
q5=multiprocessing.Queue()
#q5.put(port)
q6=multiprocessing.Queue()


def insmp(w1,w2,r1,r2):
	listen=Listen()
	listen.starting(w1,w2,r1,r2)

w1=multiprocessing.Value('i',1)
w1.value=0
w2=multiprocessing.Value('i',1)
w2.value=0
r1=multiprocessing.Queue()
r1.put(Sendinfo)
r2=multiprocessing.Queue()
r2.put(trackselected)

p=multiprocessing.Process(target=outsmp,args=(v1,v2,v3,v4,q1,q2,q3,q4,q5,q6))
p.start()
q=multiprocessing.Process(target=insmp,args=(w1,w2,r1,r2))
q.start()


try: 
	seq=SequencerApp()
	seq.run()
finally:
	if rpi==1:
		GPIO.cleanup()
	print("cleaned")