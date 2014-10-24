from django.core.urlresolvers import reverse
from django.views.generic import FormView

from .models import Friend
from .mixins import LoginRequiredMixin


# Create your views here.
class AddFriendView(LoginRequiredMixin, FormView):
	"""
	Sends a friend request from one user to another user
	"""
	template_name = "add_friend.html"
	user = self.request.user

	def check_relationship(self):
		existing = Friend.objects.filter(user=friend, friend=user)
		if existing:
			status = 1
		else:
			status = 0
		return status

	def get_form_kwargs(self):
		kwargs = super(AddFriendView, self).get_form_kwargs(**kwargs)
		kwargs['user'] = user
		kwargs['status'] = self.check_relationship()
		return kwargs

	def get_success_url(self):
		return reverse('detail-profile', kwargs={'pk': user})

class ConfirmFriendView(LoginRequiredMixin, FormView):
	"""
	Confirms a friend request sent by user
	"""
	template_name = "confirm_friend.html"
	user = self.request.user

	def get_form_kwargs(self):
		kwargs = super(ConfirmFriendView, self).get_form_kwargs(**kwargs)
		kwargs['user'] = user
		kwargs['status'] = 1
		return kwargs

	def get_success_url(self):
		return reverse('detail-profile', kwargs={'pk': user})

class BlockFriendView(LoginRequiredMixin, FormView):
	"""
	Blocks a user from interacting with another user
	"""
	template_name = "block_friend.html"
	user = self.request.user

	def get_form_kwargs(self):
		kwargs = super(BlockFriendView, self).get_form_kwargs(**kwargs)
		kwargs['user'] = user
		kwargs['status'] = 2
		return kwargs

	def get_success_url(self):
		return reverse('detail-profile', kwargs={'pk': user})
