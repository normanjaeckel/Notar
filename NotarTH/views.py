from django.views.generic import TemplateView


class Home(TemplateView):
    """
    View for the start page, called home.
    """
    template_name = 'index.html'
