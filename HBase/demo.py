'''
    Create a HBase table for movie ratings by user
    -> Quickly query it for individual users (example of sparse data)

    Key: UserID
    Column family: rating 50 for movie 20, rating 29 for movie 22, etc...

    Architecture:
        Python client -> REST service -> HBase and HDFS

    Backend steps: start HBase (VM) -> add port forwarding -> start REST service (/usr/hdp/current/hbase-master/bin/hbase-daemon.sh start rest -p 8000 -infoport 8001) 
'''

from starbase import Connection

c = Connection('127.0.0.1', '8000')

ratings = c.table('ratings')    

if ratings.exists():
    print('Dropping existing rating table \n')
    ratings.drop()

ratings.create('rating')    #creates a column family

print('Parsing the ml-100k rating data... \n')
ratingFile = open('e:/Downloads/ml-100k/ml-100k/u.data', 'r')

batch = ratings.batch()

for line in ratingFile:
    (userID, movieID, rating, timeStamp) = line.split()
    batch.update(userID, {'rating' : {movieID : rating}})

ratingFile.close()



