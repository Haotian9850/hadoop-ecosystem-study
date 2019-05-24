CREATE VIEW IF NOT EXISTS avgRatings AS 
SELECT movieID, AVG(rating) as avgRating, COUNT(movieID) as ratingCount
FROM ratings
GROUP BY movieID
ORDER BY avgRating DESC 

SELECT n.title, avgRating FROM avgRatings t JOIN names n ON t.movieID = n.movieID
WHERE ratingCount > 10