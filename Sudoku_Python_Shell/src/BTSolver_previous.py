import SudokuBoard
import Variable
import Domain
import Trail
import Constraint
import ConstraintNetwork
import time
import math
from operator import itemgetter
from collections import defaultdict
class BTSolver:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, gb, trail, val_sh, var_sh, cc ):
        self.network = ConstraintNetwork.ConstraintNetwork(gb)
        self.hassolution = False
        self.gameboard = gb
        self.trail = trail

        self.varHeuristics = var_sh
        self.valHeuristics = val_sh
        self.cChecks = cc

    # ==================================================================
    # Consistency Checks
    # ==================================================================

    # Basic consistency check, no propagation done
    def assignmentsCheck ( self ):
        for c in self.network.getConstraints():
            if not c.isConsistent():
                return False
        return True

    """
        Part 1 TODO: Implement the Forward Checking Heuristic

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        Note: remember to trail.push variables before you change their domain
        Return: true is assignment is consistent, false otherwise
    """
    def forwardChecking ( self ):
        """
        assigned = []
       # print(self.network)
        
        for rowno in range(len(self.gameboard.board)):
            for colno in range(len(self.gameboard.board)):
                if self.network.variables[rowno*len(self.gameboard.board) + colno].isAssigned():
                    assigned.append(self.network.variables[rowno*len(self.gameboard.board) + colno])
        for i in assigned:
            for j in self.network.variables:
                if j.row == i.row or j.col == i.col or j.block == i.block:
                    if len(i.getValues()) > 1:
                        print("Error: thought cell was assigned but its domain length > 1")
                    elif j.row == i.row and j.col == i.col:
                        if j.block != i.block:
                            print("Error: thought cells were same but were not")
                    else:
                        j.removeValueFromDomain(i.getValues()[0])
        for j in self.network.variables:
            if len(j.getValues()) == 0:
                return False
       # print(self.network)
        
        return True
        """
        gb = self.gameboard.board
        gblen = len(self.gameboard.board)
        gbvar = self.network.variables
        for i in range(gblen):
            for j in range(gblen):
                if len(gbvar[i*gblen + j].getValues()) >= 2:
                    for k in gb[i]:    #eliminate row
                        if k != 0:
                            gbvar[i*gblen + j].removeValueFromDomain(k)
                    for k in gb[:][j]: #eliminate column
                        if k != 0:
                            gbvar[i*gblen + j].removeValueFromDomain(k)
                    dd = self.my_block(gb) #block dict
                    ll = dd[(math.ceil(i/self.gameboard.p), math.ceil(j/self.gameboard.p))]
                    for k in ll:         #eliminate block
                        if k != 0:
                            gbvar[i*gblen + j].removeValueFromDomain(k)
                            
        for j in self.network.variables:
            if len(j.getValues()) == 0:
                return False                    
        return True

    def my_block(self,mygb):
        dd = defaultdict(list)
        for i in range(len(mygb)):
            for j in range(len(mygb[i])):
                key = (math.ceil(i/self.gameboard.p), math.ceil(j/self.gameboard.p))
                dd[key].append(mygb[i][j])
        return dd
            
    def is_all_int(self,mygb):
        l = []
        for i in mygb:
            for j in i:
                l.append(type(j) ==int)
        return all(l) #True if all int type

    """
        Part 2 TODO: Implement both of Norvig's Heuristics

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        (2) If a constraint has only one possible place for a value
            then put the value there.

        Note: remember to trail.push variables before you change their domain
        Return: true is assignment is consistent, false otherwise
    """

    def eliminate(self, cell, d):
        if d in cell.getDomain:
            return cell
        cell.removeValueFromDomain(d)
        if len(cell.getDomain) == 0:
            return False
        elif len(cell.getDomain) == 1:
            d2 = cell.getDomain  
            if not all(self.eliminate(cell2, d2) for cell2 in self.network.getNeighborsOfVariable(cell2) ):
                return False
            
        for 


            
    def norvigCheck ( self ):
        
        return False

    """
         Optional TODO: Implement your own advanced Constraint Propagation

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournCC ( self ):
        return None

    # ==================================================================
    # Variable Selectors
    # ==================================================================

    # Basic variable selector, returns first unassigned variable
    def getfirstUnassignedVariable ( self ):
        for v in self.network.variables:
            if not v.isAssigned():
                return v

        # Everything is assigned
        return None

    """
        Part 1 TODO: Implement the Minimum Remaining Value Heuristic

        Return: The unassigned variable with the smallest domain
    """
    def getMRV ( self ):
        domains = []
        for i in self.network.variables:
            if not i.isAssigned():
                domains.append((i,len(i.getValues())))
        if len(domains) == 0:
            return None
        return sorted(domains,key=itemgetter(1))[0][0]
        #return Minv

    """
        Part 2 TODO: Implement the Minimum Remaining Value Heuristic
                       with Degree Heuristic as a Tie Breaker

        Return: The unassigned variable with, first, the smallest domain
                and, second, the most unassigned neighbors
    """
    def MRVwithTieBreaker ( self ):
        minvs = []
        minv = self.getMRV()
        if minv == None:
            return None
        for i in self.network.variables:
            if len(i.getValues()) == len(minv.getValues()):
                minvs.append(i)

        temp = []
        for i in minvs:
            neighbors = []
            for j in self.network.variables:
                if not j.isAssigned():
                    if i.col == j.col or i.row == j.row or i.block == j.block:
                        if not (i.col == j.col and i.row == j.row):
                            neighbors.append(j)
            temp.append((i,len(neighbors)))
        
        #print("before return")
        return sorted(temp,key=-itemgetter(1))[0][0]#Maxdegree

    """
         Optional TODO: Implement your own advanced Variable Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVar ( self ):
        return None

    # ==================================================================
    # Value Selectors
    # ==================================================================

    # Default Value Ordering
    def getValuesInOrder ( self, v ):
        values = v.domain.values
        return sorted( values )

    """
        Part 1 TODO: Implement the Least Constraining Value Heuristic

        The Least constraining value is the one that will knock the least
        values out of it's neighbors domain.

        Return: A list of v's domain sorted by the LCV heuristic
                The LCV is first and the MCV is last
    """
    def getValuesLCVOrder ( self, v ):
        #self.forwardChecking()
        neighbors = []
        originDomain = v.getDomain()
        for i in self.network.variables:
            if i.row == v.row or i.col == v.col or i.block == v.block:
                if not i.isAssigned():
                    neighbors.append(i)
                    
        knockouts = []
        for i in v.getValues():
            knockout = []
            for j in neighbors:
                if i in j.getValues():
                    if len(j.getValues()) == 1:
                        print("Error: thought cell wasn't assigned but it was")
                    knockout.append(j)
            knockouts.append((i,len(knockout)))
        
        #print("row: " + str(v.row) + ", col: " + str(v.col))
        #print(sorted(knockouts,key=itemgetter(1)))

        result = []
        for i in sorted(knockouts,key=itemgetter(1)):
            result.append(i[0])
        return result

    """
         Optional TODO: Implement your own advanced Value Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVal ( self, v ):
        return None

    # ==================================================================
    # Engine Functions
    # ==================================================================

    def solve ( self ):
        if self.hassolution:
            return

        # Variable Selection
        v = self.selectNextVariable()

        # check if the assigment is complete
        if ( v == None ):
            for var in self.network.variables:

                # If all variables haven't been assigned
                if not var.isAssigned():
                    print ( "Error" )

            # Success
            self.hassolution = True
            return

        # Attempt to assign a value
        for i in self.getNextValues( v ):

            # Store place in trail and push variable's state on trail
            self.trail.placeTrailMarker()
            self.trail.push( v )

            # Assign the value
            v.assignValue( i )

            # Propagate constraints, check consistency, recurse
            if self.checkConsistency():
                self.solve()

            # If this assignment succeeded, return
            if self.hassolution:
                return

            # Otherwise backtrack
            self.trail.undo()

    def checkConsistency ( self ):
        if self.cChecks == "forwardChecking":
            return self.forwardChecking()

        if self.cChecks == "norvigCheck":
            return self.norvigCheck()

        if self.cChecks == "tournCC":
            return self.getTournCC()

        else:
            return self.assignmentsCheck()

    def selectNextVariable ( self ):
        if self.varHeuristics == "MinimumRemainingValue":
            return self.getMRV()

        if self.varHeuristics == "MRVwithTieBreaker":
            return self.MRVwithTieBreaker()

        if self.varHeuristics == "tournVar":
            return self.getTournVar()

        else:
            return self.getfirstUnassignedVariable()

    def getNextValues ( self, v ):
        if self.valHeuristics == "LeastConstrainingValue":
            return self.getValuesLCVOrder( v )

        if self.valHeuristics == "tournVal":
            return self.getTournVal( v )

        else:
            return self.getValuesInOrder( v )

    def getSolution ( self ):
        return self.network.toSudokuBoard(self.gameboard.p, self.gameboard.q)
