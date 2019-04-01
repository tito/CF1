import os
os.environ['KIVY_GL_BACKEND']='gl'

# CFM1 APP version 1.0

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
import mido
import serial
import rtmidi
import numpy
from iconfonts import *
from os.path import join, dirname


register('default_font', 'Icons.ttf',
			 join(dirname(__file__), 'Icons.fontd'))
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

rpi = 0
if platform.system()=='Linux':
	try:
		from RPi import GPIO
		rpi = 1
	except:
		pass

print(("rpi detected:",rpi))
if rpi==1:
	import smbus
	from RPi import GPIO
	ser=serial.Serial('/dev/ttyAMA0', 38400)
	bus = smbus.SMBus(1)
	clk = 21
	dt = 20
	sw = 16
	pwm = 13
	jackstart = 12
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(pwm,GPIO.OUT)
	GPIO.setup(jackstart,GPIO.OUT)
	pwmsync = GPIO.PWM(13,4)



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
		global playing
		v1.value=0
		playing=0
		rangeCVTrack=0
		rangeMidi=0
		rangeCV=0
		self.midiupdate()
		self.CVupdate()
		self.convert()
		self.syncupdate()
		self.versionupdate()
		self.b1000005.pos=320,1170
		Clock.schedule_interval(self.listening, 0.002)
		w1.value=0		

	def versionupdate(self):
		self.b1000004.text='CFM1 Version '+str(version)

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


	def syncupdate(self):
		print("here sync")
		if paramcf1["sync"][0]["midi-din"]=="on":
			print('here')
			self.b100001.text="On"
		else:
			self.b100001.text="Off"
		if paramcf1["sync"][1]["midi-usb"]=="on":
			print('here')
			self.b100002.text="On"
		else:
			self.b100002.text="Off"
		self.b100003.text=paramcf1["sync"][2]["ppq"]
		if paramcf1["sync"][3]["BPMmult"]=="1":
			print('here')
			self.b100004.text="24"
		else:
			self.b100004.text="48"
		if paramcf1["sync"][4]["USBstate"]=="in":
			print('here')
			self.b100005.text="In"
		else:
			self.b100005.text="Out"		




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
		self.b4001.text="DIN"
		self.b4002.text="USB"
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

	def PPQselect(self):
		self.b5017.pos=310,305
		self.b5017.text="PPQ:"
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
		self.b5001.text="/48"
		self.b5005.text="/4"
		self.b5009.text="4"
		self.b5013.text="32"
		self.b5002.text="/24"
		self.b5006.text="/2"
		self.b5010.text="8"
		self.b5014.text="48"
		self.b5003.text="/16"
		self.b5007.text="1"
		self.b5011.text="16"
		self.b5015.text="64"
		self.b5004.text="/8"
		self.b5008.text="2"
		self.b5012.text="24"
		self.b5016.text="96"



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
		for key, val in list(self.ids.items()):
			if val==button:
				ID=key
		trackselectedparam=int(ID[-3:])+rangeMidi
		print(trackselectedparam)


	def CVselected(self,button):
		global CVselectedparam
		for key, val in list(self.ids.items()):
			if val==button:
				ID=key
		CVselectedparam=int(ID[-2:])+rangeCV
		print(CVselectedparam)

	def port1(self,button):
		global Sendinfo
		for key, val in list(self.ids.items()):
			if val==button:
				ID=key
		new=(ID[-1:])

		if self.b4003.text=="MIDI PORT:":
			if int(new)==1:
				paramcf1["midi-map"][trackselectedparam-1]["port"] = "USB"
			if int(new)==2:
				paramcf1["midi-map"][trackselectedparam-1]["port"] = "DIN"
			if rpi==1:
				with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile:
					json.dump(paramcf1, jsonFile)
			else:
				with open("param.json", "w") as jsonFile:
					json.dump(paramcf1, jsonFile)				
			self.midiupdate()
			self.convert()


		if self.b4003.text=="VOLTAGE:":
			if int(new)==1:
				paramcf1["CV-map"][CVselectedparam-1]["Voltage"] = "[ 0V ; 10V ]"
				#CVassign[CVselectedparam-1][2]=5
			if int(new)==2:
				paramcf1["CV-map"][CVselectedparam-1]["Voltage"] = "[ -5V ; 5V ]"
				#CVassign[CVselectedparam-1][2]=0
			if rpi==1:
				with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile:
					json.dump(paramcf1, jsonFile)
			else:
				with open("param.json", "w") as jsonFile:
					json.dump(paramcf1, jsonFile)				
			self.CVupdate()
			self.convert()
			#Sendinfo[CVassign[trackselectedparam-1][1]-1][5]=CVassign[CVselectedparam-1][2]



		if self.b4003.text=="CV TYPE:":
			if int(new)==1:
				paramcf1["CV-map"][CVselectedparam-1]["Type"] = "PITCH"
				paramcf1["CV-map"][CVselectedparam-1]["Voltage"] = "[ -5V ; 5V ]"
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
				paramcf1["CV-map"][CVselectedparam-1]["Voltage"] = "[ -5V ; 5V ]"
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
			if rpi==1:
				with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile:
					json.dump(paramcf1, jsonFile)
			else:
				with open("param.json", "w") as jsonFile:
					json.dump(paramcf1, jsonFile)				
			self.CVupdate()
			self.convert()
			print(Sendinfo)


	def port2(self,button):
		global Sendinfo
		for key, val in list(self.ids.items()):
			if val==button:
				ID=key
		new=int((ID[-2:]))

		if self.b5017.text=="TRACK:":
			new=int(new)+rangeCVTrack
			paramcf1["CV-map"][CVselectedparam-1]["Track"] = str(new)
			paramcf1["CV-map"][CVselectedparam-1]["Voltage"] = "[ -5V ; 5V ]"
			i=0
			while i<12:
				if paramcf1["CV-map"][i]["Track"]== str(new) and i!=CVselectedparam-1 and paramcf1["CV-map"][i]["Type"]==paramcf1["CV-map"][CVselectedparam-1]["Type"]:
					paramcf1["CV-map"][i]["Track"] = "NONE"
					break
				i+=1
			if rpi==1:
				with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile:
					json.dump(paramcf1, jsonFile)
			else:
				with open("param.json", "w") as jsonFile:
					json.dump(paramcf1, jsonFile)				
			self.CVupdate()
			self.convert()


		if self.b5017.text=="MIDI CHANNEL:":
			paramcf1["midi-map"][trackselectedparam-1]["channel"] = str(new)
			if rpi==1:
				with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile:
					json.dump(paramcf1, jsonFile)
			else:
				with open("param.json", "w") as jsonFile:
					json.dump(paramcf1, jsonFile)
			self.midiupdate()
			self.convert()
			print(Sendinfo)

		if self.b5017.text=="PPQ:":
			table=["/48","/24","/16","/8","/4","/2","1","2","4","8","16","24","32","48","64","96"]
			print((str(table[new-1])))
			paramcf1["sync"][2]["ppq"] = str(table[new-1])
			if rpi==1:
				with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile:
					json.dump(paramcf1, jsonFile)
			else:
				with open("param.json", "w") as jsonFile:
					json.dump(paramcf1, jsonFile)				
			self.syncupdate()
			self.convertsync()

	def convert(self):
		i=0
		j=0
		k=0
		while j<len(Sendinfo):
			Sendinfo[j]=[0,0,0,0,0,0,0]
			j+=1
		while i<12:

			if paramcf1["CV-map"][i]["Type"]=="PITCH" and paramcf1["CV-map"][i]["Track"]!="NONE":
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][1]=CVinfo[i][0]
				Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][2]=CVinfo[i][1]
				if paramcf1["CV-map"][i]["Voltage"]=="[ 0V ; 10V ]":
					Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][5]=5
				else:
					pass
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
			#print("here voltage")
			#if paramcf1["CV-map"][i]["Voltage"]=="[ 0V ; 10V ]" and paramcf1["CV-map"][i]["Track"]!="NONE":
			#	print("here voltage 5")
			#	Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][5]=5
			#elif paramcf1["CV-map"][i]["Track"]=="NONE":
			#	print("here voltage NONE")
			#	pass
			#else:
			#print("voltage 0")
			#Sendinfo[int(paramcf1["CV-map"][i]["Track"])-1][5]=0
			i+=1

		while k<len(Sendinfo):
			Sendinfo[k][0]=int(paramcf1["midi-map"][k]["channel"])
			if paramcf1["midi-map"][k]["port"]=="USB":
				Sendinfo[k][6]=1
			if paramcf1["midi-map"][k]["port"]=="DIN":
				Sendinfo[k][6]=2
			k+=1
		if start==1:
			q4.put(Sendinfo)
			r1.put(Sendinfo)
			s1.put(Sendinfo)			
		return Sendinfo

	def convertsync(self):
		table=["/48","/24","/16","/8","/4","/2","1","2","4","8","16","24","32","48","64","96"]
		#pulse per quarter note => x4 = pulses per note => xBPM= pulses per minutes
		#tableinv=[1/720,1/360,1/240,1/120,1/60,2/60,4/60,8/60,16/60,32/60,64/60,96/60,128/60,192/60,256/60,384/60]
		tableinv=[0.00138888,0.00277777,0.00416666,0.00833333,0.01666666,0.03333333,0.06666666,0.13333333,0.26666666,0.53333333,1.06666666,1.6,2.13333333,3.2,4.26666666,6.4]
		if paramcf1['sync'][0]["midi-din"]=="on":
			Syncinfo[0]=1
		else:
			Syncinfo[0]=0
		if paramcf1['sync'][1]["midi-usb"]=="on":
			Syncinfo[1]=1
		else:
			Syncinfo[1]=0
		for i,elem in enumerate(table):
			if paramcf1['sync'][2]["ppq"]==str(elem):
				Syncinfo[2]=tableinv[i]
		if paramcf1['sync'][3]["BPMmult"]=="1":
			Syncinfo[3]=1
		else:
			Syncinfo[3]=2
		if paramcf1['sync'][4]["USBstate"]=="in":
			Syncinfo[4]=1
		else:
			Syncinfo[4]=0			
		#print(Syncinfo)
		if start==1:
			q5.put(Syncinfo)
			r3.put(Syncinfo)
			s3.put(Syncinfo)					
		return Syncinfo

	def MIDIsync(self):
		if rpi==1:
			with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile:
				if self.b100001.text=='Off':
					print ("on")
					self.b100001.text='On'
					paramcf1["sync"][0]["midi-din"] = "on"
				else:
					print("off")
					self.b100001.text='Off'
					paramcf1["sync"][0]["midi-din"] = "off"
				json.dump(paramcf1, jsonFile)
		else:
			with open("param.json", "w") as jsonFile:
				if self.b100001.text=='Off':
					print ("on")
					self.b100001.text='On'
					paramcf1["sync"][0]["midi-din"] = "on"
				else:
					print("off")
					self.b100001.text='Off'
					paramcf1["sync"][0]["midi-din"] = "off"
				json.dump(paramcf1, jsonFile)			
		self.convertsync()

	def USBsync(self):
		if rpi==1:
			with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile:
				if self.b100002.text=='Off':
					self.b100002.text='On'
					print ("on")
					paramcf1["sync"][1]["midi-usb"] = "on"
				else:
					print("off")
					self.b100002.text='Off'
					paramcf1["sync"][1]["midi-usb"] = "off"
				json.dump(paramcf1, jsonFile)
		else:
			with open("param.json", "w") as jsonFile:
				if self.b100002.text=='Off':
					self.b100002.text='On'
					print ("on")
					paramcf1["sync"][1]["midi-usb"] = "on"
				else:
					print("off")
					self.b100002.text='Off'
					paramcf1["sync"][1]["midi-usb"] = "off"
				json.dump(paramcf1, jsonFile)			
		self.convertsync()

	def BPMmult(self):
		if rpi==1:
			with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile:
				if self.b100004.text=='24':
					self.b100004.text='48'
					print ("x2")
					paramcf1["sync"][3]["BPMmult"] = "2"
				else:
					print("x1")
					self.b100004.text='24'
					paramcf1["sync"][3]["BPMmult"] = "1"
				json.dump(paramcf1, jsonFile)
		else:
			with open("param.json", "w") as jsonFile:
				if self.b100004.text=='24':
					self.b100004.text='48'
					print ("x2")
					paramcf1["sync"][3]["BPMmult"] = "2"
				else:
					print("x1")
					self.b100004.text='24'
					paramcf1["sync"][3]["BPMmult"] = "1"
				json.dump(paramcf1, jsonFile)			
		self.convertsync()

	def USBstate(self):
		if rpi==1:
			with open("/home/pi/Desktop2/UIP/param.json", "w") as jsonFile:
				if self.b100005.text=='In':
					self.b100005.text='Out'
					print ("out")
					paramcf1["sync"][4]["USBstate"] = "out"
				else:
					print("in")
					self.b100005.text='In'
					paramcf1["sync"][4]["USBstate"] = "in"
				json.dump(paramcf1, jsonFile)
		else:
			with open("param.json", "w") as jsonFile:
				if self.b100005.text=='In':
					self.b100005.text='Out'
					print ("out")
					paramcf1["sync"][4]["USBstate"] = "out"
				else:
					print("in")
					self.b100005.text='In'
					paramcf1["sync"][4]["USBstate"] = "in"
				json.dump(paramcf1, jsonFile)			
		self.convertsync()				

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
		for val in list(self.ids.items()):
			if (str(val[0])== str('b001') or val[0]== 'b002' or val[0]== 'b003' or val[0]== 'b004'):
				pass
			else:
				self.clearStep(val[1])

	def scrollDownMIDI(self):
		global rangeMidi
		if rangeMidi <  10:
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

	def kill(self):
		print("poweroff")
		if rpi==1:
			os.system("sudo poweroff")


	def update(self):
		print("updating.........")
		if rpi==1:
			for files in os.walk('/media/pi'):
				resulted=files
				break
			resulted=str(resulted[1])
			resulted=resulted[:-2]
			location=str(resulted[2:])
			print(location)
			if len(location)<1:
				print('no usb stick detected')
				self.b1000005.pos=320,170
				self.b1000005.text='No USB stick detected'
			else:
				for root, dirs, files in os.walk("/media/pi/"+location):
					if "CFM1update1.1.zip" in files:
						print("Updating.. Do not power off")
						self.b1000005.pos=320,170
						self.b1000005.text="Updating.. Do not power off"
						try:
							os.system("cp /media/pi/"+location+"/CFM1update1.1.zip ~/Desktop2")
							os.system("unzip ~/Desktop2/CFM1update1.1.zip -d ~/Desktop2")
							from distutils.dir_util import copy_tree
							try:
								copy_tree("/home/pi/Desktop2/CFM1update1.1", "/home/pi/Desktop2/UIP")
								os.system('rm /home/pi/Desktop2/CFM1update1.1.zip')
								os.system('rm -rf /home/pi/Desktop2/CFM1update1.1')
								os.system("sudo reboot")
							except: print("copy tree error")
						except:
							print("error updating")						
						break
					else:
						print("Update file not detected")
						self.b1000005.pos=320,170
						self.b1000005.text="Update file not detected"


	def brightness(self,value):
		command="sudo rpi-backlight -b"
		brightness=str(value*2)
		print((command + " " + brightness))
		if rpi==1:
			os.system(command + " " + brightness)

	def close(self):
		if rpi==1:
			GPIO.cleanup()
			print("cleaned")
			#os.system("lxterminal")			
			os.system('killall python')

	def listening(self,*args):
		global wheel
		global buttonparam
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		if self.b000000001.current_tab.text=="MIDI":
			buttonparam=0
		elif self.b000000001.current_tab.text=="CV":
			buttonparam=1
		if buttonparam==0:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					self.scrollDownMIDI()
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					self.scrollUpMIDI()


		if buttonparam==1:
			if encodervalue>0:
				wheel+=1
				if wheel==2:
					wheel=0
					self.scrollDownCV()
			elif encodervalue<0:
				wheel+=1
				if wheel==2:
					wheel=0
					self.scrollUpCV()

	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule param")


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
		if rangeYs<=7:
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
		for val in list(self.ids.items()):
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
		for val in list(self.ids.items()):
			if (str(val[0])== str('b001') or val[0]== 'b002' or val[0]== 'b003' or val[0]== 'b004'):
				pass
			else:
				self.clearStep(val[1])

	def monitor(self, button):
		global song
		global buttonpushedsong
		for key, val in list(self.ids.items()):
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
		for key, val in list(self.ids.items()):
			if val==button:
				ID=key
		trackselected=-(int(ID[1])-9)+rangeYs
		r2.put(trackselected)
		s2.put(trackselected)		
		v5.value=trackselected
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
				for val in list(self.ids.items()):
					if val[0]==b:
						if val[1].state=='normal':
							val[1].state='down'
							song[bx+rangeXs-1].append(byc+rangeYs+1)
							song[bx+rangeXs-1]=sorted(song[bx+rangeXs-1])
		q3.put(song)

	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule song")


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
		global playing
		if v6.value==1:
			v6.value=2
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			self.b001.state='down'
			Clock.schedule_interval(self.movebar, 0.002)
		elif v6.value==0:
			self.b001.text="%s"%(icon('icon-play', 22))
			self.b001.state='normal'
			playing=0
			v6.value=2	
			Clock.unschedule(self.movebar)	
			self.b015.pos=50,0				


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
		print("unschedule seq")

	def monitor(self, button):
		global sequencepool2
		global sequencepool3
		global buttonpushed
		global xseq
		global yseq

		for key, val in list(self.ids.items()):
			if val==button:
				ID=key
		yseq=int(ID[1])
		xseq=int(ID[-2:])
		buttonpushed=ID

		if button.state=="normal":
			print(("x",(xseq-1)*zoom+rangeX+1))
			print(("y",yseq+rangeY-1))
			for elem in sequencepool2[trackselected-1]:
				if elem[0]==(xseq-1)*zoom+rangeX+1 and elem[1]==yseq+rangeY-1 and elem[2]==1:
					duration=elem[3]
					break
			try:
				sequencepool2[trackselected-1].remove([(xseq-1)*zoom+rangeX+1,yseq+rangeY-1,1,duration])
				sequencepool2[trackselected-1].remove([(xseq-1)*zoom+rangeX+1+duration,yseq+rangeY-1,0,duration])
			except:
				print("******* Note 2 error ********")
			for elem in sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX]:
				if sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX][0]==yseq+rangeY-1:
					duration=elem[2]
					break
			try:
				sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX].remove([yseq+rangeY-1,1,duration])
				sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+duration].remove([yseq+rangeY-1,0,duration])
			except:
				print("******* Note 3 error ********")
			#print(sequencepool3[trackselected-1])
			self.loadseq()
			q1.put(sequencepool2)
			q6.put(sequencepool3[trackselected-1])

		if button.background_color==[0.3, 0.7, 1, 1]:
			i=0
			for elem in sequencepool2[trackselected-1]:
				if elem[1]==yseq+rangeY-1 and elem[2]==1:
					result=i
				if elem[0]>(xseq-1)*zoom+rangeX+1:
					break
				i+=1
			try:
				i=result
				removed=sequencepool2[trackselected-1][i]
				sequencepool2[trackselected-1].remove(removed)
				removed[0]=removed[0]+removed[3]
				removed[2]=0
				sequencepool2[trackselected-1].remove(removed)
			except:
				print("******* Chrods 2 error ********")


			j=0
			for elem in sequencepool3[trackselected-1]:
				if len(elem)>0:
					if j > (xseq-1)*zoom+rangeX+1:
						break					
					for elem2 in elem:
						if elem2[0]==yseq+rangeY-1 and elem2[1]==1:
							result2=j
				j+=1
			for elem in sequencepool3[trackselected-1][result2]:
				if elem[0]==yseq+rangeY-1 and elem[1]==1:
					duration=elem[2]
					break
			try:
				sequencepool3[trackselected-1][result2].remove([yseq+rangeY-1,1,duration])
				sequencepool3[trackselected-1][result2+duration].remove([yseq+rangeY-1,0,duration])
			except:
				print("******* Chrods 3 error ********")
			#print(sequencepool3[trackselected-1])
			self.loadseq()
			q1.put(sequencepool2)
			q6.put(sequencepool3[trackselected-1])


		if button.state=="down":
			sequencepool2[trackselected-1].append([(xseq-1)*zoom+rangeX+1+zoom,yseq+rangeY-1,0,zoom])
			sequencepool2[trackselected-1].append([(xseq-1)*zoom+rangeX+1,yseq+rangeY-1,1,zoom])
			sequencepool2[trackselected-1]=sorted(sequencepool2[trackselected-1], key=operator.itemgetter(0,2))
			sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+zoom].append([yseq+rangeY-1,0,zoom])
			sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+zoom]=sorted(sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+zoom],key=operator.itemgetter(1,0))
			sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX].append([yseq+rangeY-1,1,zoom])
			sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX]=sorted(sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX],key=operator.itemgetter(1,0))
			#print(sequencepool3[trackselected-1])
			q1.put(sequencepool2)
			q6.put(sequencepool3[trackselected-1])



	def clearsequence(self):
		global sequencepool2
		global sequencepool3
		sequencepool2[trackselected-1]=[]
		for i,elem in enumerate(sequencepool3[trackselected-1]):
			sequencepool3[trackselected-1][i]=[]
		q1.put(sequencepool2)
		q6.put(sequencepool3[trackselected-1])
		#print(sequencepool2)
		print((sequencepool3[trackselected-1]))


	def clearStep(self,button):
		button.state="normal"


	def clear(self):
		for val in list(self.ids.items()):
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
		for val in list(self.ids.items()):
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
		for val in list(self.ids.items()):
			if button==val[0]:
				buttonfound=val[1]
				buttonfound.state="down"

	def findButtonC(self,button):
		for val in list(self.ids.items()):
			if button==val[0]:
				buttonfound=val[1]
				buttonfound.background_color=[0.3, 0.7, 1, 1]

	def findButtonCi(self,button):
		for val in list(self.ids.items()):
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
			self.b022.pos= 344,900			
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
			self.b022.pos= 344,900			
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
			self.b022.pos= 344,124			
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
			self.b022.pos= 344,900			
			self.b010.pos= 1000,0

	def recordingbut(self):
		global recordingON
		if self.b022.text=='REC OFF':
			self.b022.text='REC ON'
			recordingON=1
		else:
			self.b022.text='REC OFF'
			recordingON=0	
		print(recordingON)		


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
		print(("buton mode",seqbuttonmode))



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
					b="b"+str(by)+str(bx)
				for val in list(self.ids.items()):
					if val[0]==b:
						if val[1].state=='normal':
							val[1].background_color=[0.3, 0.7, 1, 1]
					if val[0]==buttonpushed and erased==0:
						val[1].state=='normal'
						try:
							sequencepool2[trackselected-1].remove([(xseq-1)*zoom+rangeX+1+zoom,yseq+rangeY-1,0,zoom])
							sequencepool2[trackselected-1].remove([(xseq-1)*zoom+rangeX+1,yseq+rangeY-1,1,zoom])
							sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+zoom].remove([yseq+rangeY-1,0,zoom])
							sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX].remove([yseq+rangeY-1,1,zoom])
							erased=1
						except:
							print("************* Touch move remove error ***********")



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
				for val in list(self.ids.items()):
					if val[0]==b:
						erased=0
						binit=int(buttonpushed[-2:])
						duration=(bx-binit)+1
						try:
							sequencepool2[trackselected-1].append([(xseq-1)*zoom+rangeX+1,yseq+rangeY-1,1,duration*zoom])
							sequencepool2[trackselected-1].append([(xseq-1)*zoom+rangeX+1+duration*zoom,yseq+rangeY-1,0,duration*zoom])
							sequencepool2[trackselected-1]=sorted(sequencepool2[trackselected-1], key=operator.itemgetter(0,2))
							sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX].append([yseq+rangeY-1,1,duration*zoom])
							sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+duration*zoom].append([yseq+rangeY-1,0,duration*zoom])
							sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX]=sorted(sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX], key=operator.itemgetter(1,0))
							sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+duration*zoom]=sorted(sequencepool3[trackselected-1][(xseq-1)*zoom+rangeX+duration*zoom], key=operator.itemgetter(1,0))
							#print(sequencepool3[trackselected-1])
						except:
							print("****************************************")
						q1.put(sequencepool2)
						q6.put(sequencepool3[trackselected-1])
						self.loadseq()


	def recording(self):
		while s4.empty() is False:
				noterec=s4.get()
				#print(('noterec USB', noterec))
				self.recordingnote(noterec)
		while r4.empty() is False:
				noterec=r4.get()
				#print(('noterec DIN', noterec))
				self.recordingnote(noterec)
				

	def recordingnote(self,noterec):
		step=v2.value%loopsize[trackselected-1]
		step=step/4 *4
		if recordingON==1:
			if [step+1,noterec-24,1,4] not in sequencepool2[trackselected-1]:
				sequencepool2[trackselected-1].append([step+1,noterec-24,1,4])
				sequencepool2[trackselected-1].append([step+5,noterec-24,0,4])
				sequencepool2[trackselected-1]=sorted(sequencepool2[trackselected-1], key=operator.itemgetter(0,2))
				sequencepool3[trackselected-1][step].append([noterec-24,1,4])
				sequencepool3[trackselected-1][step+4].append([noterec-24,0,4])
				sequencepool3[trackselected-1][step]=sorted(sequencepool3[trackselected-1][step], key=operator.itemgetter(1,0))
				sequencepool3[trackselected-1][step+4]=sorted(sequencepool3[trackselected-1][step+4], key=operator.itemgetter(1,0))					
				self.loadseq()
				q1.put(sequencepool2)
				q6.put(sequencepool3[trackselected-1])	

	def listening(self,*args):
		global wheel
		global seqbuttonmode
		global loopsize
		global BPM
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		step=v2.value
		self.recording()

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
		global playing
		if v6.value==1:
			v6.value=2
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			self.b001.state='down'
			Clock.schedule_interval(self.movebar, 0.002)
		elif v6.value==0:
			self.b001.text="%s"%(icon('icon-play', 22))
			self.b001.state='normal'
			playing=0
			v6.value=2	
			Clock.unschedule(self.movebar)	
			self.b015.pos=50,0


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
		global playing
		v1.value=0
		playing=0
		rangeFile=0
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)		
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
			if rpi==1:
				with open('/home/pi/Desktop2/UIP/savedseq.json', "w") as s:
					saved["savedseq"][chosen+rangeFile*4-1]["sequence"] = sequencepool2[trackselected-1]
					json.dump(saved, s)
			else:
				with open('savedseq.json', "w") as s:
					saved["savedseq"][chosen+rangeFile*4-1]["sequence"] = sequencepool2[trackselected-1]
					json.dump(saved, s)				
		else:
			from midi import MIDIFile
			track    = 0
			channel  = 0
			time     = 0
			tempo    = 120
			volume   = 100
			MyMIDI = MIDIFile(1)
			MyMIDI.addTempo(track, time, tempo)			
			for elem in sequencepool2[trackselected-1]:
				if elem[2]==1:
					MyMIDI.addNote(track, channel, elem[1]+24, Decimal(elem[0]-1)/16, Decimal(elem[3])/16, volume)
			for files in os.walk('/media/pi'):
				resulted=files
				break
			resulted=str(resulted[1])
			resulted=resulted[:-2]
			location=str(resulted[2:])
			print(location)
			if len(location)>1:
				filetext='/media/pi/'+location+'/'+str(chosen+rangeFile*4)+'.mid'
				print(filetext)
			try:
				with open(filetext, "wb") as output_file:
					MyMIDI.writeFile(output_file)
			except:
				print("error usb")
		self.leaving()


	def up(self):
		global rangeFile
		if rangeFile<21:
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

	def listening(self,*args):
		global wheel
		global buttonparam
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		if encodervalue>0:
			wheel+=1		
			if wheel==2:
				wheel=0
				self.up()
		elif encodervalue<0:
			wheel+=1
			if wheel==2:
				wheel=0
				self.dw()
		self.usbcheck()

	def usbcheck(self):
		for files in os.walk('/media/pi'):
			resulted=files
			break
		resulted=str(resulted[1])
		resulted=resulted[:-2]
		location=str(resulted[2:])
		if len(location)<1:
			self.b002.state="normal"
			self.b001.state="down"
			self.b002.text="EXPORT %s"%(icon('icon-lock', 22))
		else:
			self.b002.text="EXPORT"

	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule SaveSeq")

