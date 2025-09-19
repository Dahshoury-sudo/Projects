from rest_framework.decorators import api_view,permission_classes
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from base.models import Task,User
from rest_framework import status
from django.contrib.auth import authenticate,login,logout
from .serializers import TaskSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import IsArab

@api_view(['get'])
# @permission_classes([IsAdminUser])
def getroutes(request):
    routes = [
        'GET / api/',
        'GET / api/getalltasks/',
        'GET / api/getusertask/:id',
        'GET / api/getcurrentusertasks',
        'POST / api/SignUp',
        'POST / api/login',
        'POST / api/tasks/add',
        'GET / api/task/:id',
        'GET,PATCH / api/tasky/edit/:id',
        'PATCH / api/tasky/complete/:id',
        'DELETE / api/tasky/delete/:id',
        'GET / api/csrf/'
        ]

    return Response(routes)


@api_view(['GET'])
def getcsrf(request):
    token = get_token(request)
    return Response({"token":token})


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


@api_view(['POST'])
def registeruser(request):

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

    return Response({'message':'user created successfully'},status=status.HTTP_201_CREATED)


@api_view(['POST'])
def addtask(request):
    title = request.data.get('title')
    description = request.data.get('description')
    user_id = request.data.get('user_id')

    try:
        task = Task.objects.create(
            message = title,
            description = description, 
            user = User.objects.get(id=user_id),
            completed = False
        )
        return Response({"message":"task created"},status=status.HTTP_201_CREATED)

    except:
        return Response({"error":"Error occured try again"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def gettask(request):
    task_id = request.data.get('task_id')
    task = Task.objects.get(id=task_id)
    serializer = TaskSerializer(task)
    return Response(serializer.data)




@api_view(['GET','PATCH'])
def edittask(request):
    task_id = request.data.get('task_id')
    if request.method == 'GET':
        task = Task.objects.get(id=task_id)
        serializer = TaskSerializer(task)
        return Response({"task":serializer.data})

    else:
        task = Task.objects.get(id=task_id)
        title = request.data.get('title')
        description = request.data.get('description')
        task.title = title
        task.description = description
        task.save()
        return Response({"message":"the task was edited successfully"},status=status.HTTP_200_OK)



@api_view(['DELETE'])
def deletetask(request):
    task_id = request.data.get('task_id')
    task = Task.objects.get(id=task_id)
    task.delete()
    return Response({"message":"Task deleted successfully"},status=status.HTTP_200_OK)
    

@api_view(['PATCH'])
def completetask(request,pk):
    task_id = request.data.get('task_id')
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.save()
    return Response({"message":"task is now completed"},status=status.HTTP_200_OK)
