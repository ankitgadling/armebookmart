# Create your views here.
from django.shortcuts import render, redirect
from .models import  CartItems, UserEbook, PdfToMp3, Order
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.contrib.auth.models import User
import PyPDF2
from gtts import gTTS
import pyttsx3
import os 
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
import random

def home(request):
	cart_items=CartItems.objects.all()
	cart_item_total=0
	for item in cart_items:
		cart_item_total+=1
	booklist=list(UserEbook.objects.all())
	#randombooklist=random.sample(booklist,4)
	ebooks={'userbooks': booklist,'cart_item_total':cart_item_total}
	if request.method=="GET":
		st=request.GET.get('search')
		if st!=None:
			ebooks={
				'userbooks':UserEbook.objects.filter(title__icontains=st),'cart_item_total':cart_item_total
			}

	return render(request, "index.html", ebooks)


def all_books(request):
	cart_items=CartItems.objects.all()
	cart_item_total=0
	for item in cart_items:
		cart_item_total+=1
	ebooks={'userbooks': UserEbook.objects.all(),'cart_item_total':cart_item_total}
	if request.method=="GET":
		st=request.GET.get('search')
		if st!=None:
			ebooks={
				'userbooks':UserEbook.objects.filter(title__icontains=st), 'cart_item_total':cart_item_total
			}
	return render(request, "books.html", ebooks)


#def search(request):
#	if request.method=="GET":
#		st=request.GET.get('search')
#		if st!=None:
#			ebooks={
#				'ebooks':Ebook.objects.filter(title__icontains=st), 'userbooks':UserEbook.objects.filter(title__icontains=st)
#			}
#	return redirect('allbooks/')


#@ xframe_options_sameorigin
#def view(request, slug):
#	cart_items=CartItems.objects.all()
#	cart_item_total=0
#	for item in cart_items:
#		cart_item_total+=1
#	newebooks=Ebook.objects.get(slug=slug)
#	newebooks={'newebooks':newebooks, 'cart_item_total':cart_item_total}
#	#ebooks={'ebooks':Ebook.objects.all()}
#	return render(request, "view.html",newebooks)

@ xframe_options_sameorigin
def viewuserbook(request, slug):
	cart_items=CartItems.objects.all()
	cart_item_total=0
	for item in cart_items:
		cart_item_total+=1
	newebooks=UserEbook.objects.get(slug=slug)
	newebooks={'newebooks':newebooks, 'cart_item_total':cart_item_total}
	#ebooks={'ebooks':Ebook.objects.all()}
	return render(request, "view.html",newebooks)

def cart(request):
	cart_items= CartItems.objects.all()
	cart_total = 0
	cart_item_total=0
	for item in cart_items:
		cart_total += item.price
		cart_item_total+=1
	return render(request, "cart.html",
	{
		'cart_items' : cart_items,
		'cart_total': cart_total,
		'cart_item_total': cart_item_total

	}
	
	)


def buy(request):
	return render(request, "buy.html")
#@ csrf_exempt
#def add_cart_item(request):
#	book_id=request.POST['book_id']
#	title = Ebook.objects.get(pk=book_id).title
#	price = Ebook.objects.get(pk=book_id).price
#	if CartItems.objects.filter(title=title):
#		messages.info(request, 'The Ebook is already in Cart')
#		return redirect('cart')
#	else:
#		item= CartItems.objects.create(title=title, price=price)
#		messages.success(request, 'Ebook Added Sucessfully')
#		return redirect('cart')//

@ csrf_exempt
def add_cart_user_item(request):
	book_id=request.POST['book_id']
	title = UserEbook.objects.get(pk=book_id).title
	price = UserEbook.objects.get(pk=book_id).price
	if CartItems.objects.filter(title=title):
		messages.info(request, 'The Ebook is already in the Cart')
		return redirect('cart')
	else:
		item= CartItems.objects.create(title=title, price=price)
		messages.success(request, 'Ebook Sucessfully added to Cart')
		return redirect('cart')

@ csrf_exempt
def del_cart_item(request):
	item_id =request.POST['item_id']
	CartItems.objects.get(pk=item_id).delete()
	messages.error(request, 'Cart Item Removed', extra_tags='remove')
	return redirect('cart')


def checkout(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			cart_items= CartItems.objects.all()
			customer=request.user
			for item in cart_items:
				ebooks=UserEbook.objects.filter(title=item.title)
				order=Order.objects.create(title=item.title,ebooks=ebooks[0],customer=customer,status=True)
				order.save()
			cart_items.delete( )
			return render(request,"ordersucess.html")
	else:
		return redirect('signin')







	if request.method=='POST':
		cart_items= CartItems.objects.all()
		customer=request.user
		for item in cart_items:
				ebooks=UserEbook.objects.filter(title=item.title)
				order=Order.objects.create(title=item.title,ebooks=ebooks[0],customer=customer,status=True)
				order.save()
		cart_items.delete( )
		return render(request,"ordersucess.html")
	


def user(request):
	cart_items=CartItems.objects.all()
	cart_item_total=0
	for item in cart_items:
		cart_item_total+=1
	books={'books': UserEbook.objects.filter(author=request.user), 'cart_item_total': cart_item_total,'pbooks':Order.objects.filter(customer=request.user)}
	return render(request,"user.html", books)

@ csrf_exempt
def update_username(request):
	if request.method=='POST':
		username=request.POST['username']
		first_name=request.POST['fname']
		last_name=request.POST['lname']
		myuser=User.objects.filter(username=username).update(first_name=first_name, last_name=last_name)
		return redirect('/user')

@ csrf_exempt
def upload_book(request):
	if request.method=='POST':
		title=request.POST['title']
		cover=request.FILES['cover']
		book=request.FILES['book']
		bookaudio=request.FILES['bookaudio']
		newbook=UserEbook.objects.create(author=request.user, title=title,price=00,cover=cover,book=book,bookaudio=bookaudio)
		newbook.save()
		return redirect('/user')


@ csrf_exempt
def delete_book(request):
	if request.method=='POST':
		book_id=request.POST['book_id']
		UserEbook.objects.get(pk=book_id).delete()
		return redirect('/user')




def pdf_to_mp3_converter(request):
	return render(request,"pdftomp3.html")

def convert(request):
	if request.method=='POST':
		book=request.FILES.get('pdf')
		obj=PdfToMp3()
		obj.book=book
		obj.save()
		book=PdfToMp3.objects.last()
		bookurl=str(book.book.url)
		print(bookurl)
		path='D:\Mini Project\ankitgadling\armebookmart\media\audio'
		pdfFileObj = open('D:/Mini Project/ankitgadling/armebookmart/'+bookurl, "rb")
		pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
		totalpages=pdfReader.numPages
		print(totalpages)
		if totalpages > 300:
			messages.error(request, 'File is Too Large to convert please upload another file',extra_tags='largefile')
			return redirect('/pdftomp3converter/')
		mytext = ""
		for pageNum in range(pdfReader.numPages):
			pageObj = pdfReader.getPage(pageNum)
			mytext += pageObj.extractText()
		print(mytext)
		pdfFileObj.close()
		PdfToMp3.objects.all().delete()
		engine = pyttsx3.init()
		engine.save_to_file(mytext,"media/audio/audiobook.mp3")
		engine.runAndWait()
		#tts = gTTS(text=mytext, lang='en')
		#tts.save("media/audio/audiobook.mp3")
		return render(request, 'mp3sucess.html')


def about_us(request):
	return render(request,"aboutus.html")

def contact_us(request):
	return render(request,"contactus.html")

def terms_and_conditions(request):
	return render(request,"termsandconditions.html")