class LoadSeq(Screen):

	def on_enter(self):
		global rangeFile
		global playing
		v1.value=0
		playing=0
		rangeFile=0
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)		
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
			if rpi==1:
				with open('/home/pi/Desktop2/UIP/savedseq.json') as s:
					saved = json.load(s)
					print((saved["savedseq"][chosen+rangeFile*4-1]["sequence"]))
					sequencepool2[trackselected-1]=saved["savedseq"][chosen+rangeFile*4-1]["sequence"]
					q1.put(sequencepool2)
			else:
				with open('savedseq.json') as s:
					saved = json.load(s)
					print((saved["savedseq"][chosen+rangeFile*4-1]["sequence"]))
					sequencepool2[trackselected-1]=saved["savedseq"][chosen+rangeFile*4-1]["sequence"]
					q1.put(sequencepool2)				
		else:
			from midiconvert import MIDIconvert
			for files in os.walk('/media/pi'):
				resulted=files
				break
			resulted=str(resulted[1])
			resulted=resulted[:-2]
			location=str(resulted[2:])
			print(location)
			if len(location)>1:
				filetext='/media/pi/'+location+'/'+str(chosen+rangeFile*4)+'.mid'
				print(filetext)
				try:
					sequencepool2[trackselected-1]=MIDIconvert(filetext)
					print(sequencepool2)
				except:
					print('no such file')
					sequencepool2[trackselected-1]=[]
			else:
				sequencepool2[trackselected-1]=[]
		self.convert()
		self.leaving()

	def usbcheck(self):
		for files in os.walk('/media/pi'):
			resulted=files
			break
		resulted=str(resulted[1])
		resulted=resulted[:-2]
		location=str(resulted[2:])
		if len(location)<1:
			self.b002.state="normal"
			self.b001.state="down"
			self.b002.text="IMPORT %s"%(icon('icon-lock', 22))
		else:
			self.b002.text="IMPORT"

	def convert(self):
		for i,elem in enumerate(sequencepool3[trackselected-1]):
			sequencepool3[trackselected-1][i]=[]
		for elem in sequencepool2[trackselected-1]:
			sequencepool3[trackselected-1][elem[0]-1].append([elem[1],elem[2],elem[3]])
		q6.put(sequencepool3[trackselected-1])

	def up(self):
		global rangeFile
		if rangeFile<21:
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

	def listening(self,*args):
		global wheel
		global buttonparam
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		if encodervalue>0:
			wheel+=1
			if wheel==2:
				wheel=0
				self.up()
		elif encodervalue<0:
			wheel+=1
			if wheel==2:
				wheel=0
				self.dw()
		self.usbcheck()


	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule LoadSeq")




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




