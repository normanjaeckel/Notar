from django.views.generic import DetailView, TemplateView

from .models import FlatPage


class Home(TemplateView):
    """
    View for the start page, called home.
    """
    template_name = 'index.html'


class FlatPageView(DetailView):
    """
    View for a single static page.
    """
    model = FlatPage
