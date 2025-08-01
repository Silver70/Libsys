# Generated by Django 5.2.4 on 2025-07-21 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrow', '0002_extensionrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowing',
            name='approved_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='borrowing',
            name='pickup_code',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='borrowing',
            name='pickup_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='is_extended',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('borrowed', 'Borrowed'), ('returned', 'Returned'), ('overdue', 'Overdue'), ('expired', 'Expired')], default='pending', max_length=20),
        ),
    ]
