from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)

class AddToCartForm(forms.Form):
    product_id = forms.CharField(max_length=100, required=True)
    quantity = forms.CharField(max_length=100, required=True)
    redirect_path = forms.CharField(max_length=100, required=True)

class ReviewForm(forms.Form):
    product_id = forms.CharField(max_length=50)
    text = forms.CharField(max_length=50)
    file = forms.FileField()

class AppointmentForm(forms.Form):
    date = forms.DateField()
    location_id = forms.CharField(max_length=50)

class FinalAppointmentForm(forms.Form):
    slot_id = forms.CharField(max_length=50)

class WishListForm(forms.Form):
    product_id = forms.CharField(max_length=50)

class RatingForm(forms.Form):
    product_id = forms.CharField(max_length=50)
    rating = forms.CharField(max_length=50)