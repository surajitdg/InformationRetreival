class Movies:
    movie_id = 0
    movie_title = 0
    #genres = []

    def __init__(self, var1, var2, var3):
        self.movie_id = var1
        self.movie_title = var2
        #genres_string = ''.join(var3)
        #self.genres = genres_string.split('|')


class Ratings:
    movie_id = 0
    user_id = 0
    rating = 0

    def __init__(self, var1, var2, var3):
        self.user_id = var1
        self.movie_id = var2
        self.rating = var3


