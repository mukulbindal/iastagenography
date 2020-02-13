from django.db import models
from account.models import Users,Followers
from django.utils import timezone
class Room(models.Model):
    """Represents chat rooms that users can join"""
    name = models.CharField(max_length=30 , unique = True)
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)

    def __str__(self):
        """Returns human-readable representation of the model instance."""
        return self.name

class ReadMessages(models.Model):
	chat_id = models.ForeignKey(Followers , related_name = "JoinsRead" , on_delete = None)
	From = models.ForeignKey(Users, related_name = "fromRead" , on_delete = None)
	To = models.ForeignKey(Users , related_name = "toRead" , on_delete = None)
	message = models.CharField(max_length = 800)
	time_date = models.DateTimeField(default = timezone.now)
	class Meta:
		ordering = ('-time_date',)


class UnreadMessages(models.Model):
	chat_id = models.ForeignKey(Followers, related_name = "JoinsUnread" , on_delete = None)
	From = models.ForeignKey(Users, related_name = "fromUnread" , on_delete = None)
	To = models.ForeignKey(Users , related_name = "toUnread" , on_delete = None)
	message = models.CharField(max_length = 800)
	time_date = models.DateTimeField(default = timezone.now)
	class Meta:
		ordering = ('-time_date',)


