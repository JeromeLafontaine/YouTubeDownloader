from YoutubeDownloader_pack import download_video_and_audio
from YoutubeDownloader_pack import merge_video_and_audio
from YoutubeDownloader_pack import get_links

SAVE_PATH = "Videos"
#link_path='links_file.txt'
video_names_path='video_names.txt'
error_path = 'Videos/error_link.txt'
channel_URL = 'UCYGjxo5ifuhnmvhPvCc3DJQ' #Wankil

link_path='Videos/links_file/links_file'


#get_links(link_path , channel_URL)

#for i in range(0,1):
#    print("file n°"+str(i))
#    download_video_and_audio(link_path+str(i)+".txt" , SAVE_PATH , video_names_path , error_path)

download_video_and_audio('links_file.txt' , SAVE_PATH , video_names_path , error_path)

#merge_video_and_audio(SAVE_PATH , video_names_path)