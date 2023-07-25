from django.db import models
from userAuth.models import User   
    
    
class Group(models.Model):
    group = models.CharField(max_length=250)
    
    def __str__(self):
        return self.group



class Post(models.Model):
    LOCATION_CHOICES = (
        ('NAIROBI', 'NAIROBI'),
        ('KISUMU', 'KISUMU'),
        ('MOMBASA', 'MOMBASA'),
        ('THIKA', 'THIKA'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='post_images/')
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    content = models.TextField()
    negotiable = models.BooleanField(default=True)
    availability = models.BooleanField(default=True)
    can_be_traded_in = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    favorites = models.ManyToManyField(User, related_name='favorite_posts', blank=True)
    status = models.TextField()
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-timestamp']
        
    def clean(self):
        if not self.content:
            raise models.ValidationError("Description cannot be empty.")
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
class DeliveryRequest(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    user_address = models.CharField(max_length=200)
    customer_address = models.CharField(max_length=200)
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery Request for {self.post.name}"
