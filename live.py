from imageai.Detection import VideoObjectDetection
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

# import serial
import serial
arduino = serial.Serial('/dev/cu.usbmodem1411', 115200, timeout=.1)

personX = 0
personY = 0
trackAc = 8
adjmag = 10


execution_path = os.getcwd()
color_index = {'bus': 'red', 'handbag': 'steelblue', 'giraffe': 'orange', 'spoon': 'gray', 'cup': 'yellow', 'chair': 'green', 'elephant': 'pink', 'truck': 'indigo', 'motorcycle': 'azure', 'refrigerator': 'gold', 'keyboard': 'violet', 'cow': 'magenta', 'mouse': 'crimson', 'sports ball': 'raspberry', 'horse': 'maroon', 'cat': 'orchid', 'boat': 'slateblue', 'hot dog': 'navy', 'apple': 'cobalt', 'parking meter': 'aliceblue', 'sandwich': 'skyblue', 'skis': 'deepskyblue', 'microwave': 'peacock', 'knife': 'cadetblue', 'baseball bat': 'cyan', 'oven': 'lightcyan', 'carrot': 'coldgrey', 'scissors': 'seagreen', 'sheep': 'deepgreen', 'toothbrush': 'cobaltgreen', 'fire hydrant': 'limegreen', 'remote': 'forestgreen', 'bicycle': 'olivedrab', 'toilet': 'ivory', 'tv': 'khaki', 'skateboard': 'palegoldenrod', 'train': 'cornsilk', 'zebra': 'wheat', 'tie': 'burlywood', 'orange': 'melon', 'bird': 'bisque',
               'dining table': 'chocolate', 'hair drier': 'sandybrown', 'cell phone': 'sienna', 'sink': 'coral', 'bench': 'salmon', 'bottle': 'brown', 'car': 'silver', 'bowl': 'maroon', 'tennis racket': 'palevilotered', 'airplane': 'lavenderblush', 'pizza': 'hotpink', 'umbrella': 'deeppink', 'bear': 'plum', 'fork': 'purple', 'laptop': 'indigo', 'vase': 'mediumpurple', 'baseball glove': 'slateblue', 'traffic light': 'mediumblue', 'bed': 'navy', 'broccoli': 'royalblue', 'backpack': 'slategray', 'snowboard': 'skyblue', 'kite': 'cadetblue', 'teddy bear': 'peacock', 'clock': 'lightcyan', 'wine glass': 'teal', 'frisbee': 'aquamarine', 'donut': 'mincream', 'suitcase': 'seagreen', 'dog': 'springgreen', 'banana': 'emeraldgreen', 'person': 'honeydew', 'surfboard': 'palegreen', 'cake': 'sapgreen', 'book': 'lawngreen', 'potted plant': 'greenyellow', 'toaster': 'ivory', 'stop sign': 'beige', 'couch': 'khaki'}
resized = False

camera = cv2.VideoCapture(1)

detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
# detector.setModelTypeAsTinyYOLOv3()
# detector.setModelPath(os.path.join(execution_path , "yolo.h5"))
detector.setModelPath(os.path.join(execution_path, "yolo.h5"))
# detector.loadModel()
detector.loadModel(detection_speed="fastest")

currentPitch = 0
currentYaw = 0
arduino.write((str(currentPitch)+','+str(currentYaw)+'.').encode("ascii"))

def translate(sensor_val, in_from, in_to, out_from, out_to):
    out_range = out_to - out_from
    in_range = in_to - in_from
    in_val = sensor_val - in_from
    val=(float(in_val)/in_range)*out_range
    out_val = out_from+val
    return int(round(out_val))





