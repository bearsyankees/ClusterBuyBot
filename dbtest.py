import redis
import pandas as panda
import re

r = redis.StrictRedis.from_url(
    "redis://:pe1cc77fa5e5d32b955c02b9977ce5c4140208ea331f8295050c276cd423b5b20@ec2-34-194-145-51.compute-1.amazonaws.com:30969",
    encoding="utf-8",
    decode_responses=True)

print(r.mget("latest_stock"))

url = 'http://openinsider.com/latest-cluster-buys'
tables = panda.read_html(url)  # get all tables on page
pandaData = tables[11]  # the one I want is the 11th
data1 = pandaData.to_dict()  # read it into a dictionary
data = {re.sub(r'[^\x00-\x7F]', ' ', k): v for k, v in data1.items()}  # clean up white space
# reformat dict so each item is about one ticker
data = [{key.strip(): data[key][i] for key in data.keys()} for i in range(len(data["X"]))]
print(data[0]["Filing Date"])
#r.set("latest_stock", data[0]["Filing Date"])