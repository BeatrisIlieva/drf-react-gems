from rest_framework import serializers
from src.accounts.models.user_address import UserAddress, State, City, ZipCode, StreetAddress


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']


class CitySerializer(serializers.ModelSerializer):
    state_name = serializers.CharField(source='state.name', read_only=True)
    
    class Meta:
        model = City
        fields = ['id', 'name', 'state', 'state_name']


class ZipCodeSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    state_name = serializers.CharField(source='city.state.name', read_only=True)
    
    class Meta:
        model = ZipCode
        fields = ['id', 'zip_code', 'city', 'city_name', 'state_name']


class StreetAddressSerializer(serializers.ModelSerializer):
    zip_code_display = serializers.CharField(source='zip_code.zip_code', read_only=True)
    city_name = serializers.CharField(source='zip_code.city.name', read_only=True)
    state_name = serializers.CharField(source='zip_code.city.state.name', read_only=True)
    
    class Meta:
        model = StreetAddress
        fields = ['id', 'street_address', 'zip_code', 'zip_code_display', 'city_name', 'state_name']


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    state_name = serializers.CharField(source='state.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    zip_code_display = serializers.CharField(source='zip_code.zip_code', read_only=True)
    street_address_display = serializers.CharField(source='street_address.street_address', read_only=True)
    
    class Meta:
        model = UserAddress
        fields = [
            'user', 'apartment', 'state', 'city', 'street_address', 'zip_code',
            'state_name', 'city_name', 'zip_code_display', 'street_address_display'
        ]
        read_only_fields = ['user']
