from moviepy.editor import *
clip1 = VideoFileClip("D:\\稳像\\192.168.20.195_01_20210924090204496_11_day100-200.mp4").subclip(0,) #读取视频1.mp4，并截取0-158秒的内容
clip1.write_videofile("D:\\稳像\\test3.mp4")#视频写入2.mp4