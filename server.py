#-*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import time
import RPi.GPIO as gpio
import socket


#set pins
E1=18
M1=17
E2=19
M2=20
#set modes
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(E1,gpio.OUT)
gpio.setup(M1,gpio.OUT)
gpio.setup(E2,gpio.OUT)
gpio.setup(M2,gpio.OUT)
pwm_left=gpio.PWM(E2,50)
pwm_right=gpio.PWM(E1,50)
pwm_left.start(0)
pwm_right.start(0)

#define directions
def forward():
  gpio.output(E1,gpio.HIGH)
  gpio.output(M1,gpio.HIGH)
  gpio.output(E2,gpio.HIGH)
  gpio.output(M2,gpio.LOW)

def left():
  gpio.output(E1,gpio.HIGH)
  gpio.output(M1,gpio.HIGH)
  gpio.output(E2,gpio.HIGH)
  gpio.output(M2,gpio.HIGH)

def right():
  gpio.output(E1,gpio.HIGH)
  gpio.output(M1,gpio.LOW)
  gpio.output(E2,gpio.HIGH)
  gpio.output(M2,gpio.LOW)

def stop():
  gpio.output(E1,gpio.LOW)
  gpio.output(M1,gpio.LOW)
  gpio.output(E2,gpio.LOW)
  gpio.output(M2,gpio.HIGH)

#to set dutycycles
def dutycycle(val):
  pwm_left.ChangeDutyCycle(val)
  pwm_right.ChangeDutyCycle(val)


#for tcp connection
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
  data = conn.recv(1024).decode("ascii")
  print"I sent a message back in response to:" + data
  
  # process your message
  if data =='forward':
    dutycycle(30)
    forward()
    time.sleep(3)
    reply ='COOL! there are no obstacles I am going FORWARDâ'
  elif data =='right':
    dutycycle(20)
    right()
    time.sleep(3)
    stop()
    reply ='OOPS! Move away from that thing on the Left! RIGHT RIGHT!'
  
  elif data == 'left':
    dutycycle(20)
    left()
    time.sleep(3)
    stop()
    reply = 'OK, I can see an obstacle on the right! So I am turning LEFT!'

  #and so on and on until quit¦
  elif data =='quit':
    dutycycle(0)
    stop()
    conn.send('Terminating')  
    sys.exit()

  else:
    reply ='Unknown command'

# Sending reply
  conn.send(reply)

gpio.cleanup()
conn.close() # Close connections
