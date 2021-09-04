# Generated by Django 3.2.5 on 2021-08-02 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributor', '0003_alter_carmodel_brand_car'),
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='carmodel',
            name='is_publish',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='brandcar',
            name='affiliates',
            field=models.ManyToManyField(blank=True, to='distributor.Affiliate'),
        ),
    ]