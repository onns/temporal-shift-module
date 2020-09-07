# Code for "TSM: Temporal Shift Module for Efficient Video Understanding"
# arXiv:1811.08383
# Ji Lin*, Chuang Gan, Song Han
# {jilin, songhan}@mit.edu, ganchuang@csail.mit.edu

import os
import threading
import sys
import time

NUM_THREADS = 4
VIDEO_ROOT = 'E:\\ss2\\video'         # Downloaded webm videos
FRAME_ROOT = 'E:\\ss2\\frame'  # Directory for extracted frames


def split_l(l, n):
    """Yield successive n-sized chunks from l."""
    temp_list = []
    for i in range(0, len(l), n):
        temp_list.append(l[i:i + n])
    return temp_list


def extract(video, tmpl='%06d.jpg'):
    # os.system(f'ffmpeg -i {VIDEO_ROOT}/{video} -vf -threads 1 -vf scale=-1:256 -q:v 0 '
    #           f'{FRAME_ROOT}/{video[:-5]}/{tmpl}')
    cmd = 'D:\\ffmpeg\\bin\\ffmpeg.exe -i \"{}/{}\" -threads 1 -vf scale=-1:256 -q:v 0 \"{}/{}/%06d.jpg\"'.format(VIDEO_ROOT, video,
                                                                                             FRAME_ROOT, video[:-5])
    os.system(cmd)


def target(video_list):
    for video in video_list:
        os.makedirs(os.path.join(FRAME_ROOT, video[:-5]))
        extract(video)


if __name__ == '__main__':
    if not os.path.exists(VIDEO_ROOT):
        raise ValueError('Please download videos and set VIDEO_ROOT variable.')
    if not os.path.exists(FRAME_ROOT):
        os.makedirs(FRAME_ROOT)

    # n = int(sys.argv[1])
    n = 10
    for j in range(11042,11043):
        t = 20 
        n = j*t + 1
        # del video_list
        video_list = []
        for i in range(n,n+t):
            if i > 220847:
                break
            video_list.append(os.path.join(str(i)+'.webm'))
        # video_list = os.listdir(VIDEO_ROOT)
        print(video_list)
        # print(split(video_list, NUM_THREADS))
        splits = split_l(video_list, NUM_THREADS)
        # print(splits)
        old = time.time()

        # del threads
        threads = []
        for i, split_m in enumerate(splits):
            # print(split)
            thread = threading.Thread(target=target, args=(split_m,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        new = time.time()

        print(old)
        print(new)
        # time.sleep(8)