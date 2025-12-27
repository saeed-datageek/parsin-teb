from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

# accounts/models.py (at the top)


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where the mobile_number is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError('The Mobile Number must be set')
        
        # Normalize the mobile number if necessary, although optional for charfield
        # mobile_number = self.normalize_mobile_number(mobile_number) 
        
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given mobile_number and password.
        """
        # Ensure superusers have appropriate staff/superuser flags
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Optional: Set superusers to have the ADMIN role
        extra_fields.setdefault('role', self.model.UserRole.ADMIN) 
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(mobile_number, password, **extra_fields)


class UserRole(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        STORE_MANAGER = 'MANAGER', 'Store Manager'
        ADMIN = 'ADMIN', 'Administrator' # Superuser equivalent

class CustomUser(AbstractUser):
      # --- Override core fields for phone authentication

      class UserRole(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        STORE_MANAGER = 'MANAGER', 'Store Manager'
        ADMIN = 'ADMIN', 'Administrator' # Superuser equivalent
      

      objects = CustomUserManager()
      username = None

      mobile_number = models.CharField(
           max_length=15,
           unique=True,
           verbose_name="Mobile Phone Number"
      )

      USERNAME_FIELD = 'mobile_number'

      email = models.CharField(max_length=100,  unique=False, blank=True, null=True)      


      # --- NEW: Role Field ---
      role = models.CharField(
        max_length=50,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER, # Default role for new signups
        verbose_name='User Role'
      )
      # --- Helper methods for role checking ---
      @property
      def is_customer(self):
        return self.role == UserRole.CUSTOMER

      @property
      def is_store_manager(self):
        # A store manager can also be a superuser (for Admin panel access)
        return self.role == UserRole.STORE_MANAGER or self.is_superuser

      @property
      def is_staff_member(self):
        # General check for anyone with elevated permissions
        return self.role in [UserRole.STORE_MANAGER, UserRole.ADMIN] or self.is_staff
    
    # ... (Other fields and methods: full_name, etc.) ...
    
    # We must explicitly set is_staff based on the role to grant Admin access
      def save(self, *args, **kwargs):
        if self.role == UserRole.STORE_MANAGER:
            self.is_staff = True
        elif self.role == UserRole.CUSTOMER and not self.is_superuser:
            self.is_staff = False
        super().save(*args, **kwargs)
      REQUIRED_FIELDS = []

      first_name = models.CharField(max_length=150, blank=False)
      last_name = models.CharField(max_length=150, blank=False)
      is_mobile_verified = models.BooleanField(default=False)





class UserAddress(models.Model):
      user = models.ForeignKey(
           CustomUser,
           on_delete=models.CASCADE,
           related_name='addresses'
      ) 

      street_address = models.CharField(max_length=255)
      city = models.CharField(max_length= 100)
      state = models.CharField(max_length=100)
      zipcode = models.CharField(max_length=20)

         

class Brand(models.Model):
      name = models.CharField(max_length=100)
      description = models.TextField(max_length=200, blank=True)


class Product(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=5)
    price = models.IntegerField(default=0)
    description = models.TextField(max_length=200)

    brand = models.ForeignKey(
            Brand,
            on_delete=models.SET_NULL,
            null = True, 
            blank = True,
            related_name='products'
    )
    def __str__(self):
        return f"{self.name} - {self.size}"
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-id']  # Show newest first

class ProductImages(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to="products/"
    )
    def __str__(self):
        return self.product.name
        

class Order(models.Model):
     
     customer = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='orders')
     total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     def cal_total_price(self):
          self.total_cost = sum(item.price*item.quantity for item in self.items.all())
          self.save()
       

class OrderItem(models.Model):
      order = models.ForeignKey(Order, related_name='items', # Order.items.all()
                                 on_delete=models.CASCADE) # correct if the order is deleted 
      product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT)
      quantity = models.IntegerField(default=1) 

      # store the price at the time of the order to protect against later price changes
      price = models.DecimalField(max_digits=10, decimal_places=2)


      def __str__(self):
           return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"

      
       



