from django.db import models
from members.models import Member
from items.models import Item
# Create your models here.
class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,default='Ordered')
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    items = models.ManyToManyField(Item,through='Order_Item')

    class Meta:
        db_table = 'orders'

class Order_Item(models.Model):
    count = models.IntegerField()
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_items'
