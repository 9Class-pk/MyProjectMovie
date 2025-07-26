from django.contrib import admin
from .models import *



admin.site.register(Country)
admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Rating)
admin.site.register(Favorite)
admin.site.register(FavoriteMovie)
admin.site.register(History)


class MovieLanguageInLine(admin.TabularInline):
    model = MovieLanguages
    extra = 1

class MomentsInLine(admin.TabularInline):
    model = Moments
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [MovieLanguageInLine, MomentsInLine]

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = [RatingInline]