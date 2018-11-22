from mrjob.job import MRJob
from mrjob.step import MRStep

'''
Custom mapper and reducer that determines how many movie receives a 5-star rating in ml-100k dataset
'''

class RatingsBreakdown(MRJob):

    def steps(self):
        return [
            MRStep(mapper = self.mapper_get_ratings, reducer = self.reducer_count_ratings)
        ]

    def mapper_get_ratings(self, _, line):
        (userID, movieID, rating, timestamp) = line.split('\t')
        yield rating, 1

    def reducer_count_ratings(self, key, values):
        yield key, sum(values)

# for every mrjob..
if __name__ == '__main__':
    RatingsBreakdown.run()