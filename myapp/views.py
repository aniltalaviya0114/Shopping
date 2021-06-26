from django.shortcuts import render,redirect
from . models import *
import random
from django.conf import settings 
from django.core.mail import send_mail
from django.http import JsonResponse
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# Create your views here.

def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'pay.html')
    try:
        made_by=Register.objects.get(email=request.session['email'])
        amount = int(request.POST['amount'])
        
    except:
        return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=made_by, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)


def validate_email(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Register.objects.filter(email__iexact=username).exists()
    }
    return JsonResponse(data)

def index(request):
	return render(request,'index.html')

def about(request):
	return render(request,'about.html')

def service(request):
	return render(request,'service.html')

def shop(request):
	return render(request,'shop.html')


def product(request):
	return render(request,'product.html')

def contact(request):
	if request.method=="POST":
		Contact.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			phone=request.POST['phone'],
			address=request.POST['address']
		)
		msg="Successfully "
		return render(request,'contact.html',{'mag':msg})
	else:
		msg="incorrect form"
		return render(request,'contact.html',{'msg':msg})

def single(request):
	return render(request,'single.html')

def hearder(request):
	return render(request,'hearder.html')

def register(request):
	if request.method=="POST":
		Register.objects.create(
				fname=request.POST['fname'],
				lname=request.POST['lname'],
				email=request.POST['email'],
				password=request.POST['password'],
				phone=request.POST['phone'],
				address=request.POST['address'],
				usertype=request.POST['usertype'],
				image=request.FILES['image']
			)
		user=Register.objects.get(email=request.POST['email'])
		if user:
			rec=[request.POST['email'],]
			subject="OTP Forgot Password"
			otp=random.randint(1000,9999)
			message="Your OTP Forgot Password Is "+str(otp)
			email_from=settings.EMAIL_HOST_USER
			send_mail(subject,message,email_from,rec)
			
			return render(request,'otp.html',{'otp':otp,'email':request.POST['email']})
		else:
			pass
	else:
		return render(request,'register.html')

def login(request):
	if request.method=="POST":
		try:
			user=Register.objects.get(email=request.POST['email'])
			#,password=request.POST['password']
			if user.password==request.POST['password']:
				if user.usertype=="user":
					request.session['fname']=user.fname
					request.session['email']=user.email
					request.session['image']=user.image.url
					return render(request,'index.html')
				elif user.usertype=="saller":
					request.session['fname']=user.fname
					request.session['email']=user.email
					request.session['image']=user.image.url
					return render(request,'saller_login.html')
			else:
				return render(request,'login.html')
		except:
			return render(request,'login.html')
	else:
		return render(request,'login.html')

def validate_otp(request):
	otp1=request.POST['otp1']
	otp2=request.POST['otp2']
	email=request.POST['email']

	user=Register.objects.get(email=request.POST['email'])
	
	if otp1==otp2:
		user.status="active"
		user.save()
		return render(request,'login.html')
	else:
		return render(request,'otp.html',{'otp':otp1,'email':email})


def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['image']
		return render(request,'login.html')
	except:
		return render(request,'login.html')

def saller_login(request):
	return render(request,'saller_login.html')

def saller_add_product(request):
	if request.method=="POST":
		saller=Register.objects.get(email=request.session['email'])
		Product.objects.create(
				saller=saller,
				product_brand=request.POST['product_brand'],
				product_price=request.POST['product_price'],
				product_desc=request.POST['product_desc'],
				product_image=request.FILES['product_image']
			)
		return render(request,'saller_add_product.html')
	else:
		return render(request,'saller_add_product.html')

def saller_index(request):
	return render(request,'saller_index.html')

def saller_view_product(request):
	saller=Register.objects.get(email=request.session['email'])
	product=Product.objects.filter(saller=saller)
	return render(request,'saller_view_product.html',{'product':product})

def saller_details_product(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'saller_details_product.html',{'product':product})


def saller_edit_product(request,pk):
	product=Product.objects.get(pk=pk)

	if request.method=="POST":

		product.product_brand=request.POST['product_brand']
		product.product_price=request.POST['product_price']
		product.product_desc=request.POST['product_desc']

		try:
			product.product_image=request.FILES['product_image']
			product.save()
			return redirect('saller_view_product')

		except:
			product.save()
			return redirect('saller_view_product')
	else:
		return render(request,'saller_edit_product.html',{'product':product})

def saller_delete_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	return redirect('saller_view_product')

def user_view_product(request,pb):
	if pb=="all":
		product=Product.objects.all()
		return render(request,'user_view_product.html',{'product':product})
	else:
		product=Product.objects.filter(product_brand=pb)
		return render(request,'user_view_product.html',{'product':product})

def user_details_product(request,pid):
	flag=False
	flag1=False
	user=Register.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pid)
	try:
		Wishlist.objects.get(user=user,product=product)
		flag=True
	except:
		pass
	try:
		Cart.objects.get(user=user,product=product)
		flag1=True
	except:
		pass
	return render(request,'user_details_product.html',{'product':product,'flag':flag,'flag1':flag1})

def mywishlist(request):
	user=Register.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlists)
	return render(request,'mywishlist.html',{'wishlists':wishlists})

def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=Register.objects.get(email=request.session['email'])
	Wishlist.objects.create(user=user,product=product)
	return redirect('mywishlist')

def remove_from_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=Register.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.get(user=user,product=product)
	wishlists.delete()
	return redirect('mywishlist')

def mycart(request):
	net_price=0
	user=Register.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user)
	for i in carts:
		net_price=net_price+int(i.total_price)
	request.session['cart_count']=len(carts)
	return render(request,'mycart.html',{'carts':carts,'net_price':net_price})

def add_to_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=Register.objects.get(email=request.session['email'])
	Cart.objects.create(
			user=user,
			product=product,
			price=product.product_price,
			total_price=product.product_price
		)
	return redirect('mycart')

def remove_from_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=Register.objects.get(email=request.session['email'])
	carts=Cart.objects.get(user=user,product=product)
	carts.delete()
	return redirect('mycart')

def change_qty(request):
	carts=Cart.objects.get(pk=request.POST['pk'])
	qty=request.POST['qty']
	carts.qty=qty
	carts.total_price=int(qty)*int(carts.price)
	carts.save()
	return redirect('mycart')

def user_product_search(request):
	if request.method=="POST":
		product_brand=request.POST['product_brand']
		product=Product.objects.filter(product_brand=product_brand)
		return render(request,'user_product_search.html',{'product':product})
	else:
		return render(request,'user_product_search.html')