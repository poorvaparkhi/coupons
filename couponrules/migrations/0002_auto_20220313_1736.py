# Generated by Django 3.2.5 on 2022-03-13 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('couponrules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreeSamplesRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threshold_amount', models.IntegerField(default=10000, verbose_name='Threshold amount above which free samples to be given')),
                ('is_eligible', models.BooleanField(default=False, verbose_name='Is Free Samples Gift Eligible?')),
            ],
            options={
                'verbose_name': 'Free Sample Rule',
                'verbose_name_plural': 'Free Sample Rules',
            },
        ),
        migrations.CreateModel(
            name='FreeShippingRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_eligible', models.BooleanField(default=False, verbose_name='Is Free Shipping Eligible?')),
            ],
            options={
                'verbose_name': 'Free Shipping Rule',
                'verbose_name_plural': 'Free Shipping Rules',
            },
        ),
        migrations.CreateModel(
            name='LoyaltyStatusRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threshold_loyalty_points', models.IntegerField(default=10000, verbose_name='Threshold loyalty points above which benefits can be redeemed')),
                ('is_eligible', models.BooleanField(default=False, verbose_name='Is Loyalty Points Discount Eligible?')),
            ],
            options={
                'verbose_name': 'Loyalty Status Rule',
                'verbose_name_plural': 'Loyalty Status Rules',
            },
        ),
        migrations.CreateModel(
            name='BOGORule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_eligible', models.BooleanField(default=False, verbose_name='Is BOGO Rule applicable ?')),
                ('free_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='free_product', to='users.product')),
                ('main_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_product', to='users.product')),
            ],
            options={
                'verbose_name': 'BOGO Rule',
                'verbose_name_plural': 'BOGO Rules',
            },
        ),
        migrations.AddField(
            model_name='ruleset',
            name='bogo_offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='couponrules.bogorule', verbose_name='BOGO rule'),
        ),
        migrations.AddField(
            model_name='ruleset',
            name='free_samples',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='couponrules.freesamplesrule', verbose_name='Free Samples rule'),
        ),
        migrations.AddField(
            model_name='ruleset',
            name='free_shipping',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='couponrules.freeshippingrule', verbose_name='Free shipping rule'),
        ),
    ]