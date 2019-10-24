from django import forms


class LaunchForm(forms.Form):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, '남성'),
        (FEMALE, '여성')
    ]
    name = forms.CharField(label='name', max_length=30, min_length=2)
    gender_choice = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    age = forms.IntegerField(min_value=20, max_value=99)
    phone = forms.RegexField(label='phone', max_length=11, regex=r'^\d{3}\d{3,4}\d{4}$')
    is_married = forms.BooleanField(required=False)
    job = forms.CharField(label='job', max_length=30)
    city = forms.CharField(label='city', max_length=30)
    has_fund = forms.BooleanField(required=False)
    has_stock = forms.BooleanField(required=False)
    has_derivative = forms.BooleanField(required=False)
    recommender = forms.CharField(label='recommender', max_length=30, required=False)
