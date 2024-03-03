import re
from django.template import loader
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .models import ABC_data
from rest_framework.response import Response
from .serializers import FindNumberSerializer, FindNumSerializer


class FindNum(APIView):

    # Переопределение  метода post
    def post(self, request):
        serializer = FindNumberSerializer(data=request.data)

        # Проверка на валидность
        if serializer.is_valid():

            # Извлекаем параметр number
            num = serializer.validated_data['number']

            # Парсинг октетов (NDC, SN) формата MSISDN для подстановки в запрос
            result = re.search(
                r'^(?P<CC>[7|8|+7]{1,2})(?P<NDC>[0-9]{3})(?P<SN>[0-9]{7})',
                num, re.S)
            ndc = int(result.group('NDC'))
            sn = int(result.group('SN'))

            try:
                ABC_base = ABC_data.objects.filter(
                    cod=ndc, from_range__lte=sn, to_range__gte=sn).latest(
                    'created_at')

                serializer = FindNumSerializer(
                    ABC_base, context={'number': num}, many=False)
                content = {'number': [serializer.data]}
                return Response(content)
            except ABC_data.DoesNotExist:
                content = ['Информация не надена']
                return Response({'number': content}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)


def index(request):
    loader.get_template('num_data/index.html')
    return render(request, 'num_data/index.html')
