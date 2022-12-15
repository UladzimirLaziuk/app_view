import json
import uuid

from django.db import models

# Create your models here.
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django_celery_beat.models import CrontabSchedule, PeriodicTask, IntervalSchedule


class ProgramModel(models.Model):

    id_site = models.IntegerField()
    name = models.CharField(max_length=255)
    name_aliases = models.CharField(max_length=255)
    site_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    gotolink = models.URLField(blank=True, null=True)
    products_xml_link = models.CharField(default='', max_length=255, null=True)



class Score(models.Model):
    """['name', 'vendor', 'price', 'description', 'picture', 'url']"""
    program = models.ForeignKey(ProgramModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    picture = models.URLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('score-detail', args=[str(self.pk)])





class AttrProgramModel(models.Model):
    program = models.OneToOneField(ProgramModel, unique=True, on_delete=models.CASCADE)
    ecpc_trend = models.CharField(default='', max_length=100, null=True)
    epc_trend = models.CharField(default='', max_length=100, null=True)
    cr_trend = models.CharField(default='', max_length=100, null=True)
    landing_code = models.CharField(default='', max_length=100, null=True)
    landing_title = models.CharField(default='', max_length=100, null=True)
    max_hold_time = models.CharField(default='', max_length=100, null=True)
    action_testing_limit = models.CharField(default='', max_length=100, null=True)
    mobile_device_type = models.CharField(default='', max_length=100, null=True)
    mobile_os = models.CharField(default='', max_length=30, null=True)
    mobile_os_type = models.CharField(default='', max_length=100, null=True)
    feeds_info = models.CharField(default='', max_length=30, null=True)

    ecpc = models.FloatField(null=True)
    cr = models.FloatField()
    goto_cookie_lifetime = models.IntegerField()
    avg_hold_time = models.IntegerField()
    avg_money_transfer_time = models.IntegerField()

    denynewwms = models.BooleanField()
    retag = models.BooleanField()

    actions_limit = models.CharField(default='', max_length=100, null=True)
    actions_limit_24 = models.CharField(default='', max_length=100, null=True)

    modified_date = models.DateTimeField(blank=True, null=True)
    connection_status = models.CharField(max_length=155)

    show_products_links = models.BooleanField()
    geotargeting = models.BooleanField()
    allow_deeplink = models.BooleanField()
    coupon_iframe_denied = models.BooleanField()
    allow_actions_all_countries = models.BooleanField()
    connected = models.BooleanField()
    moderation = models.BooleanField()
    exclusive = models.BooleanField()
    products_csv_link = models.CharField(default='', max_length=100, null=True)
    currency = models.CharField(max_length=155)
    activation_date = models.DateTimeField(blank=True, null=True)
    rating = models.CharField(max_length=100)
    status = models.CharField(max_length=100)



class Categories(models.Model):
    id_category = models.IntegerField()
    name = models.CharField(default='', max_length=100)
    language = models.CharField(default='', max_length=100)
    program = models.ForeignKey('ProgramModel', on_delete=models.CASCADE, related_name='categories')


class RegionsModels(models.Model):
    region = models.CharField(max_length=10)
    program = models.ForeignKey('ProgramModel', on_delete=models.CASCADE, related_name='regions')


class ParentModel(models.Model):
    name = models.CharField(max_length=255)
    id_parent = models.IntegerField()
    language = models.CharField(max_length=10)
    parent = models.CharField(max_length=10)#TODO
    cat = models.ManyToManyField('Categories')

class TrafficsModel(models.Model):
    id_traffic = models.IntegerField()
    name = models.CharField(max_length=255)
    enabled = models.BooleanField()
    program = models.ForeignKey('ProgramModel', on_delete=models.CASCADE, related_name='traffics')



class ActionsModel(models.Model):
    id_action = models.IntegerField()
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    # TODO % "70.00%"
    payment_size = models.CharField(max_length=255)
    hold_time = models.IntegerField()
    program = models.ForeignKey('ProgramModel', on_delete=models.CASCADE, related_name='actions')


class RatesModel(models.Model):
    price_s = models.DecimalField(max_digits=6, decimal_places=2)
    size = models.DecimalField(max_digits=6, decimal_places=2)
    tariff_id = models.IntegerField()
    country = models.CharField(max_length=255, default='')
    date_s = models.DateField()
    is_percentage = models.BooleanField()
    id_model_rates = models.IntegerField()




class TariffsModel(models.Model):
    action_id = models.IntegerField()
    name = models.CharField(max_length=255)
    rates = models.ForeignKey('RatesModel', on_delete=models.CASCADE)


class ActionCountriesModel(models.Model):
    name = models.CharField(max_length=10)
    action_countries = models.ManyToManyField('ProgramModel')

class ActionsDetailModel(models.Model):
   tariffs =  models.ForeignKey(TariffsModel, on_delete=models.CASCADE)


def choises_list(max_hour=24):
    list(zip(range(1, max_hour+1), (str(integer) for integer in range(1, max_hour+1))))

class PeriodPost(models.Model):
    periodic_hour = models.IntegerField(choices=choises_list(max_hour=24), default='24')



def function_create_beat_site_track(time_beat, task_name, name_beat,  **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(every=time_beat,period=IntervalSchedule.HOURS)

    kwargs.update({'periodic_time': time_beat})

    periodic_task, created = PeriodicTask.objects.update_or_create(
        interval=schedule,
        name=name_beat,
        task=task_name,
        kwargs=json.dumps(kwargs),
    )
class SettingModel(models.Model):
    token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    base_token_url = models.URLField(default='https://api.admitad.com/token/')
    url_data = models.URLField()
    path_url_refresh = models.URLField()



@receiver(post_save, sender=PeriodPost)
def create_track_signal_peer_track(sender, instance, **kwargs):
    beat_time = instance.periodic_hour
    name_beat = f'{beat_time}id{instance.id}'
    function_create_beat_site_track(beat_time, task_name="send_post_api", name_beat=name_beat)

@receiver(post_delete, sender=PeriodPost)
def delete_Period(sender, instance, **kwargs):
    PeriodicTask.objects.filter(name__icontains=f'id{instance.id}')
    for model in PeriodicTask.objects.filter(name__contains=f'id{instance.id}'):
        if model.name.split('id')[-1] == str(instance.id):
            model.delete()
