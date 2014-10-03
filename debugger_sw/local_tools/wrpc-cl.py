#! /usr/bin/python

import serial
import sys
import time
import re
from select import select
import os.path


tintchar=0.01
eol=0xd
  
def load_ram():
	global file
	f = open(file, 'r')
	word = "write"
	print "Start"
	for line in f:
		if word in line:
			segmentLine = line.split(" ")
			call(["sudo", "../fmc-delay/fine-delay-sw/spec-sw/tools/specmem", set_adr(segmentLine[1]), hex(int(segmentLine[2], 16))])
	print "Done!!!"
	f.close()
		

def _exec (cmd, port):
	global tintchar
	global eol
	
	for c in cmd:
		port.write(c)
		time.sleep(tintchar)
	port.write(chr(eol))

def _resp (port):
	global tintchar
	
	time.sleep(10*tintchar)
	nbytes = port.inWaiting()
	return(port.read(nbytes))

def execute_cmd(cmd, port):
	_exec (cmd, port)
	return _resp (port)


def set_lm32_state(state, reg, port):
	global tintchar
	global eol
	
	if state == "reset":
		ctrl = " 0x1"
	elif state == "run":
		ctrl = " 0x0"
	else:
		sys.exit(-1)
	cmd = "dbgmem "+reg+ctrl+"deadbee"
	return(execute_cmd(cmd, port))
	


def process_files (old,new):
	
	token="write"
	
	if new != None:
		fold = open(old)
		fnew = open(new)
		mold = {}
		mnew = {}
		
		for line in fold:
			line = line.lower()
			splitted_line = re.split(token+"\s",line)
			splitted_line = re.split("\s",splitted_line[1])
			mold[splitted_line[0]]=splitted_line[1]
			
		for line in fnew:
			line = line.lower()
			splitted_line = re.split(token+"\s",line)
			splitted_line = re.split("\s",splitted_line[1])
			mnew[splitted_line[0]]=splitted_line[1]
			
		fold.close()
		fnew.close()
		
		mf = {}
		
		for k in mold:
			if mnew.has_key(k) and mold[k] != mnew[k]:
				mf[k] = mnew[k]
			for k in mnew:
				if not mold.has_key(k):
					mf[k] = mnew[k]
		cmd = []
		lmf = mf.items()
		lmf.sort()
		for k in lmf:
			cmd.append(token+" "+k[0]+" "+k[1])
	else:
		mold = {}
		fold = open(old)
		for line in fold:
			line = line.lower()
			splitted_line = re.split(token+"\s",line)
			splitted_line = re.split("\s",splitted_line[1])
			mold[splitted_line[0]]=splitted_line[1]
			
		fold.close()
		
		cmd = []
		lmf = mold.items()
		lmf.sort()
		
		for k in lmf:
			cmd.append(token+" "+k[0]+" "+k[1])
		
	return cmd

#os.path.isfile(fname)
def execute_program(dev,ram_file,pbaudrate=115200,pparity=serial.PARITY_NONE,pstopbits=serial.STOPBITS_ONE,pbytesize=serial.EIGHTBITS,pxonxoff=False,prtscts=False,pdsrdtr=False):
	global tintchar
	global eol
	port = serial.Serial(dev, baudrate=pbaudrate,parity=pparity,stopbits=pstopbits,bytesize=pbytesize,xonxoff=pxonxoff,rtscts=prtscts,dsrdtr=pdsrdtr)
	cmd = "dbgmem -i"
	response=execute_cmd(cmd, port)
	rsp = response.split(chr(eol))
	for elem in rsp:
		if "WB4-BlockRAM" in elem:
			index = elem.split(":")
			ram = index[0]
		elif "WR-Periph-Syscon" in elem:
			index = elem.split(" - ")
			syscon = index[1]
			
	response = set_lm32_state("reset", syscon, port)
	cmd = "dbgmem -i"+ram
	response=execute_cmd(cmd, port)
	#try:
	#	f = open(ram_file, 'r')
	#except IOError, e:
	#	print e.errno
	#	print e
	word = "write"
	print "Start"
	for line in ram_file:
		if word in line:
			segmentLine = line.split("', '")
			segmentLine = segmentLine[0].split(" ")
			cmd="dbgmem 0x"+segmentLine[1]+" 0x"+segmentLine[2]
			print cmd
			#_exec(cmd, port)
	print "Done!!!"
	cmd = "dbgmem -b0x0"
	response=execute_cmd(cmd, port)
	response = set_lm32_state("run", syscon, port)
	print response

print
print "**********************************************************"
print "*     Soft-Micro Debugger Re-programming Application     *"
print "*                           by                           *"
print "*                      Jose Jimenez                      *"
print "*                                                        *"
print "*                                                        *"
print "*                      - WARNING -                       *"
print "*     This is a beta version, please report bugs to:     *"
print "*            <fmc-delay-1ns-8cha-sa@ohwr.org>            *"
print "**********************************************************"
print
print

if len(sys.argv) != 3:
	print "ERROR: use ",sys.argv[0]," <USB device>"
	print "ERROR: use ",sys.argv[0]," <USB device> <program_file>"
	print
	sys.exit(-1)
	
dev = sys.argv[1]
ram_file = sys.argv[2]
print  str(sys.argv)
#execute_program(dev, ram_file)
#print process_files(ram_file, None)
execute_program(dev, process_files(ram_file, None))
