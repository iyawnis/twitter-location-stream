from tweepy import OAuthHandler


#Variables that contains the user credentials to access Twitter API
# DO NOT SHARE
consumer_key = "nel4trcqJZM9FLDAclQeEiInZ"
consumer_secret = "yLoqOZsGdAG0HpotNENs5jJrqosQpDUGeca8QL5LzboOFquDzN"
access_token = "202391387-NYS4tAD2QrvAKOzeg6BYfnB3vmVHv9lcVaE3c6m4"
access_token_secret = "nloMvygjutwo4Ltrt6C6aLxgrh9ky3lT7QCyJMTjK8oRj"


auth_handler = OAuthHandler(consumer_key, consumer_secret)
auth_handler.set_access_token(access_token, access_token_secret)