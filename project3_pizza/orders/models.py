from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MenuPosition(models.Model):
	name = models.CharField(max_length=64)
	name_id = models.CharField(max_length=64)

	def __str__(self):
		return f"{self.name}"

class Orders(models.Model):
	order_number = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	order_status = models.CharField(max_length=64, default='in basket')
	
	def __str__(self):
		return f"{self.user} - {self.order_status}"

class MenuTable(models.Model):
	id_position = models.AutoField(primary_key=True)
	category = models.CharField(max_length=64, help_text="Enter the category of dish")
	dish_name = models.CharField(max_length=64, null=True, help_text="Enter a dish")
	price_sml = models.DecimalField(max_digits=4, decimal_places=2, \
									null=True, blank=True, help_text="Enter price")
	price_lrg = models.DecimalField(max_digits=4, decimal_places=2, \
									null=True, blank=True, help_text="Enter price")
	topping_count = models.IntegerField(null=True, blank=True,\
									help_text="Enter topping count")
	def __str__(self):
		return f"{self.category} - {self.dish_name} - {self.price_sml} - {self.price_lrg}"

class OrderDetails(models.Model):
	order_number = models.ForeignKey(Orders, on_delete=models.CASCADE)
	dish_id = models.ForeignKey(MenuTable, on_delete=models.CASCADE, related_name='dish_name_ref')
	price = models.DecimalField(max_digits=4, decimal_places=2, \
									null=True, blank=True)
	topping_for = models.ForeignKey("OrderDetails", on_delete=models.CASCADE,\
		null=True, blank=True)
	def __str__(self):
		return f"{self.order_number} - {self.dish_id} - {self.price} - {self.topping_for} "