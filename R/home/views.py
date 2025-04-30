from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Person, Question, Answer
from.serializers import PersonSerializer, QuestionSerializers, AnswerSerializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from permissions import IsOwnerOrReadOnly
from django.core.paginator import Paginator

class HomeView(APIView):
    permission_classes=[IsAuthenticated,]
    def get(self, request):
        persons = Person.objects.all()
        ser_data=PersonSerializer(instance=persons, many=True)
        return Response(data=ser_data.data)
    
class QuestionListView(APIView):
    throttle_classes=[UserRateThrottle, AnonRateThrottle]
    def get(self, request):
        questions=Question.objects.all()
        page_number=self.request.query_params.get('page',1)
        page_size=self.request.query_params.get('limit',2)
        paginator=Paginator(questions, page_size)
        srz_data=QuestionSerializers(instance=paginator.page(page_number), many=True)
        return Response(srz_data.data, status=status.HTTP_200_OK)

class QuestionCreateView(APIView):
    """
        create new question
    """
    permission_classes=[IsAuthenticated,]
    serializer_class=QuestionSerializers
    def post(self, request):
        srz_data=QuestionSerializers(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuestionUpdateView(APIView):
    permission_classes=[IsOwnerOrReadOnly,]
    def put(self, request, pk):
        question=Question.objects.get(id=pk)
        self.check_object_permissions(request, question)
        srz_data=QuestionSerializers(instance=question, data=request.data, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuestionDeleteView(APIView):
    permission_classes=[IsOwnerOrReadOnly,]
    def delete(self, request, pk):
        question=Question.objects.get(id=pk)
        self.check_object_permissions(request, question)
        question.delete()
        return Response({'messages': 'question deleted'}, status=status.HTTP_200_OK)
    
#"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNzUzNjMxMywiaWF0IjoxNzI3NDQ5OTEzLCJqdGkiOiI3ODAwZDQzNDg2ZjY0ODA5YWI2MzU0MjZjMDFiYmQ1YyIsInVzZXJfaWQiOjF9.nW7AIGuxWDxv_QG-U-zJ_NRL-RmXQlMGlp86fjVcj3Q",
#"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI3NDUwMjEzLCJpYXQiOjE3Mjc0NDk5MTMsImp0aSI6IjVjZDkzNWRkMDQ3NTQ1Zjk4Y2YzZDE2ZWY4ZjcxYmIxIiwidXNlcl9pZCI6MX0.CHb_d3jjF7go2eQcyeDnNmGTlM43YMtibAEdGC0uE9k"