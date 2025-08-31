from django.contrib import admin
from django.urls import path, include
from bookings import views as bviews

urlpatterns = [
    path("signup/", bviews.signup, name="signup"),  # ✅ додано
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", bviews.home, name="home"),
    path("search/", bviews.search_trains, name="search_trains"),
    path("trips/<int:trip_id>/", bviews.trip_details, name="trip_details"),
    path("book/<int:trip_id>/", bviews.book_trip, name="book_trip"),
    path("bookings/", bviews.my_bookings, name="my_bookings"),
    path("wallet", bviews.wallet, name = "wallet"),
]
