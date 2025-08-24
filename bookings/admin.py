from django.contrib import admin
from .models import Station, Train, Carriage, Trip, Booking, Ticket

class CarriageInline(admin.TabularInline):
    model = Carriage
    extra = 1

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    inlines = [CarriageInline]
    list_display = ("number", "name")

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("train","origin","destination","departure","arrival","base_price")
    list_filter = ("origin","destination","train")
    search_fields = ("train__number","train__name")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id","user","trip","created_at","paid")
    list_filter = ("paid",)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id","booking","passenger_name","carriage_index","seat_number")
    list_filter = ("carriage_index",)
