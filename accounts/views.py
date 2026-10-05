from django.shortcuts import render, redirect
from .forms import RegistrationForm, StudentForm, StudentFormSet
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from rest_framework.permissions import IsAdminUser

# Create your views here.
def register(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html',{'form':form})
            
        
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'accounts/login.html')      

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')  

def logout_view(request):
    logout(request)
    return redirect('login')

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def hello_api(request):
    return Response({
        'message': 'Hello from my first REST API!',
        'status': 'success'
    })
    
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def student_list(request):

    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdminUser])
def student_detail(request, pk):

    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    elif request.method == 'PATCH':
        serializer = StudentSerializer(
            student,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=204)
    
from rest_framework import viewsets
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    search_fields = ['name']
    ordering_fields = ['name', 'age']
    filterset_fields = ['age']
    
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('student_list_page')
    else:
        form = StudentForm()

    return render(request, 'accounts/add_student.html', {'form': form})

def add_multiple_students(request):
    if request.method == 'POST':
        formset = StudentFormSet(request.POST)

        if formset.is_valid():
            formset.save()
            return redirect('student_list_page')
    else:
        formset = StudentFormSet(queryset=Student.objects.none())

    return render(
        request,
        'accounts/add_multiple_students.html',
        {'formset': formset}
    )

def student_list_page(request):
    students = Student.objects.all()
    return render(
        request,
        'accounts/student_list.html',
        {'students': students}
    )