from rest_framework import serializers
from .models import Member,Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['city','street','zipcode']

class MemberSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Member
        fields = ['id','name','address']

    def create(self, validated_data):
        address_validated_data = validated_data.pop('address')
        member = Member.objects.create(**validated_data)
        Address.objects.create(member=member,**address_validated_data)
        return member

    def update(self,instance,validated_data):
        address_data = validated_data.pop('address')
        address = instance.address

        instance.name = validated_data.get('name',instance.name)
        instance.save()

        address.city = address_data.get('city',address.city)
        address.street = address_data.get('street',address.street)
        address.zipcode = address_data.get('zipcode',address.zipcode)
        address.save()

        return instance