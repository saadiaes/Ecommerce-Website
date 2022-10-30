from django.shortcuts import render
from .models import Order, Products
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View
from django.template.loader import render_to_string




# Create your views here.

def produits(request):
    product_objects=Products.objects.all()

    item_name=request.GET.get('item_name')
    if item_name !='' and item_name is not None:
        product_objects=product_objects.filter(title=item_name)

    paginator=Paginator(product_objects,4)
    page=request.GET.get('page')
    product_objects=paginator.get_page(page)
    
    return render(request,'shop/produits.html',{'product_objects':product_objects})
    
class index(View):
     def get(self,request):
       return render(request,'shop/index.html')   

def detail(request,id):
    product_object=Products.objects.get(id=id)
    return render(request,'shop/detail.html',{'product_object':product_object})
def checkout(request):
    if request.method=="POST":
       items=request.POST.get('items','')
       name=request.POST.get('name',"")
       email=request.POST.get('email',"")
       adress=request.POST.get('adress',"")
       city=request.POST.get('city',"")
       state=request.POST.get('state',"")
       Zipcode=request.POST.get('Zipcode',"")
       order=Order(items=items,name=name,email=email,adress=adress,city=city,state=state,Zipcode=Zipcode)
       order.save()
    return render(request,'shop/checkout.html')


   
class addTocart(View):
    def get(self,request):
        
        cart_p={}
        cart_p[str(request.GET['id'])]={
		    'image':request.GET['image'],
		    'title':request.GET['title'],
		    'qty':request.GET['qty'],
		    'price':request.GET['price'],
	    }
        if 'cartdata' in request.session:
            if str(request.GET['id']) in request.session['cartdata']:
                cart_data=request.session['cartdata']
                cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
                cart_data[str(request.GET['id'])]['price']=float(cart_p[str(request.GET['id'])]['price'])
                cart_data.update(cart_data)
                request.session['cartdata']=cart_data
            else:
                cart_data=request.session['cartdata']
                cart_data.update(cart_p)
                request.session['cartdata']=cart_data
        else:
            request.session['cartdata']=cart_p
        return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

class ShoppingCartDetail(View):
    def get(self,request):
        total_amt=0
        try:
            for p_id,item in request.session['cartdata'].items():
                total_amt+=int(item['qty'])*float(item['price'])
            context={
                'items':request.session['cartdata'],
                'totalitems':len(request.session['cartdata']),
                'total_amt':total_amt,
            }
            return render(request, 'shop/cart.html',context)
        except KeyError:
            return render(request, 'shop/cart.html',{'total_amt':total_amt,'totalitems':0})

# Delete cart
def delete_cart_item(request):
	p_id=str(request.GET['id'])
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			del request.session['cartdata'][p_id]
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# Update cart

def update_cart_item(request):
	p_id=str(request.GET['id'])
	p_qty=request.GET['qty']
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=p_qty
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})



