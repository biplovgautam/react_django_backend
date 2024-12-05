from django.db import migrations, models

def handle_null_images(apps, schema_editor):
    ProductImage = apps.get_model('app', 'ProductImage')
    for product_image in ProductImage.objects.filter(image_binary__isnull=True):
        product_image.image_binary = b''  # Set a default empty binary value
        product_image.save()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_productimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='image_binary',
            field=models.BinaryField(null=True),
        ),
        migrations.RunPython(handle_null_images),
        migrations.RemoveField(
            model_name='productimage',
            name='image',
        ),
        migrations.RenameField(
            model_name='productimage',
            old_name='image_binary',
            new_name='image',
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.BinaryField(null=False),
        ),
    ]