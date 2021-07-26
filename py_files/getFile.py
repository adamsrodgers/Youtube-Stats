import pandas as pd
import json
import time
from youtube import YoutubeStats


api_key = 'AIzaSyCc_l3JvppRYKgGRL5CbXyidf_HZ1SWM30'
channel_id = 'UCBJycsmduvYEL83R_U4JriQ'

yt = YoutubeStats(api_key, channel_id)
yt.get_channel_satisitics()
yt.get_video_data()
yt.dump_in_json()