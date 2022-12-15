from typing import Dict

import requests
from django.conf import settings

from app.models import RegionsModels, Categories, TrafficsModel, ActionsModel, SettingModel, ProgramModel, Score
from app.serializers import ProgramModelSerializer
from app_view.celery import app
from celery.utils.log import get_task_logger

from app_view.tasks_util_xml import response_iter, create_list_result

logger = get_task_logger(__name__)


def bulk_create_model(data_list: Dict, instance: object, model) -> None:
    list_model = [model.objects.get_or_create(**data, program=instance) for data in data_list]
    model.objects.bulk_create(list_model)


def bulk_create_or_update(data_list: Dict, instance: object, model, created=False) -> None:
    if created:
        list_model = [model(**data, program=instance) for data in data_list]
        model.objects.bulk_create(list_model)
        return
    list_update = [model.objects.update_or_create(**data, program=instance) for data in data_list]
    logger.info(list_update)


def write_in_base_response(data_write):

    serializer = ProgramModelSerializer(data=data_write)
    serializer.is_valid()

    logger.info(serializer.errors)
    val_data = serializer.validated_data
    list_pop = [val_data.pop(name) for name in ['regions', 'categories', 'traffics', 'actions']]
    model = serializer.Meta.model
    model_data = model.objects.filter(id_site=data_write['id'])
    if model_data.exists():
        model_data.update(**val_data)
        created = False
        instance = model_data.get()

    else:
        instance = model.objects.create(**val_data)
        created = True

    logger.info(f'Created-{created}')

    for dict_data, mdl in zip(list_pop, (RegionsModels, Categories, TrafficsModel, ActionsModel)):
        result = bulk_create_or_update(dict_data, instance, mdl, created)
        logger.info(result)


def send_requests(url, token, token_type='Bearer'):
    headers = {
        'Authorization': f'{token_type} {token}'}
    logger.info('send_requests')
    if token_type == 'Basic':
        data = {}
        data.update({'grant_type': 'client_credentials',
                     'client_id': 'Mt44BBCMKwYD5BEPLiY9FFdaul21xn',
                     'scope': 'advcampaigns websites public_data advcampaigns_for_website',
                     })
        response = requests.post(url, headers=headers, data=data)
    else:
        logger.info('send_requests')
        logger.info(headers)
        response = requests.get(url, headers=headers)
    return response


@app.task(name="send_post_api")
def send_post_api(*args, **kwargs):
    logger.info('send_post_api')
    model_setting = SettingModel.objects.first()

    token = model_setting.token
    url = model_setting.url_data
    refresh_token = model_setting.refresh_token
    path_url_refresh = model_setting.path_url_refresh
    logger.info(token)
    logger.info(url)

    response = send_requests(url, token)
    logger.info(response.status_code)
    if response.status_code == 200:
        response_json_data = response.json()
        for data_write in response_json_data.get('results'):
            write_in_base_response(data_write)



def parse_xml_link_product(id, url_xml):
    logger.info(url_xml)
    obj_program = ProgramModel.objects.get(id=id)
    for data in response_iter(url_xml):
        data_iter = data.iter('offer')
        data_list = create_list_result(data_iter)
        list_score = [Score(**val, program=obj_program) for val in data_list]
        Score.objects.bulk_create(list_score)



@app.task(name="parse_data_base_links")
def parse_data_base_links(list_id):
    logger.info(list_id)
    val_list = ProgramModel.objects.filter(id__in=list_id).values_list('id', 'products_xml_link')
    logger.info(len(val_list))
    for id, url_xml in val_list:
        if url_xml:
            parse_xml_link_product(id, url_xml)

