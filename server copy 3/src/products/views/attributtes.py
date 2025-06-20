from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q

from src.products.models.attributes import Stone
from src.products.serializers.attributes import StoneSerializer

class StoneRetrieveView(RetrieveAPIView):
    model = Stone
    permission_classes = [AllowAny]
    serializer_class = StoneSerializer
    
    def get(self, request, *args, **kwargs):
        category = self.request.query_params.get('category')
        filters = self._get_filters(category)
        data = self.model.objects.get_attributes_count(filters, category)
       
        serializer = self.get_serializer(data, many=True)
 
        return Response({
            'stones': serializer.data,
        })
    
    
    def _get_filters(self, category):
        colors = self.request.query_params.getlist('colors')
        stones = self.request.query_params.getlist('stones')
        metals = self.request.query_params.getlist('metals')
        collections = self.request.query_params.getlist('collections')

        filters = Q()
        if colors:
            filters &= Q(**{f'{category}__color_id__in': colors})
        if stones:
            filters &= Q(stone_id__in=stones)
        if metals:
            filters &= Q(metal__id__in=metals)
        if collections:
            filters &= Q(earwear__collection__id__in=collections)

        return filters