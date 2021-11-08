import os
import threading
import numpy as np
import cv2
from PIL import Image as im
import mmcv

video_path_1 = "./drive-download-20211105T195818Z-001/1.mp4"
video_path_2 = "./drive-download-20211105T195818Z-001/2.mp4"
video_path_3 = "./drive-download-20211105T195818Z-001/3.mp4"
video_path_4 = "./drive-download-20211105T195818Z-001/4.mp4"
assert os.path.isfile(video_path_1)
assert os.path.isfile(video_path_2)
assert os.path.isfile(video_path_3)
assert os.path.isfile(video_path_4)


class MyThread (threading.Thread):
    maxRetries = 20
    frame_no = []
    img1 = []
    count = 0
    def __init__(self, thread_id, name, video_url, thread_lock):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.video_url = video_url
        self.thread_lock = thread_lock
        MyThread.frame_no=[]

    def run(self):
        print("Starting " + self.name)
        window_name = self.name
        #cv2.namedWindow(window_name)
        video = cv2.VideoCapture(self.video_url)
        c = 0
        while True:
            # self.thread_lock.acquire()  # These didn't seem necessary
            got_a_frame, image = video.read()
            if got_a_frame:
                #global frame_no
                MyThread.frame_no.append(image)
            videos = np.stack(MyThread.frame_no, axis=0)
            #print(videos[1].shape)
            # self.thread_lock.release()
            if not got_a_frame:  # error on video source or last frame finished
                break
            c +=1
            try:

                if len(MyThread.frame_no)==4 or len(MyThread.frame_no)%4==0:
                    if(MyThread.frame_no[MyThread.count].shape[0]==0):
                        MyThread.frame_no[MyThread.count] = np.zeros((1920,1080)) 
                    print(MyThread.frame_no[MyThread.count].shape[0])
                    if(MyThread.frame_no[MyThread.count+1].shape[0]==0):
                        MyThread.frame_no[MyThread.count+1] = np.zeros((1920,1080))
                    if(MyThread.frame_no[MyThread.count+2].shape[0]==0):
                        MyThread.frame_no[MyThread.count+2] = np.zeros((1920,1080))
                    if(MyThread.frame_no[MyThread.count+3].shape[0]==0):
                        MyThread.frame_no[MyThread.count+3] = np.zeros((1920,1080))
                    img_tile = self.concat_vh([[MyThread.frame_no[MyThread.count],MyThread.frame_no[MyThread.count+1]],
                                        [MyThread.frame_no[MyThread.count+2], MyThread.frame_no[MyThread.count+3]]])
                    MyThread.img1 = img_tile
                    MyThread.img1 = cv2.resize(MyThread.img1, (1920,1080))
                    MyThread.count +=4
                    thread_lock1 = threading.Lock()
                    thread5 = MergeThread(5, "Thread 5", MyThread.img1, thread_lock1)
                    thread5.start()
                    #print("yes")
                    #cv2.imwrite(os.path.join("Demo/","result{}.png".format(c)),MyThread.img1)
            #cv2.imshow(window_name, image)
            #print('yes')
            except Exception as exp:
                print(exp)
            key = cv2.waitKey(50)
            if key == 27:
                break
            print(MyThread.img1)
            #data = im.fromarray(MyThread.img1)

            # saving the final output 
            # as a PNG file
            #data.save('gfg_dummy_pic.png', "PNG")
            
        #cv2.destroyWindow(window_name)
        print(self.name + " Exiting")
    def concat_vh(self, list_2d):
    
      # return final image
        return cv2.vconcat([cv2.hconcat(list_h) 
                        for list_h in list_2d])

class MergeThread (threading.Thread):
    maxRetries = 0
    frame_no = []
    def __init__(self, thread_id, name, video_url, thread_lock):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.video_url = video_url
        self.thread_lock = thread_lock
        MergeThread.frame_no=[]
        MergeThread.maxRetries = 0

    def run(self):
        print("Starting " + self.name)
        MergeThread.maxRetries+=1
        #cv2.imwrite(os.path.join("Demo/","result{}.png".format(MergeThread.maxRetries)),self.video_url)
        cv2.imwrite("frame%d.jpg" % MergeThread.maxRetries , self.video_url)
        print("image saved")
        print(MergeThread.maxRetries)

def main():
    thread_lock = threading.Lock()
    thread1 = MyThread(1, "Thread 1", video_path_1, thread_lock)
    thread2 = MyThread(2, "Thread 2", video_path_2, thread_lock)
    thread3 = MyThread(3, "Thread 3", video_path_3, thread_lock)
    thread4 = MyThread(4, "Thread 4", video_path_4, thread_lock)
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    print("Exiting Main Thread")
    

if __name__ == '__main__':
    main()
