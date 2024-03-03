import re

from rest_framework import serializers


class FindNumSerializer(serializers.Serializer):
    number = serializers.SerializerMethodField('get_number')
    cod = serializers.IntegerField()
    from_range = serializers.IntegerField()
    to_range = serializers.IntegerField()
    capacity_range = serializers.IntegerField()
    operator = serializers.CharField(max_length=100)
    region = serializers.CharField(max_length=100)

    def get_number(self, obj):
        return self.context['number']


class FindNumberSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=12, min_length=11)

    def validate_number(self, value):
        if value:
            result = re.search(
                r'^(?P<CC>[7|8|+7]{1,2})(?P<NDC>[0-9]{3})(?P<SN>[0-9]{7})',
                value, re.S)
            if result:
                CC = result.group('CC')
                NDC = result.group('NDC')
                SN = result.group('SN')
            else:
                raise serializers.ValidationError(
                    'Значение ' + value + ' \
                    не соответсвует телефонному номеру в стандарте MSISDN')

            oktets = ['7', '+7', '8']
            if CC in oktets and NDC.isdigit() and SN.isdigit():
                return value
            else:
                raise serializers.ValidationError(
                    'Значение ' + value + ' \
                    не соответсвует телефонному номеру в стандарте MSISDN')
        else:
            raise serializers.ValidationError(
                'Значение ' + value + ' \
                    не соответсвует телефонному номеру в стандарте MSISDN')
