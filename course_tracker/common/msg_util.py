import os, sys, string
    
def msg(m):
    print m
    
def dashes():
    msg(40*'-')

def msgt(s):
    dashes()
    msg(s)
    dashes()

def msgu(s):
    dashes()
    msg(s)
    
def msgx(s):
    msgt('Error: %s' % s)
    msg(s)
    dashes()
    msg('exiting..')
    sys.exit(0)
 

