from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.
class TaskCategory(models.Model):
    title = models.CharField(max_length=200)
    sub_category_of = models.ForeignKey('TaskCategory', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.sub_category_of:
            return f"{self.sub_category_of} - {self.title}"
        return f"{self.title}"
    
    class Meta:
        unique_together = ('title', 'user')

class Task(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    sub_task_of = models.ForeignKey('Task', blank=True, null=True, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.sub_task_of:
            return f"{self.sub_task_of} - {self.title}"
        return f"{self.title}"
    
    class Meta:
        ordering = ['-due_date', 'completed']

class TaskMaterial(models.Model):
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif',
                       'pdf',
                       'html', 'htm',
                       'mp4', 'avi', 'mkv',
                       'doc', 'docx', 'ppt', 'pptx',
                       'xls', 'xlsx',
                       'txt', 'rtf',
                       'zip', 'rar', 'tar',
                       'csv', 'json', 'yml', 'ods', 'tsv']
    title = models.CharField(max_length=200)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    reference_link = models.URLField(null=True, blank=True)
    document = models.FileField(upload_to='task_documents/',null=True, blank=True, 
                                validators=[FileExtensionValidator(allowed_extensions=valid_extensions)])
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class TaskNote(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    note = models.TextField()

    def __str__(self):
        return f"{self.task} - Note"