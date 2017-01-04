
me = True
you = False

class State(object):
	def __init__(self, whose_turn, board):
		self.whose_turn = whose_turn
		self.board = board
		#self.definite_winner = None
	def is_game_over(self):
		#if self.definite_winner != None:
		#	return True
		if self.board.my_mancala.marbles > 24 or self.board.your_mancala.marbles > 24:
			return True
		for who in (me, you):
			all_empty = True
			for i in range(6):
				if self.board.bucket(who, i).marbles > 0:
					all_empty = False
					break
			if all_empty:
				return True
	def did_they_win(self, who):
		if not self.is_game_over():
			return False
		#if self.definite_winner != None:
		#	return self.definite_winner == who
		if self.board.my_mancala.marbles > 24:
			return who == me
		if self.board.your_mancala.marbles > 24:
			return who == you
		return self.board.sum_marbles(who) > self.board.sum_marbles(not who)
	def __str__(self):
		if self.whose_turn == me:
			return "My turn:\n" + str(self.board)
		return "Your turn:\n" + str(self.board)
	def __eq__(self, other):
		return self.whose_turn == other.whose_turn and \
				self.board == other.board
	def __hash__(self):
		return (3 if self.whose_turn else 5) * hash(self.board)

class Bucket(object):
	def __init__(self, is_mancala, owner, marbles=None):
		if marbles is None:
			self.marbles = 0 if is_mancala else 4
		else:
			self.marbles = marbles
		self.is_mancala = is_mancala
		self.owner = owner
		self.neighbor = None
		self.opposite = None
	def set_neighbor(self, neighbor):
		assert self.neighbor is None
		assert neighbor.owner == self.owner or self.is_mancala
		self.neighbor = neighbor
	def set_opposite(self, opposite):
		assert self.opposite is None
		assert opposite.owner != self.owner
		self.opposite = opposite
	def copy(self):
		return Bucket(self.is_mancala, self.owner, self.marbles)#, self.position)
	#def copyWithNeighbor(self, neighbor):
	#	b = Bucket(self.is_mancala, self.owner)#, self.position)
	#	b.set_neighbor(neighbor)
	#	return b
	def put_was_empty(self, n=1):
		self.marbles += n
		return self.marbles == n
	def take(self, forgiving=False):
		assert forgiving or self.marbles > 0
		r = self.marbles
		self.marbles = 0
		return r
	def __str__(self):
		if not self.is_mancala:
			return "(" + str(self.marbles).rjust(2) + ")"
		return "[ " + str(self.marbles).rjust(2) + " ]"
	def __eq__(self, other):
		return self.marbles == other.marbles and \
				self.is_mancala == other.is_mancala
	def __hash__(self):
		return self.marbles

class Board(object):
	def __init__(self, copiedBoard=None):
		if copiedBoard:
			#print "copying board"
			self.my_buckets   = [b.copy() for b in copiedBoard.my_buckets]
			#print "my buckets are " + str(self.my_buckets)
			self.your_buckets = [b.copy() for b in copiedBoard.your_buckets]
			#print "your buckets are " + str(self.your_buckets)
			self.my_mancala   = copiedBoard.my_mancala.copy()
			self.your_mancala = copiedBoard.your_mancala.copy()
		else:
			#print "blank board"
			self.my_buckets   = [Bucket(False, me) for b in range(6)]
			self.your_buckets = [Bucket(False, you) for b in range(6)]
			self.my_mancala   =  Bucket(True, me)
			self.your_mancala =  Bucket(True, you)
		self.organize_buckets()
	def organize_buckets(self):
		self.my_mancala.set_neighbor(self.your_buckets[0])
		self.your_mancala.set_neighbor(self.my_buckets[0])
		self.your_buckets[-1].set_neighbor(self.your_mancala)
		self.my_buckets[-1].set_neighbor(self.my_mancala)
		for i in range(6):
			if i < 5:
				self.my_buckets[i].set_neighbor(self.my_buckets[i+1])
				self.your_buckets[i].set_neighbor(self.your_buckets[i+1])
			self.my_buckets[i].set_opposite(self.your_buckets[5-i])
			self.your_buckets[i].set_opposite(self.my_buckets[5-i])
	def copy(self):
		return Board(self)
	def mancala(self, who):
		return self.my_mancala if who == me else self.your_mancala
	def bucket(self, who, i):
		return self.my_buckets[i] if who == me else self.your_buckets[i]
	def sum_marbles(self, who):
		if who == me:
			return sum([b.marbles for b in self.my_buckets]) + self.my_mancala.marbles
		else:
			return sum([b.marbles for b in self.your_buckets]) + self.your_mancala.marbles
	def __str__(self):
		return "you: " + str(self.your_mancala) + " " + \
				" ".join([str(self.your_buckets[5-i]) for i in range(6)]) + "\n" + \
				"me:         " + " ".join([str(self.my_buckets[i]) for i in range(6)]) + \
				" " + str(self.my_mancala)
	def __eq__(self, other):
		return str(self) == str(other)
	def __hash__(self):
		return hash(str(self))

def state_transition(state):
	if state.is_game_over():
		#if state.did_they_win(me):
			#print "\nGame over! I win!"
			#print state.board
		#elif state.did_they_win(you):
			#print "\nGame over! I lose!"
			#print state.board
		#else:
			#print "\nGame over, it's a tie!"
			#print state.board
		return []
	#for i in range(6):
	#	if state.board.bucket(state.whose_turn, i).marbles == 0:
	#		print "Skipping moving at " + str(i) + " which is empty"
 	return [move(state, i) for i in range(6) \
			if state.board.bucket(state.whose_turn, i).marbles > 0]

def move(state, i):
	#print "@@@@Move " + str(i) + " from state:"
	#print state

	new_board = state.board.copy()
	bucket = new_board.bucket(state.whose_turn, i)
	#print "gonna take from bucket " + str(bucket)
	marbles = bucket.take()
	#print "Picked up marbles."
	#print new_board
	was_empty = False
	while marbles:
		#print "I have " + str(marbles) + " marbles."
		bucket = bucket.neighbor
		if bucket.is_mancala and bucket.owner != state.whose_turn:
			# Don't place a marble in the opponen'ts mancala
			#print "skipping the opponent's mancala"
			continue
		was_empty = bucket.put_was_empty()
		#print "put marbles in a bucket"
		#print new_board
		marbles -= 1
	if was_empty and not bucket.is_mancala and bucket.owner == state.whose_turn:
		# Ended on your own empty bucket, take opponent's marbles
		#print "I take opponent's marbles!"
		new_board.mancala(state.whose_turn).put_was_empty(bucket.opposite.take(True))
		#print new_board
	if bucket.is_mancala and bucket.owner == state.whose_turn:
		# Ended in my mancala, next turn is mine:
		#print "It's still my turn, returning"
		#print new_board
		return State(state.whose_turn, new_board)
	else:
		#print "Switching turn"
		#print new_board
		return State(not state.whose_turn, new_board)

def new_game(whose_turn):
	return State(whose_turn, Board())
