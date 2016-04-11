


FILENAME = "phonebook.txt"
COMMANDS = ["call", "offhook", "onhook", "transfer", "conference"]

phonenumbers = {}

def parse_phonebook():


    with open(FILENAME) as f:
        for line in f:
            number, name = line.split(' ', 1)
            number = number.strip()
            name = name.strip()
            if number.isdigit() and (len(number) == 5) and name.isalpha() and (len(name) <= 12):
                phonenumbers[number] = name



def main():
    
    print "Hello World!"
    
    parse_phonebook()

    print "Phonenumber dictionary:"
    print phonenumbers



    return 0

if __name__ == '__main__':
    main()