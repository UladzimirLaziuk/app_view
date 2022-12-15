from rest_framework import serializers

from app import models


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RegionsModels
        fields = 'region',


class CategoriesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id_category')

    class Meta:
        model = models.Categories
        fields = 'id', 'name', 'language'

class TrafficsModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id_traffic')
    class Meta:
        model = models.TrafficsModel
        fields = 'id', 'name', 'enabled'

class ActionsModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id_action')
    class Meta:
        model = models.ActionsModel
        fields = 'id', 'name', 'type', 'payment_size', 'hold_time'

class ProgramModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id_site')
    regions = RegionSerializer(many=True, write_only=True)
    categories = CategoriesSerializer(many=True, write_only=True)
    traffics = TrafficsModelSerializer(many=True, write_only=True)
    actions = ActionsModelSerializer(many=True, write_only=True)


    class Meta:
        model = models.ProgramModel
        fields = 'id', 'name', 'name_aliases', 'site_url', 'description', \
                 'image', 'gotolink','products_xml_link', 'regions', 'categories', 'traffics', 'actions'



