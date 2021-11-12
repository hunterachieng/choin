from django.shortcuts import redirect, render
from leadership.models import Metrics, Transaction
from trainer.models import Trainer
from .forms import TrainerUpdateProfileForm, TrainerUserProfileForm
from django.core.exceptions import ObjectDoesNotExist
import csv, io
from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.paginator import Paginator
from student.models import Student
from trainer.models import Trainer
from .models import *
from leadership.forms import AddMetricsForm
from RewardSystem.settings import EMAIL_HOST_USER
from django.core import mail
from django.core.mail import send_mail
import datetime
import hashlib
import json
from uuid import uuid4
import socket
from urllib.parse import urlparse
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt #New
from django.db.models import Q
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = [] #New
        self.create_block(nonce = 1, previous_hash = '0')
        self.nodes = set() #New
    def create_block(self, nonce, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'nonce': nonce,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions #New
                }
        self.transactions = [] #New
        self.chain.append(block)
        return block
    def get_last_block(self):
        return self.chain[-1]
    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_nonce = False
        while check_nonce is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_nonce = True
            else:
                new_nonce += 1
        return new_nonce
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    def add_transaction(self, sender, receiver, amount, time): #New
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount,
                                  'time': str(datetime.datetime.now())})
        previous_block = self.get_last_block()
        return previous_block['index'] + 1
    def add_node(self, address): #New
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    def replace_chain(self): #New
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
# Creating our Blockchain
blockchain = Blockchain()
# Creating an address for the node running our server
node_address = str(uuid4()).replace('-', '') #New
root_node = 'e36f0158f0aed45b3bc755dc52ed4560d' #New

# Getting the full Blockchain
def get_chain(request):
    if request.method == 'GET':
        response = {'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
    return JsonResponse(response)
# Checking if the Blockchain is valid
def is_valid(request):
    if request.method == 'GET':
        is_valid = blockchain.is_chain_valid(blockchain.chain)
        if is_valid:
            response = {'message': 'All good. The Blockchain is valid.'}
        else:
            response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return JsonResponse(response)
# Adding a new transaction to the Blockchain
@csrf_exempt
def add_transaction(request): #New
    if request.method == 'POST':
        received_json = json.loads(request.body)
        transaction_keys = ['sender', 'receiver', 'amount','time']
        if not all(key in received_json for key in transaction_keys):
            return 'Some elements of the transaction are missing', HttpResponse(status=400)
        index = blockchain.add_transaction(received_json['sender'], received_json['receiver'], received_json['amount'],received_json['time'])
        response = {'message': f'This transaction will be added to Block {index}'}
    return JsonResponse(response)
# Connecting new nodes
@csrf_exempt
def connect_node(request): #New
    if request.method == 'POST':
        received_json = json.loads(request.body)
        nodes = received_json.get('nodes')
        if nodes is None:
            return "No node", HttpResponse(status=400)
        for node in nodes:
            blockchain.add_node(node)
        response = {'message': 'All the nodes are now connected. The Sudocoin Blockchain now contains the following nodes:',
                    'total_nodes': list(blockchain.nodes)}
    return JsonResponse(response)
# Replacing the chain by the longest chain if needed
def replace_chain(request): #New
    if request.method == 'GET':
        is_chain_replaced = blockchain.replace_chain()
        if is_chain_replaced:
            response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                        'new_chain': blockchain.chain}
        else:
            response = {'message': 'All good. The chain is the largest one.',
                        'actual_chain': blockchain.chain}
    return JsonResponse(response)


def reward(request):
    allStudents = User.objects.all().filter(role=3)
    paginator = Paginator(allStudents, 6)
    page = request.GET.get('page')
    students = paginator.get_page(page)
    return render(request,'trainer_reward.html',{'students':students})

def trans(request):
    tran = Transaction.objects.all().filter(sender =request.user)
    paginator = Paginator(tran, 6)
    page = request.GET.get('page')
    transactions = paginator.get_page(page)
   
    return render(request,'trainer_transactions.html',{'transactions':transactions})


def reward_confirm(request,id):
    student = User.objects.get(id=id)
    metrics = Metrics.objects.all()
    # return render(request,'reward_confirm.html',{'metrics':metrics})


    val = request.GET
    met =None
    for v in val.values():
        met =Metrics.objects.values_list('value',flat=True).filter(metric = v)[0]
        if request.method == 'GET':
            previous_block = blockchain.get_last_block()
            previous_nonce = previous_block['nonce']
            nonce = blockchain.proof_of_work(previous_nonce)
            previous_hash = blockchain.hash(previous_block)
            user = request.user
            blockchain.add_transaction(sender =user.email , receiver = student.username, amount = met, time=str(datetime.datetime.now()))
            block = blockchain.create_block(nonce, previous_hash)
            response = {
                    'message': f'Congratulations, you just awarded {student.username} !',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'nonce': block['nonce'],
                    'previous_hash': block['previous_hash'],
                    'transaction': block['transactions']}
            the_transactions = [v]
            for dict in block['transactions']:
                for v in dict.values():
                    the_transactions.append(v)

            transaction,created= Transaction.objects.update_or_create(
            metric=the_transactions[0],
            sender =the_transactions[1],
            receiver =the_transactions[2],
            value =the_transactions[3],
            time =the_transactions[4],)
            transaction.save()
    return render(request,'trainer_reward_confirm.html',{'student':student,'metrics':metrics,'met':met})
   


def search_student(request):
    search_post = request.GET.get('search')
    if search_post:
        students = User.objects.filter(Q(username__icontains=search_post))
        results=students.count()
    else:
        students = Student.objects.all()
        message="Looks like the student doesn't exist. Try searching using the first name"
        return render (request,'reward.html',{'students':students,'message':message})
    return render (request,'trainer_reward.html',{'students':students,'results':results})




def trainer_home(request):
    trainers=Trainer.objects.all()
    print(trainers)
    return render(request,'trainer.html')

def trainer_profile(request):
    try:
        traineruserprofile = request.user.traineruserprofile
    except ObjectDoesNotExist:
        traineruserprofile = Trainer(user=request.user)
        
    if request.method == 'POST':
        user_form = TrainerUpdateProfileForm(request.POST, instance=request.user)
        profile_form = TrainerUserProfileForm(request.POST, instance=request.user.traineruserprofile.user)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            #user.username = user.email
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('trainer-home')
    else:
        profile_form = TrainerUserProfileForm(instance=request.user.traineruserprofile)
        user_form = TrainerUpdateProfileForm(instance=request.user)
    args = {
        'user_form': user_form, # basic user form
        'profile_form': profile_form # user profile form
        }
    return render(request, 'trainer_profile.html', args)
    
def trainer_dashboard(request):
    return render(request,"trainer_dashboard.html")



