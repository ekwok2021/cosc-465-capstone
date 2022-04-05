import random
class subnets:
    def addressRanges():
        subnet = random.sample(range(0,255), 4)
        subnet.append(random.randint(1,32))
        print(subnet)

        mask = subnet[4]

        dividend = mask // 8  
        remainder = mask % 8
        #print(dividend)
        #print(remainder)

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

        answer2 = 

        print(answer1)
        
        



        




        #answer1 = 
        #print(answer1)
        
        return

    def subnetMembership():
        return

def main():
    print("DEBUG")
    subnets.addressRanges()
    return
    
if __name__ == "__main__":
    main()
