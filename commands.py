import re


class Commands:

	def __init__(self, commands_prefix, **commands_keywords):
		regex_strings = {
			'vote'		 : r'{}\s*(?P<vcmd>{})\s*(0*(?P<percent>\d+)\s*%?|'
						   r'\\#\s*0*(?P<nvotes>\d+))',
			'unvote'	 : r'{}\s*(?P<unvcmd>{})',
			'view'		 : r'{}\s*{}',
			'disablevote': r'{}\s*{}',
		}
		for command_name, regex_string in regex_strings.items():
			command_keyword = commands_keywords.get(command_name)
			formatted_regex_string = regex_string.format(commands_prefix,
														 command_keyword)
			setattr(self,
					f'{command_name}_regex',
					re.compile(formatted_regex_string, re.I))

	def is_valid(self, command_name, text):
		return getattr(self, f'{command_name}_regex').search(text) is not None

	def percentage(self, text, votes):
		nvotes = self.vote_regex.search(text).group('nvotes')
		if nvotes is None:
			percent = int(self.vote_regex.search(text).group('percent'))
		else:
			percent = int((int(nvotes) * 100) / votes) 
		if percent > 100:
			percent = 100
		elif percent < 1:
			return None
		return percent
