from pyrplidar import PyRPlidar
import jetson.inference
import jetson.utils
import argparse
import sys
from pynput.mouse import Listener
import numpy as np
import time

def on_click(x, y, button, pressed):
    global coordX,coordY
    if pressed:
        coordX = x
        coordY = y

        xDist_toCenter=coordX-705
        newX_Angle = 272.5 + 180 / np.pi * np.arctan(xDist_toCenter/(640*np.sqrt(3)))

        actual_distance = 0
        scanned_angle = 0

        for scan in scan_generator():
            if (scan.quality!=0):
                actual_distance= scan.distance/1000
                scanned_angle = (((scan.angle*-1) + 360) * np.pi/180)
                if((scanned_angle < np.pi*252/180) and (scanned_angle > np.pi*302/180)):
                    if newX_Angle == scanned_angle:
                        print(actual_distance)
                    
def setupLidar():
    lidar = PyRPlidar()

    lidar.connect(port="/dev/ttyUSB0", baudrate=256000, timeout=3)
        # Linux   : "/dev/ttyUSB0"
        # MacOS   : "/dev/cu.SLAB_USBtoUART"
        # Windows : "COM5
    
    return lidar

def startLidar(lidar):
    lidar.set_motor_pwm(1000)
    time.sleep(2)
    scan_generator = lidar.start_scan_express(4)


def stopLidar(lidar):
    lidar.stop()
    lidar.set_motor_pwm(0)
    lidar.disconnect()

parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
                                jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]

try:
    opt = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)

net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv+is_headless)
tempX = 0
tempY = 0
slidar = setupLidar()

with Listener(on_click=on_click) as listener:
    startLidar(lidar)   
    while True:
        img = input.Capture()

        detections = net.Detect(img, overlay=opt.overlay)

        output.Render(img)

        output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))
		
        if(tempX != coordX or tempY != coordY):
            print(coordX, coordY)
		
        tempX = coordX
        tempY = coordY

        for i in detections:
            if tempX-66 > i.Left and tempX-66 < i.Right and tempY-53 >i.Top and tempY-53 < i.Bottom:
                print("{0} .class => {1},{2},{3},{4} Mouse => {5},{6}".format(i.ClassID,i.Left,i.Top,i.Right,i.Bottom,coordX,coordY))
                break

        if not input.IsStreaming() or not output.IsStreaming():
            stopLidar(lidar)
            break
    listener.join()
