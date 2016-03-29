from .models import FlatPage


def flatpages(request):
    """
    Adds a queryset of all root flatpages (without parents) to the template
    context.
    """
    return {'flatpages': FlatPage.objects.filter(parent_id=None)}
