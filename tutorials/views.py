from django.shortcuts import render

# Create your views here.
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerializer
from rest_framework.decorators import api_view

from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.template import loader


@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    # GET list of tutorials, POST a new tutorial, DELETE all tutorials
    if request.method == 'GET':
        tutorials = Tutorial.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
 
    elif request.method == 'POST':
        print("Đã vào đây")
        tutorial_data = JSONParser().parse(request)
        print(tutorial_data)
        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Tutorial.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    # find tutorial by pk (id)
    try: 
        tutorial = Tutorial.objects.get(pk=pk) 
        if request.method == 'GET': 
            tutorial_serializer = TutorialSerializer(tutorial) 
            return JsonResponse(tutorial_serializer.data)
        
        elif request.method == 'PUT': 
            tutorial_data = JSONParser().parse(request) 
            tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data) 
            if tutorial_serializer.is_valid(): 
                tutorial_serializer.save() 
                return JsonResponse(tutorial_serializer.data) 
            return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE': 
            tutorial.delete() 
            return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except Tutorial.DoesNotExist: 
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    # GET / PUT / DELETE tutorial
    
        
@api_view(['GET'])
def tutorial_list_published(request):
    # GET all published tutorials
    tutorials = Tutorial.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)


@api_view(['GET'])
def admin_index(request):
    template = loader.get_template('admin.html')
    tutorials = Tutorial.objects.all()
    #tutorials_serializer = TutorialSerializer(tutorials, many=True)
    
    return HttpResponse(template.render({'data': tutorials}, request))
    #return TemplateResponse(request, 'admin.html', {"name": "to van thanh dat"})

    