from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class User(AbstractUser):
    class UserRole(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        SALES = "SALES", "Commercial"

    role = models.CharField(max_length=5, choices=UserRole.choices, default=UserRole.ADMIN)
    groups = models.ManyToManyField(
         Group,
         verbose_name=_('groups'),
         blank=True,
         related_name='gestion_user_groups',
         help_text=_(
             'The groups this user belongs to. A user will get all permissions '
             'granted to each of their groups.'
         ),
         related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        # Définissez un related_name unique pour éviter les conflits
        related_name='%(app_label)s_%(class)s_permissions',
        blank=True,
    )

class SupplierBilling(models.Model):
    class FinancingType(models.TextChoices):
        CASH = 'Cash', 'Cash'
        BANK = 'Bank', 'Bank'
        OTHER = 'Other', 'Other'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    dateSupplier = models.DateTimeField()
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    payment = models.CharField(max_length=50, choices=FinancingType.choices, default=FinancingType.CASH)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class CustomerBilling(models.Model):
    class FinancingType(models.TextChoices):
        CASH = 'Cash', 'Cash'
        BANK = 'Bank', 'Bank'
        OTHER = 'Other', 'Other'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    dateBilling = models.DateTimeField()
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    payment = models.CharField(max_length=50, choices=FinancingType.choices, default=FinancingType.CASH)
    comment = models.CharField(max_length=200)

class Delivery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    dateDelivery = models.DateTimeField()
    liter = models.IntegerField(default=1)
    comment = models.CharField(max_length=200)

class Production(models.Model):
    class ProductionType(models.TextChoices):
        CHEESE = 'Cheese', 'Fromage'
        WHOOL = 'Laine', 'Laine'
        SOAP = 'Savon', 'Savon'
        BASKETRY = 'Vannerie', 'Vannerie'
        GOATSKINS = 'Peau', 'Peau de chèvre'
        OTHER = 'Autre', 'Autre'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, choices=ProductionType.choices, default=ProductionType.CHEESE)

class Herd(models.Model):
    class Sex(models.TextChoices):
        FEMALE = 'F', "Female"
        MALE = 'M', "Male"

    class AnimalType(models.TextChoices):
        CABRI = 'C', "Cabri"
        CHEVRETTE = 'CH', "Chevrette"
        CHEVRE = 'CHV', "Chèvre"
        BOUC = 'B', "Bouc"

    class StockType(models.TextChoices):
        REBOUCLAGE = 'RE', "Rebouclage"
        CHEVRE = 'CHV', "Chevre électronique et conventionnelle"
        CABRIT = 'CA', "Tiptag"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    birth_date = models.DateTimeField()
    ear_tag = models.IntegerField(default=1)
    sex = models.CharField(max_length=1, choices=Sex.choices)
    type = models.CharField(max_length=3, choices=AnimalType.choices)
    rebouclage_quantity = models.IntegerField(default=0)  # Quantité de rebouclage
    chevre_quantity = models.IntegerField(default=0)  # Quantité de chevre électronique et conventionnelle
    tiptag_quantity = models.IntegerField(default=0)  # Quantité de tiptag

    def __str__(self):
        return f"{self.id} - {self.get_sex_display()} - {self.get_type_display()}"

class ModelAction(models.Model):
    class Action(models.TextChoices):
        CREATE = 'CREATE', 'Create'
        UPDATE = 'UPDATE', 'Update'
        DELETE = 'DELETE', 'Delete'

    action = models.CharField(max_length=50, choices=Action.choices)
    action_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='model_actions_gestion')
    content_type = models.ForeignKey(
            ContentType,
            on_delete=models.CASCADE,
            related_name='%(app_label)s_%(class)s_actions'
        )
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.action} - {self.content_type} - {self.object_id}"

class SupplierBillingAction(models.Model):
   action = models.ForeignKey(ModelAction, on_delete=models.CASCADE)
   supplier_billing = models.ForeignKey(SupplierBilling, on_delete=models.CASCADE)

class CustomerBillingAction(models.Model):
   action = models.ForeignKey(ModelAction, on_delete=models.CASCADE)
   customer_billing = models.ForeignKey(CustomerBilling, on_delete=models.CASCADE)

class DeliveryAction(models.Model):
   action = models.ForeignKey(ModelAction, on_delete=models.CASCADE)
   delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)

class ProductionAction(models.Model):
   action = models.ForeignKey(ModelAction, on_delete=models.CASCADE)
   production = models.ForeignKey(Production, on_delete=models.CASCADE)
