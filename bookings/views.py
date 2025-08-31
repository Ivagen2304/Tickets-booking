from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from .models import Station, Train, Carriage, Trip, Booking, Ticket
from .forms import SearchForm, BookingForm
from django.contrib.auth import login
from .forms import SignupForm

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматичний вхід після реєстрації
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})


def home(request):
    form = SearchForm(request.GET or None)
    ctx = {"form": form}
    return render(request, "bookings/home.html", ctx)

def search_trains(request):
    form = SearchForm(request.GET or None)
    trips = []
    if form.is_valid():
        origin = form.cleaned_data["origin"]
        destination = form.cleaned_data["destination"]
        date = form.cleaned_data["date"]
        start = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.min.time()))
        end = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.max.time()))
        trips = Trip.objects.filter(origin=origin, destination=destination, departure__range=(start, end)).select_related("train","origin","destination")
    return render(request, "bookings/search_results.html", {"form": form, "trips": trips})

def trip_details(request, trip_id):
    trip = get_object_or_404(Trip.objects.select_related("train","origin","destination"), pk=trip_id)
    return render(request, "bookings/trip_details.html", {"trip": trip})

@login_required
@transaction.atomic
def book_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    if trip.available_seats() <= 0:
        messages.error(request, "Вибачте, вільних місць немає.")
        return redirect("trip_details", trip_id=trip.id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = Booking.objects.create(user=request.user, trip=trip, paid=False)
            taken = set((t.carriage_index, t.seat_number) for t in trip.tickets.select_for_update())
            carriage_map = [(c.index, c.seats) for c in trip.train.carriages.all().order_by("index")]
            assigned = None
            for c_index, seats in carriage_map:
                for seat in range(1, seats+1):
                    if (c_index, seat) not in taken:
                        assigned = (c_index, seat)
                        break
                if assigned:
                    break
            if not assigned:
                messages.error(request, "Не вдалося призначити місце.")
                return redirect("trip_details", trip_id=trip.id)
            Ticket.objects.create(
                booking=booking,
                trip=trip,
                carriage_index=assigned[0],
                seat_number=assigned[1],
                passenger_name=form.cleaned_data["passenger_name"],
            )
            messages.success(request, "Бронювання створено! (Оплата умовна — приклад)")
            return redirect("my_bookings")
    else:
        form = BookingForm()
    return render(request, "bookings/book_trip.html", {"trip": trip, "form": form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related("trip","trip__train")
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})
