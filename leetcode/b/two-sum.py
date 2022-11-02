'''
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
Bir tamsayı dizisi ve bir tamsayı hedefi verildiğinde, iki sayının endekslerini, hedefe eklenecek şekilde döndürün.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]

'''

from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        d = {}
        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in d:
                return [d[complement],i]
            d[nums[i]]=i


if __name__ == '__main__':
    solution = Solution()
    print(solution.twoSum([2,7,11,18,15],18))