class LFOScreen(Screen):

	def on_enter(self):
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)
		self.b003.text=str(BPM)
		if playing==1:
			self.b001.state="down"
			self.b001.text="%s"%(icon('icon-pause', 22))
		else:
			self.b001.state="normal"
			self.b001.text="%s"%(icon('icon-play', 22))
		global Lline1
		#global Lline2
		#global Lline3
		global Lline4
		#global Lline5
		#global Lline6	
		global Lline7											
		Lline1 = self.ids.w_canvas.canvas.get_group('a')[0]
		#Lline2 = self.ids.w_canvas.canvas.get_group('c')[0]
		#Lline3 = self.ids.w_canvas.canvas.get_group('d')[0]				
		Lline4 = self.ids.w_canvas.canvas.get_group('b')[0]
		#Lline5 = self.ids.w_canvas.canvas.get_group('e')[0]
		#Lline6 = self.ids.w_canvas.canvas.get_group('f')[0]
		Lline7 = self.ids.w_canvas.canvas.get_group('g')[0]					
		global LFOcoord
		global LFOcoordPool
		global trackmode
		LFOcoordPool=[[52,15,400,385,748,15,55,100],[52,15,400,385,748,15,55,100],[52,15,400,385,748,15,55,100],[52,15,400,385,748,15,55,100],[52,15,400,385,748,15,55,100],[52, 83, 540, 317, 748, 83, 175, 60]]
		LFOcoord=LFOcoordPool[trackselected-1]
		trackmode=[1,2,3,1,1,1,1,1,1,1,1,1,1,1,1,1] #1=seq, 2=LFO, 3=ADSR
		self.display()
		global lfobutmode
		lfobutmode=6
		print(trackselected-1)

	def display(self):
		global LFOcoordPool
		Lline1.points=[(LFOcoord[0],LFOcoord[1]),(LFOcoord[2],LFOcoord[3])]
		Lline4.points=[(LFOcoord[2],LFOcoord[3]),(LFOcoord[4],LFOcoord[5])]
		self.b023.pos=(LFOcoord[2]-20,180)
		self.b024.pos=(17,LFOcoord[3]-20)
		self.b024.text=str(LFOcoord[7])
		self.b025.pos[0]=LFOcoord[6]
		Lline7.pos=(LFOcoord[2]-10,LFOcoord[3]-10)		
		LFOcoordPool[trackselected-1]=LFOcoord
		print(LFOcoordPool)

	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule seq")


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
			self.b022.pos= 344,900			
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
			self.b022.pos= 344,900			
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
			#self.b014.pos= 344,301
			#self.b016.pos= 344,242
			#self.b020.pos= 344,183
			#self.b022.pos= 344,124			
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
			self.b022.pos= 344,900			
			self.b010.pos= 1000,0

	def recording(self):
		if self.b022.text=='REC OFF':
			self.b022.text='REC ON'
		else:
			self.b022.text='REC OFF'			


	def mode(self,num):
		global lfobutmode
		if num==1:
			if lfobutmode==1:
				lfobutmode=0
				self.b020.state='normal'
			else:
				lfobutmode=1
				self.b020.state='down'
				w2.value=0
		if num==2:
			if lfobutmode==2:
				lfobutmode=0
				self.b003.state='normal'
			else:
				lfobutmode=2
				self.b003.state='down'
				w2.value=0
		if num==3:
			if lfobutmode==3:
				lfobutmode=0
				self.b004.state='normal'
			else:
				lfobutmode=3
				self.b004.state='down'
				w2.value=0
		if num==4:
			if lfobutmode==4:
				lfobutmode=0
				self.b025.state='normal'
			else:
				lfobutmode=4
				self.b025.state='down'
				w2.value=0
		if num==5:
			if lfobutmode==5:
				lfobutmode=0
				self.b024.state='normal'
			else:
				lfobutmode=5
				self.b024.state='down'
				w2.value=0				


		if num==6:
			lfobutmode=6
			self.b003.state='normal'
			self.b004.state='normal'
			self.b020.state='normal'
		print(("buton mode",lfobutmode))



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
		else:
			self.b001.text="%s"%(icon('icon-play', 22))
			playing=0
			v1.value=2



	def stop(self):
		global playing
		self.b001.state="normal"
		self.b001.text="%s"%(icon('icon-play', 22))
		v1.value=0
		playing=0

	def reset(self):
		global LFOcoord
		LFOcoord=[52,15,400,385,748,15,55,100]
		self.display()


	def rgt(self):
		global LFOcoord
		if LFOcoord[2]<730:
			LFOcoord[2]+=20
			self.display()

	def lft(self):
		global LFOcoord
		if LFOcoord[2]>70:
			LFOcoord[2]+=-20
			self.display()

	def up(self):
		global LFOcoord
		if int(self.b024.text)>10:
			LFOcoord[1]+=17
			LFOcoord[3]+=-17
			LFOcoord[5]+=17
			LFOcoord[7]+=-10	
			self.display()

	def dw(self):
		global LFOcoord
		if int(self.b024.text)<100:		
			LFOcoord[1]+=-17
			LFOcoord[3]+=17
			LFOcoord[5]+=-17
			LFOcoord[7]+=10				
			self.display()

	def strl(self):
		global LFOcoord
		if self.b025.pos[0]>70:
			LFOcoord[6]+=-20
			self.display()


	def strr(self):
		global LFOcoord
		if self.b025.pos[0]<730:
			LFOcoord[6]+=20
			self.display()


	def listening(self,*args):
		global wheel
		global lfobutmode
		global loopsize
		global BPM
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		step=v2.value

		if lfobutmode==0:
			pass

		if lfobutmode==1:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.rgt()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.lft()
			if encoderpushed==1:
				lfobutmode=0
				self.b023.state='normal'
				self.closemenus()

		if lfobutmode==2:
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
				lfobutmode=0
				self.b003.state='normal'


		if lfobutmode==3:
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
				lfobutmode=0
				self.b004.state='normal'

		if lfobutmode==4:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.strr()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.strl()
			if encoderpushed==1:
				lfobutmode=0
				self.b025.state='normal'
				self.closemenus()
		if lfobutmode==5:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.up()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.dw()
			if encoderpushed==1:
				lfobutmode=0
				self.b024.state='normal'
				self.closemenus()
		global playing
		if v6.value==1:
			v6.value=2
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			self.b001.state='down'
		elif v6.value==0:
			self.b001.text="%s"%(icon('icon-play', 22))
			self.b001.state='normal'
			playing=0
			v6.value=2


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



