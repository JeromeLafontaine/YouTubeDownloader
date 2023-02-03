from pytube import YouTube 
from pytube import Channel
from scrapetube import *
import ffmpeg
import os 
import subprocess
import urllib.request



def get_links(link_path , channel_URL):
    i = 0
    videos = get_channel(channel_URL) #scrapetube
    for video in videos:
        print("link n° " + str(i))
        f = open(link_path+str(i//20)+".txt" , "a")
        f.write("http://www.youtube.com/watch?v="+video['videoId'])
        f.write("\n")
        f.close()
        i += 1
    print('Links Collected!')


def download_video_and_audio(link_path , SAVE_PATH , video_names_path , error_path):
    SAVE_PATH_V = SAVE_PATH + '/video'
    SAVE_PATH_A = SAVE_PATH + '/audio'
    SAVE_PATH_T = SAVE_PATH + '/thumbnail'
    check = 0
    f = open(video_names_path, "a")
    f.close()
    f = open(error_path, "a")
    f.close()

    link=open(link_path,'r') 
    for i in link: 
        print("downloading video: " + i)
        try: 
            yt = YouTube(i) 
        except: 
            print("Connection Error")  
        
        try:
            for stream in yt.streams:
                print("video :" + str(stream))
            d_video = yt.streams.get_by_itag(299)
            d_audio = yt.streams.filter(only_audio=True)
            for audio in d_audio:
                print("audio :" + str(audio))
            d_audio = d_audio.get_by_itag(140)
            thumbnail = yt.thumbnail_url
            print(thumbnail)
            urllib.request.urlretrieve(thumbnail, SAVE_PATH_T + '/' + d_video.default_filename[:-4] + '.jpg')
            print("downloading thumbnail: " + SAVE_PATH_T + '/' + d_video.default_filename[:-4] + '.jpg')
        except:
            print("Error during download")
            f = open(error_path, "r")
            if(i not in f.read()):
                f.close()
                f = open(error_path, "a")
                f.write(i)
                f.write("\n")
            f.close()
            d_audio = None
            d_video = None
            check = 1

        checkf = open(video_names_path, "r")
        if(check == 0 and d_video.default_filename[:-4] in checkf.read()):
            print('video already exists')
            check = 1

        if(check == 0):
            f = open(video_names_path, "a")
            f.write(d_video.default_filename[:-4])
            f.write("\n")
            f.close()
            print("adding \" " + d_video.default_filename[:-4] + " \" to the list")
            try: 
                d_video.download(SAVE_PATH_V) 
                d_audio.download(SAVE_PATH_A)
                #print(subprocess.run('ffmpeg -i '+SAVE_PATH_A+'/'+d_video.default_filename[:-4]+'.mp4 "TEST".mp3',shell=True,capture_output=True))
                #print(subprocess.run('ffmpeg -i Videos/audio/VOS PIRES CADEAUX DE NOËL 4.mp4 TEST.mp3',shell=True,capture_output=True))
                ffmpeg.output(ffmpeg.input(SAVE_PATH_A+'/'+d_video.default_filename[:-4]+'.mp4'), SAVE_PATH_A+'/'+d_video.default_filename[:-4]+'.mp3').run()
            except: 
                print("error during download") 
        else:
            check = 0
    link.close()
    print('Download Completed!') 

def merge_video_and_audio(SAVE_PATH , video_names_path):
    check = 0
    video_names = open(video_names_path, "r")
    for video_name in video_names:
        if(os.path.exists(SAVE_PATH + '/' + video_name[:-1] + '.mp4')):
            print('video already merged')
            check = 1
            continue
        if(check == 0):
            print('merging video: ' + video_name[:-1] + '.mp4')
            video = ffmpeg.input(SAVE_PATH + '/video/' + video_name[:-1] + '.mp4')
            audio = ffmpeg.input(SAVE_PATH + '/audio/' + video_name[:-1] + '.mp4')
            ffmpeg.output(video, audio, SAVE_PATH + '/' + video_name[:-1] + '.mp4').run()
        else:
            check = 0
    video_names.close()
