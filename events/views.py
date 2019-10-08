from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from events.forms import LaunchForm
from events.models import Launch


class IndexView(TemplateView):
    template_name = 'events/index.html'


class LaunchView(FormView):
    form_class = LaunchForm
    template_name = 'events/launch.html'
    success_url = reverse_lazy('events:thanks')

    def form_valid(self, form):
        # Cleaned Data
        name = form.cleaned_data['name']
        gender = form.cleaned_data['gender']
        age = form.cleaned_data['age']
        phone = form.cleaned_data['phone']
        is_married = form.cleaned_data['is_married']
        job = form.cleaned_data['job']
        city = form.cleaned_data['city']
        has_fund = form.cleaned_data['has_fund']
        has_stock = form.cleaned_data['has_stock']
        has_derivative = form.cleaned_data['has_derivative']
        recommender = form.cleaned_data['recommender']
        # Launch Create
        Launch.objects.create(
            name=name, gender=gender, age=age, phone=phone, is_married=is_married, job=job, city=city, 
            has_fund=has_fund, has_stock=has_stock, has_derivative=has_derivative, recommender=recommender,
        )
        return super().form_valid(form)


class ThanksView(TemplateView):
    template_name = 'events/thanks.html'