class ADSRScreen(Screen):

	def on_enter(self):
		w1.value=0
		Clock.schedule_interval(self.listening, 0.002)
		self.b003.text=str(BPM)
		if playing==1:
			self.b001.state="down"
			self.b001.text="%s"%(icon('icon-pause', 22))
		else:
			self.b001.state="normal"
			self.b001.text="%s"%(icon('icon-play', 22))
		global Lline1
		global Lline2
		global Lline3
		global Lline4
		global Lline5
		global Lline6	
		global Lline7									
		Lline1 = self.ids.w_canvas.canvas.get_group('a')[0]
		Lline2 = self.ids.w_canvas.canvas.get_group('b')[0]
		Lline3 = self.ids.w_canvas.canvas.get_group('c')[0]				
		Lline4 = self.ids.w_canvas.canvas.get_group('d')[0]
		Lline5 = self.ids.w_canvas.canvas.get_group('e')[0]
		Lline6 = self.ids.w_canvas.canvas.get_group('f')[0]
		Lline7 = self.ids.w_canvas.canvas.get_group('g')[0]	
		global ADSRcoord
		global ADSRcoordPool
		global trackmode
		ADSRcoordPool=[[52, 30, 100, 385, 150, 200, 300, 200, 500, 30, 100, 50],[52,15,400,385,748,15,55,100],[52,15,400,385,748,15,55,100],[52,15,400,385,748,15,55,100],[52,15,400,385,748,15,55,100],[52, 83, 540, 317, 748, 83, 175, 60]]
		ADSRcoord=ADSRcoordPool[trackselected-1]
		trackmode=[1,2,3,1,1,1,1,1,1,1,1,1,1,1,1,1] #1=seq, 2=LFO, 3=ADSR
		self.display()
		global adsrbutmode
		adsrbutmode=0
		print(trackselected-1)

	def display(self):
		global ADSRcoordPool
		Lline1.points=[(ADSRcoord[0],ADSRcoord[1]),(ADSRcoord[2],ADSRcoord[3])]
		Lline2.points=[(ADSRcoord[2],ADSRcoord[3]),(ADSRcoord[4],ADSRcoord[5])]
		Lline3.points=[(ADSRcoord[4],ADSRcoord[5]),(ADSRcoord[6],ADSRcoord[7])]
		Lline4.points=[(ADSRcoord[6],ADSRcoord[7]),(ADSRcoord[8],ADSRcoord[9])]				
		self.b023.pos=(ADSRcoord[2]-20,13)
		self.b024.pos=(17,ADSRcoord[3]-20)
		self.b024.text=str(ADSRcoord[10])
		self.b028.pos=(17,ADSRcoord[5]-20)
		self.b028.text=str(ADSRcoord[11])
		self.b025.pos=(ADSRcoord[4]-20,13)
		self.b026.pos=(ADSRcoord[6]-20,13)
		self.b027.pos=(ADSRcoord[8]-20,13)
		ADSRcoordPool[trackselected-1]=ADSRcoord
		Lline5.pos=(ADSRcoord[2]-10,ADSRcoord[3]-10)
		Lline6.pos=(ADSRcoord[4]-10,ADSRcoord[5]-10)
		Lline7.pos=(ADSRcoord[6]-10,ADSRcoord[7]-10)		
		print(ADSRcoordPool)

	def leaving(self):
		Clock.unschedule(self.listening)
		print("unschedule seq")


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
			self.b022.pos= 344,900			
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
			self.b022.pos= 344,900			
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
			#self.b014.pos= 344,301
			#self.b016.pos= 344,242
			#self.b020.pos= 344,183
			#self.b022.pos= 344,124			
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
			self.b022.pos= 344,900			
			self.b010.pos= 1000,0

	def recording(self):
		if self.b022.text=='REC OFF':
			self.b022.text='REC ON'
		else:
			self.b022.text='REC OFF'			


	def mode(self,num):
		global adsrbutmode
		if num==1:
			if adsrbutmode==1:
				adsrbutmode=0
				self.b023.state='normal'
			else:
				adsrbutmode=1
				self.b023.state='down'
				w2.value=0
		if num==2:
			if adsrbutmode==2:
				adsrbutmode=0
				self.b003.state='normal'
			else:
				adsrbutmode=2
				self.b003.state='down'
				w2.value=0
		if num==3:
			if adsrbutmode==3:
				adsrbutmode=0
				self.b004.state='normal'
			else:
				adsrbutmode=3
				self.b004.state='down'
				w2.value=0
		if num==4:
			if adsrbutmode==4:
				adsrbutmode=0
				self.b025.state='normal'
			else:
				adsrbutmode=4
				self.b025.state='down'
				w2.value=0
		if num==5:
			if adsrbutmode==5:
				adsrbutmode=0
				self.b024.state='normal'
			else:
				adsrbutmode=5
				self.b024.state='down'
				w2.value=0				
		if num==6:
			if adsrbutmode==6:
				adsrbutmode=0
				self.b028.state='normal'
			else:
				adsrbutmode=6
				self.b028.state='down'
				w2.value=0	
		if num==7:
			if adsrbutmode==7:
				adsrbutmode=0
				self.b026.state='normal'
			else:
				adsrbutmode=7
				self.b026.state='down'
				w2.value=0	
		if num==8:
			if adsrbutmode==8:
				adsrbutmode=0
				self.b027.state='normal'
			else:
				adsrbutmode=8
				self.b027.state='down'
				w2.value=0	
										

		if num==9:
			adsrbutmode=0
			self.b003.state='normal'
			self.b004.state='normal'
			self.b020.state='normal'
		print(("buton mode",adsrbutmode))



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
		else:
			self.b001.text="%s"%(icon('icon-play', 22))
			playing=0
			v1.value=2



	def stop(self):
		global playing
		self.b001.state="normal"
		self.b001.text="%s"%(icon('icon-play', 22))
		v1.value=0
		playing=0

	def reset(self):
		global ADSRcoord
		ADSRcoord=[52, 30, 100, 385, 150, 200, 300, 200, 500, 30, 100, 50]
		self.display()


	def rgt(self):
		global ADSRcoord
		if ADSRcoord[2]<730:
			ADSRcoord[2]+=20
			ADSRcoord[4]+=20
			ADSRcoord[6]+=20
			ADSRcoord[8]+=20
			self.display()

	def lft(self):
		global ADSRcoord
		if ADSRcoord[2]>70:
			ADSRcoord[2]+=-20
			ADSRcoord[4]+=-20
			ADSRcoord[6]+=-20
			ADSRcoord[8]+=-20			
			self.display()

	def strl(self):
		global ADSRcoord
		if self.b025.pos[0]>self.b023.pos[0]+50:
			ADSRcoord[4]+=-20
			ADSRcoord[6]+=-20			
			ADSRcoord[8]+=-20			
			self.display()

	def strr(self):
		global ADSRcoord
		if self.b025.pos[0]<730:
			ADSRcoord[4]+=20
			ADSRcoord[6]+=20			
			ADSRcoord[8]+=20	
			self.display()

	def strll(self):
		global ADSRcoord
		if self.b026.pos[0]>self.b025.pos[0]+50:
			ADSRcoord[6]+=-20			
			ADSRcoord[8]+=-20			
			self.display()

	def strrr(self):
		global ADSRcoord
		if self.b026.pos[0]<730:
			ADSRcoord[6]+=20			
			ADSRcoord[8]+=20	
			self.display()

	def strlll(self):
		global ADSRcoord
		if self.b027.pos[0]>self.b026.pos[0]+50:		
			ADSRcoord[8]+=-20			
			self.display()

	def strrrr(self):
		global ADSRcoord
		if self.b027.pos[0]<730:			
			ADSRcoord[8]+=20	
			self.display()

	def up(self):
		global ADSRcoord
		if int(self.b024.text)<100:
			ADSRcoord[3]+=34
			ADSRcoord[10]+=10	
			self.display()

	def dw(self):
		global ADSRcoord
		if int(self.b024.text)>int(self.b028.text) and int(self.b024.text)>20:		
			ADSRcoord[3]+=-34
			ADSRcoord[10]+=-10			
			self.display()

	def up2(self):
		global ADSRcoord
		if int(self.b028.text)<int(self.b024.text):
			ADSRcoord[5]+=34
			ADSRcoord[7]+=34
			ADSRcoord[11]+=10	
			self.display()

	def dw2(self):
		global ADSRcoord
		if int(self.b028.text)>10:		
			ADSRcoord[5]+=-34
			ADSRcoord[7]+=-34
			ADSRcoord[11]+=-10			
			self.display()


	def listening(self,*args):
		global wheel
		global adsrbutmode
		global loopsize
		global BPM
		encodervalue=w1.value
		encoderpushed=w2.value
		w1.value=0
		step=v2.value

		if adsrbutmode==0:
			pass

		if adsrbutmode==1:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.rgt()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.lft()
			if encoderpushed==1:
				adsrbutmode=0
				self.b023.state='normal'
				self.closemenus()

		if adsrbutmode==2:
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
				adsrbutmode=0
				self.b003.state='normal'


		if adsrbutmode==3:
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
				adsrbutmode=0
				self.b004.state='normal'

		if adsrbutmode==4:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.strr()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.strl()
			if encoderpushed==1:
				adsrbutmode=0
				self.b025.state='normal'
				self.closemenus()

		if adsrbutmode==5:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.up()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.dw()
			if encoderpushed==1:
				adsrbutmode=0
				self.b024.state='normal'
				self.closemenus()				

		if adsrbutmode==6:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.up2()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.dw2()
			if encoderpushed==1:
				adsrbutmode=0
				self.b028.state='normal'
				self.closemenus()

		if adsrbutmode==7:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.strrr()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.strll()
			if encoderpushed==1:
				adsrbutmode=0
				self.b026.state='normal'
				self.closemenus()

		if adsrbutmode==8:
			if encodervalue>0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.strrrr()
			elif encodervalue<0:
				self.closemenus()
				wheel+=1
				if wheel==2:
					wheel=0
					self.strlll()
			if encoderpushed==1:
				adsrbutmode=0
				self.b027.state='normal'
				self.closemenus()								
		global playing
		if v6.value==1:
			v6.value=2
			playing=1
			self.b001.text="%s"%(icon('icon-pause', 22))
			self.b001.state='down'
		elif v6.value==0:
			self.b001.text="%s"%(icon('icon-play', 22))
			self.b001.state='normal'
			playing=0
			v6.value=2


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


	def Timer(self,v1,v2,v3,v4,v5,v6,q1,q2,q3,q4,q5,q6):
		nextcall=time.time()
		count=0
		MIDIstoped=0
		paused=0
		portopened=0

		while 1:
			BPM=v4.value
			interval=float(60/Decimal(BPM)/Decimal(16))
			v2.value=count
			trackselected=v5.value
			while q1.empty() is False:
					sequencepool2=q1.get()
					if rpi==0:print('sequencepool2', sequencepool2)
			while q2.empty() is False:
					loopsize=q2.get()
					if rpi==0:print(('loopsize', loopsize))
			while q3.empty() is False:
					song=q3.get()
					if rpi==0:print(('song', song))
			while q4.empty() is False:
					Sendinfo=q4.get()
					if rpi==0:print(('sendinfo', Sendinfo))
			while q5.empty() is False:
					Syncinfo=q5.get()
					if rpi==0:print(('Syncinfo',Syncinfo))
			while q6.empty() is False:
					update3=q6.get()
					#print(("updated seq3",update3))
					#print(('trackselected',trackselected))
					sequencepool3[trackselected-1]=update3
					if rpi==0:print('sequencepool3[track]', sequencepool3[trackselected-1])
					#print('sequencepool3queue', sequencepool3)
					#pass


			if rpi==1 and Syncinfo[4]==0:
				available_ports = midiout.get_ports()
				port = available_ports[0]
				if len(available_ports)>1:
				  port = available_ports[1]
				port = mido.open_output(port)
				#pwmsync.start(0)
				#GPIO.setup(pwm,GPIO.OUT)
				#GPIO.setup(jackstart,GPIO.OUT)
			else:
				port=0

			if v1.value==1:
				if MIDIstoped==1 and paused==0:
					self.MIDImessage(250,Syncinfo)
					self.USBmessage("start",Syncinfo,port)
					self.jacksyncstart(Syncinfo,BPM)

				if paused==1:
					paused=0
					self.MIDImessage(251,Syncinfo)
					self.USBmessage("continue",Syncinfo,port)
					self.jacksyncstart(Syncinfo,BPM)
				MIDIstoped=0
				count+=1
				if count > v3.value:
					count=1
				nextcall = nextcall+interval
				self.send2(count,sequencepool3,loopsize,song,Sendinfo,port,Syncinfo)
				print((nextcall-time.time()))
				if nextcall-time.time()>0:
					time.sleep(nextcall-time.time())
				else:
					nextcall=time.time()
			elif v1.value==2:
				paused=1
				if MIDIstoped==0:
					self.MIDImessage(252,Syncinfo)
					self.USBmessage("stop",Syncinfo,port)
					self.jacksyncstop()
					MIDIstoped=1
					for i in range(0,15):
						self.noteoffUSB(i,Sendinfo,port)
						self.noteoffMIDI(i,Sendinfo)
			else:
				if MIDIstoped==0 or paused==1:
					MIDIstoped=1
					paused=0
					self.MIDImessage(252,Syncinfo)
					self.USBmessage("stop",Syncinfo,port)
					self.jacksyncstop()
					for i in range(0,15):
						self.noteoffUSB(i,Sendinfo,port)
						self.noteoffMIDI(i,Sendinfo)
				count=0
			time.sleep(0.0005)



	def send2(self,count,sequencepool3,loopsize,song,Sendinfo,port,Syncinfo):
		for n,track in enumerate(sequencepool3): #n is track number
			pos=count%loopsize[n]-1
			if pos==0:
				if n+1 in song[int(count/(16*4))-1]:
					#print(("All Notes Off on track: ",n+1))
					if Sendinfo[n][6]==1:
						self.noteoffUSB(n,Sendinfo,port)
					if Sendinfo[n][6]==2:
						self.noteoffMIDI(n,Sendinfo)
				if n+1 in song[int(v3.value/(16*4))-1] and count==1:
					#print(("All Notes Off on track (looped): ",n+1))
					if Sendinfo[n][6]==1:
						self.noteoffUSB(n,Sendinfo,port)
					if Sendinfo[n][6]==2:
						self.noteoffMIDI(n,Sendinfo)
			if n+1 in song[int(count/(16*4))]:
				if len(track[pos])>0:
					for elem in track[pos]:
						#print(("Sending",elem))
						if Sendinfo[n][6]==1:
							self.USBsend2(n,elem,Sendinfo,port)
						if Sendinfo[n][6]==2:
							self.MIDIsend2(n,elem,Sendinfo)
						if Sendinfo[n][1]>0:
							self.CVsendPitch2(n,elem,Sendinfo)
						if Sendinfo[n][3]>0:
							self.CVsendGate2(n,elem,Sendinfo)

		if count%2==0:
			self.MIDImessage(248,Syncinfo)
			self.USBmessage("clock",Syncinfo,port)
			self.MIDImessage(248,Syncinfo)
			self.USBmessage("clock",Syncinfo,port)
		else:
			self.MIDImessage(248,Syncinfo)
			self.USBmessage("clock",Syncinfo,port)


	def noteoffUSB(self,n,Sendinfo,port):
		#print("note off USB")
		channel=Sendinfo[n][0]-1
		msg=mido.Message('control_change', channel=channel,control=123)
		try:
			port.send(msg)
		except:
			pass
			#print('(Port error note off)')

	def noteoffMIDI(self,n,Sendinfo):
		#print("note off DIN")
		byte1=bin(int(176+Sendinfo[n][0]-1))
		byte2=bin(int(123))
		byte3=bin(0)
		byte_chr1 = chr(int(byte1,2))
		byte_chr2 = chr(int(byte2,2))
		byte_chr3 = chr(int(byte3,2))
		if rpi==1:
			ser.write(byte_chr1)
			ser.write(byte_chr2)
			ser.write(byte_chr3)


	def MIDImessage(self,message,Syncinfo):
		#stop 252, continue 251, start 250, clock 248
		#print(message)
		if Syncinfo[0]==1:
			byte1=bin(int(message))
			#print(message)
			byte_chr1 = chr(int(byte1,2))
			if rpi==1:
				ser.write(byte_chr1)

	def USBmessage(self,message,Syncinfo,port):
		#stop, continue, start, clock
		if Syncinfo[1]==1:
			msg=mido.Message(message)
			#print(message)
			try:
				port.send(msg)
				#print("clock1")
				if Syncinfo[3]==2 and message=="clock":
					port.send(msg)
					#print("clock2")
			except:
				pass
				#print('(Port error message)')


	def CVsendGate2(self,n,elem,Sendinfo):
			if elem[1]==1:
				#print(('CV Gate On',Sendinfo[n][3], Sendinfo[n][4], 'Value: 8V'))
				if rpi==1:
					try:
						bus.write_i2c_block_data(Sendinfo[n][3], Sendinfo[n][4], [0x0D, 0xE0])
					except:
						#print("No DAC found")
						pass
			else:
				#print(('CV Gate Off',Sendinfo[n][3], Sendinfo[n][4], 'Value: 0V'))
				if rpi==1:
					try:
						bus.write_i2c_block_data(Sendinfo[n][3], Sendinfo[n][4], [0x05, 0x55])
					except:
						#print("No DAC found")
						pass

	def CVsendPitch2(self,n,elem,Sendinfo):
			if elem[1]==1:
				a,b=divmod(4096*elem[0]/15/12+4096/15*Sendinfo[n][5],256)
				#print(('CV Pitch On',Sendinfo[n][1],Sendinfo[n][2], 'Value',elem[0], 'Offset' , Sendinfo[n][5]))
				if rpi==1:
					try:
						bus.write_i2c_block_data(Sendinfo[n][1], Sendinfo[n][2], [a, b])
					except:
						#print("No DAC found")
						pass


	def MIDIsend2(self,n,elem,Sendinfo):
		if elem[1]==1:
			#print(("DIN send" , elem[0] ,"channel" , Sendinfo[n][0]))
			byte1=bin(int(128+16+Sendinfo[n][0]-1))
			byte3=bin(100)
		else:
			#print(("DIN stop" , elem[0] ,"channel" , Sendinfo[n][0]))
			byte1=bin(int(128+Sendinfo[n][0]-1))
			byte3=bin(0)
		byte2 = bin(int(24+elem[0]))
		byte_chr1 = chr(int(byte1,2))
		byte_chr3 = chr(int(byte3,2))
		byte_chr2 = chr(int(byte2,2))
		if rpi==1:
			ser.write(byte_chr1)
			ser.write(byte_chr2)
			ser.write(byte_chr3)

	def USBsend2(self,n,elem,Sendinfo,port):
		#print(port)
		channel=Sendinfo[n][0]-1
		if elem[1]==1:
			msg=mido.Message('note_on', note=elem[0]+24, channel=channel)
		else:
			msg=mido.Message('note_off', note=elem[0]+24, channel=channel)
		try:
			port.send(msg)
		except:
			#print('(Port error sending)')
			pass

	def jacksyncstart(self,Syncinfo,BPM):
		if rpi==1:
			GPIO.output(jackstart,GPIO.HIGH)
			#print(("BPMM",BPM*Syncinfo[2]/4))
			pwmsync.ChangeFrequency(BPM*Syncinfo[2]/4)
			pwmsync.start(50)


	def jacksyncstop(self):
		if rpi==1:
			GPIO.output(jackstart,GPIO.LOW)
			#pwmsync.ChangeDutyCycle(0)
			pwmsync.stop()




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


	def starting(self,w1,w2):
		global clkLastState
		global swLastState

		if rpi==1:
			clkLastState = GPIO.input(clk)
			swLastState = GPIO.input(sw)
		while 1:
			self.encoder()
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
					w1.value+=-1
				else:
					w1.value+=1
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



