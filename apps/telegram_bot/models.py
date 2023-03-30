from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class Client(models.Model):
	class States(models.IntegerChoices):
		active = 0
		blocked = 10
		dead = 20

	login = models.CharField(max_length=25, validators=[RegexValidator(r"^\w+[\w\.\-]+\w+$")])
	email = models.CharField(max_length=50, validators=[RegexValidator(r"^\w+[\w\.\-]+\w+@([\w\-]+\.)+\w+$")])
	password = models.CharField(max_length=25, validators=[RegexValidator(r'^[\w!@#$%^&*()+\-=[\]{};:\'",.<>/?]+$')])
	password_hash = models.CharField(max_length=64)
	last_login = models.DateTimeField()
	state = models.IntegerField(choices=States.choices, default=States.active)
	max_settings_count = models.PositiveIntegerField(default=5)

	def __str__(self):
		return f"{self.pk}: {self.login}"


class Service(models.Model):
	title = models.CharField(max_length=25)
	api_class_name = models.CharField(max_length=25)
	required_parameters = models.JSONField(default=list)

	def __str__(self):
		return self.title


class CurrencyPair(models.Model):
	class States(models.IntegerChoices):
		active = 0
		disabled = 10

	service = models.ForeignKey(Service, on_delete=models.CASCADE)
	name = models.CharField(max_length=25)
	state = models.IntegerField(choices=States.choices, default=States.active)

	def __str__(self):
		return f"{self.name} (service {self.service.title})"


class Setting(models.Model):
	MAX_INDICATORS_PER_SETTING = 10

	client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='settings')
	currency_pair = models.ForeignKey(CurrencyPair, on_delete=models.CharField, related_name='settings')
	trading_value = models.FloatField(default=0)
	stop_loss = models.FloatField(default=0)
	take_profit = models.FloatField(default=0)
	parameters = models.JSONField(default=dict)
	label = models.CharField(max_length=25, default="Trading setting")

	def save(self, *args, **kwargs):
		if self.client.settings.count() >= self.client.max_settings_count:
			raise ValueError("Maximum number of settings reached.")
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.label} (client {self.client.pk})"

	def clean(self):
		super().clean()
		missing_parameters = []
		for parameter in self.currency_pair.service.required_parameters:
			if parameter not in self.parameters:
				missing_parameters.append(parameter)
		if missing_parameters:
			raise ValidationError(f"Missing required parameters: {', '.join(missing_parameters)}")


class Indicator(models.Model):
	class Kinds(models.TextChoices):
		RSI = "RSI"

	setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name='indicators')
	kind = models.CharField(max_length=15, choices=Kinds.choices)
	parameters = models.JSONField(default=dict)

	def save(self, *args, **kwargs):
		if self.setting.indicators.count() >= self.setting.MAX_INDICATORS_PER_SETTING:
			raise ValueError("Maximum number of indicators per setting reached.")
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.kind} (client {self.setting.client.pk})"
