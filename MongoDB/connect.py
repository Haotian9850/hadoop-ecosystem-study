from pyspark.sql import SparkSession
from pyspark.sql import Row 
from pyspark.sql import function 


def parseInput(line):
    fields = line.split('|')
    return Row(user_id=int(fields[0]), age=int(fields[1]), gender=fields[2], occupation=fields[3], zip=fields[4])

if __name__ = '__main__':

    spark = SparkSession.builder.appName('MongoDBIntegration').getOrCreate()

    lines = spark.sparkContext.textFile('hdfs:///user/maria_dev/ml-100k/u.user')

    users = lines.map(parseInput)

    usersDataset = spark.createDataFrame(users)

    #write to MongoDB
    usersDataset.write.format('com.mongodb.spark.sql.DefaultSource').option('uri', 'mongodb://127.0.0.1/movielens.users').mode('append').save()
    
    