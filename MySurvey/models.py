from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save

from django.dispatch import receiver

from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=200, blank = True)
    
    last_name = models.CharField(max_length=200, blank = True)
    
    email = models.EmailField(max_length=254, blank = True)
    
    password = models.CharField(max_length=200, blank = True)

    def __str__(self):
        
        return 'Profile of user: %s' % (self.user.username)

@receiver(post_save, sender=User)

def create_user_profile(sender, instance, created, **kwargs):
    
    if created:
        
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)

def save_user_profile(sender, instance, **kwargs):
    
    instance.profile.save()


class Product(models.Model):

    product_name = models.CharField(max_length=200)
    
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):

        return self.product_name


#Product question:
class Question(models.Model):
    
    product = models.ManyToManyField(Product)

    question_text = models.CharField(max_length=200)
    
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):

        return self.question_text

#Programming question:
class ProgrammingQuestion(models.Model):

    programming_question_text = models.CharField(max_length=200)
    
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        
        return self.programming_question_text



class Rating(models.Model):

    question =  models.ManyToManyField(Question)

    programming_question =  models.ManyToManyField(ProgrammingQuestion)

    rating_text = models.CharField(max_length=200)

    rating_number=models.IntegerField(default=0)

    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
    
        return self.rating_text


class productResults(models.Model):

    user_id_number = models.IntegerField(default=0)
    
    question_number = models.IntegerField(default=0)
    
    rating_number =  models.IntegerField(default=0)
    
    update_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
    
        return 'Results of user: %s, Question number: %s, rating_number: %s' % (self.user_id_number, self.question_number, self.rating_number)


class programmingResults(models.Model):
    
    user_id_number = models.IntegerField(default=0)
    
    question_number = models.IntegerField(default=0)
    
    rating_number =  models.IntegerField(default=0)
    
    update_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        
        return 'Results of user: %s, Question number: %s, rating_number: %s' % (self.user_id_number, self.question_number, self.rating_number)














