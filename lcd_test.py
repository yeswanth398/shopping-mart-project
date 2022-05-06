'''from time import sleep
import RPi.GPIO as GPIO
import lcd
lcd.lcd_init()
GPIO.setwarnings(False)
def display(data_1,data_2):
    line1=str(data_1)
    line2=str(data_2)
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    lcd.lcd_string(line1, 2)
    lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
    lcd.lcd_string(line2, 2)

display("MAILCHIMP","Welcome's you")
sleep(1)'''
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM) 
button = 2 #Button(2)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    
    if GPIO.input(button) :
        t=1
        print("pressed")
        sleep(1)
    if not GPIO.input(button) :
        t=0
        print(t)