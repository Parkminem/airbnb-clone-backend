from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):

    title = "Filter by words!"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]
    
    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            reviews

class RatingFilter(admin.SimpleListFilter):

    title = "Rating"

    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return [
            ("three_or_more", "Three OR MORE"),
            ("less_than_three", "Less than three")
        ]
    
    def queryset(self, request, reviews):
        rating = self.value()
        if rating == "three_or_more":
            reviews.filter(rating__gte=3)
            print(reviews.query)

        elif rating == "less_than_three":
            return reviews.filter(rating__lt=3)
        else:
            return reviews

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    
    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        WordFilter,
        RatingFilter,
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
