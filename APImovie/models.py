from django.db import models
from accounts.models import UserAccount
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField


class MovieList(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=False, null= False)
#    title = models.CharField(max_length=255, default='Untitled')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='lists', null=True, blank=True)
    is_public = models.BooleanField(default=True, null=True)
    movies = models.ManyToManyField('Movie', related_name='lists', blank=True)
    upvotes = models.PositiveIntegerField(default=0, null=True, blank=True)
    downvotes = models.PositiveIntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    total_time_of_movies = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['-upvotes']  # Optional: Order lists by upvotes in descending order

    def get_upvotes(self):
        return self.votes.filter(is_upvote=True).count()
    
    def get_downvotes(self):
        return self.votes.filter(is_upvote=False).count()
    
    def __str__(self):
        return self.title

class Vote(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    movie_list = models.ForeignKey(MovieList, on_delete=models.CASCADE, related_name='votes')
    is_upvote = models.BooleanField()

    class Meta:
        unique_together = ('user', 'movie_list')


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    imdb_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255)
    background_path = models.CharField(max_length=255)
    original_language = models.CharField(max_length=20)
    original_title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.IntegerField()
    runtime = models.FloatField()  
    vote_average = models.FloatField(max_length=255)  # Updated to DecimalField
    vote_count = models.FloatField(max_length=255)
    popularity = models.FloatField(max_length=255)  # Updated to DecimalField

    def get_similar_movies(self):
        import AI.movietomovie as mtm
        return mtm.movie_to_movie(self.id)

    def __str__(self):
        return self.title
class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    genre_name = models.CharField(max_length=50)

    def __str__(self):
        return self.genre_name
class Movie_Genre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,null = True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,null = True)

    def __str__(self):
        return f"{self.movie.title} - {self.genre.genre_name}"
    


class Actor(models.Model):
    id =  models.IntegerField(primary_key=True)
    actor_name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255)

# class Character(models.Model):
#     id = models.IntegerField(primary_key=True)
#     character_name = models.CharField(max_length=255)

# class Cast(models.Model):
#     id = models.IntegerField(primary_key=True)
#     actor_id = models.ForeignKey(Actor, on_delete=models.CASCADE)
#     character_id = models.ForeignKey(Character, on_delete=models.CASCADE)
#     movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
class Cast(models.Model):
    id = models.IntegerField(primary_key=True)
    actor_id = models.ForeignKey(Actor, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=255)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
class Crew(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
class MovieCrew(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,null = True)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE,null = True)
class Comment(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"{self.user.username} - {self.text[:50]}"
    

class Rate(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='rates')
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    rate_point = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} rates {self.movie.title} with {self.rate_point} points"
