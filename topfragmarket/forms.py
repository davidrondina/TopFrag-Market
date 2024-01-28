from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email'] 
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'w-full px-4 py-2.5 shadow', 
                    'placeholder': 'Enter your username'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'w-full px-4 py-2.5 shadow',
                    'placeholder': 'Enter your email'
                }
            ),
            'password1': forms.PasswordInput(
                attrs={
                    'class': 'block w-full px-4 py-2.5 shadow',
                    'type': 'password',
                    'placeholder': 'Enter your password',
                }
            ),
            'password2': forms.PasswordInput(
                attrs={
                    'class': 'block w-full px-4 py-2.5 shadow', 
                    'type': 'password',
                    'placeholder': 'Re-enter your password',
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({
            "class": "form-control px-4 py-2.5 shadow",
            "placeholder": "Enter your password"
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control px-4 py-2.5 shadow",
            "placeholder": "Re-enter your password"
        })

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': 'Enter your first name',
                'class': 'w-full px-4 py-2.5 shadow'
            }
        ),
    )
    
    middle_name = forms.CharField(
        required=False, 
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': 'Enter your middle name',
                'class': 'w-full px-4 py-2.5 shadow'
            }
        ),
        label='Middle name (optional)'
    )
    
    surname = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': 'Enter your surname',
                'class': 'w-full px-4 py-2.5 shadow'
            }
        ),
    )
    
    contact_no = forms.CharField(
        max_length=11,
        required=False, 
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': 'Ex. 09123456789',
                'class': 'w-full px-4 py-2.5 shadow'
            }
        ),
        label='Phone No. (optional)'
    )
    
    birthdate = forms.DateField(
        required=True, 
        widget=forms.widgets.DateInput(
            attrs={
                'class': 'px-4 py-2.5 shadow',
                'type': 'date'
            }
        ),
    )
    
    sex = forms.ChoiceField(
        choices=Profile.SEX_CHOICES,
        required=True,
        widget=forms.widgets.Select(
            attrs={
               'class': 'px-4 py-2.5 shadow' 
            }
        ),
    )
    
    class Meta:
        model = Profile
        exclude = ('user', 'profile_photo',)
    

class ListingForm(forms.ModelForm): 
    name = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(
            attrs={
                'id': 'name',
                'placeholder': 'Enter the listing name',
                'class': 'w-full px-4 py-2.5 shadow'
            }
        ),
        label='Listing Name'
    )
    description = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                'id': 'description',
                'placeholder': 'Provide a description about your listing',
                'class': 'w-full h-[150px] px-4 py-2.5 shadow'
            }
        )
    )
    price = forms.IntegerField(
        min_value=0, 
        max_value=200000, 
        required=True,
        widget=forms.widgets.NumberInput(
            attrs={
                'id': 'price',
                'class': 'px-4 py-2.5 shadow' 
            }
        ),
    )
    condition = forms.ModelChoiceField(
        queryset=Condition.objects.all(),
        required=True,
        widget=forms.widgets.Select(
            attrs={
               'class': 'px-4 py-2.5 shadow' 
            }
        ),
    )
    category = forms.ChoiceField(
        choices=Listing.CATEGORY_CHOICES,
        required=True,
        widget=forms.widgets.Select(
            attrs={
               'class': 'px-4 py-2.5 shadow' 
            }
        ),
    )
    deal_option = forms.ChoiceField(
        choices=Listing.DEAL_CHOICES,
        required=True,
        widget=forms.widgets.Select(
            attrs={
               'class': 'px-4 py-2.5 shadow' 
            }
        ),
    )
    location = forms.ChoiceField(
        choices=Listing.LOCATION_CHOICES,
        required=True,
        widget=forms.widgets.Select(
            attrs={
               'class': 'px-4 py-2.5 shadow' 
            }
        ),
    )

    class Meta:
        model = Listing
        exclude = ('seller', 'is_sold')
        
class ChatMessageForm(forms.ModelForm):
    content = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': 'Ask something to the seller',
                'class': 'w-full px-4 py-2.5 shadow' 
            }
        ),
        label='',
    )
    
    class Meta:
        model = ChatMessage
        exclude = ('chat', 'sender')
        
class ThreadForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': 'Ask something to the seller',
                'class': 'w-full px-4 py-2.5 shadow' 
            }
        ),
        # label='',
    )
    
    content = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                'id': 'description',
                'placeholder': 'Provide a description about your listing',
                'class': 'w-full h-[150px] px-4 py-2.5 shadow'
            }
        )
    )
    
    image = forms.ImageField(
        required=False,
        widget=forms.widgets.FileInput(
            attrs={
                'id': 'image'
            }
        )
    )
    
    topic = forms.ChoiceField(
        choices=Thread.TOPIC_CHOICES,
        required=True,
        widget=forms.widgets.Select(
            attrs={
               'class': 'px-4 py-2.5 shadow' 
            }
        ),
    )
    
    class Meta:
        model = Thread
        exclude = ('user',)
        
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                'id': 'content',
                'placeholder': 'Say something...',
                'class': 'w-full h-[150px] px-4 py-2.5 shadow'
            }
        ),
        label=''
    )
    
    class Meta:
        model = Comment
        exclude = ('user', 'thread')