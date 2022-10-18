#What is linked list in python:
# https://www.youtube.com/watch?v=Ast5sKQXxEU
# https://leetcode.com/problems/add-two-numbers/
class ListNode(object):

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next



class Solution:
    def addTwoNumbers(self,l1,l2):

        l1 = l1.reversed()
        l2 = l2.reversed()
        
        s1 = ''
        s2 = ''

        while l1 != None:
            s1 += str(l1.val)
            l1 = l1.next 
        while l2 !=None:
            s2 += str(l2.val)
            l2 = l2.next 

        sum1 = int(s1) + int(s2)
        sum1 = str(sum1)
        head = ListNode(int(sum1[0]))
        for i in sum1[1:]:
            node = ListNode(int(i))
            node.next = head
            head = node
        return head



