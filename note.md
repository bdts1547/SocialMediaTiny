
## Todo:
- pagination search - OK
- autoload home
- test all

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

2. In code
```
# file this_filter.py
from django import template
register = template.Library()

@register.filter(name='zip')
def zipFilter(x, value):
    return zip(x, value)


# file .html
{% load this_filter %}
``` 


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


##### Save image to firebase storage
```
import pyrebase
config = {
    ... # get from firebase
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# Store image to Firebase
image = 'path/to/image'
dest = '/media/profile_iamges/i2.jpg'
storage.child(dest).put(image) 

# Get url
storage.child('path/to/image/firebase').get_url(None)
```


##### Create Group & add User to Group
```
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

# Create the group 
mod, created = Group.objects.get_or_create(name='mod')
ct = ContentType.objects.get_for_model(model=Post)
perms = Permission.objects.filter(content_type=ct)

# Add permissions to the mod group
mod.permissions.add(*perms)
# Add user to the group
user = User.objects.get(username='dang')
mod.user_set.add(user)


# views.py
class Home(PermissionRequiredMixin, View):
permission_required = ['core.add_post']
...
```



