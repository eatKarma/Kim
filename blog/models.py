from django.db import models
from django.utils import timezone

from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail

class Post(models.Model):
  author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  text = models.TextField()
  photo = models.ImageField(upload_to='%Y/%m/%d/orig')
  # thumbnail = models.ImageField(upload_to='%Y/%m/%d/thumb')
  thumbnail = ImageSpecField(source='photo', processors=[Thumbnail(200, 200)], 
    format='JPEG', options={'quality': 60})
  published_date = models.DateTimeField(default=timezone.now)

  def delete(self, *args, **kwargs):
    self.photo.delete()
    self.thumbnail.delete()
    super(Post, self).delete(*args, **kwargs)

  def __str__(self):
    return self.title