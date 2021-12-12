import os
import sys
import time
import ctypes
import serial
import picamera
import base64
import plan
import tng

ser = serial.Serial(
				port='/dev/ttyS0',
				baudrate = 115200,
				timeout=1
				)

camera = picamera.PiCamera()
camera.resolution = (430, 140)


			
def runPlanetCNC():
	try:
		# Run
		if tng.API.IsRunning():
			print("Using existing TNG process")
		elif tng.API.IsRunningExt():
			print("Using existing external TNG process")
		else:
			print("starting new TNG process")
			tng.Run()
			
		time.sleep(5)
		tng.API.SetStatusW("Matic Zevnik was here")
	
	except Exception as e:
		print("Exception: ", str(e))
		tng.API.ExitForce()




runPlanetCNC()


while 1:
	
	while ser.in_waiting:
		                      
		rawdata=ser.readline()
		
		
		#clear whole board
		if rawdata[0] == "c":
			#print(rawdata)
			tng.API.Print("I will open file") # dialog show
				tng.API.OpenFnW("/home/pi/PlanetCNC/pobrisi_vse.nc")
				time.sleep(1)
				x = tng.API.GetLineCount()
				tng.API.Print("line count is " + str(x))
				tng.API.Start()
				
				while tng.API.IsIdle() == False:
					time.sleep(1)
		
		#stops (emergency stop)	
		elif rawdata[0] == "s":
			#print(rawdata)
			tng.API.Estop()
			
			
		
		
  ##############################################
################## clean area ####################
  ##############################################
		elif rawdata[0] == "[":
			if rawdata[1] == "1":
				#print(rawdata)
				processeddata = rawdata.replace("1","",1)
				processeddata = processeddata.replace(",","",1)
				processeddata = processeddata.replace(" ","",1)
				processeddata = processeddata.replace("[","",2)
				processeddata = processeddata.replace("]]","")
				processeddata = processeddata + "]"
				#print(processeddata)
				
				dissectdata = list(processeddata.split("[["))
				
				fnew = open("c.nc","w")
				fnew.write("%\nG17 G21 G90\nM04\nG4 P1.5\nM05\n")
				
				for i in dissectdata:			
					i = i.replace("[","")
					i = i.split("], ")
					first= i[0].split(", ")
					
					fnew.write("G0 X"+str(first[0])+" Y"+str(first[1])+"\n")
					fnew.write("M3\nG4 P1\nM05\n")
					
					for j in i:
						if j == i[len(i) - 1]:
							part = j.replace("]","")
							fnew.write("G1 X"+str(part[0])+" Y"+str(part[1])+"\n")
							
						elif j != i[0]:
							part = j.split(", ")
							fnew.write("G1 X"+str(part[0])+" Y"+str(part[1])+"\n")
							
						
					
					fnew.write("M4\nG4 P1.5\nM05\n")
				
				fnew.write("G0 X0 Y0")
				fnew.close()
				print("done")
				
				
				tng.API.Print("I will open file") # dialog show
				tng.API.OpenFnW("/home/pi/PlanetCNC/c.nc")
				time.sleep(1)
				x = tng.API.GetLineCount()
				tng.API.Print("line count is " + str(x))
				tng.API.Start()
				
				while tng.API.IsIdle() == False:
					time.sleep(1)	
  ###############################################
################## send picture ###################
  ###############################################				
			
			
			
		elif rawdata[0] == "p":
			camera.capture('foo.png')
			time.sleep(1)
			with open('foo.png','rb') as image_file:
				base = base64.b64encode(image_file.read())
				#print(base)
				ser.write(base)
				time.sleep(0.05)
				ser.write("*")
				time.sleep(1)
				print ("done")
				
				
			
			
			
			
