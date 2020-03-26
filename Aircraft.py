class Aircraft:
    '''Class modeling the Aircraft'''
    def __init__(self, dest, startTime, start = [0, 0]):
        # To store the source location
        self.start = start
        # To store the destination location
        self.dest = dest
        self.allHeading = ['N', 'W', 'S', 'E']
        # TO store the current direction of motion/ heading
        self.currentHeading = self.allHeading[0]
        # To store the flight time
        self.flightTime = 0
        self.startTime = startTime
        # To store the current location of the aircraft. Initially set to the source location
        self.currentLocation = start

    def isDestination(self):
        '''To check whether the flight has reached its destination. Returns True if the aircraft has reached its
        destination, else False'''
        reached = False
        if self.currentLocation[0] == self.dest[0] and self.currentLocation[1] == self.dest[1]:
            reached = True
        return reached

    def perfromAction(self, action):
        '''Update the current position and the heading of the aircraft based on the action issued by the controller'''
        self.flightTime += 1
        if self.currentHeading == 'N':
            if action == 'Forward':
                self.currentLocation[1] += 1
            elif action == 'Turn_Right':
                self.currentHeading = 'E'
            elif action == 'Turn_Left':
                self.currentHeading = 'W'
        elif self.currentHeading == 'W':
            if action == 'Forward':
                self.currentLocation[0] -= 1
            elif action == 'Turn_Right':
                self.currentHeading = 'N'
            elif action == 'Turn_Left':
                self.currentHeading = 'S'
        elif self.currentHeading == 'S':
            if action == 'Forward':
                self.currentLocation[1] -= 1
            elif action == 'Turn_Right':
                self.currentHeading = 'W'
            elif action == 'Turn_Left':
                self.currentHeading = 'E'
        elif self.currentHeading == 'E':
            if action == 'Forward':
                self.currentLocation[0] += 1
            elif action == 'Turn_Right':
                self.currentHeading = 'S'
            elif action == 'Turn_Left':
                self.currentHeading = 'N'

    def Message(self):
        """Generates the message to be sent to the controller"""
        message = []
        message.append(self.currentLocation)
        message.append(self.currentHeading)
        message.append(self.flightTime)
        remDist = abs(abs(self.currentLocation[0] - self.dest[0]) + abs(self.currentLocation[1] - self.dest[1]))
        message.append(remDist)
        message.append(self.dest)
        return message


# A1 = Aircraft([1,2], 0, [0, 0])
# print(A1.Message())
# if None:
#     print(True)
# else:
#     print(False)