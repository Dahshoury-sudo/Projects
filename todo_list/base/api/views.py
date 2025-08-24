from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from base.models import Task,User
from rest_framework import status
from django.contrib.auth import authenticate,login,logout
from .serializers import TaskSerializer


@api_view(['get'])
def getroutes(request):
    routes = [
        'GET / api/',
        'GET / api/getalltasks/',
        'GET / api/getusertask/:id',
        'GET / api/getcurrentusertasks',
        ]

    return Response(routes)


@api_view(['get','post','put','delete'])
def getalltasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks,many=True)
    return Response(serializer.data)


@api_view(['get','post','put','delete'])
def getusertasks(request,pk):
    user = User.objects.get(id=pk)
    tasks = user.task_set.all()
    serializer = TaskSerializer(tasks,many=True)
    return Response(serializer.data)


@api_view(['get','post','put','delete'])
def getcurrentusertasks(request):
    user = request.user
    tasks = user.task_set.all()
    serializer = TaskSerializer(tasks,many=True)
    return Response(serializer.data)


@api_view(['get','POST'])
def registeruser(request):
    if request.method == 'GET':
        return Response({'message': 'Use POST to register a new user'})
    
    username = request.data.get('username').strip()
    fname = request.data.get('fname').strip()
    lname = request.data.get('lname').strip()
    email = request.data.get('email').strip()
    password1 = request.data.get('password1').strip()
    password2 = request.data.get('password2').strip()

    if password1 != password2:
        return Response({'error':'passwords does not match'})
    
    if User.objects.filter(username=username).exists():
        print("from user")
        return Response({'error':'username already exist'},status = status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        print("from email")
        return Response({'error':'email already exist'},status= status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(
        username = username,
        first_name = fname,
        last_name = lname,
        email = email,
        password = password1,
    )

    return Response({'message':'user created','user':{'id':user.id,'username':user.username,'email':user.email}},status=status.HTTP_201_CREATED)


@api_view(['GET','POST'])
def loginuser(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request,email=email,password=password)

    if user is not None:
        login(request,user)
        return Response({'message':'login successful'})
    else:
        return Response({'error':'either the email or password is wrong'},status=status.HTTP_400_BAD_REQUEST)
