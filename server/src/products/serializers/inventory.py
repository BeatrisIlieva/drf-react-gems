from rest_framework import serializers


class SizedInventorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['size', 'quantity']
        depth = 2


class SimpleInventorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['quantity']
        depth = 2
