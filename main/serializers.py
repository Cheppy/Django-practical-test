from rest_framework import serializers
from .models import CV

class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = ['id', 'firstname', 'lastname', 'bio', 'contacts', 'skills', 'projects']
        read_only_fields = ['id'] 