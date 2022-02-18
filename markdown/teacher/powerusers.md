---
title: "Instructor notes: power-user interfaces"
...


# Outcomes
The students should be able to

1. Appreciate that they are becoming a privileged class by learning CS
2. Explain the inequities of access created by both (a) two-interface systems and (b) only power-user-interface systems
3. Explain why power-user-interfaces tend to have opaque-to-novices UX design
4. Understand that learning curves create imbalanced usability impedance

# Scheduling
This should be placed around the time that students are engaged with learning command-line interfaces.

# Flow
1. Ask the question "why are we teaching you the command line?"
    
    Expect a lot of correct-ish answers like "sometimes you only have it" and "some people expect you to use it" and "some tasks require it." Accept and reinforce each, but do not suggest they are the one true answer.

2. Explain that the Linux command line is an example of an interface aimed at the "power user." Define [power user](https://en.wikipedia.org/wiki/Power_user) as one who (a) uses a system extensively enough to want to learn all it can do and (b) does things with it that most cannot.
    
3. Most power-user interfaces make use of options that are not displayed in any way, such as
        
    - keyboard shortcuts, like typing "F6" in a web browser
    - invisible state machines, like typing "Ctrl+U 2 6 3 A Enter" in a GTK-based system or switching between insertion and control mode in VI
    - type any of a giant list of commands in a command line or console
    
    Many power-user interfaces are actually programming languages; the linux command line is commonly bash, for example[^webconsole].

4. We teach you CLI so you can be power users.
    
    Power users want more options that good GUI design can represent. Consider the 4000+ programs listed by `ls /usr/bin | wc -l`, and the dozens of options each has as `ls --help` exemplifies, and try to imagine a menu system that got at all of that...

5. Explain that power user interfaces *create* new class systems within the digital world: the cans and cannots. This is true whether they are the only interface (how many MacOS users ever open the terminal?) or a secondary interface (how many browser users ever interact with the console?).

6. Ask for solutions to this problem of creating inequity, and discuss replies. I found it good to be prepared to discuss the following kinds of answers:
    
    - We need mandatory power-user training, CS education, etc.
    
        <div class="note">
        
        In reply I mention the idea of learning curves: it takes time to learn, time not used for other things, so what are we sacrificing?
        
        I also sometimes discuss the lack of qualified teachers and thus the long-term character of such solutions.
        
        </div>
    
    - We should not make power-user interfaces; make all programs simple.

        <div class="note">
        
        In reply I ask how many people, given power, will willingly give it up to become equal with the unempowered.
        
        </div>
    
    - This isn't a problem; the casual user doesn't want that power and wouldn't know what to do with it if they had it.
        
        <div class="note">
        
        I don't have a single standard reply, but often can do some kind of echo-and-confirm "just to be clear, you're saying that people who don't know how to do something must not want the power to do it---power they don't even know they don't have?"
        
        </div>
        
    - Once AI masters understanding what we want this problem will go away.
        
        <div class="note">
        
        I usually reply with something like "AI is just another class of applications, which themselves have power-user and casual-user interfaces. I can't predict the future, but at least on their current trajectory they are making the separation of cans and cannots more, not less, extreme."
        
        Some student have strong views on AI, so I also tread this path with some caution.
        
        </div>
        
    - Better help guides, UI design, etc, can make the separation go away.
        
        <div class="note">
        
        In reply I often summarize "Good UI is intuitive, but intuition comes from subconscious learning by repeated exposure to a pattern. When we are offering more power than most users even realize can exist, there is no intuition to use, and hence no good UI---until people become accustomed to whatever UI we make and start to develop an "intuitive" expectation for that design."
        
        It's not a perfect response, but it does the job.
        
        </div>

# More context

This lesson was inspired by the March 2019 CACM article by Sepehr Vakil and Jennifer Higgs, "[It's About Power](https://cacm.acm.org/magazines/2019/3/234921-its-about-power/fulltext)".
I recommend that article to any instructor presenting on this subject.


[^webconsole]:
    I like to show other power-user PL-CLI interfaces they won't expect, such as the web browser javascript console. For example, I have done enough web scraping in my day that I can go to <https://engineering.virginia.edu/departments/computer-science/faculty> and type
    
    ```javascript
    document.body.innerHTML =
        Array.from(document.querySelectorAll('.image'))
            .map(x=>
                x.style.backgroundImage
                .replace('url(','<img src=').replace(')','/>')
            )
            .join('\n')
    ```
    
    to get a page of faculty photos, so I sometimes will create something like this live for the students.

