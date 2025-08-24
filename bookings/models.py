from django.db import models
from django.contrib.auth.models import User

class Station(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class Train(models.Model):
    number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"{self.number} {self.name}".strip()

class Carriage(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="carriages")
    index = models.PositiveIntegerField(help_text="Номер вагона (1..n)")
    seats = models.PositiveIntegerField(default=50)

    class Meta:
        unique_together = ("train", "index")
        ordering = ["index"]

    def __str__(self):
        return f"Вагон {self.index} ({self.train})"

class Trip(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="trips")
    origin = models.ForeignKey(Station, on_delete=models.PROTECT, related_name="departures")
    destination = models.ForeignKey(Station, on_delete=models.PROTECT, related_name="arrivals")
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    base_price = models.DecimalField(max_digits=8, decimal_places=2, default=200.00)

    class Meta:
        ordering = ["departure"]

    def __str__(self):
        return f"{self.train} {self.origin} → {self.destination} ({self.departure:%Y-%m-%d %H:%M})"

    def total_seats(self):
        return sum(c.seats for c in self.train.carriages.all())

    def booked_seats(self):
        return self.tickets.count()

    def available_seats(self):
        return self.total_seats() - self.booked_seats()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="bookings")
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Бронювання #{self.id} для {self.user} ({self.trip})"

class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="tickets")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="tickets")
    carriage_index = models.PositiveIntegerField()
    seat_number = models.PositiveIntegerField()
    passenger_name = models.CharField(max_length=120)

    class Meta:
        unique_together = ("trip", "carriage_index", "seat_number")

    def __str__(self):
        return f"Квиток {self.passenger_name} {self.trip} вагон {self.carriage_index} місце {self.seat_number}"
