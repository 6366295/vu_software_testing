# Requirements Specification

1. At startup, the program will read a file containing phone numbers
and names. There may be up to 20 such pairs, one per line.
2. The phone numbers are 5 digits long, all numbers. A phone number
may begin with 0.
3. The names are a single name field up to 12 characters. Names are
a single word (no first name, last name; let’s keep it simple.)
Names are all alphabetic: A-Z a-z.
4. Commands are:
a. phone call phone
b. phone offhook
c. phone onhook
d. phone transfer phone
e. phone conference phone
5. In each command, the phone is either the phone number or the
name.
6. Possible responses are as follows. See later requirements for the
conditions for each response.
a. phone hears dialtone
b. phone hears ringback
c. phone hears ringing
d. phone hears busy
e. phone hears denial
f. phone hears silence
g. phone and phone are talking
h. phone and phone and phone are talking
7. Normal call:
a. phone1 offhook (command from user)
b. phone1 hears dialtone (response from computer)
c. phone1 call phone2 (command from user)
d. phone1 hears ringback (response from computer)
e. phone2 hears ringing (response from computer)
f. phone2 offhook (command from user)
g. phone1 and phone2 are talking (response from computer)
h. phone2 onhook (command from user)
i. phone1 hears silence (response from computer) 
8. Conference call: After phone1 and phone2 are talking:
a. phone1 (or phone2) conference phone3
b. phone1 hears ringback
c. phone3 hears ringing
d. phone3 offhook
e. phone1 and phone2 and phone3 are talking
f. phone1 onhook
g. phone2 and phone3 are talking
h. phone1 hears silence
9. Transfer: After phone1 and phone2 are talking:
a. phone1 transfer phone3
b. phone1 hears ringback
c. phone3 hears ringing
d. phone3 offhook
e. phone1 hears silence
f. phone2 and phone3 are talking
10. If phone1 and phone2 are talking on a phone call:
a. phone3 offhook
b. phone3 hears dialtone
c. phone3 call phone1
d. phone3 hears busy
11. Illegal cases:
a. phone1 offhook
b. phone1 hears dialtone
c. phone1 call illegal_phone
d. phone1 hears denial
e. In general: if the phone is offhook, and tries to do
something illegal: dial an invalid phone number, or tries
to do more than a 3-way conference, the phone hears denial.
See one exception below.
12. Another one:
a. phone1 call phone2 (without going offhook)
b. phone1 hears silence
c. In general: if the phone is onhook, and tries to do
anything except going offhook, the phone hears silence.
13. Another one:
a. phone1 offhook
b. phone1 hears dialtone
c. phone1 offhook
d. (nothing happens)
e. In general: if the phone is offhook, and tries to go
offhook again, the action is ignored. You decide whether to
print a message or not.
14. One more important command: “Status”
a. Displays the status of the system. Lists each phone’s
status, and if it is on a call, who it is talking to (could
be more than one other phone.) 
