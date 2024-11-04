import RPi.GPIO as GPIO                    
import time                                

# GPIO BCM(Broadcom SoC) 핀 번호 설정 
GPIO.setmode(GPIO.BCM)      

TRIG = 14                                 
ECHO = 4                                   

GPIO.setup(TRIG, GPIO.OUT)                  
GPIO.setup(ECHO, GPIO.IN)

# HC-SR04 초음파 센서에서 거리 측정
def getDistance():
    GPIO.output(TRIG, GPIO.LOW)                 
    time.sleep(1)  # 안정화 시간

    GPIO.output(TRIG, GPIO.HIGH)                  
    time.sleep(0.00001)  # 10us 동안 HIGH 신호
    GPIO.output(TRIG, GPIO.LOW)

    # ECHO가 LOW일 때, 펄스 시작 시간 기록
    while GPIO.input(ECHO) == 0:                
        pulse_start = time.time()               

    # ECHO가 HIGH일 때, 펄스 종료 시간 기록
    while GPIO.input(ECHO) == 1:               
        pulse_end = time.time()                 

    # 펄스 지속 시간 계산
    pulse_duration = pulse_end - pulse_start 
    # 펄스 지속 시간을 17150으로 곱하여 거리 계산 (cm 단위)
    distance = pulse_duration * 17150        
    distance = round(distance, 2)  # 소수점 2자리로 반올림
 
    return distance

# 메인 루프
try:
    while True:
        dist = getDistance()  # 거리 측정
        print("Measured Distance = {} cm".format(dist))  # 거리 출력
        time.sleep(1)  # 1초 대기

except KeyboardInterrupt:  # Ctrl+C로 종료 시
    print("Measurement stopped by User")
    GPIO.cleanup()  # GPIO 핀 정리
