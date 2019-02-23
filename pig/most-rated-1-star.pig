ratings = LOAD '/user/maria_dev/ml_100k/u.data' AS (userID:int, movieID:int, rating:int, ratingTime:int);

metatdata = LOAD '/user/maria_dev/ml-100k/u.item' USING PigStorage('|')
    AS (movieID:int, movieTitle:chararray, releaseDat:chararray, videoRelease:chararray, imdbLink:chararray);

nameLookup = FOREACH metatdata GENERATE movieID, movieTitle;

groupRatings = GROUP ratings BY movieID;

averageRatings = FOREACH groupRatings GENERATE group AS movieID,
    AVG(ratings.rating) AS avgRating, COUNT(ratings.rating) AS numRatings;

badMovies = FILTER badMovies BY movieID, nameLookup BY movieID;

namedBadMovies = JOIN badMovies BY movieID, nameLookup BY movieID;

finalResults = FOREACH namedBadMovies GENERATE nameLookup::movieTitle AS movieName, 
    badMovies::avgRating AS avgRating, badMovies::numRatings AS numRatings;

finalResultsSorted = ORDER finalResults BY numRatings DESC;

DUMP finalResultsSorted;