from thread import Thread


thread_example = Thread('example')
##########################

thread_example.update_votes('A', 'B', 40)
thread_example.update_votes('B', 'A', 70)

#########################
for username, user in thread_example:
    print(username, f'{user.votes:.2f}')
