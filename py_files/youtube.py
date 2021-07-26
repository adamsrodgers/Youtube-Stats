import requests
import pandas as pd
import sqlalchemy
import json
from googleapiclient.discovery import build
from tqdm import tqdm

#api_key = 'AIzaSyCc_l3JvppRYKgGRL5CbXyidf_HZ1SWM30'
#channels_url = 'https://www.googleapis.com/youtube/v3'

#youtube = build('youtube', 'v3', developerKey = api_key)

#request = youtube.channels().list(part = 'statistics', id = 'UCPow-1SaRZVeFyPRphOqOxQ')

#response = request.execute()

#print(response)



#ef statistics_dataframe():
 #  col_names = ['SucriberCount', 'ViewCount' ]
  # df = pd.DataFrame(columns = col_names)

class YoutubeStats():
    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = None
 
    #getting the channel statistics from youtube
    def get_channel_statistics(self):
        #the url that connects the api to the application for the statistics
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}' 
        #using a get request to get the data from the api
        response = requests.get(url)
        #loads the data from the url in json text format 
        data = json.loads(response.text)
        #using a try catch to get only the statistical part of the url, but if it isnt there we set the data to none
        try:
            data = data["items"][0]["statistics"]
        except:
            data = None
        
        #setting channel_statistics parameter to data for constructor
        self.channel_statistics = data
        #returns the data recieved from the api
        return data
    
    #method to get video data from a channel
    def get_video_data(self):
        #getting video ids of the 5 most recent videos from channel
        channel_videos = self.get_channel_videos(limit = 40)
        print(channel_videos)
        
        #gets the 3 separate parts of a video
        parts = ['snippet', 'statistics', 'contentDetails']
        #for each video in the list of the channels videos
        for video_id in tqdm(channel_videos):
            #for each part that we want to extract from the video data, you extract the data from each part and store it into the channel_videos variable
            for part in parts:
                data = self.get_single_video_data(video_id, part)
                channel_videos[video_id].update(data)
        #the the data gets stored into the video_data variable        
        self.video_data = channel_videos
        return channel_videos
                
    #Method to extract video data from a single video
    def get_single_video_data(self, video_id, part):
        #url to get data from each video
        url = f'https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}'
        #using a get request to to the url and getting the response in plain text
        response = requests.get(url)
        data = json.loads(response.text)
        #trying to get the data of each specific part we want and parse it into data. if there is no data in that part it will print out an error statement and set data to an empty dictionary
        try:
            data = data['items'][0][part]
        except:
            print('error loading data')
            data = dict()
            
        return data
        
        
    #Method to get list of channels videos 
    def get_channel_videos(self, limit = None):
        #url to list channels videos
        url = f'https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date'
        #if there is no limit on the amount of videos to list 
        if limit is not None and isinstance(limit, int):
            url += '&maxResults=' + str(limit)
        
        #setting variables to getting all of the videos per page and setting index to 0
        vid, npt = self.get_channel_videos_per_page(url)
        idx = 0
        #while there is still more pages of videos to go through , keep looping through the the pages of video data until there isnt any left
        while(npt is not None and idx < 10):
            #adding next page token to loop through the video dat for that channel
            next_url = url + '&pageToken=' + npt
            #store video data into 
            next_vid, npt = self.get_channel_videos_per_page(next_url)
            vid.update(next_vid)
            idx+= 1
            
        return vid
        
    #method to get video data from each page    
    def get_channel_videos_per_page(self, url):
        #using a get request to get the data from each video and putting it in text format
        response = requests.get(url)
        data = json.loads(response.text)
        #setting videos variable to empty dictionary
        videos = dict()
        #if there isnt any data for the videos, just return the videos with no data
        if 'items' not in data:
            return videos, None
        
        #setting item_data variable to the items variable for each video
        item_data = data['items']
        #giving the data the next pagw tokenn so that it may go the next page and start extracting data from there
        nextpageToken = data.get('nextpageToken', None)
        #for each item in the youtube data, try to go into the id and kind headers and if the kind is a youtube video, extract the video id and place into the dictionary
        for item in item_data:
            try:
                kind = item['id']['kind']
                if kind == 'youtube#video':
                    video_id = item['id']['videoId']
                    videos[video_id] = dict()
            except KeyError:
                #if there is an error, print the error statement
                print('error getting ids')
                
        return videos, nextpageToken
                

    #This method is used to dump the statistics data into a json file
    def dump_in_json(self):
        #if channel_statistics variable is empty then we return nothing
        if self.channel_statistics is None or self.video_data is None:
            print('data is none')
            return
        
        added_data = {self.channel_id: {'channel_statistics': self.channel_statistics, 'video_data': self.video_data}}
        #change file name to youtube channel name.json
        channel_title = self.video_data.popitem()[1].get('channelTitle', self.channel_id) #get channel name
        #replacing the space in the channel_title variable so it looks like "file_name" instead of file name
        channel_title = channel_title.replace(" ", "_").lower()
        #set file name to a .json file
        file_name = channel_title + '.json'
        #open file name in write mode and dump all of the data we recieved from the api into a json file
        with open(file_name, 'w') as f:
            json.dump(added_data, f, indent = 4)
            
        print('file dumped')
            


        
        
