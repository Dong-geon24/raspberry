import RPi.GPIO as GPIO
import time
import numpy as np
import cv2
import math

# 모터 핀 설정
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

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # BCM 번호 사용

# 모터 핀 출력 모드 설정
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

# 초기화: 모든 핀 LOW
GPIO.output(L_IN1, GPIO.LOW)
GPIO.output(L_IN2, GPIO.LOW)
GPIO.output(L_IN3, GPIO.LOW)
GPIO.output(L_IN4, GPIO.LOW)
GPIO.output(R_IN1, GPIO.LOW)
GPIO.output(R_IN2, GPIO.LOW)
GPIO.output(R_IN3, GPIO.LOW)
GPIO.output(R_IN4, GPIO.LOW)

# PWM 설정 및 시작
pwm_R1 = GPIO.PWM(R_PWM1, 100)
pwm_R2 = GPIO.PWM(R_PWM2, 100)
pwm_L1 = GPIO.PWM(L_PWM1, 100)
pwm_L2 = GPIO.PWM(L_PWM2, 100)

pwm_R1.start(0)
pwm_L1.start(0)
pwm_R2.start(0)
pwm_L2.start(0)

# 모터 제어 함수
def drive(angle, speed):
    # 방향 제어
    if angle > 0:  # 오른쪽으로 회전
        GPIO.output(L_IN1, GPIO.LOW)
        GPIO.output(L_IN2, GPIO.HIGH)
        GPIO.output(R_IN1, GPIO.HIGH)
        GPIO.output(R_IN2, GPIO.LOW)
        
        GPIO.output(L_IN3, GPIO.HIGH)
        GPIO.output(L_IN4, GPIO.LOW)
        GPIO.output(R_IN3, GPIO.LOW)
        GPIO.output(R_IN4, GPIO.HIGH)
    elif angle < 0:  # 왼쪽으로 회전
        GPIO.output(L_IN1, GPIO.LOW)
        GPIO.output(L_IN2, GPIO.HIGH)
        GPIO.output(R_IN1, GPIO.HIGH)
        GPIO.output(R_IN2, GPIO.LOW)
        
        GPIO.output(L_IN3, GPIO.HIGH)
        GPIO.output(L_IN4, GPIO.LOW)
        GPIO.output(R_IN3, GPIO.LOW)
        GPIO.output(R_IN4, GPIO.HIGH)
    else:  # 직진
        GPIO.output(L_IN1, GPIO.LOW)
        GPIO.output(L_IN2, GPIO.HIGH)
        GPIO.output(R_IN1, GPIO.HIGH)
        GPIO.output(R_IN2, GPIO.LOW)
        
        GPIO.output(L_IN3, GPIO.HIGH)
        GPIO.output(L_IN4, GPIO.LOW)
        GPIO.output(R_IN3, GPIO.LOW)
        GPIO.output(R_IN4, GPIO.HIGH)

    # 속도 제어
    pwm_L1.ChangeDutyCycle(speed)
    pwm_R1.ChangeDutyCycle(speed)
    pwm_L2.ChangeDutyCycle(speed)
    pwm_R2.ChangeDutyCycle(speed)

# 라인 추적 함수
def process_image(frame):
    height, width = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur_gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edge_img = cv2.Canny(blur_gray, 60, 70)

    # 관심 영역 설정
    roi = edge_img[int(height / 2):height, :]
    lines = cv2.HoughLinesP(roi, 1, math.pi / 180, 30, minLineLength=30, maxLineGap=10)

    # 라인이 감지되지 않으면 직진 유지
    if lines is None:
        return 0, 20

    left_lines, right_lines = [], []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2 - y1) / (x2 - x1) if x2 != x1 else 0
        if slope < 0:
            left_lines.append(line)
        elif slope > 0:
            right_lines.append(line)

    # 양쪽 라인의 중심을 계산
    if left_lines:
        left_x1 = np.mean([line[0][0] for line in left_lines]).astype(int)
    else:
        left_x1 = 0

    if right_lines:
        right_x1 = np.mean([line[0][2] for line in right_lines]).astype(int)
    else:
        right_x1 = width

    # 좌우 차선을 기준으로 중심 계산
    center = (left_x1 + right_x1) // 2
    deviation = center - (width // 2)
    angle = deviation / (width // 2) * 25  # -25 ~ 25도 각도로 변환

    return angle, 20  # 기본 속도는 20으로 설정

# 메인 루프
cap = cv2.VideoCapture(0)  # 카메라에서 영상 읽기
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        angle, speed = process_image(frame)
        drive(angle, speed)
        print("Angle:", angle, "Speed:", speed)

        # 시각화
        #cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

finally:
    pwm_R1.stop()
    pwm_L1.stop()
    pwm_R2.stop()
    pwm_L2.stop()
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()

