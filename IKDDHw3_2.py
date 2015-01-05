import sys
import itertools
from math import sqrt
from operator import add
from os.path import join, isfile, dirname

from pyspark import SparkConf, SparkContext
from pyspark.mllib.recommendation import ALS

def parseRating(line):
    fields = line.strip().split("::")
    return long(fields[3]) % 10, (int(fields[0]), int(fields[1]), float(fields[2]))

def parseMovie(line):
    fields = line.split("::")
    return int(fields[0]), fields[1]


def loadRatings(ratingsFile):
    f = open(ratingsFile, 'r')
    ratings = filter(lambda r: r[2] > 0, [parseRating(line)[1] for line in f])
    f.close()
    if not ratings:
        print "No ratings provided."
        sys.exit(1)
    else:
        return ratings

if __name__ == "__main__":

    sc = SparkContext()

    # load personal ratings
    myRatings = loadRatings('userRating.dat')
    myRatingsRDD = sc.parallelize(myRatings, 1)

    # load ratings and movie titles

    movieLensHomeDir = './lesson'

    # ratings is an RDD of (last digit of timestamp, (userId, movieId, rating))
    ratings = sc.textFile(join(movieLensHomeDir, "ratings.dat")).map(parseRating)

    # movies is an RDD of (movieId, movieTitle)
    movies = dict(sc.textFile(join(movieLensHomeDir, "movies.dat")).map(parseMovie).collect())

    numPartitions = 1
    training = ratings.filter(lambda x: x[0] < 6) \
      .values() \
      .union(myRatingsRDD) \
      .repartition(numPartitions) \
      .cache()

    rank = 12
    lmbda = 0.1
    numIter = 10

    model = ALS.train(training, rank, numIter, lmbda)

    # make personalized recommendations

    myRatedMovieIds = set([x[1] for x in myRatings])
    candidates = sc.parallelize([m for m in movies if m not in myRatedMovieIds])
    predictions = model.predictAll(candidates.map(lambda x: (0, x))).collect()
    recommendations = sorted(predictions, key=lambda x: x[2], reverse=True)[:10]

    # clean up
    sc.stop()

    print "Movies recommended :"
    for i in xrange(len(recommendations)):
        print ("%2d: %s" % (i + 1, movies[recommendations[i][1]])).encode('ascii', 'ignore')
