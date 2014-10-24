from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """
    Ensures that user must be authenticated in order to access view.
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class FriendshipRequiredMixin(object):
	"""
	Ensures that users must be friends in order to perform a task
	"""
	def dispatch(self, *args, **kwargs):
		return super(FriendshipRequired, self).dispatch(*args, **kwargs)

class PendingRequired(object):
	"""
	Ensures that users must be pending friends in order to perform
	a task
	"""
	def dispatch(self, *args, **kwargs):
		return super(PendingRequired, self).dispatch(*args, **kwargs)