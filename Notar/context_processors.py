from .models import CarouselSlide, FlatPage


def flatpages(request):
    """
    Adds a queryset of all root flatpages (without parents) to the template
    context.
    """
    return {'flatpages': FlatPage.objects.filter(parent_id=None)}


def carousel_slides(request):
    """
    Adds a queryset of all carousel slides to the template context.
    """
    return {'carousel_slides': CarouselSlide.objects.all()}
