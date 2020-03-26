class AircraftController:
    """This class models the aircraft controller"""
    def __init__(self, aircraft1 = None, aircraft2 = None):
        pass

    def newPose(self, curloc_1, curHeading_1, action):
        """Method to get the new location of the aircraft based on the action and the current location and heading"""
        newLoc = [0, 0]
        if action == 'Forward':
        # If action is forward, then the new coordinates are obtained by updating the current coordinates in the
        # direction of heading
            if curHeading_1 == 'N':
                newLoc[1] = 1 + curloc_1[1]
                newLoc[0] = curloc_1[0]
                newHeading = 'N'
            elif curHeading_1 == 'S':
                newLoc[1] = curloc_1[1] - 1
                newLoc[0] = curloc_1[0]
                newHeading = 'S'
            elif curHeading_1 == 'E':
                newLoc[0] = curloc_1[0] + 1
                newLoc[1] = curloc_1[1]
                newHeading = 'E'
            else:
                newLoc[0] = curloc_1[0] - 1
                newHeading = 'W'
                newLoc[1] = curloc_1[1]
        else:
            # If the action is turn, then coordinates remain unchanged, only the heading is updated
            newLoc = [curloc_1[0], curloc_1[1]]
            if curHeading_1 == 'N' and action == 'Turn_Right':
                newHeading = 'E'
            else:
                newHeading = 'W'
            if curHeading_1 == 'W' and action == 'Turn_Right':
                newHeading = 'N'
            else:
                newHeading = 'S'
            if curHeading_1 == 'S' and action == 'Turn_Right':
                newHeading = 'W'
            else:
                newHeading = 'E'
            if curHeading_1 == 'E' and action == 'Turn_Right':
                newHeading = 'S'
            else:
                newHeading = 'N'
        return [newLoc, newHeading]

    def noInterferanceAction(self, curLoc_1, curHeading_1, dest_1):
        """This method generates the action to be performed by the aircraft if no other aircraft is in its vicinity"""
        if curHeading_1 == 'N':
            if curLoc_1[1] < dest_1[1]:
                u = 'Forward'
            else:
                if curLoc_1[0] < dest_1[0]:
                    u = 'Turn_Right'
                else:
                    u = 'Turn_Left'

        elif curHeading_1 == 'S':
            if curLoc_1[1] > dest_1[1]:
                u = 'Forward'
            else:
                if curLoc_1[0] > dest_1[0]:
                    u = 'Turn_Right'
                else:
                    u = 'Turn_Left'

        elif curHeading_1 == 'E' :
            if curLoc_1[0] < dest_1[0]:
                u = 'Forward'
            else:
                if curLoc_1[1] > dest_1[1]:
                    u = 'Turn_Right'
                else:
                    u = 'Turn_Left'

        elif curHeading_1 == 'W':
            if curLoc_1[0] > dest_1[0]:
                u = 'Forward'
            else:
                if curLoc_1[1] < dest_1[1]:
                    u = 'Turn_Right'
                else:
                    u = 'Turn_Left'
        return u

    def getTurnDirection(self, curLoc_1, curHeading_1, dest_1):
        """This method returns the optimal directio to turn in , either left or right,based on the current location and heading and the
        destination"""
        if curHeading_1 == 'N':
            if curLoc_1[0] < dest_1[0]:
                u = 'Turn_Right'
            else:
                u = 'Turn_Left'
        if curHeading_1 == 'S':
            if curLoc_1[0] > dest_1[0]:
                u = 'Turn_Right'
            else:
                u = 'Turn_Left'
        if curHeading_1 == 'E':
            if curLoc_1[1] > dest_1[1]:
                u = 'Turn_Right'
            else:
                u = 'Turn_Left'
        else:
            if curLoc_1[1] < dest_1[1]:
                u = 'Turn_Right'
            else:
                u = 'Turn_Left'
        return u

    def generateAction(self, g, aircraft1 = None, aircraft2 = None, t = 0):
        """The main method which generates the action to be performed by the aircraft
        g captures the priority. If the value of g is 1 then priority is with aircraft 1 else with aircraft 2
        t captures the consecutive time steps where priority has overridden the optimal action for aircraft 1"""
        # Message from the aircraft
        curLoc_1 = aircraft1[0]
        curHeading_1 = aircraft1[1]
        time_1 = aircraft1[2]
        remDist_1 = aircraft1[3]
        dest_1 = aircraft1[4]
        u = 'Forward'

        # Checking if the message from aircraft 2 is available or not
        if aircraft2:
            # If available, that is aircraft 2 is in the communication zone, then the action generated must take the 2nd
            # aircraft into account

            # Message from 2nd aircraft
            curLoc_2 = aircraft2[0]
            curHeading_2 = aircraft2[1]
            time_2 = aircraft2[2]
            remDist_2 = aircraft2[3]
            dest_2 = aircraft2[4]

            # generating the optimal action if no other aircraft was present
            act = self.noInterferanceAction(curLoc_1, curHeading_1, dest_1)

            # Generate new coordinates for aircraft 1 based on the optimal action and for aircraft 2 based on the
            # Forward action
            newLoc_1, newH_1 = self.newPose(curLoc_1, curHeading_1, act)
            newLoc_2, newH_2 = self.newPose(curLoc_2, curHeading_2, 'Forward')

            # Checking the occurrence of collision of the new position of air craft1 with both the new and the current
            # position of Aircraft 2. As controller doesn't know what action aircraft 2 would take. But aircraft 2 could
            # Only be at either its new position or its current position in the next time step
            if abs(newLoc_1[0] - newLoc_2[0])>=1 or abs(newLoc_1[1] - newLoc_2[1])>=1:
                if abs(newLoc_1[0] - curLoc_2[0])>=1 or abs(newLoc_1[1] - curLoc_2[1])>=1:
                    # Checking 2 steps ahead from the current location to prevent deadlock
                    nextAct = self.noInterferanceAction(newLoc_1, newH_1, dest_1)
                    nLoc2_1, nH2_1 = self.newPose(newLoc_1, newH_1, nextAct)
                    if nLoc2_1[0] != curLoc_2[0] or nLoc2_1[1] != curLoc_2[1]: # previously
                        # if g == 1 or t>1:
                        #     t = 0
                        #     return act, t
                        # else:
                        #     t+=1
                        #     if act == 'Forward':
                        #         u = self.getTurnDirection(curLoc_1, curHeading_1, dest_1)
                        #         return u, t
                        #     else:
                        #         u = 'Forward'
                        #         return u, t
                        u = act
                        return u, t
                    else:
                        # If aircraft 1 has priority or t>1 return optimal action
                        if g == 1 or t>1:
                            t = 0
                            return act, t
                        else:
                            # Else return the complementary of the optimal action, that is turn if optimal action was
                            # forward and forward if optimal action was turn
                            if act == 'Forward':
                                u = self.getTurnDirection(curLoc_1, curHeading_1, dest_1)
                                return u, t+1
                            else:
                                u = 'Forward'
                                return u, t+1
                else:
                    if act == 'Forward':
                        u = self.getTurnDirection(curLoc_1, curHeading_1, dest_1)
                    else:
                        u = 'Forward'
                    return u, t

            elif newLoc_1[0] == curLoc_1[0] and newLoc_1[1] == curLoc_1[1]:
                # If the optimal action as turn, check if forward motion prevents collision
                nxy_1, nH_1 = self.newPose(curLoc_1, curHeading_1, 'Forward')
                if abs(nxy_1[0] - newLoc_2[0])>=1 or abs(nxy_1[1] - newLoc_2[1])>=1:
                    return 'Forward', t

            else:
                if abs(newLoc_1[0] - curLoc_2[0])>=1 or abs(newLoc_1[1] - curLoc_2[1])>=1:
                    if g == 1:
                        return act, t
                    else:
                        u = self.getTurnDirection(curLoc_1, curHeading_1, dest_1)
                        return u, t
                else:
                    u = self.getTurnDirection(curLoc_1, curHeading_1, dest_1)
                    return u, t

        else:
            # If no other aircraft is in the vicinity, return optimal action
            u = self.noInterferanceAction(curLoc_1, curHeading_1, dest_1)

        return u, t

