---
title: "Instructor notes: Debugging hooks and back doors"
...

# Outcomes
The students should be able to

1. articulate the trade-offs intrinsic in an ethical dilemma
2. take an ethical principle from statement of principle through suggested practical activity
3. understand how engineering considerations may be at odds with ethical considerations such as privacy and social good
4. feel prepared to address ethical issues with supervisors and managers

# Scheduling
This lesson should follow the students' learning C and attempting to implement a program that is not trivially testable. Ideally they should have had to add hooks outside the API to verify some required behaviors.
    
A simple example is a program that is required to invoke `malloc` and `free` a particular number of times in a particular order. This lesson will work more effectively if you have had a conversation about how to add hooks to help.

# Flow
1. Review the idea of debugging hooks, and their prevalence in real systems

2. Pose the following question: "should you remove debugging hooks before releasing software?" Encourage a debate, supporting the less-defended side:
    - what if you need to fix a bug after release?
    - but these have performance costs
    - but some bugs depend on timing, so you need live timing
    - but hooks are rarely debugged and likely to have exploits
    - ...

3. Suggest that sometimes you need more than a simple hook; how do you respond when someone says

    - "I forgot my password and can't get into my system"
    - They call up and ask you to log in remotely and fix something
    - ...

    Solution: maintenance back door

4. What percentage of your fellow students would you trust to have access to a maintenance back door?
    
    - do you trust yourself?
    - is there a way to get the advantages without the risk?

# Assignment
Write a draft email replying to whichever of the following you object to:

- Your boss has instructed you to include a secret master password in every copy of the product so you can provide high-value support to those who pay for such. You are assured that by company policy no one will use it unless they request it use.
    
    Draft an email expressing your objection to having such a master password included. Assume your boss is a decent person with experience (but not formal education) with coding but mostly focused on business.

- Your boss's boss has instructed you to remove all hooks and back doors, even the ones you added after spending fifteen hours trying to help clients who misused the system in a way you could have diagnosed in five seconds if you had already had the back door in place.
    
    Draft an email *either* to your boss's boss explaining why this policy should have an exception for your back door *or* to your boss explaining why your leaving the back door in place is something your boss should not tell your boss's boss.

# Post-assignment activity
Discuss the down-side potential of anonymized excerpt from various student-submitted emails. Help emphasize the dilemma: both options are giving something up.

Review ACM code of ethics^[<https://ethics.acm.org/>], article 2.8. Discuss why this is not a black-and-white rule ("without a reasonable belief...") but still so strongly worded ("extraordinary precautions must be taken...")
