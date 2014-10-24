from django.conf import settings
from django.db import models

# Create your models here.
class Friend(models.Model):
	PENDING = 0
	FRIENDS = 1
	BLOCKED = 2
	STATUS_CHOICES = (
		(PENDING, "Pending"),
		(FRIENDS, "Friends"),
		(BLOCKED, "Blocked"),
	)

	# Relations
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	friend = models.ForeignKey(settings.AUTH_USER_MODEL)
	
	# Fields
	status = models.IntegerField(choice = STATUS_CHOICES)
	created = models.DateTimeField(auto_add_now = True)

	# Models
	def __str__(self):
		return "%s's %s" % (self.user, self.friend)