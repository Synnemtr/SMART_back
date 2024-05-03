from rest_framework import serializers
from api.food.models import Food, MacronutrientFood, FoodIntake, PlannedFood
from api.user.models import User


class FoodByUserSerializer(serializers.Serializer):
    class Meta:
        model = FoodIntake
        fields = '__all__'
        depth = 1
    
    #name = serializers.CharField(max_length=255)
    #code = serializers.CharField(max_length=255)
    #quantity = serializers.FloatField()
    #date = serializers.DateTimeField()


class RankingFoodByCaloriesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    code = serializers.CharField(max_length=255)
    calories = serializers.FloatField()


class UserFoodConsumptionSerializer(serializers.ModelSerializer):
    total_food_consumed = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id', 'username', 'total_food_consumed']


class FoodIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodIntake
        depth = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "GET":
            self.Meta.depth = 1
            self.Meta.exclude = None
            self.Meta.fields= '__all__'
        else:
            self.Meta.depth = 0
            self.Meta.exclude = ["user"]
            self.Meta.fields= None

    # Custom read-only field for Calories
    calories = serializers.SerializerMethodField()

    def get_calories(self, obj):
        if obj.quantity:
            food = Food.objects.get(id=obj.food.id)
            food_calories = food.calories
            if food_calories is not None:
                calories = food_calories * obj.quantity / 100
            else:
                calories = 0
        else:
            calories = 0
        return calories
    
    def create(self, validated_data):
        print(validated_data)
        user = self.context["request"].user
        food_intake = FoodIntake.objects.create_food_intake(user, **validated_data)
        return food_intake

    def update(self, instance, validated_data):
        instance = FoodIntake.objects.update_food_intake(instance, **validated_data)
        return instance

class PlannedFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannedFood
        depth = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "GET":
            self.Meta.depth = 1
            self.Meta.exclude = None
            self.Meta.fields= '__all__'
        else:
            self.Meta.depth = 0
            self.Meta.exclude = ["user"]
            self.Meta.fields= None

    # Custom read-only field for Calories
    calories = serializers.SerializerMethodField()

    def get_calories(self, obj):
        if obj.quantity:
            food = Food.objects.get(id=obj.food.id)
            food_calories = food.calories
            if food_calories is not None:
                calories = food_calories * obj.quantity / 100
            else:
                calories = 0
        else:
            calories = 0
        return calories
    
    def create(self, validated_data):
        user = self.context["request"].user
        planned_food = PlannedFood.objects.create_planned_food(user, **validated_data)
        return planned_food

    def update(self, instance, validated_data):
        instance = PlannedFood.objects.update_planned_food(instance, **validated_data)
        return instance

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"
        read_only_fields = ("id",)

    def create(self, validated_data):
        food = Food.objects.create_food(**validated_data)
        return food

    def update(self, instance, validated_data):
        instance = Food.objects.update_food(instance, **validated_data)
        return instance


class MacronutrientFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = MacronutrientFood
        fields = ["id", "food", "macronutrient", "amount"]
        read_only_fields = ("id",)

    def create(self, validated_data):
        macronutrient_food = MacronutrientFood.objects.create_macronutrient_food(**validated_data)
        Food.objects.add_macronutrient_to_food(macronutrient_food.food, macronutrient_food.macronutrient)
        return macronutrient_food

    def update(self, instance, validated_data):
        instance = MacronutrientFood.objects.update_macronutrient_food(instance, **validated_data)
        return instance
