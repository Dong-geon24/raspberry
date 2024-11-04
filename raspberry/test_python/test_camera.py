import cv2

cap = cv2.VideoCapture(0)
fourcc = cap.get(cv2.CAP_PROP_FOURCC)
print(fourcc)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


if not cap.isOpened():
    print('camera fuck')
    exit()

while True:
    ret,frame = cap.read()
    if not ret:
        print('frame fuck')
        break

    cv2.imshow('camera frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()