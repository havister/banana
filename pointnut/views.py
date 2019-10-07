from django.http import Http404
from django.shortcuts import redirect
from django.views.generic.base import TemplateView


def http404_redirect(request):
    raise Http404()


def login_redirect(request):
    return redirect('users:index')


class IndexView(TemplateView):
    template_name = 'index.html'
  