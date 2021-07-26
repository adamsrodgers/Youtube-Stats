import unittest
import requests
from youtube import YoutubeStats

api_key = 'AIzaSyCc_l3JvppRYKgGRL5CbXyidf_HZ1SWM30'
channel_id = 'UCPow-1SaRZVeFyPRphOqOxQ'
part = 'statistics'
video_id = 'Tbu4xOtMZ70' 
class TestYoutube(unittest.TestCase):
#testing if the channel statistics function is getting the statistics from youtube
    def test_1_get_channel_statistics(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}'         
        response = requests.get(url)
#check if the request is successfully processed 
        self.assertEqual(response.status_code, 200)
        yt = YoutubeStats(api_key, channel_id)
        data = yt.get_channel_statistics()
        self.assertNotEqual(data, None)
#Testing the single video data if the data is getted from each video
    def test_2_get_single_video_data(self):
        url = f'https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={api_key}'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        yt = YoutubeStats(api_key, channel_id)
        data = yt.get_single_video_data(video_id, part)
        self.assertNotEqual(data, None)
    def test_3_get_channel_videos(self):
        url = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=id&order=date'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        yt = YoutubeStats(api_key, channel_id)
        data = yt.get_channel_videos(limit = 5)
        self.assertNotEqual(data, None)
    def test_4_get_video_data(self):
        url = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=id&order=date'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        yt = YoutubeStats(api_key, channel_id)
        data = yt.get_video_data()
        self.assertNotEqual(data, None)
    def test_5_get_channel_videos_per_page(self):
        url = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&part=id&order=date'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        yt = YoutubeStats(api_key, channel_id)
        data = yt.get_channel_videos_per_page(url)
        self.assertNotEqual(data, None)

if __name__ == '__main__':
    unittest.main()