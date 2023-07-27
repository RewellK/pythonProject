from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests


class ObjAddress:
    def __init__(self, strStreet, strNumber, strCity, strState, strCEP):
        self.strStreet = strStreet
        self.strNumber = strNumber
        self.strCity = strCity
        self.strState = strState
        self.strCEP = strCEP
        self.latitude = None
        self.longitude = None

    def get_location(self, strKey):
        strAddress = f"{self.strStreet}, {self.strNumber}, {self.strCity}, {self.strState}, {self.strCEP}"
        url = f"https://api.opencagedata.com/geocode/v1/json?q={strAddress}&key={strKey}"
        response = requests.get(url)

        try:
            if response.status_code == 200:
                data = response.json()
                results = data['results']
                if results:
                    result = results[0]
                    geometry = result['geometry']
                    latitude = geometry['lat']
                    self.latitude = latitude
                    longitude = geometry['lng']
                    self.longitude = longitude
                else:
                    print("No results found.")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Exception: {str(e)}")


class Address(models.Model):
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    cep = models.CharField(max_length=10)


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        address = Address()
        address.save()

        obj_address = ObjAddress(
            strStreet=extra_fields.get('street', ''),
            strNumber=extra_fields.get('number', ''),
            strCity=extra_fields.get('city', ''),
            strState=extra_fields.get('state', ''),
            strCEP=extra_fields.get('cep', ''),
        )
        obj_address.get_location("60a91a7e7e514c2fa9502f125df630ac")

        address.street = obj_address.strStreet
        address.number = obj_address.strNumber
        address.city = obj_address.strCity
        address.state = obj_address.strState
        address.cep = obj_address.strCEP
        address.save()

        extra_fields['address'] = address
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)

    objects = CustomUserManager()


@receiver(post_save, sender=User)
def create_address(sender, instance, created, **kwargs):
    if created and not instance.address:
        address = Address()
        address.save()

        instance.address = address
        instance.save()

        obj_address = ObjAddress(
            strStreet=address.street,
            strNumber=address.number,
            strCity=address.city,
            strState=address.state,
            strCEP=address.cep,
        )
        obj_address.get_location("60a91a7e7e514c2fa9502f125df630ac")

        address.street = obj_address.strStreet
        address.number = obj_address.strNumber
        address.city = obj_address.strCity
        address.state = obj_address.strState
        address.cep = obj_address.strCEP
        address.save()
