from django.core.exceptions import ValidationError
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy


class FlatPage(models.Model):
    """
    Model for pages with static content.
    """
    slug = models.SlugField(
        gettext_lazy('Slug/URL'),
        unique=True,
        help_text=gettext_lazy(
            "Example: 'legal-notice'. Each page must have a unique slug."))

    title = models.CharField(
        gettext_lazy('Menu title'),
        max_length=255,
        help_text=gettext_lazy(
            "Example: 'Legal notice'. The title is used for the entry in the "
            "menu. Do not use long titles."))

    submenu_title = models.CharField(
        gettext_lazy('Submenu title'),
        max_length=255,
        blank=True,
        help_text=gettext_lazy(
            "Example: 'All services'. The submenu title is used for the entry "
            "in the submenu and only if the page has children. Do not use "
            "long titles."))

    subtitle = models.CharField(
        gettext_lazy('Subtitle'),
        max_length=255,
        blank=True,
        help_text=gettext_lazy(
            "Example: 'The legal details of our business.'. The subtitle is "
            "used as subheading at the top of the page."))

    parent = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        verbose_name=gettext_lazy('Parent element'),
        null=True,
        blank=True,
        help_text=gettext_lazy(
            'If this field is empty, the page appears in the main menu '
            'at root level. Else the page is a subpage of its parent.'))

    weight = models.IntegerField(
        gettext_lazy('Weight'),
        default=100,
        help_text=gettext_lazy(
            'Use this for ordering. A higher number means that the entry '
            'appears further down in the menu.'))

    content = models.TextField(
        gettext_lazy('Content (HTML)'),
        blank=True,
        help_text=gettext_lazy('You can use full HTML here.'))

    sitemap_priority = models.DecimalField(
        gettext_lazy('Priority in the sitemap'),
        max_digits=2,
        decimal_places=1,
        default=0.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text=gettext_lazy(
            'The sitemap is used by search engines: See '
            '<a href="http://www.sitemaps.org/protocol.html#prioritydef">'
            'Sitemap protocol</a>.'))

    class Meta:
        ordering = ('weight', 'slug',)
        verbose_name = gettext_lazy('Static Page')
        verbose_name_plural = gettext_lazy('Static Pages')

    def __unicode__(self):
        # Rename this to __str__() in Python 3.
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
        super(FlatPage, self).clean()
        ancestor = self.parent
        while ancestor is not None:
            if ancestor == self:
                raise ValidationError(_(
                    'Error: Do not create a circular hierarchy. Choose '
                    'another parent element.'))
            ancestor = ancestor.parent

    def get_submenu_title(self):
        """
        Returns the value of the field submenu_title if it is set, else a
        default string 'All <title>'.
        """
        return self.submenu_title or _('All {flatpage_title}').format(
            flatpage_title=self.title)


class MediaFile(models.Model):
    """
    Model for uploaded files like images.
    """
    mediafile = models.FileField(
        gettext_lazy('File'),
        max_length=255)

    uploaded_on = models.DateTimeField(
        gettext_lazy('Uploaded on'),
        auto_now_add=True)

    class Meta:
        ordering = ('-uploaded_on',)
        verbose_name = gettext_lazy('File')
        verbose_name_plural = gettext_lazy('Files')

    def __str__(self):
        return self.mediafile.url


class CarouselSlide(models.Model):
    """
    Model for the slides for the header carousel.
    """
    slide = models.ForeignKey(
        MediaFile,
        on_delete=models.PROTECT,
        verbose_name=gettext_lazy('File'),
        help_text=gettext_lazy(
            'Use an 1900x1080 image (e. g. JPG or PNG) here.'))

    weight = models.IntegerField(
        gettext_lazy('Weight'),
        default=100,
        help_text=gettext_lazy(
            'Use this for ordering. A higher number means that the slide '
            'appears further right in the carousel.'))

    caption = models.CharField(
        gettext_lazy('Caption'),
        max_length=255,
        blank=True,
        help_text=gettext_lazy(
            "Example: 'Trust me'."))

    class Meta:
        ordering = ('weight',)
        verbose_name = gettext_lazy('Carousel slide')
        verbose_name_plural = gettext_lazy('Carousel slides')

    def __str__(self):
        return self.caption or str(self.slide)
