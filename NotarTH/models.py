from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy


class FlatPage(models.Model):
    """
    Model for pages with static content.
    """
    slug = models.SlugField(
        ugettext_lazy('Slug/URL'),
        unique=True,
        help_text=ugettext_lazy(
            "Example: 'legal-notice'. Each page must have a unique slug."))

    title = models.CharField(
        ugettext_lazy('Menu title'),
        max_length=255,
        help_text=ugettext_lazy(
            "Example: 'Legal notice'. The title is used for the entry in the "
            "menu. Do not use long titles."))

    parent = models.ForeignKey(
        'self',
        verbose_name=ugettext_lazy('Parent element'),
        null=True,
        blank=True,
        help_text=ugettext_lazy(
            'If this field is empty, the page appears in the main menu '
            'at root level. Else the page is a subpage of its parent.'))

    weight = models.IntegerField(
        ugettext_lazy('Weight'),
        default=100,
        help_text=ugettext_lazy(
            'Use this for ordering. A higher number means that the entry '
            'appears further down in the menu.'))

    content = models.TextField(
        ugettext_lazy('Content (HTML)'),
        blank=True,
        help_text=ugettext_lazy('You can use full HTML here.'))

    sitemap_priority = models.DecimalField(
        ugettext_lazy('Priority in the sitemap'),
        max_digits=2,
        decimal_places=1,
        default=0.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text=ugettext_lazy(
            'The sitemap is used by search engines: See '
            '<a href="http://www.sitemaps.org/protocol.html#prioritydef">'
            'Sitemap protocol</a>.'))

    class Meta:
        ordering = ('weight', 'slug',)
        verbose_name = ugettext_lazy('Static Page')
        verbose_name_plural = ugettext_lazy('Static Pages')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the URL to the flatpage. Slugs of child and parent pages are
        combined.
        """
        url = reverse('flatpage', args=[self.slug])
        if self.parent is not None:
            url = self.parent.get_absolute_url()[:-1] + url
        return url

    def clean(self):
        """
        Checks parent field to prevent hierarchical loops.
        """
        super().clean()
        ancestor = self.parent
        while ancestor is not None:
            if ancestor == self:
                raise ValidationError(_(
                    'Error: Do not create a circular hierarchy. Choose '
                    'another parent element.'))
            ancestor = ancestor.parent


class MediaFile(models.Model):
    """
    Model for uploaded files like images.
    """
    mediafile = models.FileField(
        ugettext_lazy('File'),
        max_length=255)

    uploaded_on = models.DateTimeField(
        ugettext_lazy('Uploaded on'),
        auto_now_add=True)

    class Meta:
        ordering = ('-uploaded_on',)
        verbose_name = ugettext_lazy('File')
        verbose_name_plural = ugettext_lazy('Files')

    def __str__(self):
        return self.mediafile.url
