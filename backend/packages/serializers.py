# packages/serializers.py
from rest_framework import serializers
from .models import Package, PackageType

class PackageSerializer(serializers.ModelSerializer):

    package_name = serializers.ReadOnlyField(source='package_type.name')

    class Meta:
        model = Package
        fields = ('id', 'user', 'package_name', 'generations_remains', 'purchase_date')


class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = ('id', 'name', 'total_generations', 'amount')