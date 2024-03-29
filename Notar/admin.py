from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy

from .models import CarouselSlide, FlatPage, MediaFile


class FlatPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'weight',)

    class Media:
        css = {
            'all': ('css/admin.css',)
        }

    def get_changeform_initial_data(self, request):
        return {'content': '<div class="row">\n<div class="col-xs-12">'
                           '\n\n</div>\n</div>'}


class MediaFileAdmin(admin.ModelAdmin):
    date_hierarchy = 'uploaded_on'
    list_display = ('mediafile', 'uploaded_on', 'mediafile_url',)

    def mediafile_url(self, obj):
        """
        Returns the URL to the uploaded file.
        """
        return obj.mediafile.url
    mediafile_url.short_description = gettext_lazy('URL')

    def has_change_permission(self, request, obj=None):
        """
        Returns the default value (True) if obj is None else False. This
        indicates editing of objects of this type is permitted in general
        but not for (every) specific object. This way we get the admin list
        view but not the update (change) views.
        """
        if obj is not None:
            return False
        return super(MediaFileAdmin, self).has_change_permission(request, obj)


class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ('slide', 'caption', 'weight',)


site_instance = admin.site
site_instance.site_title = gettext_lazy('Notar Administration')
site_instance.site_header = gettext_lazy('Notar Administration')

site_instance.register(FlatPage, FlatPageAdmin)
site_instance.register(MediaFile, MediaFileAdmin)
site_instance.register(CarouselSlide, CarouselSlideAdmin)
site_instance.unregister(Group)
