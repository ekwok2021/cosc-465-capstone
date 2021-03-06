import random
class subnets:

    def genSubnet(): #returns array 
        subnet = random.sample(range(0,255), 4)
        subnet.append(random.choice([1,7,8,9,15,16,17,23,24,25,30,31]))
        print(subnet)
        return subnet

    def addressRanges(subnet): #returns an array of 2 arrays with the range
        mask = subnet[4]

        dividend = mask // 8  
        remainder = mask % 8
        

        answer1 = subnet[0:dividend]

        int1 = subnet[dividend]

        bin1 = '{0:0{1}b}'.format(int1, 8)
        bin2 = bin1[0:remainder]
        bin2 = bin2 + ('0' * (8-remainder))

        int2 = int(bin2, 2)

        answer1.append(int2)
        while(len(answer1) < 4):
            answer1.append(0)
        
        answer2 = answer1[0:dividend]
        answer2bin = '{0:0{1}b}'.format(int1, 8)

        bin3 = bin1[0:remainder]
        bin3 = bin3 + ('1' * (8-remainder))

        int3 = int(bin3, 2)
        answer2.append(int3)
        while(len(answer2) < 4):
            answer2.append(255)

        answer = [answer1, answer2]
        return answer

    def compare(input_start, input_end, subnet_str):
        l = subnet_str.split(".")
        last_two = l[-1].split("/")
        l = l[:-1]
        subnet = []
        for s in l:
            subnet.append(int(s))
        subnet.append(int(last_two[0]))
        subnet.append(int(last_two[1]))
        correct_range = subnets.addressRanges(subnet)
        start = correct_range[0]
        end = correct_range[1]
        start_mask = str(start[-1])
        end_mask = str(end[-1])
        start = start[:-1]
        end = end[:-1]
        start_str = ".".join(map(str, start)) + "." + start_mask
        end_str = ".".join(map(str, end)) + "." + end_mask
        print("user_t1 " + input_start)
        print("user_t2 " + input_end)
        print("start " + start_str)
        print("end " + end_str)
        if (start_str == input_start) and (end_str == input_end):
            return True
        return False

    def subnetMembership(IPaddress, addressRanges):
        

        return

def main():
    #print("DEBUG")
    print(subnets.addressRanges(subnets.genSubnet()))
    return
    
if __name__ == "__main__":
    main()