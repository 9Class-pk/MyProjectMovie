from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    MovieListAPIView, MovieDetailAPIView, UserProfileViewSet, CountryViewSet,
    ActorListAPIView, ActorDetailAPIView, MovieLanguagesViewSet, MomentsViewSet,
    RatingViewSet, FavoriteViewSet, FavoriteMovieViewSet, HistoryViewSet,
    RegisterView, CustomLoginView, LogoutView, DirectorListAPIView, DirectorDetailAPIView, GenreListAPIView,
    GenreDetailAPIView, )


router = routers.SimpleRouter()
router.register(f'users', UserProfileViewSet, basename='users')
router.register(f'countries', CountryViewSet, basename='countries')
router.register(f'languages', MovieLanguagesViewSet, basename='languages')
router.register(f'moments', MomentsViewSet, basename='moments')
router.register(f'ratings', RatingViewSet, basename='ratings')
router.register(f'favorites', FavoriteViewSet, basename='favorites')
router.register(f'favorite-movies', FavoriteMovieViewSet, basename='favorite-movies')
router.register(f'history', HistoryViewSet, basename='history')



urlpatterns = [
path('', include(router.urls)),
    path('login/signup/', RegisterView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('movie/', MovieListAPIView.as_view(), name='movie_list'),
    path('movie/<int:pk>/',MovieDetailAPIView.as_view(), name='movie_detail'),
    path('director/', DirectorListAPIView.as_view(), name='director_list'),
    path('director/<int:pk>/', DirectorDetailAPIView.as_view(), name='director_detail'),
    path('actor/', ActorListAPIView.as_view(), name='actor_list'),
    path('actor/<int:pk>/', ActorDetailAPIView.as_view(), name='actor_detail'),
    path('genre/', GenreListAPIView.as_view(), name='genre_list'),
    path('genre/<int:pk>/', GenreDetailAPIView.as_view(), name='genre_detail')
]
