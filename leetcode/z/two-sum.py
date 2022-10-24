class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        x = len(nums)
        for i in range(0,x+1):
            n1 = nums[i]            
            for k in range(i,x-1):
                
                n2= nums[k+1]
                
                if n1 + n2 == target:
                    return i,k+1
                 
                
                