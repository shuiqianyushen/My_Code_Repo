#/bin/env python
#_*_code: UTF-8
#**************************************************************************************
#
#                   description
# Define a function to print python log into file ,combine python log with compiler log
#**************************************************************************************
import sys
def printlog(name,target,config,string,ide='iar'):
	standard_out=sys.stdout
	log_file='log//'+ide+'build.log'
	file_out=open(log_file,'a')
	sys.stdout=file_out
	print '%s--%s[%s]%s' %(name,target,config,string)
	sys.stdout=standard_out
	file_out.close()
