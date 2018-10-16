from collections import defaultdict
from datetime import datetime

from user import User


class Thread:
	def __init__(self, post_id):
		self._name = None
		self.id = post_id
		self.users = defaultdict(lambda: User(self._name, self.id))
		self.sticky_comment = None
		self.pasted_comment = None
		self.pinned_users = set()
		self.created = None
		self.last_checked = datetime(1, 1, 1)
		self.total_voters = 0
		self.casted_votes = 0
		self.disabled = False

	def __iter__(self):
		return iter(self.users.items())

	def __repr__(self):
		return f'Thread({self.id})'

	def __str__(self):
		return f'{self.id}'

	def _del_user(self, dictionary, user):
		return {k: (v[0], self._del_user(v[1], user)) for
				k, v in dictionary.items() if k != user}

	def _vote_loop(self, current_name, other_names_values, seen=None):
		stack = [(current_name, other_name, value) 
				 for other_name, value in other_names_values.items()]
		while stack:
			current_name, other_name, value = stack.pop()
			if other_name not in seen:
				current = self.user(current_name)
				other = self.user(other_name)
				updated_voted_by = self._del_user(current.voted_by, other_name)
				other.voted_by[current_name] = (value, updated_voted_by)
				seen.add(other_name)
				stack += [(other_name, name, percentage)
						  for name, percentage in other.voted_for.items()]

	def update_votes(self, voter_name, parent_name, value=100, unvote=False):
		voter = self.user(voter_name)
		if unvote:
			other = self.user(parent_name)
			other.voted_by.pop(voter_name)
			_seen = {parent_name}
			self._vote_loop(parent_name, other.voted_for, seen=_seen)
			voter.voted_for.pop(parent_name)
			if not voter.voted_for:
				self.total_voters -= 1
			self.casted_votes -=1
		else:
			if not voter.voted_for:
				self.total_voters += 1
			self._vote_loop(voter_name, {parent_name: value}, seen=set())
			voter.voted_for[parent_name] = value
			self.casted_votes += 1

	def sorted_users(self):
		valid_users = [user for username, user in self if user.votes != 1]
		return sorted(valid_users, reverse=True)

	def user(self, username):
		self._name = username
		return self.users[username]
