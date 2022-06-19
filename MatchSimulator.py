'''
AUTHOR: endlessutopia7
DATE: 2022/06/19
A tennis match process simulator
'''

# for random implementation rand()
from random import *

class Mode(object):
	def __init__(self, winningSet, enterTiebreakerPoint = -1, tiebreakerIndex = -1):
		self.winningSet = winningSet
		self.enterTiebreakerPoint = enterTiebreakerPoint
		self.tiebreakerIndex = tiebreakerIndex

	def getSetCount(self):
		return self.winningSet

	def getEnterTiebreakerPoint(self):
		return self.enterTiebreakerPoint

	def getTiebreakerIndex(self):
		return self.tiebreakerIndex

# for constant setup variables
class Constants(object):
	# score for display for non-tiebreaker games
	SCORE_MAP = {0: "0", 1: "15", 2: "30", 3: "40"}

	# coefficients
	PREFIX_COEFFICIENT = 0.4
	CURVE_COEFFICIENT = 0.002

	# ordinary constants
	LOVEGAME_INDEX = 4
	DEFAULT_WINGAME_INDEX = 6

	# mode configurations
	ONE_SET_TIEBREAKER = Mode(1, 6, 7)
	ONE_SET_TIEBREAKER_TEN_POINTS = Mode(1, 6, 10)
	ONE_SET_NON_TIEBREAKER = Mode(1)
	ONE_GAME_TIEBREAKER_TEN_POINTS = Mode(1, 0, 10)

	THREE_SETS_TIEBREAKER = Mode(3, 6, 7)
	THREE_SETS_TIEBREAKER_TEN_POINTS = Mode(3, 6, 10)
	THREE_SETS_SUPER_TIEBREAKER = Mode(3, 12, 12)
	THREE_SETS_NON_TIEBREAKER = Mode(3)
	THREE_SETS_ONE_GAME_TIEBREAKER = Mode(3, 0, 10)

	FIVE_SETS_TIEBREAKER = Mode(5, 6, 7)
	FIVE_SETS_TIEBREAKER_TEN_POINTS = Mode(5, 6, 10)
	FIVE_SETS_SUPER_TIEBREAKER = Mode(5, 12, 12)
	FIVE_SETS_NON_TIEBREAKER = Mode(5)
	FIVE_SETS_ONE_GAME_TIEBREAKER = Mode(5, 0, 10)

	def constructMode(modeNumber):
		if modeNumber == 1:
			return Constants.ONE_SET_TIEBREAKER
		elif modeNumber == 2:
			return Constants.ONE_SET_TIEBREAKER_TEN_POINTS
		elif modeNumber == 3:
			return Constants.ONE_SET_NON_TIEBREAKER
		elif modeNumber == 4:
			return Constants.ONE_GAME_TIEBREAKER_TEN_POINTS
		elif modeNumber == 5:
			return Constants.THREE_SETS_TIEBREAKER
		elif modeNumber == 6:
			return Constants.THREE_SETS_TIEBREAKER_TEN_POINTS
		elif modeNumber == 7:
			return Constants.THREE_SETS_SUPER_TIEBREAKER
		elif modeNumber == 8:
			return Constants.THREE_SETS_NON_TIEBREAKER
		elif modeNumber == 9:
			return Constants.THREE_SETS_ONE_GAME_TIEBREAKER
		elif modeNumber == 10:
			return Constants.FIVE_SETS_TIEBREAKER
		elif modeNumber == 11:
			return Constants.FIVE_SETS_TIEBREAKER_TEN_POINTS
		elif modeNumber == 12:
			return Constants.FIVE_SETS_SUPER_TIEBREAKER
		elif modeNumber == 13:
			return Constants.FIVE_SETS_NON_TIEBREAKER
		elif modeNumber == 14:
			return Constants.FIVE_SETS_ONE_GAME_TIEBREAKER
		else:
			return None

class Player(object):
	def __init__(self, playerName = "Player"):
		# player info
		self.playerName = playerName

		# current match data
		self.currentPoints = 0
		self.currentGames = 0

		# total match data
		self.totalPoints = 0
		self.totalGames = 0

		self.sets = 0

	# getters
	def getPlayerName(self):
		return self.playerName

	def getCurrentPoints(self):
		return self.currentPoints

	def getCurrentGames(self):
		return self.currentGames

	def getTotalPoints(self):
		return self.totalPoints

	def getTotalGames(self):
		return self.totalGames

	def getSets(self):
		return self.sets

	# setters
	def addPoint(self):
		self.currentPoints += 1
		self.totalPoints += 1

	def addGame(self):
		self.currentGames += 1
		self.totalGames += 1

	def addSet(self):
		self.sets += 1

	def finishGame(self):
		self.currentPoints = 0

	def finishSet(self):
		self.finishGame()
		self.currentGames = 0

	def finishMatch(self):
		self.finishGame()
		self.finishSet()
		self.playerName = ""
		self.totalPoints, self.totalGames, self.sets = 0, 0, 0

