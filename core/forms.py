from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    seats = forms.IntegerField(min_value=1, max_value=10)

    class Meta:
        model = Booking
        fields = ["movie_title", "user_name", "seats", "show_time"]
        widgets = {
            "movie_title": forms.TextInput(attrs={"maxlength": 200}),
            "user_name": forms.TextInput(attrs={"maxlength": 100}),
            "show_time": forms.TextInput(attrs={"maxlength": 50}),
        }

    def clean_movie_title(self):
        movie_title = self.cleaned_data["movie_title"].strip()
        if not movie_title:
            raise forms.ValidationError("Please enter a movie title.")
        return movie_title

    def clean_user_name(self):
        user_name = self.cleaned_data["user_name"].strip()
        if not user_name:
            raise forms.ValidationError("Please enter your name.")
        return user_name
