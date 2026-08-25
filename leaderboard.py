import sqlite3 as sql
import math
import json

class Leaderboard:
    def __init__(self, databasepath="Assets\Database\mainDatabase.db", leaderboardfile="Assets\Leaderboard\leaderboard.json"):
        self.databasepath = databasepath
        self.leaderboardfile = leaderboardfile
 
    def calculatePlayerWeight(self, score, time):
        #prevents time from being negative
        #if it is, return 100x the score
        if time <= 0:
            return score * 100  

        #score provides the most weight
        scoreWeight = score * 100

        #time using logrithms
        timeBonus = 500 * math.log10(1 + (300 / time))

        weight = scoreWeight + timeBonus #gets the total weight
        return round(weight) #rounds it to closest integer
    
    def updatePlayerStats(self, username, score, time):

        connection = sql.connect(self.databasepath) #connects to the database
        cursor = connection.cursor()
        
        #gets the players currently best stats
        cursor.execute("""
            SELECT bestScore, bestTime, playerWeight FROM player WHERE Username = ?
        """, (username,))
        
        result = cursor.fetchone()
        
        if result:
            currentBestScore, currentBestTime, previousWeight = result #gets current player data

            newWeight = self.calculatePlayerWeight(score, time)

            #previous values are defaulted
            bestScore = currentBestScore
            bestTime = currentBestTime
            bestWeight = previousWeight

            #checks if theres a previous value, if there isnt one, 
            #the best score and time is the one the player got this run
            if previousWeight is None or newWeight > previousWeight:
                bestScore = score
                bestTime = time
                bestWeight = newWeight

            # Update database with the BEST values only
            cursor.execute("""
                UPDATE player 
                SET bestScore = ?, bestTime = ?, playerWeight = ?
                WHERE Username = ?
            """, (bestScore, bestTime, bestWeight, username)) #adds to database

            connection.commit()
        
        connection.close()
        
        # Recalculate all ranks
        self.updateRanks()
    
    def updateRanks(self):
        connection = sql.connect(self.databasepath)
        cursor = connection.cursor()
        
        #sorts the players based on their weight
        cursor.execute("""
            SELECT Username, bestScore, bestTime, playerWeight 
            FROM player
            ORDER BY playerWeight DESC
        """)
        
        players = cursor.fetchall()
        
        #assigns player ranks depending on how high their weight is
        for rank, player in enumerate(players, start=1):
            cursor.execute("""
                UPDATE player SET rankID = ? WHERE Username = ?
            """, (rank, player[0]))
        
        connection.commit()
        connection.close() #closes database connection

        #saves the leaderboard to a file with file handling
        self.saveLeaderboardToFile(players)
    
    def saveLeaderboardToFile(self, players):
        
        #initialises an array to store leaderboard data
        leaderboardData = []
        #the 'players' includes the data fetched by the database
        #this is the username, score, time and weight
        #rank is just the index which is grabbed with enumerate

        for rank, player in enumerate(players, start=1):
            #sinces theres no rank 0, it must start at rank 1
            #the index follows the order rankID, Username, bestScore, bestTime, playerWeight as shown by the database fields
            leaderboardData.append({'rank': rank,'username': player[0],'score': player[1],'time': player[2],'weight': player[3]})
        
        #opens leaderboard file to write
        with open(self.leaderboardfile, "w") as leaderboardDataFile:
            json.dump(leaderboardData, leaderboardDataFile, indent=4) #puts all data into the file
    
    def loadLeaderboardFromFile(self):
        #uses error checking to check for the leaderboard data file
        try:
            with open(self.leaderboardfile, "r") as leaderboardDataFile: #if theres a file, it opens it as a read file
                leaderboardData = json.load(leaderboardDataFile) #gets the data in the file
            return leaderboardData #returns this data
        except FileNotFoundError:
            return [] #returns table to indicate theres no file

    def getTopPlayers(self, maxVisiblePlayers):
        
        connection = sql.connect(self.databasepath) #estabilishes a connection with the database
        cursor = connection.cursor()
        
        #the SQL code below selects the rank id, username, score, time and weight of 10 players
        #the 10 players are chosen by their rank id. rank id 1 means they are number 1 in the leaderboard
        cursor.execute("""
            SELECT rankID, Username, bestScore, bestTime, playerWeight
            FROM player
            WHERE rankID > 0
            ORDER BY rankID ASC
            LIMIT ?
        """, (maxVisiblePlayers,))
        
        results = cursor.fetchall() #fetches values of all SELECTED fields with SQL
        connection.close() #closes database
        
        #gets all leaderboard data and puts it in a dictionary
        
        leaderboard = []
        for result in results:
        #the index follows the order rankID, Username, bestScore, bestTime, playerWeight as shown by the database fields
            leaderboard.append({'rank': result[0],'username': result[1],'score': result[2],'time': result[3],'weight': result[4]})
        
        return leaderboard
    
    def getPlayerRank(self, username):
        """
        Returns the rank info of a player as a dictionary, or None if not found
        """
        # Load the leaderboard from database (or optionally from file)
        leaderboard = self.getTopPlayers(10)  # Get all players, adjust number if needed
        
        for player in leaderboard:
            if player['username'] == username:
                return player  # This contains 'rank', 'username', 'score', 'time', 'weight'
        
        return None  # Player not found
