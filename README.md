"# SocialMediaTiny" 

## Note:



##### How to write filter jinja2
1. Create folder 'templatetags' and 'your filters' in your app 
    - App/
        - model.py
        - view.py
        - ...
        - templatetags/
            - ____init__.__.py
            - this_filter.py
        - ...

2. In file template {% load filter %}  


##### Add url for media
```
# In file settings.py
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# In file root/urls.py:
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```


#### URL Namespace
```
# In urls.py
app_name = "social_media"
urlpatterns = [
    ...
]

# In templates.html
{% url 'social_media:path_url' %}
```

##### Serializer & CRUD
```
@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data) # JSON data

@api_view(['POST'])
def taskCreate(request):
    serializer = TaskSerializer(request.data)
    if serializer.is_valid():
        serializer.save() # Save to db
    
    return Response(serializer.data) # JSON data

@api_view(['POST'])
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(intance=task, request.data)
    if serializer.is_valid():
        serializer.save() # Save to db
    
    return Response(serializer.data) # JSON data

@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    
    return Response("Deleted") # JSON data
```






