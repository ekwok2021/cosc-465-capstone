import random
class subnets:

    def genSubnet(): #returns array 
        subnet = random.sample(range(0,255), 4)
        subnet.append(random.randint(1,32))
        print(subnet)
        return subnet

    def addressRanges(subnet): #returns an array of 2 arrays with the range
        mask = subnet[4]

        dividend = mask // 8  
        remainder = mask % 8
        

        answer1 = subnet[0:dividend]
        #print(answer1)

        int1 = subnet[dividend]
        #print(int1)

        bin1 = '{0:0{1}b}'.format(int1, 8)
        #print(bin1)
        #print(len(bin1))

        bin2 = bin1[0:remainder]
        #print(bin2)
        bin2 = bin2 + ('0' * (8-remainder))
        #print(bin2)

        int2 = int(bin2, 2)
        #print(int2)

        answer1.append(int2)
        while(len(answer1) < 4):
            answer1.append(0)

        #print(answer1)
        
        answer2 = answer1[0:dividend]
        #print(answer2)
        answer2bin = '{0:0{1}b}'.format(int1, 8)
        #print(answer2bin)

        bin3 = bin1[0:remainder]
        #print(bin3)
        bin3 = bin3 + ('1' * (8-remainder))
        #print(bin3)

        int3 = int(bin3, 2)
        #print(int3)
        answer2.append(int3)
        while(len(answer2) < 4):
            answer2.append(255)

        print(answer1)
        print(answer2)

        answer = [answer1, answer2]
        return answer

    def compare(useranswer, correctanswer):
        if ".".join(useranswer) == ".".join(correctanswer):
            return true
        return false

    def subnetMembership():
        return

def main():
    #print("DEBUG")
    print(subnets.addressRanges(subnets.genSubnet()))
    return
    
if __name__ == "__main__":
    main()
