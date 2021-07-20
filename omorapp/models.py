from django.db import models
from django.contrib.auth.models import User

from embed_video.fields import EmbedVideoField


class BlogPost(models.Model):
    """MODEL TO STORE THE POST OF EACH AUTHOR"""
    author = models.CharField(max_length=50, null=True)
    head_line = models.CharField(max_length=100, null=True)
    write_up = models.TextField(max_length=5000, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='post_images/')
    views = models.PositiveIntegerField(default=0, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.id} | {self.author}| {self.head_line[:20]}..."

    # def get_absolute_url(self):
    #     return reverse('current_blog_page', args=(self.author.id))


class Comment(models.Model):
    """STORES THE COMMENT FOR EACH POST"""
    post = models.ForeignKey(BlogPost, related_name="Comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    write_up = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.user} | {self.write_up}"


class UserContact(models.Model):
    """MODELS FOR THE USER CONTACT DETAILS"""
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=False)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.name}|{self.email}"


# YOUTUBE VIDEO UPLOAD
class YoutubeVideo(models.Model):
    title = models.CharField(max_length=50)
    video_url = EmbedVideoField()  # same like models.URLField()

    class Meta:
        ordering = ['-id']
        pass

    def __str__(self):
        return f"{self.title}"


# ABOUT OMOR UPDATE
class AboutOmorUpdate(models.Model):
    about = models.TextField(max_length=500)
    vision = models.TextField(max_length=500)
    mission = models.TextField(max_length=500)
    image = models.ImageField(upload_to="about_images/")

    def __str__(self):
        return f"{self.id}"


# MEMBERS OF OMOR UPDATE
class MembersDetails(models.Model):
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    image = models.ImageField(upload_to="members_images/")

    def __str__(self):
        return self.full_name
