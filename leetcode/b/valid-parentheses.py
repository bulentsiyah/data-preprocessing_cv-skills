'''
Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
An input string is valid if:
Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Every close bracket has a corresponding open bracket of the same type.

Example 1:
Input: s = "()"
Output: true

Example 2:
Input: s = "()[]{}"
Output: true

Example 3:
Input: s = "(]"
Output: false
'''

class Solution:
    def isValid(self, s: str) -> bool:

        if len(s)==0:
            return True
        elif len(s)==1:
            return False
        i = 0

        while len(s)>0:
            if i>=len(s):
                break

            siradaki_parentheses = s[i]

            try:
                siradaki_parentheses_den_sonraki = s[i+1]
            except:
                print("tek kaldi")

            karsilikli_ayni_mi = False

            if (siradaki_parentheses=='(' and siradaki_parentheses_den_sonraki==')'):
                karsilikli_ayni_mi = True

            if (siradaki_parentheses=='[' and siradaki_parentheses_den_sonraki==']'):
                karsilikli_ayni_mi = True,

            if (siradaki_parentheses=='{' and siradaki_parentheses_den_sonraki=='}'):
                karsilikli_ayni_mi = True

            if karsilikli_ayni_mi:
                s = s[:i] + s[i+1:]
                s = s[:i] + s[i+1:]
                i = 0

            else:
                i = i+1

        
        if len(s)>0:
            return False
        else:
            return True


if __name__ == '__main__':
    solution = Solution()
    s = "()"
    print(s+" -Example 1: Output: True-return: ",solution.isValid(s))

    s = "()[]{}"
    print(s+" -Example 2: Output: True-retrun: ",solution.isValid(s))

    s = "(]"
    print(s+" -Example 3: Output: False-retrun: ",solution.isValid(s))

    s = "([)]"  
    print(s+" -Example : Output: False-retrun: ",solution.isValid(s))

    s= "(){}}{" 
    print(s+" -Example : Output: False-retrun: ",solution.isValid(s))

    s = "{[]}" 
    print(s+" -Example: Output: True-retrun: ",solution.isValid(s))

    s = "["
    print(s+" -Example: Output: True-retrun: ",solution.isValid(s))