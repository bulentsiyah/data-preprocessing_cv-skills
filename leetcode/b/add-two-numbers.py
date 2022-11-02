'''
Kaynak: http://cagataykiziltan.net/veri-yapilari-data-structures/1-linked-list-bagli-listeler/#:~:text=Linked%20list%2C%20yaz%C4%B1l%C4%B1m%20d%C3%BCnyas%C4%B1nda%20%C3%B6nemli,sonraki%20node'un%20yerini%20bilir.

You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. 
Add the two numbers and return the sum as a linked list.
You may assume the two numbers do not contain any leading zero, except the number 0 itself.


Example 1:
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.

Example 2:
Input: l1 = [0], l2 = [0]
Output: [0]


Example 3:
Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]


'''

class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution(object):

    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode(0)
        current, carry = dummy, 0

        while l1 or l2: # l1 is not None or l2 is not None:
            val = carry
            if l1:
                val += l1.val # önce 2 gitti 
                l1 = l1.next # şimdi 4 head oldu
            if l2:
                val += l2.val # önce 5 
                l2 = l2.next # sonra 6
            carry, val = divmod(val, 10) #divmod başka yerde de isime yarar
            current.next = ListNode(val)
            current = current.next

        if carry == 1:
            current.next = ListNode(1)

        return dummy.next


    def addTwoNumbers2(self, l1: ListNode, l2: ListNode) -> ListNode:
        # Head of the new linked list - this is the head of the resultant list
        head = None
        # Reference of head which is null at this point
        temp = None
        # Carry
        carry = 0
        # Loop for the two lists
        while l1 is not None or l2 is not None:
            # At the start of each iteration, we should add carry from the last iteration
            sum_value = carry
            # Since the lengths of the lists may be unequal, we are checking if the
            # current node is null for one of the lists
            if l1 is not None:
                sum_value += l1.val
                l1 = l1.next
            if l2 is not None:
                sum_value += l2.val
                l2 = l2.next
            # At this point, we will add the total sum_value % 10 to the new node
            # in the resultant list
            node = ListNode(sum_value % 10)
            # Carry to be added in the next iteration
            carry = sum_value // 10
            # If this is the first node or head
            if temp is None:
                temp = head = node
            # for any other node
            else:
                temp.next = node
                temp = temp.next
        # After the last iteration, we will check if there is carry left
        # If it's left then we will create a new node and add it
        if carry > 0:
            temp.next = ListNode(carry)
        return head


if __name__ == '__main__':
    solution = Solution()

    head1 = ListNode(2)
    head1.next = ListNode(4)
    head1.next.next = ListNode(3)

    head2 = ListNode(5)
    head2.next = ListNode(6)
    head2.next.next = ListNode(4)

    result = solution.addTwoNumbers(head1, head2)

    while result:
        print(str(result.val))
        result = result.next