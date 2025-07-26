import django_filters
from .models import Movie

class MovieFilter(django_filters.FilterSet):
    year_from = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    year_to = django_filters.NumberFilter(field_name='year', lookup_expr='lte')
    country = django_filters.CharFilter(field_name='country__name', lookup_expr='icontains')
    genre = django_filters.CharFilter(field_name='genre__name', lookup_expr='icontains')
    status_movie = django_filters.CharFilter(field_name='status', lookup_expr='icontains')
    actor = django_filters.CharFilter(field_name='actors__name', lookup_expr='icontains')
    director = django_filters.CharFilter(field_name='director__name', lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ['country', 'year_from', 'year_to', 'genre', 'status_movie', 'actor', 'director']
