# Examples
#
#  Input: prices = [10,15,20,5]
#  Output: 20 (optimal route = [1]->[3] -> Finish)
#
#  Input: prices = [5,20,3,2,20,1,1,20]
#  Output: 12 (optimal route = [0]->[2]->[3]->[5]->[6] -> Finish)
#

#prices = [5,20,3,2,20,1,1,20]


prices = [10,15,20,5]

def lowestSum (prices):
    try:
        cantStation = len(prices)
        if cantStation > 0:             
            for i in range(cantStation):
                fuel = prices[i]
                
                for j in range(cantStation):
                    currStation = (i + j) % cantStation
                    print('currStation:', currStation)
                    nextStation = (currStation + 1) % cantStation
                    print('nextStation:', nextStation)
                    
                
        
        
        
        
        '''
        for i in range(len(prices)):
            fuel = prices[i]
            isAmple = True
            for j in range(len(prices)):
                currStation = (i + j) % n
                nextStation = (currStation + 1) % n
                fuel = fuel - prices[currStation]
                if fuel < 0:
                    isAmple = True
                    break
            
            if (isAmple): 
                print(i)'''
        
	    #return lowest sum
        return sum;
    except Exception as e: 
        return e

lowestSum(prices)