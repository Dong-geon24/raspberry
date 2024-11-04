import RPi.GPIO as GPIO
import time

# GPIO 핀 모드를 BCM으로 설정 (라즈베리파이 핀 번호와 일치)
GPIO.setmode(GPIO.BCM)

# 트리거와 에코 핀 설정
TRIG_PIN = 14  # 초음파 송신 핀
ECHO_PIN = 4  # 초음파 수신 핀
GPIO.setup(TRIG_PIN, GPIO.OUT)  # 트리거 핀을 출력으로 설정
GPIO.setup(ECHO_PIN, GPIO.IN)   # 에코 핀을 입력으로 설정

try:
    while True:
        # 초음파 펄스 전송 시작
        print('aaaaa')
        GPIO.output(TRIG_PIN, True)  # 트리거 핀을 HIGH로 설정
        time.sleep(0.00001)          # 10μs 동안 신호 전송
        GPIO.output(TRIG_PIN, False) # 트리거 핀을 LOW로 설정하여 신호 종료

        # 에코 핀에서 신호 수신 시작
        while GPIO.input(ECHO_PIN) == 0:  # 에코가 LOW일 때, 펄스 시작 시간 기록
            start = time.time()

        while GPIO.input(ECHO_PIN) == 1:  # 에코가 HIGH일 때, 펄스 종료 시간 기록
            end = time.time()

        # 펄스 지속 시간 계산
        duration = end - start

        # 거리 계산 (cm)
        distance = (duration * 34300) / 2  # 초음파의 속도를 이용하여 거리 계산
        print("Distance:", distance, "cm") # 거리 출력

        time.sleep(1)  # 1초 간격으로 거리 측정

except KeyboardInterrupt:  # Ctrl+C로 종료 시
    GPIO.cleanup()         # GPIO 설정 초기화
