from collections import deque, defaultdict


class User:

	@property
	def votes(self):
		return (sum(self._count_votes(self.voted_by).values()) + 100) / 100

	def __init__(self, name, post_id):
		self.post_id = post_id
		self.name = name
		self.voted_by = {}
		self.voted_for = {}
		self.pinned_at = None
		self.view_comments = deque()
		self.comments = []

	def __eq__(self, other):
		return self.name.lower() == other.name.lower()

	def __hash__(self):
		return hash(self.name.lower())

	def __lt__(self, other):
		return self.votes < other.votes 

	def __repr__(self):
		return f'User({self.name})'

	def __str__(self):
		return f'({self.name}, {self.votes})'

	def _count_votes(self, dictionary):
		received = defaultdict(int)
		for name, percent_voters in dictionary.items():
			percentage, voters = percent_voters
			received[name] += percentage
			if voters:
				for voter_name, percent in self._count_votes(voters).items():
					received[voter_name] += (percent * percentage) / 100
		for name, percentage in received.items():
			if percentage > 100:
				received[name] = 100
		return received

	def add_comment(self, comment):
		self.comments.append(comment)
		self.comments = sorted(self.comments,
							   key=lambda comment: len(comment.body),
							   reverse=True)

	def get_comment(self):
		if self.view_comments:
			return self.view_comments[0]
		elif self.comments:
			return self.comments[0]