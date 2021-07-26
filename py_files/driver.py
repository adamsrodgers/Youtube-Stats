import pandas as pd
import json
import time
from youtube import YoutubeStats

print('Welcome to the youtube Analyzer')
print('Written by: Tinsae Dejene, Joel Salguero, and Raekwon Adams-Rodgers')
time.sleep(2)

print('Here you will choose a youtube channel of the list provided down below and choose what data you would like to get such as:')
time.sleep(2)
print('Total View Count, Total Suscriber Count, The Amount of Videos on The Channel. We also give video data for the top 10 most viewed videos of each channel. Here are\nyour choices below: ')
print(" 1.lockpickinglawyer\n",  "2.john stossel\n", "3.economics explained\n", "4.louis rossman\n", "5.casually explained\n", "6.economics explained 2\n", "7.kirksicle\n", "8.reasontv\n", "9.doug demuro")

choice = input('Choose a youtube channel name to analyze: ')
while(choice != 'Exit'):
    
    data = None
    with open(choice.replace(" ", "_").lower() + '.json', 'r') as f:
        data = json.loads(f.read())
    
    channel_id, stats = data.popitem()
    channel_stats = stats['channel_statistics']
    video_stats = stats['video_data']




    print('Here are the channel stats for' + choice + ': ')


    print('Total Views: ', channel_stats['viewCount'])

    print('Subcribers: ', channel_stats['subscriberCount'])

    print('Amount of Videos: ', channel_stats['videoCount'])

    print('\t\tTop 10 most viewed videos data')

    sorted_vids = sorted(video_stats.items(), key=lambda item: int(item[1]['viewCount']), reverse = True)
    stats = []
    for vid in sorted_vids:
        video_id = vid[0]
        Title = vid[1]['title']
        Views = int(vid[1]['viewCount'])
        Comments = int(vid[1]['commentCount'])
        Likes = int(vid[1]['likeCount'])
        Dislikes = int(vid[1]['dislikeCount'])
        Duration = vid[1]['duration']
        stats.append([Title, Views, Comments, Likes, Dislikes, Duration])
    
    df = pd.DataFrame(stats, columns = ['Title', 'Views', 'Comments', 'Likes', 'Dislikes', 'Duration'])
    print(df.head(10))
    
    time.sleep(3)
    
    choice = input('\n\nChoose a youtube channel to analyze or type exit to exit program:')
    if choice == 'exit':
        quit()




#df_nested_list = pd.json_normalize(data, record_path = ['channel_statistics'])
#print(df_nested_list)