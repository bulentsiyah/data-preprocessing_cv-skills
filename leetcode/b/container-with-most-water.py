'''
You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).
Find two lines that together with the x-axis form a container, such that the container contains the most water.
Return the maximum amount of water a container can store.
Notice that you may not slant the container.


Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.

ilk sutundan başlayarak, seçili sutun ile son sütun arasında minumum olanla bu iki sütun arasındaki mesafeyi çarpıp en büyük alanı bulmak
'''

from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        maxarea = 0
        l = 0 # baştan başladık ama sağa doğru kayacağız
        r = len(height)-1 # en sağdaki sütun

        while(l<r):
            maxarea = max(maxarea, min(height[l],height[r])*(r-l))
            if(height[l]<height[r]):
                l+=1
            else:
                r-=1
        return maxarea





if __name__ == '__main__':
    solution = Solution()
    height = [1,8,6,2,5,4,8,3,7]
    print(solution.maxArea(height))