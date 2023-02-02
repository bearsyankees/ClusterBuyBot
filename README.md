
# Cluster Buy Bot
This is the code powering the backend of [@ClusterBuyBot](https://twitter.com/ClusterBuyBot) on Twitter.

## Languages/Libraries/Other Tech Used

Python

Tweepy

Pandas

Redis

Apscheduler

Heroku



## How Does it Work?

This bot checks every minute for SEC form 4 filings showing cluster buys via the OpenInsider website. It stores the latest reported date in a Redis DB so it doesn't tweet about the same filing twice, and tweets whenever there is a new cluster buy.