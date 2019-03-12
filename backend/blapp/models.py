from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from sorl.thumbnail import ImageField, get_thumbnail


class Profile(models.Model):
    # one to one relation with the User from django auth
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    friends = models.ManyToManyField("self", blank=True)
    friends_requests = models.ManyToManyField("self", blank=True)
    age = models.IntegerField(null=True)
    sex = models.CharField(null=True, max_length=6)
    bio = models.CharField(null=True, max_length=256)
    picture = models.ImageField(null=True, upload_to='images')
    picture_thumbnail = models.ImageField(null=True, upload_to='images', editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # override the save method to process the uploaded image
    # https://stackoverflow.com/questions/24373341/django-image-resizing-and-convert-before-upload
    def save(self, *args, **kwargs):
        if self.picture:
            self.picture_thumbnail = get_thumbnail(self.picture, '300x300', quality=99,
                                         crop='center', format='JPEG').name
        super(Profile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    picture = models.ImageField(null=True, upload_to='images')
    picture_standardized = models.ImageField(null=True, upload_to='images', editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # override the save method to process the uploaded image
    def save(self, *args, **kwargs):
        if self.picture:
            self.picture_standardized = get_thumbnail(self.picture, '1080x1080', quality=99,
                                         crop='center', format='JPEG').name
        super(Post, self).save(*args, **kwargs)


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