class Listen2():


	def starting(self,r1,r2,r3,r4):
		global midibyte
		global messagemidi
		midibyte=0
		messagemidi = [0, 0, 0]

		
		while 1:
			while r1.empty() is False:
				Sendinfo=r1.get()
				#print(('Sendinfo', Sendinfo))
			while r2.empty() is False:
				trackselected=r2.get()
				#print(('trackselected', trackselected))
			while r3.empty() is False:
				Syncinfo=r3.get()
				#print(('Syncinfo2', Syncinfo))	
			#print("listen2")		
			self.MIDIdinIn(Sendinfo,trackselected,Syncinfo)
			#time.sleep(0.001)
			time.sleep(0.001)
			


	def MIDIdinIn(self,Sendinfo,trackselected,Syncinfo):
		global midibyte
		if rpi==1:
			while midibyte < 3:
				data = ord(ser.read(1)) # read a byte
				#print(data)
				if data==250 or data==251 or data==252:
				#	self.DINsyncout(data,Syncinfo)
					self.DINsyncin(data)
				if data >> 7 != 0:
					midibyte = 0      # status byte!   this is the beginning of a midi message!
				messagemidi[midibyte] = data
				midibyte += 1
			midibyte=0
			messagetype = messagemidi[0] >> 4
			messagechannel = (messagemidi[0] & 15) + 1
			note = messagemidi[1] if len(messagemidi) > 1 else None
			velocity = messagemidi[2] if len(messagemidi) > 2 else None
			if messagetype==8 or messagetype==9 or messagetype==11:
				#self.ThroughDin([messagetype,note,velocity],Sendinfo,trackselected)
				self.ThroughCV([messagetype,note,velocity],Sendinfo,trackselected)
			if messagetype==9:
				self.DinINRec(note)

		else:
			pass

	def DinINRec(self,note):
		#print(note)
		r4.put(note)

	def DINsyncin(self,message):
		if v6.value==0 or 1:
			v6.value=2
		if message==250:
			#print("PLAY")
			v1.value=1
			v6.value=1
		if message==251:
			#print("CONTINUE")
			v1.value=1
			v6.value=1
		if message==252:
			#print("STOP")
			v1.value=0
			v6.value=0


	def DINsyncout(self,message,Syncinfo):
		if Syncinfo[0]==1:
			byte1=bin(int(message))
			byte_chr1 = chr(int(byte1,2))
			if rpi==1:
				ser.write(byte_chr1)
		if message==250:
			print("PLAY")
		if message==251:
			print("PAUSE")
		if message==252:
			print("STOP")


	def ThroughDin(self,Message,Sendinfo,trackselected):
		if Message[0]==9:
			print("send" , Message)
			byte1=bin(int(128+16+Sendinfo[trackselected-1][0]-1))
			byte3=bin(100)
		if Message[0]==8:
			print("stop" , Message)
			byte1=bin(int(128+Sendinfo[trackselected-1][0]-1))
			byte3=bin(0)
		if Message[0]==11:
			print("stop all notes" , Message)
			byte1=bin(int(176+Sendinfo[trackselected-1][0]-1))
			byte3=bin(0)
		byte2 = bin(int(Message[1]))
		byte_chr1 = chr(int(byte1,2))
		byte_chr3 = chr(int(byte3,2))
		byte_chr2 = chr(int(byte2,2))
		ser.write(byte_chr1)
		ser.write(byte_chr2)
		ser.write(byte_chr3)

	def ThroughCV(self,Message,Sendinfo,trackselected):
		print(Message)
		if Sendinfo[trackselected-1][3]>0:
			if Message[0]==0x90:
				if rpi==1:
					bus.write_i2c_block_data(Sendinfo[trackselected][3], Sendinfo[trackselected][4], [0x09, 0xFF])
			if Message[0]==0x80:
				if rpi==1:
					bus.write_i2c_block_data(Sendinfo[trackselected][3], Sendinfo[trackselected][4], [0x05, 0x0])
		if Sendinfo[trackselected-1][1]>0:
			if Message[0]==0x90 and (Message[1]-24)>0 and (Message[1]-24)<96 :
				a,b=divmod(4096*(Message[1]-24)/15/12+4096/15*Sendinfo[trackselected][5],256)
				if rpi==1:
					bus.write_i2c_block_data(Sendinfo[trackselected][1], Sendinfo[trackselected][2], [a, b])




