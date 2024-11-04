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

# 서보 모터 핀 설정
servoPin1 = 5
GPIO.setup(servoPin1, GPIO.OUT)

def servoPulse(servoPin, myangle):
    pulsewidth = (myangle * 11) + 500  # 펄스 너비 계산
    GPIO.output(servoPin, GPIO.HIGH)
    time.sleep(pulsewidth / 1000000.0)
    GPIO.output(servoPin, GPIO.LOW)
    time.sleep(20.0 / 1000 - pulsewidth / 1000000.0)  # 20ms 사이클


def distance():
    # 10us의 트리거 신호
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)  # 10us
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()  # 프로그램이 실행된 시간 기록
    stop_time = time.time()    # 프로그램이 실행된 시간 기록

    while GPIO.input(GPIO_ECHO) == 0:  # 초음파 파가 발사되었음을 나타냄
        start_time = time.time()  # 발사 시간 기록

    while GPIO.input(GPIO_ECHO) == 1:  # 초음파 반사파가 수신되었음을 나타냄
        stop_time = time.time()  # 수신 시간 기록

    time_elapsed = stop_time - start_time  # 송신과 수신 사이의 시간 차이
    distance = (time_elapsed * 34000) / 2  # 거리 계산 (cm 단위) (시간 * 속도는 거리 초음파의 속도 34000cm/s)
    return distance  # 계산된 거리 반환

    # 초음파 센서 핀 설정
GPIO_TRIGGER = 14
GPIO_ECHO = 4
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


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

# 초음파 센서 핀 설정
GPIO_TRIGGER = 14
GPIO_ECHO = 4
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


#==========================
#듀티사이클(speed) 0~100 -> 모터 돌아가는 속도 기본적으로 50설정
#==========================
def drive(angle):
    for g in range(0, 50):
    servoPulse(servoPin1, 90)

try:
    while True:
        dist = distance()
        print(f"Measured Distance = {dist:.1f} cm")
        time.sleep(0.01)

        if angle == 0: and dist >15 :#15cm 이상일때 직진
            pwm_L1.ChangeDutyCycle(50) 
            pwm_L2.ChangeDutyCycle(50) 
            pwm_R1.ChangeDutyCycle(50) 
            pwm_R2.ChangeDutyCycle(50) 
        else:  # 장애물이 15cm 이하일 때
            car_stop()
            # 왼쪽 거리 측정
            for i in range(0, 50):
                servoPulse(servoPin1, 180)
                time.sleep(0.1)
            left_distance = distance()
            time.sleep(0.2)

            # 오른쪽 거리 측정
            for j in range(0, 50):
                servoPulse(servoPin1, 0)
                time.sleep(0.1)

            right_distance = distance()
            time.sleep(0.2)


            elif angle < 0: and left_distance > right_distance: #좌회전
                pwm_L1.ChangeDutyCycle(20) 
                pwm_L2.ChangeDutyCycle(50) 
                pwm_R1.ChangeDutyCycle(80) 
                pwm_R2.ChangeDutyCycle(50)         
                time.sleep(0.6)
            else: #우회전
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

