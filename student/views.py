from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import UpdateProfileForm,UserProfileForm
from .models import Redeem, RewardedItem, Student
from django.core.exceptions import ObjectDoesNotExist
from leadership.models import RedeemableItem, Transaction, User, Wallet
from django.http import JsonResponse
import json
from .models import  *
from django.core.exceptions import ObjectDoesNotExist
from leadership.models import RedeemableItem, Transaction, Wallet

from django.contrib.auth.decorators import login_required
from leadership.views import view_student_leaderboard
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.decorators import user_passes_test

def group_required(Students):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if u.groups.filter(name='Students').exists() :
                return True
            else:
                return False
        return redirect('login')
    return user_passes_test(in_groups)

@login_required(login_url='login') 
@group_required('Students')
def student_profile(request):
    try:
        userprofile = request.user.userprofile
    except ObjectDoesNotExist:
        userprofile = Student(user=request.user)
        
    if request.method == 'POST':
        user_form = UpdateProfileForm(request.POST, request.FILES,instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile.user)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            #user.username = user.email
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('student_dashboard')
    else:
        profile_form = UserProfileForm(instance=request.user.userprofile)
        user_form = UpdateProfileForm(instance=request.user)
    args = {
        'user_form': user_form, # basic user form
        'profile_form': profile_form # user profile form
        }
    return render(request, 'student_profile.html', args)

@login_required(login_url='login') 
@group_required('Students')
def view_profile(request,id):
    user_id=User.objects.get(id=id)
    return render(request,"view_profile.html",{'user_id':user_id})


@login_required(login_url='login') 
@group_required('Students') 
def redeem(request):
    try:
        if request.user.is_authenticated:
            student_customer = Student.objects.get(user = request.user)
            order, created = Redeem.objects.get_or_create(student=student_customer, complete = False)
            items = order.rewardeditem_set.all()
            cartItems = order.calculate_cart_items
        else:
            items= []
            order={'get_cart_total':0,'get_cart_items':0}
            # cartItems = order['get_cart_items']
        reward_items=RedeemableItem.objects.all()
        bal = Wallet.objects.all().filter(owner = request.user)
        for reward in reward_items:
            if reward.activate_page == False:
                return render(request,'inactive_redeem.html',{'bal':bal, 'items':items})
        return render(request,'redeem.html',{'reward_items':reward_items,'bal':bal, 'items':items, 'cartItems':cartItems})
    except ObjectDoesNotExist:
        return render(request,'forbidden.html')

@login_required(login_url='login')    
@group_required('Students') 
def redeem_failed(request):
    bal = Wallet.objects.all().filter(owner = request.user)
    return render(request,'RedeemFailed.html',{'bal':bal})


@login_required(login_url='login') 
@group_required('Students')
def redeem_success(request):
    if request.user.is_authenticated:
        student_customer = Student.objects.get(user = request.user)
        order, created = Redeem.objects.get_or_create(student=student_customer, complete = False)
        items = order.rewardeditem_set.all()
        print(items)
    else:
        items= []
    context = {'items':items, 'order':order}  
    return render(request,'RedeemSucceed.html',context)

@login_required(login_url='login') 
@group_required('Students')
def cart(request):
    try:
        bal = Wallet.objects.all().filter(owner = request.user)
        if request.user.is_authenticated:
            student_customer = Student.objects.get(user = request.user)
            # student_customer = request.user.role==3
            
            order, created = Redeem.objects.get_or_create(student=student_customer, complete = False)
            
            items = order.rewardeditem_set.all()
            for item in items:
                item.save()
            
            # cartItems = order.calculate_cart_items()
        else:
            items= []


            order={'calculate_cart_total':0, 'calculate_cart_items':0}
        

        context = {'items':items, 'order':order,'bal':bal}    
        return render(request,'cart.html', context)
    except ObjectDoesNotExist:
        return render(request,'forbidden.html')
    
@login_required(login_url='login')     
@group_required('Students')
def redeem_active(request):
    return render(request,'redeem_active.html')

@login_required(login_url='login') 
@group_required('Students')
def student_dashboard(request):
    try:
        student=Student.objects.get(user=request.user)
        redeems = Redeemed.objects.filter(student=student).last()
        transactions = Transaction.objects.all().filter(receiver = request.user.username)[:4]
        students=Wallet.objects.all().order_by('-choinBalance')[:3]
        choin_balance=Wallet.objects.all().filter(owner=request.user)
        data={'student':student,'choin_balance':choin_balance,'students':students,'transactions':transactions, 'redeems':redeems}
        return render(request,'stud_dashboard.html',data)
    except ObjectDoesNotExist:
        return render(request,'forbidden.html')


@login_required(login_url='login') 
@group_required('Students')
def student_transactions(request):
    try:
        transact = Transaction.objects.all().filter(receiver = request.user.username)
        bal = Wallet.objects.all().filter(owner = request.user)
        paginator = Paginator(transact, 5)
        page = request.GET.get('page')
        transactions = paginator.get_page(page)
        return render(request,'student_transactions.html',{'transactions':transactions,'bal':bal})
    except:
        return render(request,'forbidden.html')  


@login_required(login_url='login') 
@group_required('Students')
def update_item(request):
    data = json.loads(request.body)
    productId = data['productId'] 
    action = data['action']
    student_customer = Student.objects.get(user = request.user)
    product = RedeemableItem.objects.get(id=productId)
    order, created = Redeem.objects.get_or_create(student=student_customer, complete = False)
    orderItem, created = RewardedItem.objects.get_or_create(order = order, reward=product )

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
         orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.student = Student.objects.get(user=request.user)
    orderItem.save()

    if orderItem.quantity <= 0:
       orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@login_required(login_url='login') 
@group_required('Students')
def student_redeem(request):
    try:
        bal = Wallet.objects.all().filter(owner = request.user)
        std = Student.objects.get(user = request.user)
        order = Redeem.objects.all().filter(student = std)
        the_balance=None
        item =RedeemableItem.objects.get(id =1)
    except ObjectDoesNotExist:
        return render(request,'forbidden.html')
    
    for b in bal:
        for ord in order:

            if b.choinBalance < ord.calculate_cart_total:
                return redirect('redeem_failed')
            else:
                
     
                wallets=Wallet.objects.all().filter(owner=request.user)
                the_balance =b.choinBalance - ord.calculate_cart_total
               

                red = Redeem.objects.all().filter(student = std)
                i=Redeemed.objects.create (product = item ,quantity =ord.calculate_cart_items,total =ord.calculate_cart_total,student =std)
                i.save()
                print(i)
                
                red.delete()
                
                
                
                wallets.update(owner = request.user, choinBalance = the_balance)

    return render(request,'RedeemSucceed.html',{'the_balance':the_balance,'order':order})  


@login_required(login_url='login') 
@group_required('Students')
def my_items(request):
    try:
        std = Student.objects.get(user = request.user)
        redeems = Redeemed.objects.all().filter(student = std )
        return render(request,'my_items.html',{'redeems':redeems})    
    except ObjectDoesNotExist:
        return render(request,'forbidden.html')      

