from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# Create your models here.
class Profile(models.Model):
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    first_name = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, null=True) 
    contact_no = models.CharField(max_length=11, blank=True)
    address = models.CharField(max_length=60, null=True)
    birthdate = models.DateField(null=True)
    sex = models.CharField(choices=SEX_CHOICES, max_length=1)
    profile_photo = models.ImageField(upload_to='profile_media/', blank=True) # Image will be uploaded to MEDIA_ROOT/thread_media
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.first_name} {self.surname}'
    
class Condition(models.Model):
    name = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.name

class Listing(models.Model):
    DEAL_CHOICES = (
        ('meetup', 'Meetup'),
        ('mailing', 'Mailing'),
        ('delivery', 'Delivery')
    )
    
    CATEGORY_CHOICES = (
        ('desktops', 'Desktops'),
        ('laptops & notebooks', 'Laptops & Notebooks'),
        ('phones & tablets', 'Phones & Tablets'),
        ('consoles', 'Consoles'),
        ('videogames', 'Videogames'),
        ('audio', 'Audio'),
        ('accessories', 'Accessories'),
    )
    
    name = models.CharField(max_length=30, null=True)
    description = models.TextField(max_length=255, null=True)
    price = models.PositiveIntegerField(validators=[MaxValueValidator(200000)], null=True)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50, null=True)
    deal_option = models.CharField(choices=DEAL_CHOICES, max_length=30, null=True)
    location = models.CharField(max_length=50, null=True)
    is_sold = models.BooleanField(default=False)
    seller = models.ForeignKey(User, db_column='seller_id', related_name='seller', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class ListingLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing_media/', null=True)

class Chat(models.Model):
    creator = models.ForeignKey(User, db_column='creator_id', related_name='creator', on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, db_column='sender_id', related_name='sender', on_delete=models.CASCADE)
    content = models.TextField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# THREADS
class Thread(models.Model):
    TOPIC_CHOICES = (
        ('general', 'General'),
        ('discussion', 'Discussion'),
        ('Advice', 'Advice'),
    )
    
    title = models.CharField(max_length=50, null=True)
    content = models.TextField(max_length=255, null=True)
    image = models.FileField(upload_to='thread_media/', blank=True)
    topic = models.CharField(choices=TOPIC_CHOICES, max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class ThreadLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField(max_length=255, null=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
