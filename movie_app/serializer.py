from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ('id', 'username', 'email','password')



class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'status', 'first_name', 'last_name', 'avatar']



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']

class DirectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name', ]


class DirectorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name', 'bio', 'age', 'director_image']



class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name']


class ActorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name', 'bio', 'actor_image', 'age']


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'genre_name',]


class GenreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class MovieLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['language', 'video','subtitle', 'quality']


class MomentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moments
        fields = ['movie_moments']


class RatingSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ['user', 'parent', 'movie', 'stars', 'text', 'created_date',]

    def create(self, validated_data):
        user = self.context['request'].user
        movie = validated_data['movie']
        stars = validated_data['stars']


        rating, created = Rating.objects.update_or_create(
            user=user, movie=movie,
            defaults={'stars': stars}
        )
        return rating


class MovieListSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True, read_only=True)
    year = serializers.DateField(format='%d-%m-%Y')
    genre = GenreListSerializer(many=True, read_only=True)



    class Meta:
        model = Movie
        fields = [
                'movie_name', 'year', 'country', 'genre',
              'movie_image',

        ]

class MovieDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True, read_only=True)
    year = serializers.DateField(format='%d-%m-%Y')
    director = DirectorDetailSerializer(many=True, read_only=True)
    actor = ActorDetailSerializer(many=True, read_only=True)
    genre = GenreDetailSerializer(many=True, read_only=True)
    movie_languages = MovieLanguagesSerializer(many=True, read_only=True, source='movielanguages_set')
    moments = MomentsSerializer(many=True, read_only=True, source='moments_set')
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()


    class Meta:
        model = Movie
        fields = [
            'id', 'movie_name', 'year', 'country', 'director', 'actor', 'genre', 'types',
            'movie_time', 'description', 'movie_trailer', 'movie_image', 'status_movie',
            'movie_languages', 'moments', 'get_avg_rating',  'get_count_people'
        ]

    def get_avg_rating(self,obj):
        return obj.get_avg_rating()

    def get_count_people(self,obj):
        return obj.get_count_people()


class FavoriteMovieSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)

    class Meta:
        model = FavoriteMovie
        fields = ['id', 'movie']


class FavoriteSerializer(serializers.ModelSerializer):
    favorite_movies = FavoriteMovieSerializer(many=True, source='favoritemovie_set', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'favorite_movies']


class HistorySerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)

    class Meta:
        model = History
        fields = ['id', 'movie', 'viewed_at']


