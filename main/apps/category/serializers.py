from rest_framework import serializers

from .models import Category, CategoryType


class CategoryHelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("guid", "title", "thumbnail")


class CategoryTypeSerializer(serializers.Serializer):
    guid = serializers.UUIDField(read_only=True)
    days = serializers.IntegerField(required=True)
    price = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
        required=True,
    )


class CategoryModelSerializer(serializers.ModelSerializer):
    category_types = CategoryTypeSerializer(many=True, write_only=True)

    class Meta:
        model = Category
        fields = ("guid", "thumbnail", "title", "title_uz", "title_ru", "category_types")


    def create(self, validated_data):
        types_data = validated_data.pop("category_types")
        obj = Category.objects.create(**validated_data)
        for type_ in types_data:
            CategoryType.objects.create(**type_, category=obj)
        return obj


class CategoryUpdateSerializer(serializers.ModelSerializer):
    category_types = CategoryTypeSerializer(many=True)

    class Meta:
        model = Category
        fields = ("guid", "thumbnail", "title", "title_uz", "title_ru", "category_types")


    def update(self, instance, validated_data):
        types_data = validated_data.pop('category_types')
        types = (instance.category_types).all()
        types = list(types)
        instance.thumbnail = validated_data.get('thumbnail', instance.thumbnail)
        instance.title = validated_data.get('title', instance.title)
        instance.title_ru = validated_data.get('title_ru', instance.title_ru)
        instance.title_uz = validated_data.get('title_uz', instance.title_uz)
        instance.save()

        for type_data in types_data:
            type = types.pop(0)
            type.days = type_data.get('days', type.days)
            type.price = type_data.get('price', type.price)
            type.save()
        return instance


class CategoryListSerializer(serializers.ModelSerializer):
    category_types = CategoryTypeSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "guid", 
            "thumbnail", 
            "title", 
            "title_uz", 
            "title_ru", 
            "category_types"
            )

    def get_category_types(self, obj):
        return obj.check_if_subscribed

    
