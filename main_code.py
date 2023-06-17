#!/usr/bin/env python
import telepot
import RPi.GPIO as GPIO
import time
import datetime
from telepot.loop import MessageLoop
RUNNING = True

green = 27
red = 17
blue = 22
PIR = 23
buzz = 18

GPIO.setwarnings(False)  
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN)
GPIO.setup(buzz, GPIO.OUT, initial = GPIO.HIGH) 
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

Freq = 100
RED = GPIO.PWM(red, Freq)
GREEN = GPIO.PWM(green, Freq)
BLUE = GPIO.PWM(blue, Freq)
motion = 0
motionNew = 0

time.sleep(5)
try:
    def handle(msg):
        global telegramText
        global chat_id
  
        chat_id = msg['chat']['id']
        telegramText = msg['text']
  
        print('Message received from ' + str(chat_id))
  
        if telegramText == '/start':
            bot.sendMessage(chat_id, 'Welcome to House Notification')

        while True:
            main()
    
           

    bot = telepot.Bot('892272816:AAGK1MEFFXrClsrIkPxlhtRpZ3WMgEaL2Zs')
    bot.message_loop(handle)        

    def main():
        
        global chat_id
        global motion 
        global motionNew
    
        if GPIO.input(PIR) == 1:
            print("Motion Detected")
            GPIO.output(buzz,GPIO.LOW)

            RED.start(100)
            GREEN.start(100)
            BLUE.start(100)
            
            motion = 1
            if motionNew != motion:
                motionNew = motion
                sendNotification(motion)
            time.sleep(0.1)    
            
        elif GPIO.input(PIR) == 0:
            GPIO.output(buzz,GPIO.HIGH)

            RED.start(0)
            GREEN.start(0)
            BLUE.start(0)
            
            print("No motion detected")
            motion = 0
            if motionNew != motion:
                sendNotification(motion)
                motionNew = motion
            time.sleep(0.1)

    def sendNotification(motion):   

        global chat_id
    
        if motion == 1:
            bot.sendMessage(chat_id, 'Someone is at your front door')
            bot.sendMessage(chat_id, str(datetime.datetime.now()))



    
except KeyboardInterrupt:
    RUNNING = False
    GPIO.cleanup()
