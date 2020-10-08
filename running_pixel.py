import cv2
import numpy as np
from PIL import Image

cap = cv2.VideoCapture('stegano-pixel/pixel.avi')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
img = np.zeros((height, width,3))

pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
while cap.isOpened():
    flag, frame = cap.read()
    img = np.add(img, frame)
    if flag:
        # The frame is ready and already captured
        cv2.imshow('video', frame)
        pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        print(str(pos_frame) + " frames")
    else:
        # The next frame is not ready, so we try to read it again
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame - 1)
        print("frame is not ready")
        # It is better to wait for a while for the next frame to be ready
        cv2.waitKey(1000)

    if cv2.waitKey(10) == 27:
        break
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # If the number of captured frames is equal to the total number of frames,
        # we stop
        break


cap.release()
cv2.destroyAllWindows() # destroy all opened windows

super_threshold_indices = img > 128
img[super_threshold_indices] = 255
img1 = Image.fromarray(img.astype(np.uint8), mode='RGB').save('out.png')