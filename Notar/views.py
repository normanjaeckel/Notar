from django.http import Http404
from django.views import generic

from .models import FlatPage


class Home(generic.TemplateView):
    """
    View for the start page, called home.
    """
    template_name = 'Notar/index.html'


class FlatPageView(generic.DetailView):
    """
    View for a single static page.
    """
    model = FlatPage

    def get_object(self, queryset=None):
        """
        Returns the flatpage instance. Raises Http404 if inexistent.
        """
        queryset = queryset or self.get_queryset()
        url = self.kwargs.get('url')
        for flatpage in queryset.filter(slug=url.split('/')[-1]):
            if flatpage.get_absolute_url().strip('/') == url:
                obj = flatpage
                break
        else:
            raise Http404
        return obj

    def get_context_data(self, **context):
        """
        Returns the template context. Adds breadcrumb.
        """
        context = super(FlatPageView, self).get_context_data(**context)
        parent = context['flatpage'].parent
        breadcrumb_list = [context['flatpage']]
        while parent is not None:
            breadcrumb_list.append(parent)
            parent = parent.parent
        breadcrumb_list.reverse()
        context['breadcrumb_list'] = breadcrumb_list
        return context
