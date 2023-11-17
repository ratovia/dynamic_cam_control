import cv2
from UsbVideoDevice import UsbVideoDevice

class DynamicCamControl:
    CAMERA_DEVICE_PORT = 4

    def __init__(self, usbVideoDevice: UsbVideoDevice):
        self.cap = None
        self.is_camera_active = False
        self.usbVideoDevice = usbVideoDevice

    def start_camera(self, camera_index):
        if not self.is_camera_active:
            self.cap = cv2.VideoCapture(camera_index)
            self.is_camera_active = True

    def stop_camera(self):
        if self.is_camera_active:
            self.cap.release()
            self.is_camera_active = False

    def run(self):
          self.start_camera(self.usbVideoDevice.getVideoId(self.CAMERA_DEVICE_PORT))

          while True:
              if self.is_camera_active:
                  ret, frame = self.cap.read()
                  if ret:
                      cv2.imshow(f'Camera', frame)

              if cv2.waitKey(1) & 0xFF == ord('q'):
                  break

          self.stop_camera()
          cv2.destroyAllWindows()

if __name__ == "__main__":
    usbVideoDevice = UsbVideoDevice()

    print("情報一覧")
    usbVideoDevice.disp()

    maxPort = usbVideoDevice.getMaxPort()
    print("\nポート番号とデバイスIDの一覧")
    for port in range(maxPort):
        deviceId = usbVideoDevice.getVideoId(port + 1)
        if (deviceId != -1):
            print("PORT:{} /dev/video{}".format(port + 1, deviceId))

    app = DynamicCamControl(usbVideoDevice)
    app.run()
