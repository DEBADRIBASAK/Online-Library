from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import Student,Issue,Book
from .forms import StudentForm
from django.contrib.auth.models import User
from django.http import  HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import datetime
# Create your views here.

def home(request):
    return render(request,'new1.html')

def userRegister(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            raw_password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=raw_password)
            return redirect('/Libr/studentRegister')
        else:
            form=UserCreationForm()
    return render(request,'user_register.html',{'form':form})



def studentRegister(request):
    if request.method=='POST':
        form=StudentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/Libr/home')
    else:
        form=StudentForm()
    return render(request,'register3.html',{'form':form})
    
def logging(request):
    response={}
    a=request.user.is_authenticated
    if a:
        obj1=request.user
        obj=Student.objects.get(username=obj1)
        obj2=Issue.objects.filter(stud=obj)
        return render(request,'profile_page.html',{'profile':obj,'booklist':obj2})

    elif request.method=='POST':
        usr=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=usr,password=password)
        if user is None:
            return render(request,'Log_in1.html',{'isvalid':False})
        else:
            login(request,user)
            obj=Student.objects.get(username=user)
            obj2=Issue.objects.filter(stud=obj)
            #for any in obj2:
                #print(any.bookissue.Name)

            return render(request,'profile_page.html',{'profile':obj,'booklist':obj2})
    return render(request,'Log_in1.html',{'isvalid':True})

def list_books(request):
    response={}
    obj3 = Book.objects.all()
    return render(request,'books.html',{'books':obj3,'isvalid':True})

def issue_a_book(request,bookname):
   response={}
   current_user = request.user
   obj = Student.objects.get(username=current_user)
   if obj.NoofBooks==4:
    obj3 = Book.objects.all()
    return render(request,'books.html',{'books':obj3,'isvalid':False})
   else:
    obj2 = Book.objects.get(callno=bookname)
    obj2.is_available=False
    is1 = Issue()
    obj.NoofBooks=obj.NoofBooks+1
    is1.stud = obj
    is1.bookissue = obj2
    is1.save()
    obj2.save()
    obj.save()
    print(obj.Name)
    print(bookname)
    return redirect('/Libr/books')



def re_issue(request,booknum):
    response={}
    obj2 = request.user
    obj3 = Student.objects.get(username=obj2)
    obj1 = Book.objects.get(callno=booknum)
    obj = Issue.objects.get(stud=obj3,bookissue=obj1)
    obj.issue_date=datetime.date.today()
    if obj.issue_date>obj.due_date:
        b=(obj.issue_date-obj.due_date).days
        b=b*1
        a=obj3.Fine
        a=a+b
        obj3.Fine=a
        obj3.save()
    obj.due_date=datetime.date.today()+datetime.timedelta(days=30)
    obj.save()
    return redirect('/Libr/logging')

def logout_view(request):
    logout(request)
    return redirect('/Libr/home')

def select_books(request):
    if request.method=='POST':
        part_of_name=request.POST['searchkey']
        obj1=Book.objects.filter(Name__contains=part_of_name)
        obj2=Book.objects.filter(Author__contains=part_of_name)
        obj3=Book.objects.filter(Subject__contains=part_of_name)
        #obj4=Book.objects.filter(callno__contains=part_of_name)
        obj=(obj1|obj2|obj3).distinct()
        return render(request,'books.html',{'books':obj,'isvalid':True})

def Contrib(request):
    response={}
    if request.method=='POST':
        obj=Book()
        obj.Name=request.POST['BookName']
        obj.Author=request.POST['Author']
        obj.callno=request.POST['CallNo']
        obj.accno=request.POST['AccNo']
        obj.Subject=request.POST['Subject']
        obj1=request.user
        obj2=Student.objects.get(username=obj1)
        obj2.NoofContrib=obj2.NoofContrib+1
        obj.Cotributer=obj2.Name
        obj.save()
        obj2.save()
        return redirect('/Libr/logging')
    return render(request,'Contribute.html',response)

def register(request):
    form=UserCreationForm()
    form2=StudentForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            raw_password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=raw_password)
            form2=StudentForm(request.POST,request.FILES)
            form2.username=user
            if form2.is_valid():
                form2.save()
            #return render(request,'register2.html',{'form':form,'form2':form2})
            
        else:
            form=UserCreationForm()
            form2=StudentForm()
    return render(request,'register2.html',{'form':form,'form2':form2})

def removebook(request,booknum):
    usr=request.user
    if usr.is_staff:
        response={}
        obj1=Book.objects.get(callno=booknum)
        obj=Issue.objects.get(bookissue=obj1)
        obj1.is_available=True
        obj1.save()
        obj.stud.NoofBooks=obj.stud.NoofBooks-1
        d=datetime.date.today()
        if d>obj.due_date:
            b=(d-obj.due_date).days
            b=b*1
            a=obj.stud.Fine
            a=a+b
            obj.stud.Fine=a
            obj.stud.save()
        obj.delete()
        render(request,'remove.html',response)
    else:
        return HttpResponse('<h2>You have no permission to access this page</h2>')

def allissues(request):
    obj=Issue.objects.all()
    return render(request,'remove.html',{'issues':obj})

def about(request):
    response={}
    return render(request,'about.html',response)


