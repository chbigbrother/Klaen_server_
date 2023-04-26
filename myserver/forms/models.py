from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
import os


class OverwriteStorage(FileSystemStorage):
    '''
    file 같은 이름 존재할 경우 overwrite
    '''
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

def get_random_filename(instance, filename):
    filename = "%s" % (str(filename))
    return os.path.join(filename)

# Create your models here.
class FileUploadCsv(models.Model):
    title = models.TextField(max_length=500, null=True, blank=True)
    file = models.FileField(null=True, storage=OverwriteStorage(), upload_to=get_random_filename)
    created_at = models.DateTimeField(auto_now_add=True)