class Match(object):
	def __init__(self, player1, player2, winnerPercentage, mode):
		# players info
		self.player1 = player1
		self.player2 = player2

		if winnerPercentage not in range(101):
			raise Exception("invalid percentage input")
		self.winnerPercentage = Constants.PREFIX_COEFFICIENT + Constants.CURVE_COEFFICIENT * winnerPercentage

		self.mode = mode

		# list to store game scores for each set
		self.__totalGame = 1    # start from Game 1
		self.__totalSet = 1    # start from Set 1
		self.__scoreList = []

	def playMatch(self):
		self.__initMatchStart()

		while not self.__isMatchEnd():
			findTiebreaker = self.__findTiebreaker();

			if findTiebreaker == -1:
				winnerSet = self.__playSingleGame()
				winner, loser = winnerSet[0], winnerSet[1]

				self.__updateGame(winner, loser)

				if self.__isSetEnd():
					self.__updateSet(winner, loser)

			# is tie-breaker
			else:
				winnerSet = self.__playSingleGame(findTiebreaker, False)
				winner, loser = winnerSet[0], winnerSet[1]

				# update directly
				loserPoints = loser.getCurrentPoints()
				self.__updateGame(winner, loser)
				self.__updateSet(winner, loser, True, loserPoints)

		self.__printAll("GAME, SET, MATCH")
		resultString = self.player1.getPlayerName()
		resultString += " %d:%d" % (self.player1.getSets(), self.player2.getSets())
		resultString += " (%s)" % (" ".join(self.__scoreList))
		resultString += " %s" % (self.player2.getPlayerName())

		# print total points stats
		self.__printAll(resultString, True, False)
		self.__printAll("Total Points: ")
		self.__printAll("%s: %d, %s: %d" % (
			self.player1.getPlayerName(), 
			self.player1.getTotalPoints(), 
			self.player2.getPlayerName(),
			self.player2.getTotalPoints()), 
			False, 
			True)

		self.__clearUp()

	def __initMatchStart(self):
		self.__printAll(("%s vs %s" % (self.player1.getPlayerName(), self.player2.getPlayerName())), False, True)
		self.__printAll("Set 1", False, True)

	# play a single game and return the winner set if winner is decided for direct update of game, set results
	def __playSingleGame(self, winningPoint = Constants.LOVEGAME_INDEX, isOrdinaryGame = True):
		winnerSet = None

		while True:
			currentIndex = random()

			# Player 1 wins
			if currentIndex <= self.winnerPercentage:
				self.player1.addPoint()

			# Player 2 wins
			else:
				self.player2.addPoint()

			# non-null only if winner is decided
			winnerSet = self.__isGameEnd(winningPoint)

			# last point of ordinary game won't print out
			if winnerSet == None:
				if isOrdinaryGame:
					currentScoreFormat = self.__formatCurrentScores()
				else:
					currentScoreFormat = "%d:%d" % (self.player1.getCurrentPoints(), self.player2.getCurrentPoints())
				self.__printAll(currentScoreFormat)
			else:
				if not isOrdinaryGame:
					if isOrdinaryGame:
						currentScoreFormat = self.__formatCurrentScores()
					else:
						currentScoreFormat = "%d:%d" % (self.player1.getCurrentPoints(), self.player2.getCurrentPoints())

					self.__printAll(currentScoreFormat)

				break

		return winnerSet

	def __printAll(self, string = "", hasFrontEmptyLine = False, hasBackEmptyLine = False):
		if hasFrontEmptyLine:
			print()
			# TBD: if add write to file, then add it here, 
			# *for sake of extensibility*

		print(string)

		if hasBackEmptyLine:
			print()
			# TBD: if add write to file, then add it here, 
			# *for sake of extensibility*

	def __formatCurrentScores(self):
		currentPlayer1Points = self.player1.getCurrentPoints()
		currentPlayer2Points = self.player2.getCurrentPoints()

		# for "15:0", "30:0" etc.
		if not (currentPlayer1Points >= Constants.LOVEGAME_INDEX - 1 
			and currentPlayer2Points >= Constants.LOVEGAME_INDEX - 1):
			return "%s:%s" % (Constants.SCORE_MAP[currentPlayer1Points],
					Constants.SCORE_MAP[currentPlayer2Points])

		# for deuces
		else:
			if currentPlayer1Points == currentPlayer2Points:
				return "40:40"
			elif currentPlayer1Points > currentPlayer2Points:
				return "A:40"
			else:
				return "40:A"

	def __isGameEnd(self, winningPoint):
		players = sorted((self.player1, self.player2), key = lambda x: -x.getCurrentPoints())

		winnerPoints = players[0].getCurrentPoints()
		loserPoints = players[1].getCurrentPoints()

		if winnerPoints >= winningPoint and winnerPoints - loserPoints >= 2:
			return players
		else:
			return None

	def __isSetEnd(self):
		players = sorted((self.player1, self.player2), key = lambda x: -x.getCurrentGames())

		winnerGames = players[0].getCurrentGames()
		loserGames = players[1].getCurrentGames()

		# "1-game 1:0" case
		if self.__totalSet == self.mode.getSetCount() and self.mode.getEnterTiebreakerPoint() == 0:
			return players if winnerGames == 1 and loserGames == 0 else None
		else:
			if winnerGames >= Constants.DEFAULT_WINGAME_INDEX and winnerGames - loserGames >= 2:
				return True
			else:
				return False

	def __isMatchEnd(self):
		winnerSets = max(self.player1.getSets(), self.player2.getSets())

		return winnerSets >= self.mode.getSetCount() // 2 + 1

	def __updateGame(self, winner, loser):
			winner.addGame()
			winner.finishGame()
			loser.finishGame()

			self.__printAll("%d:%d" % (self.player1.getCurrentGames(), self.player2.getCurrentGames()), True, True)
			self.__totalGame += 1

	def __updateSet(self, winner, loser, isTieBreaker = False, loserPoints = 0):
			# record previous set scores
			if isTieBreaker:
				scoreString = "%d:%d(%d)" % (self.player1.getCurrentGames(), self.player2.getCurrentGames(), loserPoints)
			else:
				scoreString = "%d:%d" % (self.player1.getCurrentGames(), self.player2.getCurrentGames())

			self.__scoreList.append(scoreString)

			# finialize the set for both players
			winner.addSet()
			winner.finishSet()
			loser.finishSet()

			self.__totalSet += 1
			self.__totalGame = 1

			if not self.__isMatchEnd():
				self.__printAll("Set %d" % (self.__totalSet), False, True)

	def __findTiebreaker(self):
		if self.__totalSet < self.mode.getSetCount():
			# normal set
			if self.__totalGame == 2 * Constants.DEFAULT_WINGAME_INDEX + 1:
				return 7
			else:
				return -1
		else:
			if self.mode.getEnterTiebreakerPoint == -1:
				return -1
			else:
				if self.__totalGame == 2 * self.mode.getEnterTiebreakerPoint() + 1:
					return self.mode.getTiebreakerIndex();
				else:
					return -1

	def __clearUp(self):
		# finalize player data
		self.player1.finishMatch()
		self.player2.finishMatch()

		# finialize match data
		self.__totalSet = 1
		self.__scoreList = []

