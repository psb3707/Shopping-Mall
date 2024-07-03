from rest_framework import viewsets,status
from rest_framework.response import Response
from .serializers import OrderRequestSerializer,OrderSerializer,ItemRequestSerializer
from .models import Order,Order_Item
from django.shortcuts import get_object_or_404
from members.models import Member
from items.models import Item
# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self,request):
        member_id = request.GET.get('memberId',None)
        if member_id != None:
            order = Order.objects.filter(member_id=member_id)
        else:
            order = Order.objects.all()    
        serializer = OrderSerializer(order,many=True)
        return Response(serializer.data)   
     
    def create(self,request):
        serializer = OrderRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        member = get_object_or_404(Member,pk=data['memberId'])
        order = Order(member=member)

        order_items = []
        items = []

        for order_item in data['items']:
            item = get_object_or_404(Item,pk=order_item['itemId'])
            if item.stock_quantity < order_item['itemQuantity']:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                item.stock_quantity -= order_item['itemQuantity']
                items.append(item)
                order_items.append(Order_Item(order=order,item=item,count=order_item['itemQuantity']))

        order.save()
        for order_item in order_items:
            order_item.save()
        for item in items:
            item.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        order = get_object_or_404(Order,pk=pk)
        order.status = 'Cancel'
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)        
        
   
    
        