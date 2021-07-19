from django.contrib import admin

from .models import (
    Comment, BlogPost,
    UserContact, YoutubeVideo,
    AboutOmorUpdate, MembersDetails,
)

admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(UserContact)
admin.site.register(YoutubeVideo)
admin.site.register(AboutOmorUpdate)
admin.site.register(MembersDetails)
