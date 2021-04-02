import time
import subprocess
import datetime
import sound


def time_controller():
    date = datetime.datetime.now()
    if date.minute <= 30:
        start_up_hour = date.hour
        start_up_minute = 30
    else:
        start_up_hour = date.hour + 1
        start_up_minute = 0

    print("{} 時 {} 分に起動します".format(start_up_hour, start_up_minute))
    while True:
        date = datetime.datetime.now()
        if date.minute % 30 == 0:
            break
        time.sleep(10)


def confirm_args():
    while True:
        label = input("引数を入力しますか？[y/N] : ")
        if label == "y" or label == "n":
            break
        else:
            print("[y/N]を入力してください : ")

    if label == "y":
        while True:
            arg = input("引数を入力してください : ")
            label = input("[{}]でよろしいですか？[y/N] : ".format(arg))
            if label == "y":
                break
            else:
                print("[y/N]を入力してください : ")
    else:
        arg = ""

    return arg


def main():
    app_path = input("起動するプログラムのパスを入力してください : ")
    arg = confirm_args()
    print("path : {}".format(app_path + " " + arg))
    time_controller()
    sound.sound()
    try:
        subprocess.Popen(app_path + " " + arg)
    except:
        sound.sound()
        sound.sound()
        sound.sound()
        time.sleep(20)


if __name__ == '__main__':
    main()
