#-*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import Stream
from datetime import datetime
from model import Tweet
from auth import auth_handler
from traceback import print_exc
from database import db_session
import json

errors = {
"304": "There was no new data to return.",
"400": "The request was invalid or cannot be otherwise served",
"401": "Missing or incorrect authentication credentials",
"403": "The request is understood, but it has been refused or access is not allowed",
"404": "The URI requested is invalid or the resource requested",
"406": "Invalid format is specified in the request.",
"410": "API endpoint has been turned off",
"420": "Returned when you are being rate limited",
"422": "Returned when an image uploaded to POST account / update_profile_banner is unable to be processed.",
"429": "Too Many Requests",
"500": "Internal Server Error",
"502": "Bad Gateway",
"503": "Service Unavailable",
"504": "Gateway timeout" }

class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            info = json.loads(data)

            coordinates = info.get('coordinates', {}).get('coordinates', None) if info.get('coordinates') else None
            place = info.get('place').get('full_name') if info.get('place') else ''
            if coordinates is None:
              # If we don't have coordinates we dont care about this tweet
              return True
            tw = Tweet(id=info.get('id'),
                      tweet_text=info.get('text'),
                      user_id=info.get('user').get('id'),
                      coordinates=coordinates,
              		    created_at=info.get('created_at'),
                      last_update=datetime.now(),
                      place=place)
            tw.save()
        except:
           print_exc()
           db_session.rollback()
        return True

    def on_error(self, status_code):
        if errors.has_key(status_code):
            print(errors.get(status_code))
        else:
            print(status_code)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    stream = Stream(auth_handler, l)

    #This line filter Twitter Streams to capture data from london and new york
    stream.filter(locations = [-74.25888888888889,40.4772222,-73.7,40.9175,-0.35138888888888886,51.3847222,0.14805555555555555,51.6722222,-77.119759,38.7916449,-76.909393,38.995548,-118.6681759,33.7036519,-118.1552891,34.3373061])
