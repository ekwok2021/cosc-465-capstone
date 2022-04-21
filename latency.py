import random
class latency:

    def genB():
        rand = random.randint(1,10)
        rand = rand*1000
        B = rand
        print("B = " + str(B))
        return B
    
    def distance():
        rand = random.randint(1,20)
        rand = rand
        distance = rand
        print("distance = " + str(distance))
        return distance

    def bandwidth():
        rand = random.randint(5,15)
        bandwidth = rand
        print("bandwidth = " + str(bandwidth))
        return bandwidth

    def calcPropDelay(distance):
        propDelay = distance/200000000
        propDelay = propDelay * 1000
        propDelay = propDelay * 1000
        propDelay = round(propDelay, 4)
        print("Propogration delay = " + str(propDelay))
        return propDelay

    def calcTransDelay(B, bandwidth):
        transDelay = (B * 8)/(bandwidth*1000000000)
        transDelay = transDelay * 1000
        transDelay = round(transDelay, 4)
        print("Transmission delay = " + str(transDelay))
        return transDelay

    def calcLat(propDelay, transDelay):
        lat = propDelay + transDelay
        lat = round(lat, 4)
        print("Latency = " + str(lat))
        return lat
    
    def generateProblem():
        B = latency.genB()
        distance = latency.distance()
        bandwidth = latency.bandwidth()
        propDelay = latency.calcPropDelay(distance)
        transDelay = latency.calcTransDelay(B, bandwidth)
        lat = latency.calcLat(propDelay, transDelay)
        inputProp = float(input())
        if inputProp == propDelay:
            print("GOOD PROP")
        else:
            print("BAD PROP")

        inputTrans = float(input())
        if inputTrans == transDelay:
            print("GOOD TRANS")
        else:
            print("BAD TRANS")

        inputLat = float(input())
        if inputLat == lat:
            print("GOOD LAT")
        else: 
            print("BAD LAT")
        return


def main():
    print("DEBUG")
    latency.generateProblem()

    return
    
if __name__ == "__main__":
    main()