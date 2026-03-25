from rest_framework import serializers
from .models import Submissions
from apps.problems.models import Problems

class SubmissionListCreateSerializer(serializers.ModelSerializer):
    # code = serializers.CharField(write_only = True)
    # verdict = serializers.CharField(read_only = True)
    # submitted = serializers.DateTimeField(read_only = True)
    # user = serializers.PrimaryKeyRelatedField(read_only = True)
    #extra_kwargs as below or explicitly defining as above both do same thing.
    class Meta:
        model = Submissions
        fields = ['id', 'user', 'problem','language','code', 'verdict','submitted'] 
        extra_kwargs = {
            'code':{'write_only': True},
            'verdict':{'read_only': True},
            'submitted':{'read_only': True},
            'user':{'read_only': True},
        }

class AllSubmissionsSerializer(serializers.ModelSerializer):
    problem_title = serializers.CharField(source = 'problem.title', read_only = True)
    class Meta:
        model = Submissions
        fields = ['id', 'user', 'problem_title','language', 'verdict','submitted'] 

