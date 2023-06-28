import cv2
import os

cam = cv2.VideoCapture(0)

cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("press space to take a photo", 500, 300)

img_counter = 0

while True:
    # 要求拍攝者輸入名字
    name = input("Please enter your name: ")
    image_path = "faces/{}.png".format(name)

    # 檢查目錄是否存在，若存在則請求重新輸入名字
    if os.path.exists(image_path):
        print("Name already exists. Please enter a new name！")
        continue

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("press space to take a photo", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            cv2.imwrite(image_path, frame)
            print("{} written!".format(image_path))
            break

    # 清理資源並關閉視窗
    cam.release()
    cv2.destroyAllWindows()
    break

