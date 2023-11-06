from rest_framework import viewsets
from products.serializers.general_serializers import MeasureUnitSerializer, CategoryProductSerializer, IndicatorSerializer
from base.api import GeneralListApiView
from rest_framework.response import Response
from products.models import MeasureUnit
from rest_framework import status

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
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state= True)

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id= self.kwargs['pk'], state= True).first()
        

    def list(self, request):
        '''
        Retorna todas las unidades de medida.

        params.
        name --> Nombre de la unidad de medida.
        '''
        data = self.get_queryset()
        data = self.get_serializer(data, many= True)
        return Response(data.data)   

    def create(self, request):
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Categoria creada correctamente.'}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk= None):
        if self.get_object().exists():
            serializer = self.serializer_class(instance=self.get_object().get(), data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Categoria actualizada correctamente.'}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def destroy(self, reuqest, pk=None):
        if self.get_object().exists():
            self.get_object().get().delete()
            return Response({'message': 'Categoria actualizada correctamente.'}, status= status.HTTP_200_OK)
        return Response({'message': '', 'error': 'Categoria no encontrada.'}, status= status.HTTP_400_BAD_REQUEST)

        

