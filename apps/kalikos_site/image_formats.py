from wagtail.images.formats import Format, register_image_format, unregister_image_format
from django.utils.translation import gettext_lazy as _

unregister_image_format('fullwidth')
unregister_image_format('left')
unregister_image_format('right')
register_image_format(Format('fullwidth', _('Full width'), 'richtext-image rounded full-width', 'width-800'))
register_image_format(Format('left', _('Left-aligned'), 'richtext-image img-fluid rounded float-left mr-2', 'width-500'))
register_image_format(Format('right', _('Right-aligned'), 'richtext-image img-fluid rounded float-right ml-2', 'width-500'))
register_image_format(Format('thumbnail', 'Thumbnail', 'richtext-image thumbnail', 'max-120x120'))