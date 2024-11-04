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
    # 트리거 펄스 전송 (20us)
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00002)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    # Echo가 시작될 때까지 대기 (타임아웃 1초 설정)
    timeout_start = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()
        if time.time() - timeout_start > 3:  # 1초 이상 대기하면 타임아웃
            print("Echo 핀이 LOW 상태로 유지됨. 물체가 너무 멀리 있을 수 있습니다.")
            return None

    # Echo가 돌아올 때까지 대기 (타임아웃 1초 설정)
    timeout_start = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()
        if time.time() - timeout_start > 3:  # 1초 이상 대기하면 타임아웃
            print("Echo 핀이 HIGH 상태로 유지됨. 물체가 너무 가깝거나 신호가 손실되었습니다.")
            return None

    # 초음파가 발사되고 돌아올 때까지 걸린 시간 계산
    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34000) / 2  # 거리 계산 (단위: cm)

    return round(distance, 2)  # 계산된 거리 반환 (소수점 2자리로 반올림)


if __name__ == '__main__':
    try:
        while True:
            dist = distance()  # 거리 측정
            if dist is not None:
                print("Measured Distance = {:.2f} cm".format(dist))  # 거리 출력
            else:
                print("Distance measurement failed.")
            time.sleep(0.1)  # 0.1초 대기

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
