'''
You are given an array people where people[i] is the weight of the ith person, and an infinite number of boats where each boat can carry a maximum weight of limit. 
Each boat carries at most two people at the same time, provided the sum of the weight of those people is at most limit.

(Her tekne aynı anda en fazla iki kişiyi taşır, bu kişilerin ağırlıkları toplamının en fazla limit olmak şartı var.)

Return the minimum number of boats to carry every given person.

 

Example 1:

Input: people = [1,2], limit = 3
Output: 1
Explanation: 1 boat (1, 2)
Example 2:

Input: people = [3,2,2,1], limit = 3
Output: 3
Explanation: 3 boats (1, 2), (2) and (3)
Example 3:

Input: people = [3,5,3,4], limit = 5
Output: 4
Explanation: 4 boats (3), (3), (4), (5)


'''
from typing import List

class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:

        people.sort() # kilolara göre en küçükleri başa alarak sırala

        left = 0
        right = len(people)-1  #ındex tutuyor

        boats_number = 0

        while(left<=right):  # sona gelene kadar
            if(left==right):
                boats_number+=1 # sona geldık tek basına bınecek
                break
            if(people[left]+people[right]<=limit): # en yakın 2 sı lımıt altındaysa ındex kayar sankı ılk kısı yok gıbı
                left+=1

            right-=1 # ındex bır yaklastırdı
            boats_number+=1
        return boats_number


if __name__ == '__main__':
    solution = Solution()
    people = [3,5,3,4]
    limit = 5
    print(solution.numRescueBoats(people,limit))