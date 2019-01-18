import re

from django import template

from wagtail.images.templatetags import wagtailimages_tags

register = template.Library()

@register.tag(name="image")
def image(parser, token):
    node = wagtailimages_tags.image(parser, token)
    return KalikosImageNode(node)
    
class KalikosImageNode(template.Node):
    def __init__(self, imagenode):
        self._node = imagenode
        
    def render(self, context):
        image = self._node.image_expr.resolve(context)
        if not 'rendered_images' in context:
            return 'IMAGE TRACK FAILED' 
        imgs = context['rendered_images']
        if image:
            imgs[image.id] = image
        return self._node.render(context)