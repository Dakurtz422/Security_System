import os
import cv2
import glob
import argparse
import time as tm

from time import sleep
from datetime import time
from play_it import PlayIt
from send_slack_photos import send_it


ap = argparse.ArgumentParser()
ap.add_argument("-n", '--nightmode', action='store_true', help="Switch to Night Mode")
args = vars(ap.parse_args())

save_path = "captured"
file_names = []
number_of_photos_to_send = 5
print_counter = 0


def check_image(img1, img2, img3):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    gray3 = cv2.cvtColor(img3, cv2.COLOR_RGB2GRAY)

    diff1 = cv2.absdiff(gray1, gray2)
    diff2 = cv2.absdiff(gray2, gray3)

    diff_and = cv2.bitwise_and(diff1, diff2)

    _, diff_wb = cv2.threshold(diff_and, 30, 255, cv2.THRESH_BINARY)

    diff = cv2.medianBlur(diff_wb, 5)
    return diff


def get_image(cam):
    try:
        img = cam.read()[1]
        img = cv2.resize(img, (600, 400))
        return img

    except Exception as e:
        print("[ERR] No Camera found")


def time_in_range(now_time):
    if now_time >= time(23,00) or now_time <= time(6,00):
        return True

    else:
        return False


def convert_time():
    now = tm.strftime("%-H:%-M", tm.localtime(tm.time()))
    now_tuple = now.split(":")
    for x in now_tuple:
        yield x


def check_time():
    tt = []
    for x in convert_time():
        tt.append(x)
    hours = int(tt[0])
    minutes = int(tt[1])
    now = time(hours, minutes)
    checked_time = time_in_range(now)
    return checked_time


def check_parser():
    return True if args["nightmode"] else False


def camera_capture():
    count2 = 0
    print("[INFO] Initializing the Camera" )
    cam = cv2.VideoCapture(0)
    sleep(3)
    img1 = img2 = img3 = get_image(cam)
    th = 300
    num = 0
    while True:
        if cv2.waitKey(1) == 13: return False

        if check_parser() == True:
            check_it = check_time()
            if check_it != True:
                print("[INFO] It's is Morning, breaking the Loop")
                break

        diff = check_image(img1, img2, img3)
        cnt = cv2.countNonZero(diff)
        if cnt > th:
            #sleep(0.2)
            print("[WARM] Captured Moves")
            cv2.imshow('Captured', img3)
            cv2.imwrite(save_path + str(num) + ".jpg", img3)

            stnum = str(num)
            stnum = (stnum + ".jpg")
            file_names.append(stnum)
            count2 += 1

            if count2 % number_of_photos_to_send == 0 and check_parser() == False:
                send_it(file_names)
                file_names.clear()
                count2 = 0

            if check_parser() == True and num % 3 == 0:
                try:
                    PlayIt("1")

                except Exception as e:
                    print(e)

            num += 1

        else:
            cv2.imshow("I'm watching You", diff)

        img1, img2, img3 = (img2, img3, get_image(cam))
    cam.release()
    sleep(5)


###############################################################

if check_parser() == True:
    print("[INFO] Starting a Camera in Night Mode")
else:
    print("[INFO] Starting a Camera in 24/7 Mode")


if not os.path.isdir(save_path):
    print("[INFO] Creating a Directory for a Photos")
    os.makedirs(save_path)

else:
    for file in glob.glob(f"{save_path}/*.jpg"):
        try:
            print("[INFO] removing %s" % file)
            os.remove(file)
        except Exception as e:
            print(e)


while True:
    if check_parser() == True:
        if __name__=="__main__":
            timerange = check_time()
            if timerange != True:
                if print_counter != 1:
                    print("[INFO] Your are in Night Mode\n       Wating for the Night to Start")
                    print_counter = 1
                sleep(60)
                continue

            else:
                x = camera_capture()
                print_counter = 0
                if x == False:
                    print("[INFO] Killed By User")
                    break

    else:
        if __name__=="__main__":
            x = camera_capture()
            if x == False:
                print("[INFO] Killed By User")
                break
