from pyspark import SparkSession #new in Spark 2.0
from pyspark.sql import Row
from pyspark.sql import functions

def loadMovieNames():
    movieNames = {}
    with open('ml-100k/u.item') as f:
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1]  #map movieID to movieName
    return movieNames

def parseInput(line):
    fields = line.split()
    return Row(movieID = int(fields[1], rating = float(fields[2])))

if __name__ == '__main__':
    spark = SparkSession.builder.appName('PopularMovies').getOrCreate() #create a new SparkSession if none exists
    movieNames = loadMovieNames()

    lines = spark.sparkContext.textFile('hdfs:///user/maria_Dev_ml-100k/u.data')    #read input file
    movies = line.map(parseInput)   #convert to RDD object
    movieDataset = spark.createDataFrame(movies)    #construct DataFrame object

    averageRatings = movieDataset.groupBy('movieID').avg('rating')
    counts = movieDataset.groupBy('movieID').count()
        
    averageAndCounts = counts.join(averageRatings, 'movieID')

    topTen = averageAndCounts.orderBy('avg(rating)').take(10)

    for movie in topTen:
        print(movieNames[movie[0]], movie[1], movie[2])
        
    spark.stop()
