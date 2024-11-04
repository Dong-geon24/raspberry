import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
import time

class MotorController(Node):
    def __init__(self):
        super().__init__('motor_controller')

        GPIO.setwarnings(false)

        #set motor pin
        self.L_IN1, self.L_IN2, self.L_PWM1 = 20, 21, 0
        self.L_IN3, self.L_IN4, self.L_PWM2 = 22, 23, 1
        self.R_IN1, self.R_IN2, self.R_PWM1 = 24, 25, 12
        self.R_IN3, self.R_IN4, self.R_PWM2 = 26, 27, 13

        #set GPIO pin mode & options
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.L_IN1, self.L_IN2, self.L_IN3, self.L_IN4, self.R_IN1, self.R_IN2, self.R_IN3, self.R_IN4]. GPIO.OUT)
        GPIO.setup([self.L_PWM1, self.L_PWM2, self.R_PWM1, self.R_PWM2], GPIO.OUT)

        #init
        self.stop_motors()

        #PWN setting
        self.pwm_R1 = GPIO.PWN(self.R_PWM1, 100)
        self.pwm_R2 = GPIO.PWN(self.R_PWM2, 100)
        self.pwm_L1 = GPIO.PWN(self.L_PWM1, 100)
        self.pwm_L2 = GPIO.PWN(self.L_PWM2, 100)
        self.pwm_R1.start(0)
        self.pwm_L1.start(0)
        self.pwm_R2.start(0)
        self.pwm_L2.start(0)
        
        #move forward
        self.move_forward()

        def move_forward(self):
            GPIO.output(self.L_IN1,GPIO,LOW)
            GPIO.output(self.L_IN2,GPIO,HIGH)
            self.pwm_L1.changeDutyCycle(50)

            GPIO.output(self.L_IN3,GPIO,HIGH)
            GPIO.output(self.L_IN4,GPIO,LOW)
            self.pwm_L2.changeDutyCycle(50)

            GPIO.output(self.L_IN1,GPIO,HIGH)
            GPIO.output(self.L_IN2,GPIO,LOW)
            self.pwm_R1.changeDutyCycle(50)

            GPIO.output(self.L_IN3,GPIO,LOW)
            GPIO.output(self.L_IN4,GPIO,HIGH)
            self.pwm_R2.changeDutyCycle(50)

            time.sleep(1)

            self.stop_motors()

        def stop_motors(self):
            GPIO.output(self.L_IN1,GPIO,LOW)
            GPIO.output(self.L_IN2,GPIO,LOW)
            GPIO.output(self.L_IN3,GPIO,LOW)
            GPIO.output(self.L_IN4,GPIO,LOW)
            GPIO.output(self.R_IN1,GPIO,LOW)
            GPIO.output(self.R_IN2,GPIO,LOW)
            GPIO.output(self.R_IN3,GPIO,LOW)
            GPIO.output(self.R_IN4,GPIO,LOW)
            self.pwm_R1.changeDutyCycle(0)
            self.pwm_R2.changeDutyCycle(0)
            self.pwm_L1.changeDutyCycle(0)
            self.pwm_L2.changeDutyCycle(0)

        def destroy_node(self):
            self.stop_motors()
            self.pwm_R1.stop()
            self.pwm_L1.stop()
            self.pwm_R2.stop()
            self.pwm_L2.stop()
            GPIO.cleanup()
            super().destroy_node()

    def main(args=None):
        rclpy.init(args=args)
        motor_controller = MotorController()
        try:
            rclpy.spin(motor_controller)
        except KeyboardInterrupt:
            pass
        finally:
            motor_controller.destroy_node()
            rclpy.shutdown()

    if __name__=='__main__':
        main()
