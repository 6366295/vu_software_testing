# Telephone Switching Simulation

This project simulates basic telephone functions. You will not be hooked up to real phones, but instead will input commands from the keyboard, and display results.

Your system will make phone calls, as well as perform three-way conferences and transfers.

## To do list

* [ ] Formalize requirements specification
* [*] Program the program
* [ ] Create test plan
* [ ] Execute test plan

## Requirements Specification (Informal)

1. At startup, the program will read a file containing phone numbers and names. There may be up to 20 such pairs, one per line. 
2. The phone numbers are 5 digits long, all numbers. A phone number may begin with 0.
3. The names are a single name field up to 12 characters. Names are a single word (no first name, last name; let’s keep it simple.) Names are all alphabetic: A-Z a-z.
4. Commands are:
 1. phone call phone
 2. phone offhook
 3. phone onhook
 4. phone transfer phone
 5. phone conference phone
5. In each command, the phone is either the phone number or the name.
6. Possible responses are as follows. See later requirements for the conditions for each response.
 1. phone hears dialtone
 2. phone hears ringback
 3. phone hears ringing
 4. phone hears busy
 5. phone hears denial
 6. phone hears silence
 7. phone and phone are talking
 8. phone and phone and phone are talking
7. Normal call:
 1. phone1 offhook (command from user)
 2. phone1 hears dialtone (response from computer)
 3. phone1 call phone2 (command from user)
 4. phone1 hears ringback (response from computer)
 5. phone2 hears ringing (response from computer)
 6. phone2 offhook (command from user)
 7. phone1 and phone2 are talking (response from computer)
 8. phone2 onhook (command from user)
 9. phone1 hears silence (response from computer) 
8. Conference call: After phone1 and phone2 are talking:
 1. phone1 (or phone2) conference phone3
 2. phone1 hears ringback
 3. phone3 hears ringing
 4. phone3 offhook
 5. phone1 and phone2 and phone3 are talking
 6. phone1 onhook
 7. phone2 and phone3 are talking
 8. phone1 hears silence
9. Transfer: After phone1 and phone2 are talking:
 1. phone1 transfer phone3
 2. phone1 hears ringback
 3. phone3 hears ringing
 4. phone3 offhook
 5. phone1 hears silence
 6. phone2 and phone3 are talking
10. If phone1 and phone2 are talking on a phone call:
 1. phone3 offhook
 2. phone3 hears dialtone
 3. phone3 call phone1
 4. phone3 hears busy
11. Illegal cases:
 1. phone1 offhook
 2. phone1 hears dialtone
 3. phone1 call illegal_phone
 4. phone1 hears denial
 5. In general: if the phone is offhook, and tries to do something illegal: dial an invalid phone number, or tries to do more than a 3-way conference, the phone hears denial. See one exception below.
12. Another one:
 1. phone1 call phone2 (without going offhook)
 2. phone1 hears silence
 3. In general: if the phone is onhook, and tries to do anything except going offhook, the phone hears silence.
13. Another one:
 1. phone1 offhook
 2. phone1 hears dialtone
 3. phone1 offhook
 4. (nothing happens)
 5. In general: if the phone is offhook, and tries to go offhook again, the action is ignored. You decide whether to print a message or not.
14. One more important command: “Status”
 1. Displays the status of the system. Lists each phone’s status, and if it is on a call, who it is talking to (could be more than one other phone.) 
