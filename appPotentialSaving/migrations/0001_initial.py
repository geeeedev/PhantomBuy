# Generated by Django 2.2 on 2020-03-28 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstnm', models.CharField(max_length=50)),
                ('lastnm', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('pswd', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('isCompleted', models.BooleanField(default=False)),
                ('isSaved', models.BooleanField(default=False)),
                ('neededBy', models.ManyToManyField(related_name='needs', to='appPotentialSaving.User')),
            ],
        ),
    ]
