import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# GPIO 핀 정의
GPIO_TRIGGER = 14
GPIO_ECHO = 4

# GPIO 모드 설정 (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # 트리거 펄스 전송 (10us)
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)  # 10마이크로초 동안 HIGH
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()  # 시작 시간을 기록
    stop_time = time.time()   # 종료 시간을 기록

    # Echo가 시작될 때까지 대기
    while GPIO.input(GPIO_ECHO) == 0:
        #print("start")
        start_time = time.time()  # 초음파가 발사된 시간을 기록

    # Echo가 돌아올 때까지 대기
    while GPIO.input(GPIO_ECHO) == 1:
        #print("final")
        stop_time = time.time()  # 초음파가 수신된 시간을 기록

    # 초음파가 발사되고 돌아올 때까지 걸린 시간 계산
    time_elapsed = stop_time - start_time
    print("disxdfs")
    distance = (time_elapsed * 34000) / 2  # 거리 계산 (단위: cm)
    print("dis")

    return distance  # 계산된 거리 반환

if __name__ == '__main__':  # 프로그램 시작
    try:
        print("ASDf")
        while True:
            print("AAAAA")
            dist = distance()  # 거리 측정
            print('bbbbb')
            print("Measured Distance = {:.2f} cm".format(dist))  # 소수점 두 자리까지 거리 출력
            time.sleep(0.1)  # 0.1초 대기

    # CTRL + C로 프로그램 종료 시
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
