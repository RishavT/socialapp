from django.contrib import admin
from mainapp.models import *

admin.site.register(CustomUser)
admin.site.register(Status)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(StatusLike)