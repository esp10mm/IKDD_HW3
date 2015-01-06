IKDD_HW3
========
HW3_1
-----
Install Spark and run word count. This program counts word of file ``pg5000.txt`` and print result.<br>
<br>Usage:<br>

    {SPARK_DIR}/bin/spark-submit IKDDHw3_1.py
HW3_2
-----
Movie recommendation using MLlib of Spark.<br>
This program trains model with data ``/lesson/ratings.dat`` and reads file ``userRating.dat`` as input printing top 10 movies result according to it. Besides, ``/lesson/movies.dat`` is table for program to look up movie data.<br>
<br>Ratings contained in the file ``/lesson/ratings.dat`` and ``useRatings.dat`` are in the following format:<br>
    
    UserID::MovieID::Rating::Timestamp
Movie information in the file ``/lesson/movies.dat`` are in the following format:<br>
    
    MovieID::Title::Genres
Usage:

    {SPARK_DIR}/bin/spark-submit IKDDHw3_2.py