class Listen3():


	def starting(self,s1,s2,s3,s4):
		portopened=0
		if rpi==1:
			midi_in = rtmidi.MidiIn()

		while 1:
			while s1.empty() is False:
				Sendinfo=s1.get()
				#if rpi==0:print(('Sendinfo', Sendinfo))
			while s2.empty() is False:
				trackselected=s2.get()
				if rpi==0:print(('trackselected', trackselected))
			while s3.empty() is False:
				Syncinfo=s3.get()
				#if rpi==0:print(('Syncinfo', Syncinfo))
			if rpi==1 and Syncinfo[4]==1:
				available_ports = midiout.get_ports()
				if len(available_ports)==2 and portopened==0:
					midi_in = rtmidi.MidiIn()
					midi_in.open_port(1)
					portopened=1
				elif len(available_ports)==2 and portopened==1:
					midi_in.close_port()
					portopened=0
					del midi_in
					print('deleted port')	
			if Syncinfo[4]==0:
				try:
					del midi_in
				except:
					pass
				portopened=0		
			if rpi==1 and portopened==1:
				self.MIDIusbIn(Sendinfo,trackselected,midi_in,Syncinfo)
			time.sleep(0.001)


	def MIDIusbIn(self,Sendinfo,trackselected,midi_in,Syncinfo):
		if rpi==1:
			try:
				message= midi_in.get_message()
				if message:
					#self.ThroughCV(message[0],Sendinfo,trackselected)
					self.USBrec(message[0])
					#print(message)
					self.USBsyncin(message[0])
					#self.USBsync(message[0],Syncinfo) #pour plus tard
			except:
				print("midi_in unknown")

	def USBsyncin(self,message):
		if v6.value==0 or 1:
			v6.value=2
		if message[0]==250:
			#print("PLAY")
			v1.value=1
			v6.value=1
		if message[0]==251:
			#print("CONTINUE")
			v1.value=1
			v6.value=1
		if message[0]==252:
			#print("STOP")
			v1.value=0
			v6.value=0


	def USBrec(self,message):
		if 144 <= message[0] <= 159:
			s4.put(message[1])

	def USBsync(self,message,Syncinfo):
		if Syncinfo[1]==1:
			if message[0]==250: #play
				print("play")
				v1.value=1
			if message[0]==252: #stop
				v1.value=2
			if message[0]==251: #continue
				v1.value=2
		print(message)


	def ThroughCV(self,Message,Sendinfo,trackselected):
		if Sendinfo[trackselected-1][3]>0:
			if Message[0]==144:
				if rpi==1:
					bus.write_i2c_block_data(Sendinfo[trackselected][3], Sendinfo[trackselected][4], [0x09, 0xFF])
			if Message[0]==128:
				if rpi==1:
					bus.write_i2c_block_data(Sendinfo[trackselected][3], Sendinfo[trackselected][4], [0x05, 0x0])
		if Sendinfo[trackselected-1][1]>0:
			if Message[0]==144 and (Message[1]-24)>0 and (Message[1]-24)<96 :
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

