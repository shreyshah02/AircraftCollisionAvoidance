from Aircraft import Aircraft
from AircraftContoller import AircraftController

# uncomment this part if you want to test other cases


# print('Enter Information for Aircraft 1:')
# d0 = int(input('Enter x coordinate for destination: '))
# d1 = int(input('Enter y coordinate for the destination: '))
# s0 = int(input('Enter x coordinate for the source: '))
# s1 = int(input('Enter y coordinate for the source: '))
# source_1 = [s0, s1]
# dest_1 = [d0, d1]
#
# d0_2 = int(input('Enter x coordinate for destination: '))
# d1_2 = int(input('Enter y coordinate for the destination: '))
# s0_2 = int(input('Enter x coordinate for the source: '))
# s1_2 = int(input('Enter y coordinate for the source: '))
# source_2 = [s0_2, s1_2]
# dest_2 = [d0_2, d1_2]
#
# A1 = Aircraft(dest_1, 0, source_1)
# A2 = Aircraft(dest_2, 0, source_2)

# Creating the instance of Aircrafts
A1 = Aircraft([1, 8], 0, [1, 2])
A2 = Aircraft([1, 2], 0, [1, 7])
# A1 = Aircraft([1, 5], 0, [1, 1])
# A2 = Aircraft([1, 5], 0, [1, 7])

# A1 = Aircraft([2,7], 0, [5, 4])
# A2 = Aircraft([5,6], 0, [8, 9])

#Creating the instance of controller
C1 = AircraftController()
C2 = AircraftController()

t1 = A1.isDestination()
t2 = A2.isDestination()
m1 = A1.Message()
m2 = A2.Message()
time1 = 0
time2 = 0

prev1 = []
prev2 = []

i = 1

# While at least one aircraft has not reached its destination
while(not t1 or not t2):

    curLoc1 = m1[0]
    curLoc2 = m2[0]
    prev1 = curLoc1
    prev2 = curLoc2
    # Checking if the two aircrafts are in the communication zone or not
    if abs(curLoc1[0] - curLoc2[0])>2 or abs(curLoc1[1] - curLoc2[1])>2:
        # Checking if A1 has reached the destination or not
        if not t1:
            # Getting action for A1 if it has not reached its destination
            action1, t = C1.generateAction(aircraft1 = m1, g = 1)
        if not t2:
            # Getting action for A2 if it has not reached its destination
            action2, t = C2.generateAction(aircraft1= m2, g = 2)
    else:
        # If the 2 aircrafts are in the communication zone
        if t2:
            # If A2 has reached its destination, it will not send any messages and thus action for A1 is independent of A2
            action1, t = C1.generateAction(aircraft1 = m1, g = 1)
        else:
            # Else A2 will also send its message to controller of A1
            action1, time1 = C1.generateAction(aircraft1=m1, aircraft2=m2, g = 1, t = time1)
        if t1:
            # If A1 has reached its destination, it will not send any messages and thus action for A2 is independent of A1
            action2, t = C2.generateAction(aircraft1=m2, g = 2)
        else:
            # Else A1 will also send its message to controller of A2
            action2, time2 = C2.generateAction(aircraft1=m2, aircraft2=m1, g = 2, t = time2)
    if not t1:
        # If A1 has not reached, perform action
        A1.perfromAction(action1)
    if not t2:
        # If A2 has not reached, perform action
        A2.perfromAction(action2)
    # Get the updated status of both flights
    t1 = A1.isDestination()
    t2 = A2.isDestination()
    m1 = A1.Message()
    m2 = A2.Message()

    print('\nTime ', i, 'minutes since start')

    if t1:
        print("Status of A1: Reached")
    else:
        print("Status of A1: ", m1)
        print('Current location: ', m1[0],'\n Current Heading: ', m1[1])
    if t2:
        print("Status of A2: Reached")
    else:
        print('\nStatus of A2: ', m2)
        print('Current location: ', m2[0], '\n Current Heading: ', m2[1])

    # Safety Monitor for the process
    if (m1[0] == m2[0] and not t1 and not t2) or (m1[0] == prev2 and m2[0] == prev1):
        # Checks if the Aircrafts are occupying the same location and both have not reached the destination
        # Or if they occupy each others previous locations in which case they would have had to pass thorugh each other
        # If any of these conditions is satisfied, a collision is encounters
        # And the monitor stops the system
        print('Error, Collision')
        break
    i +=1


