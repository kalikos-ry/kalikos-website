from django.db import migrations
from django.forms import model_to_dict

def create_kalikos_images(apps, schema_editor):
    Image = apps.get_model('wagtailimages', 'Image')
    Collection = apps.get_model('wagtailcore', 'Collection')
    KalikosImage = apps.get_model('kalikos_site', 'KalikosImage')
    for image in Image.objects.all():
        kwargs = model_to_dict(image, exclude=['tags'])
        kwargs['collection'] = Collection.objects.get(id=kwargs['collection'])
        KalikosImage.objects.create(**kwargs)


class Migration(migrations.Migration):

    dependencies = [
        ('kalikos_site', '0006_auto_20181204_0552'),
    ]

    operations = [
        migrations.RunPython(create_kalikos_images),
    ]
