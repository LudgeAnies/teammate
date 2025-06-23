from rest_framework import serializers
from .models import Organization, UserOrganizationRole

class OrganizationListSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug', 'avatar', 'description', 'role']

    def get_role(self, obj):
        user = self.context['request'].user
        role_obj = UserOrganizationRole.objects.filter(user=user, organization=obj).first()
        return role_obj.role if role_obj else None

class OrganizationSerializer(serializers.ModelSerializer):
    pass