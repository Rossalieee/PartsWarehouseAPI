from rest_framework import serializers
from .models import Category, Part


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "parent_name", "children"]
        read_only_fields = ["children"]


class LocationSerializer(serializers.Serializer):
    room = serializers.CharField(max_length=100, required=True,)
    bookcase = serializers.CharField(max_length=100, required=True,)
    shelf = serializers.CharField(max_length=100, required=True,)
    cuvette = serializers.CharField(max_length=100, required=True,)
    column = serializers.CharField(max_length=100, required=True,)
    row = serializers.CharField(max_length=100, required=True,)


class PartSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    location = LocationSerializer()

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    class Meta:
        model = Part
        fields = [
            "id",
            "serial_number",
            "name",
            "description",
            "category",
            "category_name",
            "quantity",
            "price",
            "location",
        ]
        read_only_fields = ["category_name",]

        extra_kwargs = {
            "category": {"write_only": True},
        }

        def create(self, validated_data):
            location_data = validated_data.pop('location', {})
            validated_data['location'] = {
                "room": location_data.get('room'),
                "bookcase": location_data.get('bookcase'),
                "shelf": location_data.get('shelf'),
                "cuvette": location_data.get('cuvette'),
                "column": location_data.get('column'),
                "row": location_data.get('row'),
            }

            return super().create(validated_data)
