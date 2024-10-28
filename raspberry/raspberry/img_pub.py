import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImagePublisher(Node):
    def __init__(self):
        super().__init__("image_publisher")
        self.bridge = CvBridge()
        self.publisher = self.create_publisher(Image,"original_image",10)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.get_logger().error("Failed to open camera")
            rclpy.shutdown()
            return
        self.timer = self.create_timer(0.1,self.publish_image)

    def publish_image(self):
        ret, img = self.cap.read()
        if ret:
            ros_image = self.bridge.cv2_to_imgmsg(img, encoding="bgr8")
            self.publisher.publish(ros_image)
            cv2.imshow('camera',img)
            if cv2.waitKey(1) != -1:
                self.get_logger().info("Exiting...")
                rclpy.shutdown()
        else:
            self.get_logger().error("Failed to capture image")


    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()
    
def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__=="__main__":
    main()