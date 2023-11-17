import subprocess

class UsbVideoDevice():
    def __init__(self):
        self.__deviceList = []

        try:
            cmd = 'ls -la /dev/v4l/by-id'
            res = subprocess.check_output(cmd.split())
            by_id = res.decode()
        except:
            return

        try:
            cmd = 'ls -la /dev/v4l/by-path'
            res = subprocess.check_output(cmd.split())
            by_path = res.decode()
        except:
            return

        # デバイス名取得
        deviceNames = {}
        for line in by_id.split('\n'):
            if('../../video' in line):
                tmp = self.__split(line, ' ')
                if( "" in tmp):
                    tmp.remove("")
                name = tmp[8]
                deviceId = tmp[10].replace('../../video','')
                deviceNames[deviceId]=name

        # ポート番号取得
        for line in by_path.split('\n'):
            if('usb-0' in line):
                tmp = self.__split(line, '0-usb-0:1.')
                tmp = self.__split(tmp[1], ':')
                port = int(tmp[0])
                tmp = self.__split(tmp[1], '../../video')
                deviceId = int(tmp[1])
                if deviceId % 2 == 0:
                    name = deviceNames[str(deviceId)]
                    self.__deviceList.append((deviceId , port, name))

    def __split(self, str, val):
        tmp = str.split(val)
        if('' in tmp):
            tmp.remove('')
        return tmp

    # 認識しているVideoデバイスの一覧を表示する
    def disp(self):
        for (deviceId, port, name) in self.__deviceList:
            print("/dev/video{} port:{} {}".format(deviceId, port, name))

    # ポート番号（1..）を指定してVideoIDを取得する
    def getVideoId(self, port):
        for (deviceId, p, _) in self.__deviceList:
            if(p == port):
                return deviceId
        return -1

    # 最大ポート番号を取得する
    def getMaxPort(self):
        maxPort = 0
        for (_, port, _) in self.__deviceList:
            if port > maxPort:
                maxPort = port
        return maxPort

if __name__ == "__main__":
    import cv2

    usbVideoDevice = UsbVideoDevice()

    print("情報一覧")
    usbVideoDevice.disp()

    # 最大ポート番号を取得
    maxPort = usbVideoDevice.getMaxPort()

    print("\nポート番号とデバイスIDの一覧")
    for port in range(maxPort):
        deviceId = usbVideoDevice.getVideoId(port + 1)
        if (deviceId != -1):
            print("PORT:{} /dev/video{}".format(port + 1, deviceId))
