---
title: Policies
...

# Course objectives

This course is intended to cover topics on the abstraction hierarchy 
ranging from a step above silicon to a step below languages you are likely to program.
At the end of it, you will be able to

- Read and write C and (to a lesser extent) assembly
- Understand how C become assembly and how assembly is run by a computer
- Describe how both simple and complicated data is stored in memory
- Discuss legal, ethical, and security issues related to these topics
- Use basic command-line development tools

# Logistics

## Meetings

Lecture is optional but strongly encouraged:
experience has shown that attendance is strongly correlated with grade.
Meetings are Monday, Wednesday, and Friday
with section 002 12:00–12:50 in Olsson 120
and section 001 1:00–1:50 in Nau 101.

There are two lab sections, both meeting on Thursdays in Rice 130:
one at 5:00--6:15 pm and one at 6:30–7:45.
Please attend your assigned lab section.

## Tasks

Some tasks are designed to help you learn and practice what you learned enough that the concepts solidify in your mind.
Others are designed to measure what you have learned.
The primary kinds of tasks are:

- Participate in lab
    - Labs are primarily learning exercises and most credit is for participation, but learning only occurs if sufficient progress is made so each lab has milestones that need to be reached for full credit.
    - We expect everyone to be ill, need to travel, or otherwise miss one lab, which will be excused without the need to provide documentation of your situation. To be excused for more than one lab, documentation of why each was missed is needed.
- Do homework
    - Each homework is an individual assignment unless otherwise announced.
    - Some homework will be programming assignments; others will be puzzles, worksheets, or other kinds of activities.
- Take quizzes
    - We will have weekly quizzes, administered online.
- Take exams
    - Exams will either be in-class or in-lab and must be taken in person.


## Contact


|        | Section 001 | Section 002 | TAs |
|--------|------------|-----|
| Name | Daniel Graham | Luther Tychonievich | TBA |
| Location | Rice 411 | Rice 208 | Thornton Stacks (A235) |
| Office Hours | TBA | TBA | See [the OH schedule](oh.html) |
| Phone | 243-3391| 243-3789 | (none) |
| Email | <a href="mailto:dgg6b@virginia.edu?subject=CSO1">dgg6b@virginia.edu</a> | <a href="mailto:tychonievich@virginia.edu?subject=CSO1">tychonievich@virginia.edu</a> | TBA |

