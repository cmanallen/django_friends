from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class RelationshipManager(models.Manager):
	def get_list_of_friends(self, user):
		""" Get a list of the users friends """
		return self.filter(user=user,status=FRIENDS)

	def get_relationship(self, active, passive):
		""" Get the relationship of two given users. """
		return self.filter(
			Q(user=passive,target=active) |
			Q(user=active,target=passive)
		).values('status').order_by("-status")[0]

	def request(self, user, target):
		""" Request friendship with another user """
		relation, created = self.get_or_create(
			user=user, 
			target=target, 
			defaults={'status': PENDING}
		)
		return created

	def accept(self, user, target):
		"""
		Create appropriate model relations for friends.  Returns 'True' if
		successful.
		"""
		try:
			relation, created = self.get_or_create(user=user, target=target)
			if not created:
				relation.update(status=FRIENDS)
			self.filter(user=target, target=user).update(status=FRIENDS)
		except:
			status = False
		else:
			status = True
		return status


	def deny(self, user, target):
		""" Deny the request by deleting the entry """
		try:
			self.filter(user=target,target=user,status=PENDING).delete()
		except:
			status = False
		else:
			status = True

		return status

	def block(self, user, target):
		""" Create a new entry in the Relationship model with status of '2' """
		relation, created = self.get_or_create(user=user, target=target)
		try:
			if created:
				relation.update(status=BLOCKED)
			else:
				new = Relationship(user=user, target=target, status=BLOCKED)
				new.save()
		except:
			status = False
		else:
			status = True

		return status

	def unblock(self, user, target):
		"""
		Remove a block entry from the Relationship model
		"""
		try:
			self.filter(user=user, target=target, status=BLOCKED).delete()
		except:
			status = False
		else:
			status = True

		return status

class Relationship(models.Model):
	PENDING = 0
	FRIENDS = 1
	BLOCKED = 2
	STATUS_CHOICES = (
		(PENDING, "Pending"),
		(FRIENDS, "Friends"),
		(BLOCKED, "Blocked"),
	)

	# Relations
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user')
	target = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='target')
	
	# Fields
	status = models.IntegerField(choices=STATUS_CHOICES, default=0)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	# Manager
	objects = RelationshipManager()

	# Model Methods
	def __str__(self):
		return "%s's relation with %s is %s" % (self.user, self.friend, self.status)
