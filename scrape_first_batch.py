
# for scraping app info and reviews from Google Play
from google_play_scraper import app, Sort, reviews

# for keeping track of timing
#import datetime as dt
#from tzlocal import get_localzone

# for building in wait times
import random
import time

import csv

# Retrieve reviews (and continuation_token) with reviews function
count = 200
batch_num = 0

#app_id = "im.vector.app" #Element
#app_id = "com.wire" #wire
app_id ="org.jitsi.meet" #Jitsi
#app_id = "chat.tox.antox" #tox
#app_id = "org.thoughtcrime.securesms" #signal
#app_id = "org.telegram.messenger" #telegram

token = None

#keys = "reviewId,userName,userImage,content,score,thumbsUpCount,reviewCreatedVersion,at,replyContent,repliedAt".split(",")

with open(f"{app_id}.csv", "w+", encoding="utf-8", newline='') as fs:

    csv_writer = csv.writer(fs)
    # write the header line
    fs.write("reviewId,userName,userImage,content,score,thumbsUpCount,reviewCreatedVersion,at,replyContent,repliedAt\n")
    for batch in range(4999):
        rvws, token = reviews(
            app_id,           # found in app's url
            lang='en',        # defaults to 'en'
            country='us',     # defaults to 'us'
            sort=Sort.NEWEST, # start with most recent
            count=count,       # batch size
            continuation_token=token
        )
        for review in rvws:
            csv_writer.writerow(review.values())

        # detect if we need to stop the loop
        if len(rvws) < count:
            print (f"{app_id} Last batch count:{len(rvws)}")
            print (f"Done. ({batch_num}*200+{len(rvws)}) reviews altogether.")
            break
        # Increase batch count by one
        batch_num +=1
        print(f'{app_id} Batch {batch_num} completed.')

        # Wait 1 to 5 seconds to start next batch
        time.sleep(random.randint(1,5))

print ("Bye")
