from django.urls import path
from . import views


urlpatterns = [
	path("", views.home, name="home"),
	#path("view/<slug>", views.view, name='view'),
	path("viewuserbook/<slug>", views.viewuserbook, name='view'),
	path("cart", views.cart, name="cart"),
	#path("cart_add_item/",views.add_cart_item),
	#path("allbooks/cart_add_item/", views.add_cart_item),
	path("allbooks/cart_add_user_item/",views.add_cart_user_item),
	path("cart_add_user_item/", views.add_cart_user_item),
	path("del_cart_item/",views.del_cart_item),
	path("checkout",views.checkout),
	path("user/", views.user),
	path("allbooks/", views.all_books),
	path("user/update_username/", views.update_username),
	path("user/upload_book/",views.upload_book),
	path('user/delete_book',views.delete_book),
	path("pdftomp3converter/",views.pdf_to_mp3_converter),
	path("pdftomp3converter/convert/", views.convert),
	path("aboutus", views.about_us),
	path("contactus",views.contact_us),
	path("terms-and-conditions",views.terms_and_conditions),
	path("buy",views.buy)
]


