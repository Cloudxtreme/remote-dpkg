#!/usr/bin/env python
import os
import sys
import argparse
import time
from fabric.api import run, env, hide, settings, put, cd

def scenario_cmd(hostname,username,passwd,pckgDir,install):
    cmd_out = []
    tmpstamp = str(int(time.time()))
    with hide('output','running','warnings'), settings(warn_only=True):
    	print "Connecting to host: %s"%(hostname)
        with settings(user=username,host_string=hostname,password=passwd):
        	cmd_out = run('mkdir -p '+pckgDir+tmpstamp)
        	print "Creating directory %s"%(pckgDir+tmpstamp)
        	if cmd_out.return_code == 0:
        		for pkg in install:
        			print "Uploading file %s"%(pkg)
        			put(pkg,pckgDir+tmpstamp)
        		with cd(pckgDir+tmpstamp):
        			print("Installing deb packages...")
        			cmd_out = run('dpkg -i --force-all *.deb')
        		print "DONE"
        	else:
        		print "Could not create directory %s"%(pckgDir+tmpstamp)
    return cmd_out.return_code


# Parse arguments function
def parseArguments():
	parser = argparse.ArgumentParser(description = 'remote-dpkg: remote install deb packages.')
	# Install packages option
	parser.add_argument('-i', '--install',
						help = '-i/--install <packages>',
						type  = str,
						nargs="+",
						required = False)
	# Hostname option
	parser.add_argument('-s', '--server', 
						help = '-s/--server <IP/hostname>',
						type  = str,
						nargs="+",
						required = True)

	# Username option
	parser.add_argument('-u', '--username', 
						help = 'username to connect',
						type  = str,
						required = True)

	# Password option
	parser.add_argument('-p', '--password', 
						help = 'password to connect',
						type  = str,
						required = False)

	# Directory option
	parser.add_argument('-d', '--directory', 
						help = 'remote directory to store deb packages',
						type  = str,
						default = '~/deb-packages',
						required = False)

	return vars(parser.parse_args())

if __name__ == '__main__':
	args = parseArguments()
	hostname = args['server']
	username = args['username']
	password = args['password']
	pckgDir  = args['directory']
	install  = args['install']
	for host in hostname:
		exit_code = scenario_cmd(host,username,password,pckgDir,install)
		if exit_code == 0:
			exit_code = "SUCCESS"
		else:
			exit_code = "UNKNOW:"+str(exit_code)
		print "dpkg tried to install %s on host %s and exited with status %s"%(','.join(install),host,exit_code)
