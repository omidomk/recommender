from numpy import *

# this is just a prototype for testing purposes 

articles = 10
users=5

ratings = random.randint(11, size = (articles,users))
print (ratings)

print

# lets us know who rated a article and who didnt
did_rate = (ratings != 0) * 1
print (did_rate)

print

# rate a article
my_rating = zeros((articles, 1))
print (my_rating)

print

my_rating[0] = 4
my_rating[2] = 2
my_rating[4] = 4
my_rating[6] = 2
print (my_rating)

print

# updating the matrix and adding my_rating to the matrix
ratings = append (my_rating, ratings, axis = 1)
did_rate = append (((my_rating != 0)*1), did_rate, axis = 1)

print (ratings)
print
print (did_rate)

print

# normalization
def normalize_ratings(ratings, did_rate):
    articles = ratings.shape[0]
    mean = zeros(shape=(articles, 1))
    norm = zeros(shape=ratings.shape)

    for i in range(articles):
        # Get all the indexes where there is a 1
        idx = where(did_rate[i] == 1)[0]

        # Calculate mean rating of ith article only from user's that gave a rating
        mean[i] = mean(ratings[i, idx])
        norm[i, idx] = ratings[i, idx] - mean[i]

    return (norm, mean)


# runing the normalisation function
ratings, mean = normalize_ratings(ratings, did_rate)
print (ratings)
print
print (mean)

#update the number of users
users = ratings.shape[1]

num_feature = 3

