'''
Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements. 
(Bir tamsayı dizi numarası verildiğinde, sıfır olmayan öğelerin göreli sırasını korurken tüm 0'ları sonuna taşıyın.)

Note that you must do this in-place without making a copy of the array.


Example 1:

Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0]
Example 2:

Input: nums = [0]
Output: [0]


'''
from typing import List

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        j = 0
        for num in nums:
            if(num != 0): # eğer 0 değilse en kötü kendi indexine yazılacak, veya bir geriye yazılmış olacak
                nums[j] = num
                j += 1

        for x in range(j, len(nums)):
            nums[x] = 0

        return nums # cevabı gönderirken return yollama!!!!!!



if __name__ == '__main__':
    solution = Solution()
    nums = [0,1,0,3,12]
    print(solution.moveZeroes(nums))