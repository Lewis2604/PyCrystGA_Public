import sqlite3
import json
from pprint import pprint

class SQLite:
    def __init__(self, dbFile, pycrystGA):

        self.dbFile = dbFile
        self.pycrystGA = pycrystGA
        self.conn = sqlite3.connect(self.dbFile)
        self.cur = self.conn.cursor()
    #     self.cur = self.createConnection().cursor()
    #
    # def createConnection(self):
    #     self.conn = None
    #     try:
    #         self.conn = sqlite3.connect(self.dbFile)
    #         print("Connection to DBFile established")
    #     except sqlite3.Error as error:
    #         print("Unable to establish connection to DBFile", error)
    #
    #     return self.conn

    def createTables(self):
        # conn = sqlite3.connect(self.dbFile)
        # cur = self.conn.cursor()
        try:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS AllStructures (
            runid TEXT,
            id TEXT, 
            genID REAL,     
            torsAng TEXT,
            positions TEXT,
            orientations TEXT,
            fitness REAL,
            numEvals REAL);''')
            self.cur.execute('''CREATE TABLE IF NOT EXISTS EliteStructures (
            runid TEXT,
            id TEXT, 
            genID REAL,     
            torsAng TEXT,
            positions TEXT,
            orientations TEXT,
            fitness REAL);''')
            self.cur.execute('''CREATE TABLE IF NOT EXISTS MutantStructures (
            runid TEXT,
            id TEXT, 
            genID REAL, 
            torsAng TEXT,
            positions TEXT,
            orientations TEXT,
            fitness REAL);''')
            self.cur.execute('''CREATE TABLE IF NOT EXISTS Runs (
            id INTEGER PRIMARY KEY,
            runid TEXT, 
            popSize INTEGER,
            maxGen INTEGER,
            crossoverType INTEGER,
            mutationType INTEGER,
            molFile TEXT,
            numMol REAL,
            logNval REAL,
            trigNval REAL,
            exponentFactor REAL,
            ILMDHCFactor REAL,
            DHMILCFactor REAL,
            spikeThreshold REAL,
            stdDevGradient REAL,
            rollAvgRange REAL
            );''')
            self.cur.execute('''CREATE TABLE IF NOT EXISTS Generation (
            id TEXT, 
            generation INTEGER,
            crossoverRate REAL,
            mutationRate REAL)''')

        except sqlite3.Error as error:
            print("Database already exists", error)

        # finally:
        #     # if conn:
        #     self.conn.close()



    def createElitePopulation(self):
        # conn = sqlite3.connect(self.dbFile)
        # cur = self.conn.cursor()
        dataList = []

        insertQuery = "INSERT INTO EliteStructures values (?, ?, ?, ?, ?, ?, ?);"

        for i in self.pycrystGA.population.structures:
            runID = self.pycrystGA.identifier
            iDs = i.identifier
            genId = self.pycrystGA.currentGeneration
            # tors = i.torsions[0]
            # pos = i.positions[0]
            # orient = i.orientations[0]
            tors = json.dumps(i.torsions)
            pos = json.dumps(i.positions)
            orient = json.dumps(i.orientations)
            Fitness = i.fitness.values[0]

            tuple = (runID, iDs, genId, tors, pos, orient, Fitness)

            dataList.append(tuple)

        try:
            self.cur.executemany(insertQuery, dataList)
            self.conn.commit()

        except sqlite3.Error as error:
            print("Failed to insert data in elite DB table", error)

        # finally:
        #     # if self.conn:
        #     self.conn.close()
        #     print("SQLite connection closed")


    def createMutantPopulation(self):
        # conn = sqlite3.connect(self.dbFile)
        # cur = self.conn.cursor()
        dataList = []

        insertQuery = "INSERT INTO MutantStructures values (?, ?, ?, ?, ?, ?, ?);"

        for i in self.pycrystGA.population.structures:
            runID = self.pycrystGA.identifier
            iDs = i.identifier
            genId = self.pycrystGA.currentGeneration
            # tors = i.torsions[0]
            # pos = i.positions[0]
            # orient = i.orientations[0]
            tors = json.dumps(i.torsions)
            pos = json.dumps(i.positions)
            orient = json.dumps(i.orientations)
            Fitness = i.fitness.values[0]

            tuple = (runID, iDs, genId, tors, pos, orient, Fitness)

            dataList.append(tuple)

        try:
            self.cur.executemany(insertQuery, dataList)
            self.conn.commit()

        except sqlite3.Error as error:
            print("Failed to insert data in elite DB table", error)

        # finally:
        #     # if self.conn:
        #     self.conn.close()
        #     print("SQLite connection closed")


    def createRuns(self):
        # conn = sqlite3.connect(self.dbFile)
        # cur = conn.cursor()
        try:
            a = self.pycrystGA.identifier
            b = self.pycrystGA.popSize
            c = self.pycrystGA.numGen
            d = self.pycrystGA.crossoverType
            e = self.pycrystGA.mutationType
            f = self.pycrystGA.molFile
            g = self.pycrystGA.numMol
            h = self.pycrystGA.LogNVal
            i = self.pycrystGA.trigNVal
            j = self.pycrystGA.exponentFactor
            k = self.pycrystGA.ILMDHCSF
            l = self.pycrystGA.DHMILCSF
            m = self.pycrystGA.spikeThreshold
            n = self.pycrystGA.stdDevGradient
            o = self.pycrystGA.rollingAvgRange


            insertQuery = "INSERT INTO Runs values (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

            dataList = (a,
                        b,
                        c,
                        d,
                        e,
                        f,
                        g,
                        h,
                        i,
                        j,
                        k,
                        l,
                        m,
                        n,
                        o)

            self.cur.execute(insertQuery, dataList)
            self.conn.commit()

        except sqlite3.Error as error:
            print("Failed to insert data in Runs DB table", error)

        # finally:
        #     # if self.conn:
        #     self.conn.close()
        #     print("SQLite connection closed")
        # print("Runs End")


    def createGeneration(self):
        # conn = sqlite3.connect(self.dbFile)
        # cur = conn.cursor()
        try:
            a = self.pycrystGA.identifier
            b = self.pycrystGA.currentGeneration
            c = self.pycrystGA.crossoverPercentage
            d = self.pycrystGA.mutationPercentage


            insertQuery = "INSERT INTO Generation values (?, ?, ?, ?);"

            dataList = (a,
                        b,
                        c,
                        d)

            self.cur.execute(insertQuery, dataList)
            self.conn.commit()

        except sqlite3.Error as error:
            print("Failed to insert data in Generation DB table", error)

        # finally:
        #     if self.conn:
        #         self.conn.close()
        #         print("SQLite connection closed")

    def createStructures(self, structure):
        # conn = sqlite3.connect(self.dbFile)
        # cur = conn.cursor()
        dataList = []

        insertQuery = "INSERT INTO AllStructures values (?, ?, ?, ?, ?, ?, ?, ?);"

        runID = self.pycrystGA.identifier
        iDs = structure.identifier
        genId = self.pycrystGA.currentGeneration
        # tors = i.torsions[0]
        # pos = i.positions[0]
        # orient = i.orientations[0]
        tors = json.dumps(structure.torsions)
        pos = json.dumps(structure.positions)
        orient = json.dumps(structure.orientations)
        Fitness = structure.fitness.values[0]
        nEval = self.pycrystGA.numEvals

        tuple = (runID, iDs, genId, tors, pos, orient, Fitness, nEval)

        dataList.append(tuple)

        try:
            self.cur.executemany(insertQuery, dataList)
            self.conn.commit()

        except sqlite3.Error as error:
            print("Failed to insert data in elite DB table", error)

        # finally:
        #     # if self.conn:
        #     conn.close()
        #     print("SQLite connection closed")

