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
        fields = ('id', 'username', 'email', 'password')




class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }




class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['password', 'user_permissions', 'groups', 'last_login', 'is_superuser']



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name']

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'director_name', 'bio', 'age', 'director_image']

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'actor_name', 'bio', 'age', 'actor_image']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'genre_name']

class MovieLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['id', 'language', 'video']

class MomentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moments
        fields = ['id', 'movie_moments']

class RatingSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'parent', 'movie', 'stars', 'text', 'created_date']

class FavoriteMovieSerializer(serializers.ModelSerializer):
    movie = MovieLanguagesSerializer(read_only=True)

    class Meta:
        model = FavoriteMovie
        fields = ['id', 'movie']

class FavoriteSerializer(serializers.ModelSerializer):
    favorite_movies = FavoriteMovieSerializer(many=True, source='favoritemovie_set', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'favorite_movies']

class HistorySerializer(serializers.ModelSerializer):
    movie = MovieLanguagesSerializer(read_only=True)

    class Meta:
        model = History
        fields = ['id', 'movie', 'viewed_at']

class MovieSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True, read_only=True)
    director = DirectorSerializer(many=True, read_only=True)
    actor = ActorSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    movie_languages = MovieLanguagesSerializer(many=True, read_only=True, source='movielanguages_set')
    moments = MomentsSerializer(many=True, read_only=True, source='moments_set')

    class Meta:
        model = Movie
        fields = [
            'id', 'movie_name', 'year', 'country', 'director', 'actor', 'genre', 'types',
            'movie_time', 'description', 'movie_trailer', 'movie_image', 'status_movie',
            'movie_languages', 'moments',
        ]
