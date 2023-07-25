from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from userAuth.models import User
from django import forms
from .models import Post, Comment

        
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email','password1', 'password2']
        
        
class userForm(ModelForm):    
    class Meta:
        model = User
        fields = ['email','nickname','avatar']
        labels = {
                  'email':'',
                  'nickname': '',
                  'avatar': 'Profile Picture'   
        }
        widgets ={
                  'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your Email'}),
                  'nickname':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter a fancy/business name '})
                  
                  
                  }
        
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        
        fields = ['group','name', 'location', 'price', 'content', 'negotiable','availability', 'image']
        labels = {
            'group':'Category',
            'name':'',
            'location':'Location ',
            'price':'',
            'content':'', 
            'image':'Image ',
            'availability':'Make it online',
            'negotiable':'Can someone bargain'
            
        }
        widgets ={
                  'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter name of the product'}),
                  'group':forms.Select(attrs={'class':'form-control', 'placeholder':'Category'}),
                  'price':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Enter price of the product'}),
                  'location':forms.Select(attrs={'class':'form-control', 'placeholder':'location'}),
                  'content':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Say something about the product'}),
                  }
        def clean_price(self):
            price = self.cleaned_data.get('price')
            if price is not None and price < 0:
                raise forms.ValidationError("Price cannot be negative.")
            return price
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']