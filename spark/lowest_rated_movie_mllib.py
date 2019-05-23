from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
from pyspark.sql.functions import lit 

#recommend movie based on dataset data
def loadMovieNames():
    movieNames = {}
    with open('ml-100k/u.item') as f:
        for line in f:
            fields = line.split('|')
            movieNames[(int(fields[0]))] = fields[1].decode('ascii', 'ignore')
    return movieNames

def parseInput(line):
    fields = line.value.split()
    return Row(userID = int(fields[0]), movieID = int(fields[1]), rating = float(fields[2]))


if __name__ == '__main__':
    spark = SparkSession.builder.appName('MovieRecs').getOrCreate()
    movieNames = loadMovieNames()

    lines = spark.read.text('hdfs:///user/maria_dev/ml-100k/u.data').rdd 
    ratingsRDD = lines.map(parseInput)

    ratings = spark.createDataFrame(ratingsRDD).cache() #prevent Spark from recreate it again (will use multiple times)

    als = ALS(maxIter=5, regParam=0.01, userCol='userID', itemCol='movieID', ratingCol='rating')
    model = als.fit(ratings)

    
    print('\nRatings for user ID 0:')
    userRatings = ratings.filter('userID = 0')

    for rating in userRatings.collect():
        print movieNames[rating['movieID']], rating['rating']


    