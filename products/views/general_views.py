from rest_framework import viewsets
from products.serializers.general_serializers import MeasureUnitSerializer, CategoryProductSerializer, IndicatorSerializer
from base.api import GeneralListApiView
from rest_framework.response import Response
from products.models import MeasureUnit

class MeasureUnitViewSet(viewsets.GenericViewSet):
    model = MeasureUnit
    serializer_class = MeasureUnitSerializer
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state= True)
    def list(self, request):
        '''
        Retorna todas las unidades de medida.

        params.
        name --> Nombre de la unidad de medida.
        '''
        data = self.get_queryset()
        data = self.get_serializer(data, many= True)
        return Response(data.data)


class IndicatorViewSet(viewsets.GenericViewSet):
    serializer_class = IndicatorSerializer
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state= True)
    def list(self, request):
        '''
        Retorna todas las unidades de medida.

        params.
        name --> Nombre de la unidad de medida.
        '''
        data = self.get_queryset()
        data = self.get_serializer(data, many= True)
        return Response(data.data)

class CategoryProductViewSet(viewsets.GenericViewSet):
    serializer_class = CategoryProductSerializer
