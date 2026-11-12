import logging
import os

import requests
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import urlencode

from .forms import BookingForm
from .models import Restaurant

logger = logging.getLogger(__name__)
TMDB_POPULAR_URL = "https://api.themoviedb.org/3/movie/popular"


def home(request):
    """Show popular TMDB movies and restaurants stored in the local database."""
    api_key = os.environ.get("TMDB_API_KEY")
    movies = []
    movie_error = False

    if api_key:
        try:
            response = requests.get(
                TMDB_POPULAR_URL,
                params={"api_key": api_key},
                timeout=(3.05, 8),
            )
            response.raise_for_status()
            payload = response.json()
            movies = payload.get("results", [])
        except (requests.RequestException, ValueError) as exc:
            logger.warning("Unable to retrieve popular movies from TMDB: %s", exc)
            movie_error = True
    else:
        movie_error = True

    restaurants = Restaurant.objects.all()
    return render(
        request,
        "home.html",
        {"movies": movies, "restaurants": restaurants, "movie_error": movie_error},
    )


def book_ticket(request):
    """Validate and save a ticket booking, then redirect after success."""
    movie = request.GET.get("movie", "").strip()

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            messages.success(
                request,
                f"Your booking for {booking.movie_title} has been saved.",
            )
            return redirect("home")
    else:
        form = BookingForm(initial={"movie_title": movie})

    return render(request, "booking.html", {"form": form})


def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    return render(request, "restaurant_detail.html", {"restaurant": restaurant})
