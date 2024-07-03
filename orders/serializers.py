from rest_framework import serializers


class OrderItemSerializer(serializers.Serializer):
    itemId =serializers.IntegerField(source='item.id')
    itemName = serializers.CharField(source='item.item_name')
    count = serializers.IntegerField()

class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField() 
    memberId = serializers.IntegerField(source='member.id')
    orderDate = serializers.DateTimeField(source = 'order_date')
    item = OrderItemSerializer(source='order_item_set',many=True)
    status = serializers.CharField()

           
class ItemRequestSerializer(serializers.Serializer):
    itemId = serializers.IntegerField()
    itemQuantity = serializers.IntegerField()

class OrderRequestSerializer(serializers.Serializer):
    memberId = serializers.IntegerField()   
    items = ItemRequestSerializer(many=True)

