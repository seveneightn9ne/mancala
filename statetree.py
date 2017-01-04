from mancala import *
import pickle

queue = [new_game(me)]
tree = set([])
forward_arrows = {}
backward_arrows = {}
stop_exploring = set([])
definite_winner = {}
round = 0
while queue:
	#round += 1
	#print "----- round " + str(round) + " -----"
	if len(tree) % 10000 == 0:
		print "Seen " + str(len(tree)) + " states, with " + str(len(queue)) + " in the queue"
	state = queue.pop()
	#print state
	if state in tree or state in stop_exploring:
		#print "I've been here before. Skipping!"
		continue
	tree.add(state)
	if state.is_game_over() and state.did_they_win(state.whose_turn):
		# something, surely
		backfill_result(state, state.whose_turn)
		continue
	next_states = state_transition(state)
	forward_arrows[state] = next_states
	for next_state in next_states:
		backward_arrows[next_state] = backward_arrows.get(next_state, []) + [state]
	#print str(len(next_states)) + " states from there"
	#new_states = filter(lambda s: s not in visited, all_states)
	#for state in all_states:
	#	if state in visited:
	#		print "Skipping this state, which is a duplicate:"
	#		print str(state)
	#if len(new_states) < len(all_states):
	#	print str(len(all_states)-len(new_states)) + " states skipped because they aren't new to me"
	#if next_states:
	queue.extend(next_states)
print "Finished with " + str(len(visited)) + " states found."
#for state in visited:
#	print state
pickle.dump(visited, open('states.pkl', 'w'))

def backfill_result(state, winner):
	if state in definite_winner:
		return
	definite_winner[state] = winner
	for parent in backward_arrows.get(state, []):
		backfill_result(parent, winner)
