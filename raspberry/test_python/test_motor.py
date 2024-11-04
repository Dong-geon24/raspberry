import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)


#==========================
# 모터 핀 설정
#==========================
L_IN1 = 20
L_IN2 = 21
L_PWM1 = 0

L_IN3 = 22
L_IN4 = 23
L_PWM2 = 1

R_IN1 = 24
R_IN2 = 25
R_PWM1 = 12

R_IN3 = 26
R_IN4 = 27
R_PWM2 = 13

GPIO.setmode(GPIO.BCM)  # BCM 번호 사용


#==========================
# 모터 핀 출력 모드 설정
#==========================
GPIO.setup(L_IN1, GPIO.OUT)
GPIO.setup(L_IN2, GPIO.OUT)
GPIO.setup(L_PWM1, GPIO.OUT)
GPIO.setup(L_IN3, GPIO.OUT)
GPIO.setup(L_IN4, GPIO.OUT)
GPIO.setup(L_PWM2, GPIO.OUT)
GPIO.setup(R_IN1, GPIO.OUT)
GPIO.setup(R_IN2, GPIO.OUT)
GPIO.setup(R_PWM1, GPIO.OUT)
GPIO.setup(R_IN3, GPIO.OUT)
GPIO.setup(R_IN4, GPIO.OUT)
GPIO.setup(R_PWM2, GPIO.OUT)


#==========================
# 초기화: 모든 핀 LOW
#LOW는 정지상태
#==========================
GPIO.output(L_IN1, GPIO.LOW) 
GPIO.output(L_IN2, GPIO.LOW)
GPIO.output(L_IN3, GPIO.LOW)
GPIO.output(L_IN4, GPIO.LOW)
GPIO.output(R_IN1, GPIO.LOW)
GPIO.output(R_IN2, GPIO.LOW)
GPIO.output(R_IN3, GPIO.LOW)
GPIO.output(R_IN4, GPIO.LOW)


#==========================
# PWM 설정 및 시작
#주파수 100Hz
#==========================
pwm_R1 = GPIO.PWM(R_PWM1, 100) #우측상단
pwm_R2 = GPIO.PWM(R_PWM2, 100) #우측하단
pwm_L1 = GPIO.PWM(L_PWM1, 100) #좌측상단
pwm_L2 = GPIO.PWM(L_PWM2, 100) #좌측하단

pwm_R1.start(0) #모터 회전 x (듀티사이클)
pwm_L1.start(0)
pwm_R2.start(0)
pwm_L2.start(0)


#==========================
#high = 전압 공급
#low = 전압 없음
#==========================
def motor():
    GPIO.output(L_IN1, GPIO.LOW)    # 상단 왼쪽 앞으로
    GPIO.output(L_IN2, GPIO.HIGH)
    GPIO.output(L_IN3, GPIO.HIGH)   # 하단 왼쪽 앞으로
    GPIO.output(L_IN4, GPIO.LOW)
    GPIO.output(R_IN1, GPIO.HIGH)   # 상단 오른쪽 앞으로
    GPIO.output(R_IN2, GPIO.LOW)
    GPIO.output(R_IN3, GPIO.LOW)    # 하단 오른쪽 앞으로
    GPIO.output(R_IN4, GPIO.HIGH)


#==========================
#듀티사이클(speed) 0~100 -> 모터 돌아가는 속도 기본적으로 50설정
#==========================
def drive(angle):
    if angle == 0: #직진
        pwm_L1.ChangeDutyCycle(50) 
        pwm_L2.ChangeDutyCycle(50) 
        pwm_R1.ChangeDutyCycle(50) 
        pwm_R2.ChangeDutyCycle(50) 

    elif angle < 0: #좌회전
        pwm_L1.ChangeDutyCycle(20) 
        pwm_L2.ChangeDutyCycle(50) 
        pwm_R1.ChangeDutyCycle(50) 
        pwm_R2.ChangeDutyCycle(50)         
    
    elif angle > 0: #우회전
        pwm_L1.ChangeDutyCycle(80)
        pwm_L2.ChangeDutyCycle(50)
        pwm_R1.ChangeDutyCycle(20)
        pwm_R2.ChangeDutyCycle(50)


#==========================
# 모터 제어 루프
#==========================
try:
    while True:
        motor()
        drive(1)

except KeyboardInterrupt: #control + c
    pass


#==========================
# PWM 및 GPIO 정리 -> 프로그램 종료 시 모터 중지
#==========================
finally:
    pwm_R1.stop()
    pwm_L1.stop()
    pwm_R2.stop()
    pwm_L2.stop()
    time.sleep(1)
    GPIO.cleanup()