if __name__ == "__main__":
	player1 = Player(str(input("Type Player 1 Name: ")))
	player2 = Player(str(input("Type Player 2 Name: ")))

	percentage = int(input(("How much confidence in %s winning %s (type a number in 0 - 100)? ") % (player1.getPlayerName(), player2.getPlayerName())))
	
	print("Which mode to play?")
	print("1) 1 Set w/ Tiebreaker")
	print("2) 1 Set w/ Tiebreaker (10 Points)")
	print("3) 1 Set w/o Tiebreaker")
	print("4) 1 Set Single Game Tiebreaker (10 Points)")
	print("5) 3 Sets w/ Tiebreaker")
	print("6) 3 Sets w/ Tiebreaker (10 Points)")
	print("7) 3 Sets w/ Super Tiebreaker (Wimbledon)")
	print("8) 3 Sets w/ Decisive Set")
	print("9) 3 Sets w/ Single Game Tiebreaker (10 Points)")
	print("10) 5 Sets w/ Tiebreaker")
	print("11) 5 Sets w/ Tiebreaker (10 Points)")
	print("12) 5 Sets w/ Super Tiebreaker (Wimbledon)")
	print("13) 5 Sets w/ Decisive Set")
	print("14) 5 Sets w/ Single Game Tiebreaker (10 Points)")

	modeNumber = int(input("Choose the mode to play (type a number in 0 - 14): "))
	mode = Constants.constructMode(modeNumber)
	match = Match(player1, player2, percentage, mode)
	match.playMatch()