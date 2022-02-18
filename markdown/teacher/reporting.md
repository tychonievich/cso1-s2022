---
title: "Instructor notes: Reporting Procedures"
...


# Outcomes
The students should be able to

1. know how to use responsible reporting procedures if they discover a security exploit
2. know how to look up vulnerabilities in centralized databases and understand the severity levels listed there
3. understand the importance of updating software they use, both end-user products and dependent libraries

# Scheduling
This lesson should follow a discussion of exploitable code, such as C programs vulnerable to stack overflow attacks; how at least one such exploits works; and how to recognize exploitable vs non-exploitable code for that exploit. Ideally it should also follow an exploration of assembly, what those exploits look like in assembly, and exposure to a disassembler like `objdump`.

# Flow
1. "Suppose one day you are trying to solve a particularly difficult bug in a system and are beginning to think maybe a third-party library might not be doing exactly what you thought. You disassemble the binary and are reading the code to understand what it is actually doing, and as you do you notice that several places in that code are vulnerable to *recently discussed exploit*. What should you do next?"

2. Lead a discussion. If the students do not bring these up themselves, raise the following options:
    
    - Write an exploit to prove to the library authors that they have a bug
    - Report the vulnerability to the company in secret so they can fix it before it is exploited
    - Report the vulnerability publicly to put pressure on the company to fix it
    - Switch to a different library and say no more about it, giving yourself a competitive edge over other companies using the exploitable code
    - Make a note, so that if later someone attacks your product through that exploit, you can blame the library provider, and then move on
    - Publish the exploit; you can get famous finding a big vulnerability

3. Briefly explain industry best practice:
    
    a. inform those who should fix the problem privately
    b. after a suitable time has elapsed, publish the vulnerability and (if it has been fixed) the first version of the software to fix it
    
4. Visit the [CVE List](https://cve.mitre.org/cve/) and/or the [NVD](https://nvd.nist.gov/) and discuss the meaning of each part of that database, including the idea of [vulnerability metrics](https://nvd.nist.gov/vuln-metrics/cvss). Help make this concrete by discussing the maximum downside potential of a selection of recent vulnerabilities.

5. Emphasize the importance of frequent security-patch updates to all software.
