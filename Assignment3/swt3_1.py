import sys

class Person:
    """docstring for Person"""
    def __init__(self):
        self.gender = None
        self.age = None
        self.status = None
        self.rate = 500
        
def print_usage():
    print "Usage: python <programname> <gender> <age> <status>"
    print ""
    print "\t gender: \n\t\tMust be either male or female."
    print "\t age: \n\t\tMust be an integer."
    print "\t status: \n\t\tThe relationship status should be either married or unmarried."

    sys.exit()

def main():
    # insurance_rate = 500

    if len(sys.argv) < 4:
        print "Insufficient arguments!"
        print_usage()
    elif sys.argv[1] != "male" and sys.argv[1] != "female":
        print "Invalid gender"
        print_usage()
    elif not sys.argv[2].isdigit():
        print "Age is not an integer" 
        print_usage()
    elif sys.argv[3] != "married" and sys.argv[3] != "unmarried":
        print "Invalid relationship status"
        print_usage()


    person = Person()

    # info = {"gender":"male","age":25,"status":"married"}

    # person.gender = info["gender"]
    # person.age = info["age"]
    # person.status = info["status"]
    person.gender = sys.argv[1]
    person.age = int(sys.argv[2])
    person.status = sys.argv[3]

    if person.status == "unmarried" and person.gender == "male" and person.age < 25:
        person.rate += 1500
    else:
        if person.status == "married" or person.gender == "female":
            person.rate -= 200
        if person.age >= 50 and person.age <= 65:
            person.rate -= 100

    print "Insurance rate is: $%d" % (person.rate)


if __name__ == '__main__':
    main()

