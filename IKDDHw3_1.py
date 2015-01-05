import sys
from operator import add
from pyspark import SparkContext

if __name__ == "__main__":
    sc = SparkContext()
    lines = sc.textFile('pg5000.txt', 1)
    counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
    result = len(counts.collect())
    sc.stop()
    print result
