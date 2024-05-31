from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True,symmetrical=False, related_name="followings")
    def __str__(self):
        return f"{self.username}"


class Comment(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="comment")
    comment = models.TextField()

    def __str__(self):
        return f"=>{self.user} :{self.comment}"


class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="posted")
    body = models.TextField()
    likes = models.IntegerField(default=0)
    comment = models.ManyToManyField(Comment,related_name="on_post",blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.body[:20]}..."  # Truncated 
    
    def like(self):
        self.likes=self.likes+1
        self.save()

    def unlike(self):
        if self.likes > 0:
            self.likes-=1
            self.save()
        else:
            return f"your like count is : {self.likes}"        

    def serialize(self):
        return {
            "id":self.id,
            "body":self.body,
            "likes":self.likes,
            "comment":self.comment,
            "date":self.date.strftime("%b %d %Y"),
            "time":self.time.strftime("%I:%M %p"),
        }
    

      