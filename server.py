# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import time
import RPi.GPIO as gpio
import socket

E1=18
M1=17

def setup():
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)
    gpio.setup(E1,gpio.OUT)
    gpio.setup(M1,gpio.OUT)
    pwm=gpio.PWM(E1,50)
    pwm.start(0)

setup()
HOST = "192.168.0.100" # Server IP or Hostname
PORT = 9900 # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print"Socket created"

#managing error exception
try:
  s.bind((HOST, PORT))
except socket.error:
  print"Bind failed "

s.listen(5)
print"Socket awaiting messages"
(conn, addr) = s.accept()
print"Connected"

# awaiting for message
while True:
  data = conn.recv(1024)
  print"I sent a message back in response to:" + data
  
  # process your message
  if data =='Forward':
    gpio.output(E1,gpio.HIGH)
    gpio.output(M1,gpio.HIGH)
    time.sleep(3)
    reply ='Going forwardâ'
  elif data =='This is important':
    reply ='OK, I have done the important thing you have asked me!'

  #and so on and on untilâ€¦
  elif data =='quit':
    conn.send('Terminating')  
    sys.exit()

  else:
    reply ='Unknown command'

# Sending reply
  conn.send(reply)
conn.close() # Close connections
