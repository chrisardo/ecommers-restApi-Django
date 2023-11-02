from django.db import models
from simple_history.models import HistoricalRecords
from base.models import BaseModel


class MeasureUnit(BaseModel):
    description = models.CharField(
        'Descripción', max_length=50, blank=False, null=False, unique=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Unidad de medida'
        verbose_name_plural = 'Unidades de medidas'

    def __str__(self):
        return self.description


class CategoryProduct(BaseModel):
    description = models.CharField(
        'Descripción', max_length=50, blank=False, null=False, unique=True)
    # measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE, verbose_name='Unidad de medida')
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Categoría de producto'
        verbose_name_plural = 'Categorías de productos'

    def __str__(self):
        return self.description


class Indicator(BaseModel):
    descount_value = models.PositiveSmallIntegerField(default=0)
    category_product = models.ForeignKey(
        CategoryProduct, on_delete=models.CASCADE, verbose_name='Categoría de producto', null=True, blank=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Indicador de oferta'
        verbose_name_plural = 'Indicadores de oferts'

    def __str__(self):
        return f'Oferta de la categoria {self.category_product}: {self.descount_value}%'


class Product(BaseModel):
    name = models.CharField(
        'Nombre de prducto', max_length=150, blank=False, null=False, unique=True)
    description = models.TextField('Descripción', null=False, blank=False)
    image = models.ImageField('Imagen del Producto',
                              upload_to='products/', blank=True, null=True)
    measure_unit = models.ForeignKey(
        MeasureUnit, on_delete=models.CASCADE, verbose_name='Unidad de medida', null=True, blank=True)
    category_product = models.ForeignKey(
        CategoryProduct, on_delete=models.CASCADE, verbose_name='Categoría de producto', null=True, blank=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.name
