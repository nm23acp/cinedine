from unittest.mock import Mock, patch

from django.test import TestCase
from django.urls import reverse

from .forms import BookingForm
from .models import Booking, Restaurant


class BookingFormTests(TestCase):
    def test_rejects_zero_seats(self):
        form = BookingForm(
            data={
                "movie_title": "Example Film",
                "user_name": "Alex",
                "seats": 0,
                "show_time": "19:00",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("seats", form.errors)

    def test_rejects_more_than_ten_seats(self):
        form = BookingForm(
            data={
                "movie_title": "Example Film",
                "user_name": "Alex",
                "seats": 11,
                "show_time": "19:00",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("seats", form.errors)

    def test_accepts_valid_booking(self):
        form = BookingForm(
            data={
                "movie_title": "Example Film",
                "user_name": "Alex",
                "seats": 2,
                "show_time": "19:00",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)


class BookingViewTests(TestCase):
    def test_valid_booking_is_saved_and_redirects(self):
        response = self.client.post(
            reverse("book_ticket"),
            {
                "movie_title": "Example Film",
                "user_name": "Alex",
                "seats": 2,
                "show_time": "19:00",
            },
        )
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(Booking.objects.count(), 1)

    def test_invalid_booking_is_not_saved(self):
        response = self.client.post(
            reverse("book_ticket"),
            {
                "movie_title": "Example Film",
                "user_name": "Alex",
                "seats": 0,
                "show_time": "19:00",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)
        self.assertIn("seats", response.context["form"].errors)


class HomeViewTests(TestCase):
    @patch.dict("os.environ", {"TMDB_API_KEY": "test-key"})
    @patch("core.views.requests.get")
    def test_home_displays_movies_from_tmdb(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [{"title": "Example Film", "poster_path": "/poster.jpg"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["movies"][0]["title"], "Example Film")
        mock_get.assert_called_once()

    @patch.dict("os.environ", {}, clear=True)
    @patch("core.views.requests.get")
    def test_home_handles_missing_tmdb_key(self, mock_get):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["movies"], [])
        self.assertTrue(response.context["movie_error"])
        mock_get.assert_not_called()

    @patch.dict("os.environ", {"TMDB_API_KEY": "test-key"})
    @patch("core.views.requests.get", side_effect=__import__("requests").Timeout)
    def test_home_handles_tmdb_timeout(self, mock_get):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["movies"], [])
        self.assertTrue(response.context["movie_error"])


class RestaurantViewTests(TestCase):
    def test_restaurant_detail_page(self):
        restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            rating=4.5,
            cuisine="Italian",
            price_range="££",
            distance="1 mile",
            opening_time="10:00",
            closing_time="22:00",
        )
        response = self.client.get(reverse("restaurant_detail", args=[restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Restaurant")

    def test_missing_restaurant_returns_404(self):
        response = self.client.get(reverse("restaurant_detail", args=[99999]))
        self.assertEqual(response.status_code, 404)
