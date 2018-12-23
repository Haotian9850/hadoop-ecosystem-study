ratings = LOAD '/user/maria_dev/ml-100k/u.data' AS (userID:int, movieID:int, rating:int, ratingTime:int);

metadata = LOAD '/user/maria_dev/ml-100k/u.item' USING PigStorage ('|') AS
  (movieID:int, movieTitle:chararray, releaseDate:chararray, videoRelease:chararray, imdbLink:chararray);

DUMP metadata;

nameLookup = FOREACH metadata GENERATE movieID, movieTitle, ToUnitTime(ToDate(releaseDate, 'dd-MMM-yyyy')) AS releaseTime;

ratingByMovie = GROUP ratings BY movieID;

DUMP ratingsByMovie;

avgRatings = FOREACH ratingsByMovie GENERATE group AS movieID, AVF(ratings.rating) as avgRating;

DUMP avgRatings;

DESCRIBE ratings;
DESCRIBE ratingsByMovie;
DESCRIBE avgRatings;

fiveStarMovies = FILTER avgRatings BY avgRating > 4.0;

DESCRIBE fiveStarMovies;
DESCRIBE nameLookup;

fiveStarsWithData = JOIN fiveStarMovies BY movieID, nameLookup BY movieID;

DESCRIBE fiveStarsWithData;

DUMP fiveStartsWithData;

oldestFiveStarMovies = ORDER fiveStarsWithData BY nameLookup :: releaseTime;

DUMP oldestFiveStarMovies;
