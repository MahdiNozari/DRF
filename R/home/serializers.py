from rest_framework import serializers
from .models import Question, Answer
from .custom_relational_fields import UserEmailNameRelationalField
class PersonSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    email = serializers.EmailField()

class QuestionSerializers(serializers.ModelSerializer):
    answers=serializers.SerializerMethodField()
    user=UserEmailNameRelationalField(read_only=True)
    class Meta:
        model=Question
        fields='__all__'

    def get_answers(self, obj):
        result=obj.answers.all()
        return AnswerSerializers(instance=result, many=True).data
    
class AnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields='__all__'