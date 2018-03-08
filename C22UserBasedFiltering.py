# -*- coding: utf-8 -*-

"""

Assignment 3

"""



import math

from operator import itemgetter

#################################################

# recommender class does user-based filtering and recommends items 

class UserBasedFilteringRecommender:

        # class variables:    
        # none


    ##################################

    # class instantiation method - initializes instance variables
    # usersItemRatings:
    # users item ratings data is in the form of a nested dictionary:
    # at the top level, we have User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values

    # Example: 
    #     {"Angelica":{"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #     "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}}
    #

    # k:
    # the number of nearest neighbors
    # defaults to 1
    
    # m:
    # the number of recommedations to return
    # defaults to 10


    def __init__(self, usersItemRatings, metric='pearson', k=1, m=10):
        
        # set self.usersItemRatings
        
        self.usersItemRatings = usersItemRatings
        
        # set self.k

        if k > 0:   
            self.k = k
        else:
            print ("    (FYI - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1

         

        # set self.m

        if m > 0:   
            self.m = m
        else:
            print ("    (FYI - invalid value of m (must be > 0) - defaulting to 10)")
            self.m = 10

            
    #################################################

    # pearson correlation similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}

    def pearsonFn(self, userXItemRatings, userYItemRatings):

        
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0

        n = len(userXItemRatings.keys() & userYItemRatings.keys())

        for item in userXItemRatings.keys() & userYItemRatings.keys():
            x = userXItemRatings[item]
            y = userYItemRatings[item]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)

      
        if n == 0:
            print ("    (FYI - personFn n==0; returning -2)")
            return -2

        
        denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(sum_y2 - pow(sum_y, 2) / n)

        if denominator == 0:
            print ("    (FYI - personFn denominator==0; returning -2)")
            return -2
        else:
            return round((sum_xy - (sum_x * sum_y) / n) / denominator, 2)

            



    #################################################

    # make recommendations for userX from the most similar k nearest neigibors (NNs)

    def recommendKNN(self, userX):

        userDist = []
        userSortedDist = []
        ratings = {}
        userXRatings = self.usersItemRatings[userX]

#get the pearson correlation
        
        for u in self.usersItemRatings.keys():

            if userX not in u:
                temp1 = (self.pearsonFn(self.usersItemRatings[userX],self.usersItemRatings[u])+1)/2
                userDist.append((u, temp1))

#sort the users sorted by the correlation - highest to lowest
                
        userSortedDist = sorted(userDist, key=itemgetter(1), reverse = True)

#get the k nearest neighbors
        
        sumdists = 0
        
        for i in range(0,self.k):
            sumdists += userSortedDist[i][1]

#get the weighted influence
        
        for j in range(0,self.k):
            weight = userSortedDist[j][1]/sumdists
            user = userSortedDist[j][0]
            userXNN = self.usersItemRatings[user]

#get the final recommendation sorted by order of ratings
            
            for s in userXNN.keys():
                if s not in userXRatings.keys():
                    if s not in ratings.keys():
                        ratings[s] = round (userXNN[s] * weight, 2)
                    else:
                        ratings[s] = round (ratings[s] + (userXNN[s] * weight), 2)

        userXSortedFinal = []
        userXSortedFinal = sorted(ratings.items(), key=itemgetter(1), reverse=True)

        return userXSortedFinal[:self.m]

        

      







        

