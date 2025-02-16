# Generated by Django 2.1.5 on 2019-04-09 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_cascade'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='img_url',
            field=models.CharField(max_length=260),
        ),
        migrations.RemoveField(
            model_name='image',
            name='location',
        ),
        migrations.AddField(
            model_name='image',
            name='location',
            field=models.ManyToManyField(related_name='images', to='api.Location'),
        ),
    ]
