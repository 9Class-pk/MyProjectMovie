from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    MovieViewSet, UserProfileViewSet, CountryViewSet, DirectorViewSet,
    ActorViewSet, GenreViewSet, MovieLanguagesViewSet, MomentsViewSet,
    RatingViewSet, FavoriteViewSet, FavoriteMovieViewSet, HistoryViewSet,
    RegisterView, CustomLoginView, LogoutView)


router = routers.SimpleRouter()
router.register(f'movies', MovieViewSet, basename='movies')
router.register(f'users', UserProfileViewSet, basename='users')
router.register(f'countries', CountryViewSet, basename='countries')
router.register(f'directors', DirectorViewSet, basename='directors')
router.register(f'actors', ActorViewSet, basename='actors')
router.register(f'genres', GenreViewSet, basename='genres')
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

]