def trackppl(w, h, coords, ta):
    global currentYaw, currentPitch
    # print(((w / ta) + ((w - (w - (w / ta))) / 2))) //960
    if (coords[2]-coords[0] < w-(2*(w/ta))):

        if (coords[0] <= (w / ta)):
            print("LEFT!")
            if (currentYaw < 135): currentYaw += translate(coords[0], 0, (w / ta), adjmag, 1)
            print("magnitude: "+str(translate(coords[0], 0, (w / ta), adjmag, 1)))
            print("sending to "+(str(currentPitch) + ',' + str(currentYaw) + '.'))
            arduino.write((str(currentPitch) + ',' + str(currentYaw) + '.').encode("ascii"))
            
        if (coords[2] > (w - (w / ta))):
            print("RIGHT!")
            if (currentYaw > -135): currentYaw -= translate(coords[2], (w - (w / ta)), w, 1, adjmag)
            print("magnitude: "+str(translate(coords[2], (w - (w / ta)), w, 1, adjmag)))
            print("sending to "+(str(currentPitch) + ',' + str(currentYaw) + '.'))
            arduino.write((str(currentPitch) + ',' + str(currentYaw) + '.').encode("ascii"))
    else:
        print("objects too close!")






    # if (coords[3]-coords[1] < h-(1*(h/ta))):

    if (coords[1] <= (h / ta)):
        print("UP!")
        if (currentPitch < 90): currentPitch += translate(coords[1], 0, (h / ta), adjmag, 1)
        print("magnitude: "+str(translate(coords[1], 0, (h / ta), adjmag, 1)))
        print("sending to "+(str(currentPitch) + ',' + str(currentYaw) + '.'))
        arduino.write((str(currentPitch) + ',' + str(currentYaw) + '.').encode("ascii"))
        
    if (coords[1] >= 3*(h / ta)):
        print("DOWN!")
        if (currentPitch > -90): currentPitch -= translate(coords[1], (h / ta), w, 1, adjmag)
        print("magnitude: "+str(translate(coords[1], (h / ta), h, 1, adjmag)))
        print("sending to "+(str(currentPitch) + ',' + str(currentYaw) + '.'))
        arduino.write((str(currentPitch) + ',' + str(currentYaw) + '.').encode("ascii"))
    # else:
        # print("objects too close!")







    return


def forFrame(frame_number, output_array, output_count, returned_frame):
    # print("FOR FRAME " , frame_number)

    print("Output for each object : ", output_array, "\n\n")
    asf = False
    for object in output_array:

        # print(object['name'])
        # print(object['box_points'])
        
        if (object['name'] == 'person'):
            value = object['box_points']
            print("FOUND PERSON")
            print("PERSON AT: " + str(value))
            # personX = (lastpoints[2] - lastpoints[0]) / 2
            # personY = (lastpoints[3] - lastpoints[1]) / 2
            print("\n")

            width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
            # print(width)
            # print(height)
            trackppl(width, height, value, trackAc)

        # for key, value in object.items():
        #     # if (key == 'box_points'):
        #     #     lastpoints = value
        #     if (key == 'name' and value == 'person'):
        #         asf = True

        #     if (asf and key == 'box_points'):
        #         # lastpoints = value

        #         print("FOUND PERSON")
        #         print("PERSON AT: " + str(value))
        #         # personX = (lastpoints[2] - lastpoints[0]) / 2
        #         # personY = (lastpoints[3] - lastpoints[1]) / 2
        #         print("\n")
 
        #         width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        #         height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #         print(width)
        #         print(height)
        #         trackppl(width, height, value, trackAc)
        #         asf = False






        # lastpoints = (0)

    # for eachItem in output_count:
    #     print(output_array[eachItem])
    # print("Output count for unique objects : ", output_count)
    # print("------------END OF A FRAME --------------")

    # img = cv2.cvtColor(returned_frame,cv2.COLOR_RGB2BGR)
    # cv2.imshow('Video', img)

    # cv2.imshow('Video', camera.read())
    # plt.show(returned_frame)
    plt.clf()

    # this_colors = []
    # labels = []
    # sizes = []

    # counter = 0

    # for eachItem in output_count:
    #     counter += 1
    #     labels.append(eachItem + " = " + str(output_count[eachItem]))
    #     sizes.append(output_count[eachItem])
    #     this_colors.append(color_index[eachItem])

    # global resized

    # if (resized == False):
    #     manager = plt.get_current_fig_manager()
    #     manager.resize(1000, 500)
    #     resized = True

    # plt.subplot(1, 2, 1)
    # plt.title("Frame : " + str(frame_number))
    plt.axis("off")
    plt.imshow(cv2.cvtColor(returned_frame, cv2.COLOR_BGR2RGB),
               interpolation="none")

    # plt.subplot(1, 2, 2)
    # plt.title("Analysis: " + str(frame_number))
    # plt.pie(sizes, labels=labels, colors=this_colors, shadow=True, startangle=140, autopct="%1.1f%%")

    plt.pause(0.01)


plt.show()
video_path = detector.detectObjectsFromVideo(camera_input=camera,
                                             output_file_path=os.path.join(execution_path, "camera_detected_video"), frames_per_second=20, log_progress=True, minimum_percentage_probability=30, per_frame_function=forFrame, return_detected_frame=True)

print(video_path)


# camera.release()
# cv2.destroyAllWindows()
