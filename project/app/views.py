from django.shortcuts import render,redirect
from django.http import HttpResponse
from  django.core.files.storage import FileSystemStorage
from django.conf import settings
from .encryption import decrypt_file,derive_key_from_password 
from .models import User
from .models import EncryptedFile
from .models import DecryptionRequest



def index(request):
    return render(request,'login.html')

def reg(request):
    return render(request,'register.html')


def userregistration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        context={'message':'registerd successfully'}

        if User.objects.filter(username=username).exists():
            return HttpResponse('Email already exists')

        if User.objects.filter(email=email).exists():
            return HttpResponse('Email already exists')
        
        data = User(username=username,email=email,password=password)
        data.save()
        return render(request,'login.html',context)
    
    else:
        return render(request,'register.html')
    

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    context={'message':'Invalid User Credentials'}

    if User.objects.filter(username=username,password=password).exists():
        userdetail=User.objects.get(username=request.POST['username'], password=password)
        if userdetail.password == request.POST['password']:
            request.session['uid'] = userdetail.id
          

            return redirect(userprofile)
        else:
            return render(request,'login.html',context)
        
    else:
        return render(request, 'login.html', {'status': 'Invalid Username or Password'})
    


def userprofile(request):
    tem=request.session['uid']
    vpro=User.objects.get(id=tem)
    return render(request,'landing.html',{'result':vpro})


def update(request,id):
    upt=User.objects.get(id=id)
    return render(request,'profileedit.html',{'result':upt})

def userupdate(request,id):
    if request.method=="POST":
        email=request.POST.get('email')
        username = request.POST.get('username')
        password=request.POST.get('password')
        registration=User(username=username,email=email,password=password,id=id)
        registration.save()
        return redirect(userprofile)
    

def upload_file(request):
    if request.method == 'POST':
        tem=request.session['uid']
        uploaded_file = request.FILES.get('file')
        password = request.POST.get('password')
        algorith = request.POST.get('algorith')


        if uploaded_file:  # Check if a file was uploaded
            # Retrieve the user from the session
            
            vpro=User.objects.get(id=tem)
        
            
            if vpro:
                # Save the uploaded file to the model associated with the user
                encrypted_file = EncryptedFile(user_id=vpro, file=uploaded_file, password=password,algorith=algorith)
                encrypted_file.save()

                return redirect(userprofile)  # Redirect to the user profile page
            else:
                return HttpResponse("error")
        else:
            return HttpResponse("Error: No file uploaded")
    else:

        return redirect(userprofile)


def select(request):
    tem = request.session['uid']
    vpro = User.objects.get(id=tem)
    encrypted_files = EncryptedFile.objects.filter(user_id=vpro)
    return render(request,'select.html',{'encrypted_files': encrypted_files})

def history(request):
    tem = request.session['uid']
    vpro = User.objects.get(id=tem)
    encrypted_files = EncryptedFile.objects.filter(user_id=vpro)
    return render(request,'history.html',{'encrypted_files':encrypted_files})


 # Import your decryption function



def decrypt(request):
    if request.method == 'POST':
        tem = request.session.get('uid')
        uploaded_file = request.FILES.get('file')
        password = request.POST.get('password')
        algorith = request.POST.get('algorithm')
        
        if uploaded_file:  # Check if a file was uploaded
            # Retrieve the user from the session
            
            vpro=User.objects.get(id=tem)
        
            
            if vpro:
                # Save the uploaded file to the model associated with the user
                decrypted_file = DecryptionRequest(user_id=vpro, uploaded_file=uploaded_file, password=password, algorith=algorith)
                decrypted_file.save()

                return redirect(userprofile)  # Redirect to the user profile page
            else:
                return HttpResponse("error")
        else:
            return HttpResponse("Error: No file uploaded")
    else:

        return redirect(userprofile)

