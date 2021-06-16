from django.db import models

# Create your models here.
class Course(models.Model):
    code = models.CharField(max_length=6)
    name = models.TextField()

class Class(models.Model):
    code = models.CharField(max_length=6)
    class_code = models.CharField(max_length=6)

class Assignment(models.Model):
    code = models.CharField(max_length=10)
    class_code = models.CharField(max_length=10)
    title = models.TextField()
    date = models.DateTimeField()
    location = models.FileField(upload_to="submission/")
    type = models.TextField()
    location_sample = models.FileField(upload_to="sample/")

class Student(models.Model):
    code = models.CharField(max_length=10)
    class_code = models.CharField(max_length=10)
    email = models.CharField(max_length=254)

class Submission(models.Model):
    assignment_id = models.CharField(max_length=6)
    code = models.CharField(max_length=10)
    class_code = models.CharField(max_length=10)
    email = models.CharField(max_length=254)
    location = models.FileField(upload_to="student/")
    grade = models.CharField(max_length=10)
