from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

class Student(models.Model):
    username=models.ForeignKey(User,unique=True,on_delete=False)
    Name=models.CharField(max_length=100,blank=False)
    RollNo=models.CharField(max_length=6,blank=False)
    Branch=models.CharField(max_length=10,blank=False)
    Fine=models.FloatField(default=0)
    Pic=models.FileField(upload_to='docs/')
    NoofBooks=models.IntegerField(default=0)
    NoofContrib=models.IntegerField(default=0)
    def __str__(self):
        return str(self.Name)

class Book(models.Model):
    callno=models.CharField(max_length=20,blank=False)
    accno=models.CharField(max_length=20,blank=False)
    Name=models.CharField(max_length=100,blank=False)
    Author=models.CharField(max_length=100,blank=False)
    Subject=models.CharField(max_length=100,blank=False)
    is_available=models.BooleanField(default=True)
    contributer=models.CharField(max_length=255,default='Authority')
    def __str__(self):
        return str(self.Name)
    class Meta:
        unique_together=('callno','accno',)

class Issue(models.Model):
    stud=models.ForeignKey(Student,null=False,on_delete=False)
    bookissue=models.ForeignKey(Book,null=False,on_delete=False)
    issue_date=models.DateField(default=datetime.date.today())
    due_date=models.DateField(default=(datetime.date.today()+datetime.timedelta(days=30)))
    class Meta:
        unique_together=('stud','bookissue',)
