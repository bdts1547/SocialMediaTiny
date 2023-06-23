from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikeOfPost)
admin.site.register(ImagesOfPost)
admin.site.register(CommentOfPost)