# [Channel 1, Channel 2..] => [[step 1],[step 2],[step 3],...  ] => [[note, status, length],[note, status, length],..]
sequencepool_0=[[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],
[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]]

sequencepool3=sequencepool_0

#print(sequencepool3)

#print(sequencepool3[1])
# [Midi channel, Pitch Dac N, Pitch Ch N, Gate Dac N, Gate Ch N, Pitch offeset]
Sendinfo=numpy.full((100,7),0)
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
recordingON=0



# size of the loops of each tracks
loopsize=numpy.full(100,64)
loopsize=loopsize.tolist()
playing=0

buttonpushed="b000"
buttonpushedsong="b000"
if rpi==1:
	with open('/home/pi/Desktop2/UIP/param.json') as f:
		paramcf1 = json.load(f)
	with open('/home/pi/Desktop2/UIP/savedseq.json') as s:
		saved = json.load(s)
	with open("/home/pi/Desktop2/UIP/licence.json") as l:
		licence=json.load(l)
else:
	with open('param.json') as f:
		paramcf1 = json.load(f)
	with open('savedseq.json') as s:
		saved = json.load(s)
	with open("licence.json") as l:
		licence=json.load(l)	
version=licence["licence"][0]["version"]
print("CFM1 Version: " + str(version))

paramcalc=ParamScreen()
Sendinfo=paramcalc.convert()

