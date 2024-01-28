from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import *
from .forms import *

# Create your views here.
def index(request):
    context = {
        'videogames': Listing.objects.filter(category='videogames', is_sold=False).order_by('?')[:4],
        'accessories': Listing.objects.filter(category='accessories', is_sold=False).order_by('?')[:4],
        'recent_listings': Listing.objects.filter(is_sold=False).order_by('-created_at')[:4],
    }
    
    return render(request, 'topfragmarket/pages/index.html', context)

def register_user(request):
    if request.user.is_authenticated:
        return redirect('topfragmarket:dashboard')
    
    context = {}
    
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        
        if user_form.is_valid():
            reg_user = user_form.save(commit=False)
            reg_user.username = reg_user.username.lower()
            
            # Store the user credential in the database
            reg_user.save()
            
            profile = profile_form.save(commit=False)
            profile.user_id = reg_user.id
            
            # Create profile related to the user
            profile.save()
    
            # Check if user exists in the database
            auth_user = authenticate(request, username=reg_user.username, password=user_form.cleaned_data['password1'])
            
            # If user exists, log them into the system
            if auth_user is not None:
                login(request, auth_user)

                messages.success(request, 'Registered successfully! Welcome to TopFrag Market!')
                
                return redirect('topfragmarket:dashboard')    
        else:
            messages.error(request, 'User registration error. Please make sure you provided correct input.')
    
    context['user_form'] = RegisterForm()
    context['profile_form'] = ProfileForm()
    return render(request, 'topfragmarket/pages/register.html', context)

# UNUSED VIEW FUNC
def create_profile(request):
    user = request.user
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user_id = user.id
            
            # Create profile related to the user
            profile.save()

            messages.success(request, 'Setup Done! Welcome to TopFrag Market!')
            
            return redirect('topfragmarket:dashboard')    
        else:
            messages.error(request, 'Profile setup error. Please make sure you provided correct input.')
    
    context = {
        'profile_form': ProfileForm()
    }
    
    return render(request, 'topfragmarket/pages/profile/create.html', context)
        