For most communication, [Piazza](#) is preferred to email.
If you email, include "CSO1" in the subject line to help us prioritize your email.

Our TAs are students too, with duties and work outside of their TAing. Please do not ask them to act as your TA except at the scheduled on-the-clock times they have listed as their office hours and lab time. They are also kind people; please don't put them in the position of having to say no or (worse) being nice to you at the expense of their own schooling.

## Readings

Primary readings are write-ups posted on this website.
We may also link to external articles when appropriate.
Some readgins may have "reading quizzes" associated with them:
quizzes to be taken based on the reading prior to the lecture in which they are discussed.

If you desire a different take on the same material, the textbook *Introduction to Computer Systems: From Bits and Gate to C/C++ & Beyond* by Yale Patt and Sanjay Patel contains all of the major topics we'll cover, with a different presentation than we'll cover them.

## Coding

> "If you really want to understand something, the best way is to try and explain it to someone else. That forces you to sort it out in your own mind. And the more slow and dim-witted your pupil, the more you have to break things down into more and more simple ideas. And that’s really the essence of programming. By the time you’ve sorted out a complicated idea into little steps that even a stupid machine can deal with, you’ve certainly learned something about it yourself."
> <div>---Douglas Adams</div>

This course will teach you the basics of x86-64 assembly
and quite a bit of C.
There will be multiple assignments dealing with each.

Estimating how long it will take someone to complete a coding assignment
is always difficult.
The target difficulty is 5–10 hours of focused effort each week.

# Grading

## Grading Goal

In February 2019 the CS faculty approved [a definition](http://ugrads.cs.virginia.edu/grading-guidelines.html) of what we believe grades mean.
We hope to approximate that definition in this course.
As a brief summary,

Letter  Student demonstrated                Recommendation re future courses[^future]
------  ---------------------------         ------------------------------------
A       mastery of all topics               likely to do well
B       competence in significant topics    able to do well with some review
C       sufficient competence               likely to be challenging
D       minimal competence                  unlikely to succeed
F       less than minimal competence        retake this course first

[^future]:
    The most obvious future course is CSO2.
    CSO1 material is also directly important for work in various fields including
    networks, cyber-physical systems, robotics, operating systems, and any constrained-resource or speed-sensitive application.

These goals do not map perfectly to numeric scores. If you get full or nearly full points on all graded tasks, you should expect an A. If you miss non-trivial numbers of points or deadlines, we may attempt to assess your standing on this subjective scale in lieu of a raw point-based grade.

## Points per Activity Type

Points are awarded per task.
Different tasks and different task types are given different weight, as outlined below.

|Task        |Weight|
|------------|------|
|Quizzes     |  10% | 
|Assignments |  40% | 
|Lab         |  10% |
|Exams       |  40% |

If you earn at least 93% of the points, you will earn an A. If you earn less, you will likely be given a lower grade based on the [Grading Goals](#grading-goals). We expect this will approximate the usual 10%-per-letter breakdown, but will attempt to diagnose particular learning outcomes and mastery levels rather than being constrained to pure mechanical grade computation.

Grade estimates will be provided on the submission site, accurately reflecting individual assignment performance but being only estimates of overall course grade.

## Submitting late

Quiz solutions are released the moment the quiz closes, and thus quizzes cannot be taken late.
Your lowest quiz score is dropped.

Assignments may be submitted up to 48 hours late.
They are given 90% credit between 0 and 24 hours late;
at 80% credit between 24 and 48 hours late.
If extensions beyond that time are needed, please see the professor to discuss why and if other accommodations are also needed.

Labs may be checked off late for 90% credit by visiting a TA during office hours later during the week of the lab and going through the usual checkoff process.
If extensions beyond that time are needed, please see the professor to discuss why and if other accommodations are also needed.

Exams may not be taken late without special-case permission.

# Miscellanea

## Professionalism

Behave professionally.

Never abuse anyone, including the emotional abuse of blaming others for your mistakes.
Kindness is more important than correctness.

Let our TAs be students when they are not on the clock as TAs.

## Honesty

We always hope everyone will behave honestly.
We know we all are tempted to do what we ought not;
if you do something you regret, the sooner you tell us the sooner (and more leniently) we can correct it.

### No plagiarism (nor anything like it)

You **must** cite any and every source you consult, other than those explicitly provided by the course itself.
Talked to a friend, saw an interesting video, consulted a website, had a tutor?
Tell us!
Put it in a comment in your code or quiz.

### Write your own code

You must write your own code.
Not just type it (though you need to do that too): **compose it yourself**, as your own original work.

We ask you to program to help you learn the content covered in the programming assignment and to help you demonstrate to us your knowledge.
This is unlike industry, where you program to create a product.
Because it is your mind we are looking to help develop and measure, it is your mind that must do all the work.
Working with others is *not* OK.

Our TAs have been trained to provide help that does not undermine the primary purpose of helping you learn. Other people (tutors, fellow students, etc) have not. As such, you should not give help to your peers nor accept help from others besides course staff.

### Understand what you submit

Your understanding is the primary deliverable of our assignments, not the code itself.
As such, we may ask you to explain aspects of a solution you turn in,
and may dock points if it appears you simply copied someone else's ideas (or just guessed a lot of things until one worked) without understanding them.

### No help on quizzes

It would probably go without saying if we didn't say it, but no assistance may be given or received on any supervised evaluation or online quiz unless specifically announced otherwise by the professor (or another proctor of the evaluation).

### Consequences of Dishonesty

If we believe you have acted dishonestly, we will communicate this fact to you and propose a penalty.
If you have information we lack, please share that with us; we may thereafter change our belief and/or proposed penalty.

If we are not able to come to an agreement, or if the case is particularly egregious and beyond our comfort level handling in-course, we will instead refer the case to the University Honor System and abide by their findings.


## Personal accommodations

### Disability

If you qualify for accommodations from [the SDAC](http://studenthealth.virginia.edu/sdac), please let your professor know, preferably in a private setting where we can discuss how your accommodations will interplay with the quiz- and assignment-based nature of this course.

### Religious observances

We fully support [the university's stance](https://eocr.virginia.edu/accommodations-religious-observance) on accommodating religious observances.
If such observances or other religious beliefs impact or are likely to impact your work this semester,
please let us know as soon as you are aware of this impact.

### Life

Bad things happen.
People forget things and make mistakes.
Bad days coincide with due dates.
Etc.

If you believe that circumstances warrant an change in deadline, a second chance, or some other accommodation in order to more accurately synchronize grade with knowledge, come talk to your professor and we'll resolve the situation as best we can.
