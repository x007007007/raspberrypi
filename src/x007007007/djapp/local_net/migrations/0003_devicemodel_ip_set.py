# Generated by Django 4.1.1 on 2022-09-16 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "x7_local_net",
            "0002_addripmodel_addrmacmodel_remove_devicemodel_mac_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="devicemodel",
            name="ip_set",
            field=models.ManyToManyField(
                related_name="device_set", to="x7_local_net.addripmodel"
            ),
        ),
    ]