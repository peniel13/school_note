from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'base/index.html')



def contact(request):
    return render(request,'base/contact.html')


def apropos(request):
    return render(request,'base/apropos.html')