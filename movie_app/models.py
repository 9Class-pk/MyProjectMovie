from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15),
                                                       MaxValueValidator(80)],
                                           null=True,blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    STATUS_CHOICES = (
        ('pro', 'pro'),
        ('simple', 'simple')
                      )
    status = models.CharField(choices=STATUS_CHOICES, default='simple')
    avatar = models.ImageField(upload_to='_user_avatars/', null=True, blank=True)
    data_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'



class Country(models.Model):
    country_name = models.CharField(max_length=64, unique=True)


    def __str__(self):
        return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=64)
    bio = models.TextField()
    age = models.DateField()
    director_image = models.ImageField(upload_to='director_images/')

    def __str__(self):
        return self.director_name


class Actor(models.Model):
    actor_name = models.CharField(max_length=64)
    bio = models.TextField()
    age = models.DateField()
    actor_image = models.ImageField(upload_to='actor_images/')

    def __str__(self):
        return self.actor_name


class Genre(models.Model):
    genre_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=64)
    year = models.DateField()
    country = models.ManyToManyField(Country)
    director = models.ManyToManyField(Director)
    actor = models.ManyToManyField(Actor)
    genre = models.ManyToManyField(Genre)
    TYPE_CHOICES = (
    ('144p', '144p'),
    ('360p', '360p'),
    ('480p', '480p'),
    ('720p', '720p'),
    ('1080p', '1080p'),
    )
    types = models.CharField(choices=TYPE_CHOICES)
    movie_time = models.PositiveSmallIntegerField()
    description = models.TextField()
    movie_trailer = models.FileField()
    movie_image = models.ImageField(upload_to='movie_images/')
    STATUS_CHOICES = (
    ('pro', 'pro'),
    ('simple', 'simple')
    )
    status_movie = models.CharField(choices=STATUS_CHOICES)

    def get_avg_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.stars for r in ratings) / ratings.count(), 2)
        return 0

    def get_count_people(self):
        return self.ratings.count()


    def __str__(self):
        return self.movie_name


class MovieLanguages(models.Model):
    language = models.CharField(max_length=32)
    video = models.FileField(upload_to='videos/')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    subtitle = models.FileField(upload_to='subtitles/', null=True, blank=True)
    QUALITY_CHOICES = (
        ('144p', '144p'),
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
    )
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES, default='480p')

    def __str__(self):
        return f'{self.movie}, {self.language}, {self.quality}'


class Moments(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    movie_moments = models.ImageField(upload_to='movie_moments/')

    def __str__(self):
        return f'{self.movie}'


class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    stars = models.PositiveSmallIntegerField(choices=[(i, str (i))for i in range(1,11)])
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True
                                    )

    def __str__(self):
        return f'{self.user}, {self.movie}'

class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)


class FavoriteMovie(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)




class History(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='history')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} {self.movie.movie_name} {self.viewed_at}'



