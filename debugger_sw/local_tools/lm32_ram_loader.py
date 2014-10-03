#!/usr/bin/python

import os
import struct
import ctypes
import sys, getopt

from subprocess import call


lm32_ram_base_addr = "0x40000"
file = "../fd_std.ram"

def set_adr (offset):
	global lm32_ram_base_addr
	tmp = int(lm32_ram_base_addr,16) + int(offset, 16)*4
	return hex(tmp)


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

def main(argv):
	global lm32_ram_base_addr
	global file
	try:
		opts, args = getopt.getopt(argv,"b:dh",["base address="])
	except getopt.GetoptError:
		print 'lm32_ram_loader.py -b <base_address> <file>'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-b", "--base"):
			lm32_ram_base_addr = arg
		elif opt in ("-d", "--dbg"):
			file="../dbg.ram"
		else:
			print 'lm32_ram_loader.py -b <base_address> <file>'
	print 'base ', lm32_ram_base_addr, ' file ', file
	load_ram()

if __name__ == "__main__":
   main(sys.argv[1:])