#[din sync,usb sync,clock ppq,usb ppq,usb in (1) or out (0)]
Syncinfo=[0,0,0,0,0]
Syncinfo=paramcalc.convertsync()

midiout = rtmidi.MidiOut()
#midiout = 0

def outsmp(v1,v2,v3,v4,v5,v6,q1,q2,q3,q4,q5,q6):
	ti=Timing()
	ti.Timer(v1,v2,v3,v4,v5,v6,q1,q2,q3,q4,q5,q6)

#v1: playing ; v2: count ; v3: song size ; v4: BPM
#q1:sequencepool ; q2: loopsize ; q3: song ; q4: Sendinfo

v1=multiprocessing.Value('i',1)
v1.value=0
v2=multiprocessing.Value('i',1)
v3=multiprocessing.Value('i',1)
v3.value=16*4*16
v4=multiprocessing.Value('i',1)
v4.value=BPM
v5=multiprocessing.Value('i',1)
v5.value=trackselected
v6=multiprocessing.Value('i',1)
v6.value=2

q1=multiprocessing.Queue()
q1.put(sequencepool2)
q2=multiprocessing.Queue()
q2.put(loopsize)
q3=multiprocessing.Queue()
q3.put(song)
q4=multiprocessing.Queue()
q4.put(Sendinfo)
q5=multiprocessing.Queue()
q5.put(Syncinfo)
q6=multiprocessing.Queue()
#q6.put(sequencepool3)



def insmp(w1,w2):
	listen=Listen()
	listen.starting(w1,w2)

w1=multiprocessing.Value('i',1)
w1.value=0
w2=multiprocessing.Value('i',1)
w2.value=0


def insmp2(r1,r2,r3,r4):
	listen2=Listen2()
	listen2.starting(r1,r2,r3,r4)

r1=multiprocessing.Queue()
r1.put(Sendinfo)
r2=multiprocessing.Queue()
r2.put(trackselected)
r3=multiprocessing.Queue()
r3.put(Syncinfo)
r4=multiprocessing.Queue()

def insmp3(s1,s2,s3,s4):
	listen3=Listen3()
	listen3.starting(s1,s2,s3,s4)

s1=multiprocessing.Queue()
s1.put(Sendinfo)
s2=multiprocessing.Queue()
s2.put(trackselected)
s3=multiprocessing.Queue()
s3.put(Syncinfo)
s4=multiprocessing.Queue()

p=multiprocessing.Process(target=outsmp,args=(v1,v2,v3,v4,v5,v6,q1,q2,q3,q4,q5,q6))
p.start()
pq=multiprocessing.Process(target=insmp,args=(w1,w2))
pq.start()
pq2=multiprocessing.Process(target=insmp2,args=(r1,r2,r3,r4))
pq2.start()
pq3=multiprocessing.Process(target=insmp3,args=(s1,s2,s3,s4))
pq3.start()

try:
	seq=SequencerApp()
	seq.run()
finally:
	if rpi==1:
		GPIO.cleanup()
	print("cleaned")