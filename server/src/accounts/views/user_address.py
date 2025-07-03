from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from src.accounts.models.user_address import UserAddress, State, City, ZipCode, StreetAddress
from src.accounts.serializers.user_address import (
    UserAddressSerializer, StateSerializer, CitySerializer,
    ZipCodeSerializer, StreetAddressSerializer
)


class UserAddressView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        address, _ = UserAddress.objects.get_or_create(user=self.request.user)
        return address


class StateListView(ListAPIView):
    queryset = State.objects.all().order_by('name')
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticated]


class CityListView(ListAPIView):
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        state_id = self.request.query_params.get('state_id')
        queryset = City.objects.all().order_by('name')
        if state_id:
            return queryset.filter(state_id=state_id)
        return queryset.none()


class ZipCodeListView(ListAPIView):
    serializer_class = ZipCodeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        city_id = self.request.query_params.get('city_id')
        queryset = ZipCode.objects.all().order_by('zip_code')
        if city_id:
            return queryset.filter(city_id=city_id)
        return queryset.none()


class StreetAddressListView(ListAPIView):
    serializer_class = StreetAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        zip_code_id = self.request.query_params.get('zip_code_id')
        queryset = StreetAddress.objects.all().order_by('street_address')
        if zip_code_id:
            return queryset.filter(zip_code_id=zip_code_id)
        return queryset.none()
