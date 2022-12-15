import requests
from defusedxml.ElementTree import parse, iterparse


def response_iter(url_xml):
    response = requests.get(url_xml, stream=True)
    response.raw.decode_content = True
    context = iterparse(response.raw, events={"end"})
    for event, elem in context:
        if event == 'end':
            yield elem


def create_list_result(data_iter):
    list_tag = ['name', 'vendor', 'price', 'description', 'picture', 'url']
    list_iter_result = []
    for product in data_iter:
        dict_result_data = {}
        for name_tag in list_tag:
            tag = product.find(name_tag)
            try:
                data = tag.text
            except AttributeError:
                data = 'None'
            dict_result_data[name_tag] = data
        list_iter_result.append(dict_result_data)
    return list_iter_result


