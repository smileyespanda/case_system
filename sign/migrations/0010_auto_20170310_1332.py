# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-10 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0009_auto_20170302_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='step',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
