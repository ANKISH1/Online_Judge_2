from rest_framework import serializers
from .models import Problems

class ProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problems
        fields = ['id', 'title', 'description', 'difficulty', 'created_at']
        extra_kwargs = {
            'created_at':{'read_only':True}
        }
        
class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problems
        fields = ['id', 'title', 'difficulty']        