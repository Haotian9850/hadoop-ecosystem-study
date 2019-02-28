from pyspark import SparkConf, SparkContext

def loadMovieNames():
        movieNames = {}
        with open('ml-100k/u.item') as f:
            for line in f:
                fields = line.split('|')
                movieNames[int(fields[0])] = fields[1]
        return movieNames

def parseInput(line):
    fields = line.split()
    return (int(fields[1]), (float(fields[2]), 1.0))

if __name__ == '__main__':
    conf = SparkConf().setAppName('Worst rated movies!')
    sc = SparkContext(conf = conf)

    movieNames = loadMovieNames()
