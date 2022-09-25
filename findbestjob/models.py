from django.db import models

#  Create your models here.
#  
#  You can install dbeaver(https://dbeaver.io/) to inspect your db.
#  
#  after changing models, update db:
#   
#       python manage.py makemigrations
#       python manage.py migrate


class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    account=models.CharField(verbose_name="Account", null=False, unique=True,max_length=200)
    name = models.CharField(verbose_name="Name",max_length=200)
    
    password=models.CharField(verbose_name="Password",max_length=200)
    age    =models.IntegerField(verbose_name="Age",default=15) 
    gender =models.IntegerField(verbose_name="Gender",default=1) # 1 Male  2：Female
    address=models.CharField(verbose_name="Address",max_length=200)
    
    #date = models.DateTimeField(verbose_name="Date of creation", auto_now_add=True)
 

class Answer(models.Model):
    id  = models.BigAutoField(primary_key=True)
    sid = models.BigIntegerField(null=True)   # Student id
    q1  = models.CharField(verbose_name="Question 1",max_length=10,null=True)
    q2  = models.CharField(verbose_name="Question 2",max_length=10,null=True)
    q3  = models.CharField(verbose_name="Question 3",max_length=10,null=True)
    q4  = models.CharField(verbose_name="Question 4",max_length=10,null=True)
    q5  = models.CharField(verbose_name="Question 5",max_length=10,null=True)
    
     
class Job(models.Model):
    id = models.BigAutoField(primary_key=True)
    title=models.CharField(verbose_name="Job position",max_length=200)
    company =models.CharField(verbose_name="Company name",max_length=200)
    ind1=models.IntegerField(verbose_name="Index1",default=1)
    ind2=models.IntegerField(verbose_name="Index2",default=1)
    ind3=models.IntegerField(verbose_name="Index3",default=1)
    ind4=models.IntegerField(verbose_name="Index4",default=1)
    ind5=models.IntegerField(verbose_name="Index5",default=1)
    ind6=models.IntegerField(verbose_name="Index6",default=1)
    


