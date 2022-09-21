# Generated by Django 3.1.5 on 2022-09-18 03:59

import app.printers.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outboundstock',
            name='transfer_company',
            field=models.CharField(choices=[(app.printers.models.TransferCompany['EMS'], 'EMS'), (app.printers.models.TransferCompany['EMS_PREMIUM'], 'EMS_PREMIUM'), (app.printers.models.TransferCompany['EMS_TAIWAN'], 'EMS_TAIWAN'), (app.printers.models.TransferCompany['PANTOS'], 'PANTOS'), (app.printers.models.TransferCompany['CAINAO'], 'CAINAO'), (app.printers.models.TransferCompany['YTO'], 'YTO'), (app.printers.models.TransferCompany['YUNDA'], 'YUNDA')], max_length=50),
        ),
    ]