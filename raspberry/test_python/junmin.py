import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 14
ECHO = 4

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(1)
    
    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start
    
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    
    return distance

if __name__ == '__main__':
  try:
    while True:
      distance_value = get_distance()
      print(distance_value)
      if distance_value > 2 and distance_value < 400:      
          print ("%.2f cm" %distance_value)
          
      else:
          print ("Out Of Range")                         

  except KeyboardInterrupt:
    print ("Keyboard Interrupt")
    GPIO.cleanup()