'''from time import sleep
while 1 :
    code=str(input())
    #print(code)
import lcd
lcd.lcd_init()
lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
lcd.lcd_string("Raspberry Pi", 2)
lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
lcd.lcd_string("Model B+", 2)
lcd.GPIO.cleanup()
'''
#!/usr/bin/env python3
from time import sleep
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
import lcd
lcd.lcd_init()
GPIO.setwarnings(False)
buzzer = 17
servoPIN = 27
button_1=2
button_2=3
items = {"19H51A0398":{"name":"rice packet","price":1200,"weight":160},
         "19H51A0397":{"name":"oil packet","price":800,"weight":150}}

def display(data_1,data_2):
    line1=str(data_1)
    line2=str(data_2)
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    lcd.lcd_string(line1, 2)
    lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
    lcd.lcd_string(line2, 2)
try:
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    # Create an object hx which represents your real hx711 chip
    # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
    hx = HX711(dout_pin=5, pd_sck_pin=6)
    # measure tare and save the value as offset for current channel
    # and gain selected. That means channel A and gain 128
    err = hx.zero()
    GPIO.setup(servoPIN, GPIO.OUT)
    GPIO.setup(buzzer, GPIO.OUT)
    p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
    p.start(2.5) # Initialization
    # check if successful
    if err:
        raise ValueError('Tare is unsuccessful.')

    reading = hx.get_raw_data_mean()
    if reading:  # always check if you get correct value or only False
        # now the value is close to 0
        print('Data subtracted by offset but still not converted to units:',
              reading)
    else:
        print('invalid data', reading)

    # In order to calculate the conversion ratio to some units, in my case I want grams,
    # you must have known weight.
    input('Put known weight on the scale and then press Enter')
    reading = hx.get_data_mean()
    if reading:
        print('Mean value from HX711 subtracted by offset:', reading)
        known_weight_grams = input(
            'Write how many grams it was and press Enter: ')
        try:
            value = float(known_weight_grams)
            print(value, 'grams')
        except ValueError:
            print('Expected integer or float and I have got:',
                  known_weight_grams)

        # set scale ratio for particular channel and gain which is
        # used to calculate the conversion to units. Required argument is only
        # scale ratio. Without arguments 'channel' and 'gain_A' it sets
        # the ratio for current channel and gain.
        ratio = reading / value  # calculate the ratio for channel A and gain 128
        hx.set_scale_ratio(ratio)  # set ratio for current channel
        print(ratio)
        print('Ratio is set.')
    else:
        raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:', reading)

    # Read data several times and return mean value
    # subtracted by offset and converted by scale ratio to
    # desired units. In my case in grams.
    print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
    input('Press Enter to begin reading')
    print('Current weight on the scale in grams is: ')
    item_count=0
    scode=""
    rcode=""
    load_weight=0
    total_price=0
    pl=0
    product_weight=0
    display("MAILCHIMP","Welcome's you")
    GPIO.setup(button_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #sleep(1)
    #lcd.GPIO.cleanup()
    while True:
        product_load=int(hx.get_weight_mean(20))
        sleep(1)
        pl=int(product_load)
        load_weight=load_weight+pl
        #hx.get_weight_mean(20)
        p.ChangeDutyCycle(12.5)
        sleep(1)
        if not GPIO.input(button_1) :
            display("Scan the product"," Bar Code ")
            sleep(1)
            scode=str(input())
            print(pl, 'g')
            display("Total Trolley"," weight : ")
            sleep(1)
            display(str(pl)+" grams"," ")
            sleep(1)
            for key in items.keys():
                
                
                if key==scode:
                
                    while True:
            
                        product_load=int(hx.get_weight_mean(20))
                        pl=int(product_load)
                        sleep(1)
                        p.ChangeDutyCycle(7.5)
                        sleep(2)
            
                        if pl>load_weight:
                
                            product_weight=pl-load_weight
                            if product_weight > items[key]["weight"]:
                                while True:
                                    product_load=int(hx.get_weight_mean(20))
                                    product_weight=product_load-load_weight
                                    sleep(1)
                                
                                
                                    if product_weight<=items[key]["weight"]:
                                        GPIO.output(buzzer,GPIO.LOW)
                                        sleep(0.5)
                                        display("product weight :",str(product_weight)+" grams")
                                        sleep(2)
                                        p.ChangeDutyCycle(12.5)
                                        sleep(2)
                                        break
                                    else:
                                        GPIO.output(buzzer,GPIO.LOW)
                                        sleep(0.5)
                                        GPIO.output(buzzer,GPIO.HIGH)
                                        #sleep(0.5)
                                        display("Arlert..!","!!...BEEP...!!")
                                        sleep(1)
                                        GPIO.output(buzzer,GPIO.LOW)
                                        sleep(0.5)
                                        GPIO.output(buzzer,GPIO.HIGH)
                                        #sleep(0.5)
                                        display("You have added","Extra Items")
                                        sleep(1)
                            if product_weight <= items[key]["weight"]:
                                GPIO.output(buzzer,GPIO.LOW)
                                sleep(0.5)
                                display("product weight :",str(product_weight)+" grams")
                                sleep(2)
                                p.ChangeDutyCycle(12.5)
                                sleep(2)
                                break
                        else:
                            display("put the product","in the troley")
                    item_count=item_count+1
                    total_price=total_price+items[key]['price']
                    display("Item count : ",item_count)
                    sleep(2)
                    display(items[key]['name']+": ",str(items[key]['price'])+" /-")
                    sleep(2)
                    display("Total cost :",str(total_price)+" /-")
                    sleep(2)
                    scode=""
        if not GPIO.input(button_2) :
            p.ChangeDutyCycle(7.5)
            sleep(1)
            display("Remove the product", "from Trolley ")
            sleep(2)
            display("Scan the product"," Bar Code ")
            sleep(1)
            rcode=str(input())
            print(pl, 'g')
            display("Total Trolley"," weight : ")
            sleep(1)
            display(str(pl)+" grams"," ")
            sleep(1)
            for key in items.keys():
                if key==rcode:
                    
                    while True :
                        product_load=int(hx.get_weight_mean(20))
                        sleep(1)
                        removed_item_load = load_weight-product_load
                        if removed_item_load > items[key]["weight"]:
                        
                            GPIO.output(buzzer,GPIO.LOW)
                                        
                            sleep(0.5)
                            GPIO.output(buzzer,GPIO.HIGH)
                                        #sleep(0.5)
                            display("Arlert..!","!!...BEEP...!!")
                            sleep(1)
                            GPIO.output(buzzer,GPIO.LOW)
                            sleep(0.5)
                            GPIO.output(buzzer,GPIO.HIGH)
                                        #sleep(0.5)
                            display("You have Removed","Extra Items")
                            sleep(1)
                        elif removed_item_load <=items[key]["weight"]:
                            
                            
                            GPIO.output(buzzer,GPIO.LOW)
                            sleep(0.5)
                            display("product weight :",str(removed_item_load)+" grams")
                            sleep(2)
                            p.ChangeDutyCycle(12.5)
                            sleep(2)
                            break
                    item_count=item_count-1
                    total_price=total_price-items[key]['price']
                    display("Item count : ",item_count)
                    sleep(2)
                    display(items[key]['name']+": ",str(items[key]['price'])+" /-")
                    sleep(2)
                    display("Total cost :",str(total_price)+" /-")
                    sleep(2)
                    rcode=""
                    display("Removed "," Sucessfully...!")
                    sleep(2)
                    
            
            
        else:
            
            display("To Add a ","Product")
            sleep(2)
            display(" Press Button"," ONE")
            sleep(2)
            display("To Remove a ","Product")
            sleep(2)
            display("Press Button"," TWO")
            sleep(2)
        
        '''
        if scode.null():
            print("i")
        
        display("put the product","in the troley")
        sleep(1)''
        
        t=1
        
        print(pl, 'g')
        display("Total Trolley"," weight : ")
        sleep(1)
        display(str(pl)+" grams"," ")
        sleep(1)
     
        
        for key in items.keys():
            
            if key==scode:
                
                while True:
            
                    product_load=int(hx.get_weight_mean(20))
                    pl=int(product_load)
                    sleep(1)
                    p.ChangeDutyCycle(7.5)
                    sleep(2)
            
                    if pl>load_weight:
                
                        product_weight=pl-load_weight
                        if product_weight > items[key]["weight"]:
                            while True:
                                product_load=int(hx.get_weight_mean(20))
                                product_weight=product_load-load_weight
                                sleep(1)
                                
                                
                                if product_weight<=items[key]["weight"]:
                                    GPIO.output(buzzer,GPIO.LOW)
                                    sleep(0.5)
                                    display("product weight :",str(product_weight)+" grams")
                                    sleep(2)
                                    p.ChangeDutyCycle(12.5)
                                    sleep(2)
                                    break
                                else:
                                    GPIO.output(buzzer,GPIO.LOW)
                                    sleep(0.5)
                                    GPIO.output(buzzer,GPIO.HIGH)
                                    #sleep(0.5)
                                    display("Arlert..!","!!...BEEP...!!")
                                    sleep(1)
                                    GPIO.output(buzzer,GPIO.LOW)
                                    sleep(0.5)
                                    GPIO.output(buzzer,GPIO.HIGH)
                                    #sleep(0.5)
                                    display("You have added","Extra Items")
                                    sleep(1)
                                    
                                    
                        if product_weight <= items[key]["weight"]:
                            GPIO.output(buzzer,GPIO.LOW)
                            sleep(0.5)
                            display("product weight :",str(product_weight)+" grams")
                            sleep(2)
                            p.ChangeDutyCycle(12.5)
                            sleep(2)
                            break
                    else:
                        display("put the product","in the troley")
                item_count=item_count+1
                total_price=total_price+items[key]['price']
                display("Item count : ",item_count)
                sleep(2)
                display(items[key]['name']+": ",str(items[key]['price'])+" /-")
                sleep(2)
                display("Total cost :",str(total_price)+" /-")
                sleep(2)
                scode=""
                
            
        
        lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
        lcd.lcd_string("Raspberry Pi", 2)
        lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
        lcd.lcd_string("Model B+", 2)
        '''
        

except (KeyboardInterrupt, SystemExit):
    print('Bye :)')

finally:
    p.stop()
    GPIO.cleanup()



