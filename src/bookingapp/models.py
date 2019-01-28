from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PassportPhoto(models.Model):
    owner = models.ForeignKey(User, related_name='passport', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(PassportPhoto, self).delete(*args, **kwargs)
        storage.delete(path)
