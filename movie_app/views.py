from rest_framework import viewsets, permissions, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from rest_framework.response import Response
from rest_framework.views import status, APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import PermissionDenied
from .serializer import (UserProfileSerializer, CountrySerializer,
                         ActorListSerializer, ActorDetailSerializer, GenreListSerializer, GenreDetailSerializer,
                         MovieListSerializer, MovieDetailSerializer, MomentsSerializer,
                         MovieLanguagesSerializer, RatingSerializer, FavoriteSerializer,
                         FavoriteMovieSerializer, HistorySerializer, UserSerializer,
                         LoginSerializer, DirectorListSerializer, DirectorDetailSerializer, UserRegisterSerializer
                         )

from .permissions import CheckStatus, CheckRating


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class BaseReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]



class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]


class CountryViewSet(BaseReadOnlyViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class DirectorListAPIView(generics.ListAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorListSerializer


class DirectorDetailAPIView(generics.RetrieveAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorDetailSerializer


class ActorListAPIView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer

class ActorDetailAPIView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer


class GenreListAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer


class GenreDetailAPIView(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreDetailSerializer


# МиксMovie двух листов который обьединяет двух похожих переменных
# одинаковые filter_backends, filterset_fields, search_fields, ordering_fields в двух местах (MovieListAPIView, MovieDetailAPIView).
class MovieFilterMixin:
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status_movie', 'types', 'year', 'country', 'actor', 'director', 'genre']
    search_fields = ['movie_name', 'description']
    ordering_fields = ['year', 'movie_time']


class MovieListAPIView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckRating]


class MovieDetailAPIView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckStatus]



class MovieLanguagesViewSet(BaseReadOnlyViewSet):
    queryset = MovieLanguages.objects.all()
    serializer_class = MovieLanguagesSerializer


class MomentsViewSet(BaseReadOnlyViewSet):
    queryset = Moments.objects.all()
    serializer_class = MomentsSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated, CheckRating]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Если хочешь, чтобы можно было работать только со своей записью избранного
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("Нет доступа к чужому избранному")
        return obj

class FavoriteMovieViewSet(viewsets.ModelViewSet):
    queryset = FavoriteMovie.objects.all()
    serializer_class = FavoriteMovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_fav, _ = Favorite.objects.get_or_create(user=self.request.user)
        if user_fav:
            return FavoriteMovie.objects.filter(favorite=user_fav)
        return FavoriteMovie.objects.none()


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return History.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
