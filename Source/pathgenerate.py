path = [(6, 0), (5, 0), (4, 0), (3, 0), (3, 1), (3, 2), (2, 2), (2, 3), (2, 4), (2, 5)]



def generateO(path):
    orientation = []
    orientation.append("LEFT")
    for idx in range(len(path)):
        if idx == len(path) -1:
            break
        if path[idx][1] == path[idx+1][1]:
            orientation.append(orientation[0])    
    print(orientation)


def generateP(path):
    motorcommands = []
    for idx in range(len(path)):
        if idx == len(path)-1:
            break
        if path[idx][0] > path[idx+1][0]:
            motorcommands.append("B")
        if path[idx][0] < path[idx+1][0]:
            motorcommands.append("F")
        if path[idx][1] > path[idx+1][1]:
            motorcommands.append("L")
            motorcommands.append("F")           
        if path[idx][1] < path[idx+1][1]:
            motorcommands.append("R")
            motorcommands.append("F")

    print(motorcommands)

generateP(path)
generateO(path)
