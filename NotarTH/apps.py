from django.apps import AppConfig
from django.db.models.signals import pre_delete
from django.utils.translation import ugettext_lazy


class NotarTHAppConfig(AppConfig):
    name = 'NotarTH'
    verbose_name = ugettext_lazy('NotarTH')

    def ready(self):
        """
        Method is called after app loading. Connects the mediafile_delete
        receiver to Django's pre_delete signal so we delete a mediafile
        on the filesystem if the model instance is deleted.
        """
        from .signals import mediafile_delete

        MediaFile = self.get_model('MediaFile')
        pre_delete.connect(
            mediafile_delete,
            sender=MediaFile,
            dispatch_uid='mediafile_delete')
