# Importations
import uuid
from django.db import models
from django.contrib.contenttypes.models import ContentType  # Ajoutez cette ligne
from django.contrib.contenttypes.fields import GenericForeignKey  # Ajoutez cette ligne
from gestion.models import User

# Modèles

class Recipes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)

class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='ingredients', blank=True, null=True)
    ingredient = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    mesure_unit = models.CharField(max_length=200, blank=True, null=True)  # Vous devez compléter ce champ

    def __str__(self):
        return self.ingredient  # Renvoie le nom de l'ingrédient

class Step(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='steps', blank=True, null=True)
    step_number = models.IntegerField()  # Numéro d'étape
    description = models.TextField()  # Description de l'étape
    attached_files = models.FileField(upload_to='step_attachments/', blank=True, null=True)  # Fichiers attachés

    class Meta:
        ordering = ['step_number']  # Ordonne les étapes par numéro

# Modèles spécifiques pour chaque type de recette

class Cheese(models.Model):
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE, related_name='cheese', parent_link=True)
    ferment_name = models.CharField(max_length=200)
    ferment_quantity = models.FloatField()
    ferment_mesure_unit = models.CharField(max_length=200)

    cooking_time = models.IntegerField()
    cooking_temperature = models.IntegerField()
    refining_time = models.IntegerField()
    refining_temperature = models.IntegerField()
    pressing = models.BooleanField(default=False)
    pressing_time = models.IntegerField()
    conservation_mode = models.CharField(max_length=200, choices=[("Naturel", "Naturel"), ("Sous-vide", "Sous-vide"), ("cire", "cire"), ("autre", "autre")])

class Whool(models.Model):
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE, related_name='whool', parent_link=True)
    fabrication_type = models.CharField(max_length=200, choices=[("tissage", "tissage"), ("feutrage", "feutrage"), ("filage", "filage"), ("autre", "autre")])
    dyeing = models.BooleanField(default=False)
    dyeing_color = models.CharField(max_length=200)
    dyeing_preparation = models.TextField()

    drying_time = models.IntegerField()

class Soap(models.Model):
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE, related_name='soap', parent_link=True)
    drying_time = models.IntegerField()
    dyeing = models.BooleanField(default=False)
    dyeing_color = models.CharField(max_length=200)
    dyeing_preparation = models.TextField()

# Modèles supplémentaires pour d'autres types de recettes

class Basketry(models.Model):
    pass

class GoatSkin(models.Model):
    pass

class Other(models.Model):
    pass

class ModelAction(models.Model):
    class Action(models.TextChoices):
        CREATE = 'CREATE', 'Create'
        UPDATE = 'UPDATE', 'Update'
        DELETE = 'DELETE', 'Delete'

    action = models.CharField(max_length=50, choices=Action.choices)
    action_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='model_actions_recipies')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')


    def __str__(self):
        return f"{self.action} - {self.content_type} - {self.object_id}"

# Modèles d'action spécifiques

class RecipesAction(models.Model):
    action = models.ForeignKey(ModelAction, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipes', on_delete=models.CASCADE)

class IngredientAction(models.Model):
    action = models.ForeignKey(ModelAction, on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)

class StepAction(models.Model):
    action = models.ForeignKey(ModelAction, on_delete=models.CASCADE)
    step = models.ForeignKey('Step', on_delete=models.CASCADE)

class CheeseAction(models.Model):
    action = models.ForeignKey(ModelAction, on_delete=models.CASCADE)
    cheese = models.ForeignKey('Cheese', on_delete=models.CASCADE)

class WhoolAction(models.Model):
    action = models.ForeignKey(ModelAction, on_delete=models.CASCADE)
    whool = models.ForeignKey('Whool', on_delete=models.CASCADE)

class SoapAction(models.Model):
    action = models.ForeignKey(ModelAction, on_delete=models.CASCADE)
    soap = models.ForeignKey('Soap', on_delete=models.CASCADE)

class BasketryAction(models.Model):
    action = models.ForeignKey(ModelAction, on_delete=models.CASCADE)
    basketry = models.ForeignKey('Basketry', on_delete=models.CASCADE)

class GoatSkinAction(models.Model):
    action = models.ForeignKey(ModelAction, on_delete=models.CASCADE)
    goat_skin = models.ForeignKey('GoatSkin', on_delete=models.CASCADE)

class OtherAction(models.Model):
    action = models.ForeignKey(ModelAction, on_delete=models.CASCADE)
    other = models.ForeignKey('Other', on_delete=models.CASCADE)