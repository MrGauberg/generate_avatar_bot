# packages/serializers.py
from rest_framework import serializers
from .models import Package, PackageType

class PackageSerializer(serializers.ModelSerializer):
    remaining_generations = serializers.IntegerField(source='remaining_generations', read_only=True)

    class Meta:
        model = Package
        fields = ('id', 'user', 'package_type', 'total_generations', 'used_generations', 'purchase_date', 'remaining_generations')


class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = ('id', 'name', 'total_generations', 'amount')