def login_user(request):
    if request.user.is_authenticated:
        return redirect('topfragmarket:dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Check if user exists in the database
        user = authenticate(request, username=username, password=password)
        
        # If user exists, log them into the system
        if user is not None:
            login(request, user)

            messages.success(request, 'You are now logged in!')
            
            return redirect('topfragmarket:dashboard')
        
        # Login failed; Return to login page
        else:
            messages.error(request, 'Invalid username or password')
            
            return redirect('topfragmarket:login')
        
    return render(request, 'topfragmarket/pages/login.html')

def logout_user(request):
    logout(request)
    
    messages.success(request, 'Logged out')
    
    return redirect('topfragmarket:home')

def about(request):
    return render(request, 'topfragmarket/pages/about.html')

def categories(request):
    return render(request, 'topfragmarket/pages/categories.html')

@login_required
def dashboard(request):
    user = request.user
    listings =  Listing.objects.filter(seller_id=user.id).order_by('-created_at')
    # print(user.profile)
    # print(Listing.objects.filter(seller_id=user.id))
    
    context = {
        'profile': user.profile,
        'listings': listings,
        'listings_count': listings.count(),
        'listings_sold': listings.filter(is_sold=True).count()
    }
    
    return render(request, 'topfragmarket/pages/dashboard/dashboard.html', context)

def profile(request, user_id):
    user = request.user
    listings = Listing.objects.filter(seller_id=user_id, is_sold=False).order_by('-created_at')
    
    if user.id == user_id:
        return redirect('topfragmarket:dashboard')
    
    context = {
        'profile': Profile.objects.get(user_id=user_id),
        'listings': listings,
        'listings_count': listings.count(),
        'listings_sold': listings.filter(is_sold=True).count()
    }
    
    return render(request, 'topfragmarket/pages/profile/detail.html', context)

def listings(request):
    context = {}
    search = request.GET.get('search')
    category = request.GET.get('category')
        
    if request.method == 'POST':
        filters = dict(request.POST.items())
        print(filters)
        
        listings = Listing.objects.all()
        
        if 'category' in filters:
            listings = Listing.objects.filter(category=filters['category'])
        
        if 'deal_option' in filters:
            listings = listings.filter(deal_option=filters['deal_option'])
            
        if 'condition' in filters:
            listings = listings.filter(condition=filters['condition'])
        
        if 'location' in filters:
            listings = listings.filter(location=filters['location'])
        
        if 'price' in filters:
            listings = listings.order_by(filters['price'])
            
        if 'created_at' in filters:
            listings = listings.order_by(filters['created_at'])
            
        context['listings'] = listings.filter(is_sold=False)
    else:
        context['listings'] = Listing.objects.filter(is_sold=False)
    
    if category:
        context['listings'] = Listing.objects.filter(category=category, is_sold = False)
    
    if search:
        context['listings'] = Listing.objects.filter(name__contains=search, is_sold=False)
    
    context['categories'] = Listing.CATEGORY_CHOICES
    context['locations'] = Listing.LOCATION_CHOICES
    context['deal_options'] = Listing.DEAL_CHOICES
    context['conditions'] = Condition.objects.all()
    
    return render(request, 'topfragmarket/pages/listings.html', context)

@login_required
def listing_detail(request, listing_id):
    user = request.user
    listing = get_object_or_404(Listing, pk=listing_id)
    images = list(ListingImage.objects.filter(listing_id=listing_id))
    
    if listing.seller_id == user.id:
        context = {
            'listing': listing,
            'images': list(ListingImage.objects.filter(listing_id=listing_id)),
            'images_count': len(images)
        }
        
        return render(request, 'topfragmarket/pages/dashboard/listing/detail.html', context)
        
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        
        if not(Chat.objects.filter(creator_id=user.id, listing_id=listing_id).exists()):
            print('chat not exists')
            # chat = Chat(creator_id=user.id, listing_id=listing_id)
            # chat.save()
        else:
            print('chat exists')
            # chat = Chat.objects.get(creator_id=user.id, listing_id=listing_id)
        
        if form.is_valid():
            chat_message = form.save(commit=False)
            
            # Get chat instance if it exists or create one
            if not(Chat.objects.filter(creator_id=user.id, listing_id=listing_id).exists()):
                print('chat not exists')
                chat = Chat(creator_id=user.id, listing_id=listing_id)
                chat.save()
            else:
                print('chat exists')
                chat = Chat.objects.get(creator_id=user.id, listing_id=listing_id)
            
            # Refer message to chat instance
            chat_message.chat_id = chat.id
            chat_message.sender_id = user.id
            
            chat_message.save()
            
            messages.success(request, 'Message sent!')
            
            return redirect('topfragmarket:listing_detail', listing_id=listing_id)
    
    context = {
        'form': ChatMessageForm(),
        'listing': listing,
        'listings': Listing.objects.filter(is_sold=False).order_by('?')[:8],
        'images': images,
        'images_count': len(images)
    }
    
    # imagez = ListingImage.objects.filter(listing_id=listing_id)
    # print(imagez[0].image.url)
    
    return render(request, 'topfragmarket/pages/listing/detail.html', context)

@login_required
def create_listing(request):
    user = request.user
    
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        
        # print(list(request.POST.items()))
        # print(request.POST.getlist('images[]'))
        # print(request.FILES)
        # print(request.FILES.items())
        # print(request.FILES.getlist('images[]'))
        
        # for file in request.FILES[]:
        #     print(file)
        
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller_id = user.id
            listing.is_sold = False
            listing.save()
            
            # Handle uploaded files
            for file in request.FILES.getlist('images[]'):
                obj = ListingImage(listing_id=listing.id, image=file)
                obj.save()
            
            messages.success(request, 'Listing added successfully')
            return redirect('topfragmarket:dashboard')
        else:
            messages.error(request, 'An error occured')
    
    context = {
        'form': ListingForm()
    }
    
    return render(request, 'topfragmarket/pages/listing/create.html', context)

@login_required
def update_listing_status(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    
    if not listing.seller_id == user.id:
        messages.error(request, 'You do not own this listing')
        
        return redirect('topfragmarket:dashboard')
    
    if request.method == 'POST':
        if listing.is_sold:
            listing.is_sold = False
        else:
            listing.is_sold = True
        
        listing.save()
        
    context = {
        'listing': listing
    }
    
    return redirect('topfragmarket:listing_detail', listing_id=listing_id)

@login_required
def update_listing(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id) 
    
    if not listing.seller_id == user.id:
        messages.error(request, 'You do not own this listing')
        
        return redirect('topfragmarket:dashboard')
    
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing) # prepopulate the form with an existing listing
        
        if form.is_valid():
            # Update existing listing
            form.save()

            messages.success(request, 'Listing updated successfully')
            
            # Redirect to listing detail page after updating the listing
            return redirect('topfragmarket:listing_detail', listing_id=listing_id)
        else:
            messages.error(request, 'An error occurred')
        
    context = {
        'listing': listing,
        'form': ListingForm(instance=listing)
    }
    
    return render(request, 'topfragmarket/pages/dashboard/listing/edit.html', context)

@login_required
def delete_listing(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    
    if not listing.seller_id == user.id:
        messages.error(request, 'You do not own this listing')
        
        return redirect('topfragmarket:dashboard')
    
    if request.method == 'POST':
        listing.delete()
    
    messages.success(request, 'Listing deleted successfully')
    return redirect('topfragmarket:dashboard')
    
@login_required
def chats(request):
    user = request.user
    
    # print(request.GET.urlencode())
    
    chat = request.GET.get('chat')
    
    if chat == 'seller':
        context = {
            'chats': Chat.objects.filter(creator_id=user.id).order_by('-created_at'),
        }
    elif chat == 'buyer':
        context = {
            'chats': Chat.objects.filter(listing__seller_id=user.id).order_by('-created_at'),
        }
    
    # print(chat)
    
    # Get the chats that relate to the listing owned by the current user
    # Chat.objects.filter(listing__seller_id=user.id)
    
    # Get the chats created by the current user
    # Chat.objects.filter(creator_id=user.id)
    
    # context = {
    #     'seller_chats': Chat.objects.filter(creator_id=user.id),
    #     'buyer_chats': Chat.objects.filter(listing__seller_id=user.id)
    # }
    
    return render(request, 'topfragmarket/pages/chat/chats.html', context)

@login_required
def chat_detail(request, chat_id):
    user = request.user
    
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        
        if form.is_valid():
            chat_message = form.save(commit=False)
    
            chat_message.chat_id = chat_id
            chat_message.sender_id = user.id
                
            chat_message.save()
        
            messages.success(request, 'Message sent!')
            return redirect('topfragmarket:chat_detail', chat_id=chat_id)
    
    chat = Chat.objects.get(pk=chat_id)
    
    context = {
        'chat_id': chat_id,
        'chat_messages': chat.chatmessage_set.all(),
        'form': ChatMessageForm()
    }
    
    return render(request, 'topfragmarket/pages/chat/detail.html', context)

def forum(request):
    context = {}
    topics = Thread.TOPIC_CHOICES
    topic = request.GET.get('topic')
    
    context['topics'] = topics
    
    if topic:
        context['threads'] = Thread.objects.filter(topic=topic).order_by('-created_at')
    else:
        context['threads'] = Thread.objects.order_by('-created_at')
    
    return render(request, 'topfragmarket/pages/forum/threads.html', context)

@login_required
def thread_detail(request, thread_id):
    user = request.user
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_id = user.id
            comment.thread_id = thread_id
            
            comment.save()
            
            messages.success(request, 'Comment sent!')
            return redirect('topfragmarket:thread_detail', thread_id=thread_id)
    
    thread = Thread.objects.get(pk=thread_id)
    
    context = {
        'thread': thread,
        'form': CommentForm(),
        'comments': thread.comment_set.all().order_by('-created_at')
    }
    
    return render(request, 'topfragmarket/pages/forum/thread/detail.html', context)

@login_required
def create_thread(request):
    user = request.user
    if request.method == 'POST':
        form = ThreadForm(request.POST, request.FILES)
        
        if form.is_valid():
            thread = form.save(commit=False)
            thread.user_id = user.id
            
            thread.save()
            
            # Flash message (lagay ka ng from django.contrib import messages sa pinaka-itaas)
            
            # Kapag gagamit ka nito, ilagay mo itong code sa base.html, sa labas ng block content
            # {% if messages %}
            # <ul class="messages">
            #     {% for message in messages %}
            #     <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
            #     {% endfor %}
            # </ul>
            # {% endif %}
            messages.success(request, 'Thread added successfully')
            
            # Ginagamit dito yung name="" ng url mo sa urls.py
            return redirect('topfragmarket:forum')
    
    context = {
        'form': ThreadForm()
    }
    
    return render(request, 'topfragmarket/pages/forum/thread/create.html', context)

@login_required
def update_thread(request, thread_id):
    user = request.user
    thread = Thread.objects.get(pk=thread_id) 
    
    if not thread.user_id == user.id:
        messages.error(request, 'You do not own this thread')
        
        return redirect('topfragmarket:forum')
    
    if request.method == 'POST':
        form = ThreadForm(request.POST, request.FILES, instance=thread) # prepopulate the form with an existing thread
        
        if form.is_valid():
            # Update existing thread
            form.save()

            messages.success(request, 'Thread updated successfully')
            
            # Redirect to listing detail page after updating the listing
            return redirect('topfragmarket:thread_detail', thread_id=thread_id)
        else:
            messages.error(request, 'An error occurred')
        
    context = {
        'thread': thread,
        'form': ThreadForm(instance=thread)
    }
    
    return render(request, 'topfragmarket/pages/forum/thread/edit.html', context)

@login_required
def delete_thread(request, thread_id):
    user = request.user
    thread = Thread.objects.get(pk=thread_id)
    
    if not thread.user_id == user.id:
        messages.error(request, 'You do not own this thread')
        
        return redirect('topfragmarket:dashboard')
    
    if request.method == 'POST':
        thread.delete()
    
    messages.success(request, 'Thread deleted successfully')
    return redirect('topfragmarket:forum')
        