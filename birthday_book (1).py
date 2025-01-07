import os

# Here's one function for you. No reason for everyone to write this one.

class Birthday:

    def __init__(self,firstname,lastname, month, day, year):
            self.firstname=firstname
            self.lastname = lastname
            self.month = month
            self.day = day
            self.year = year
    def __str__(self):
            return(f"{self.firstname} {self.lastname}, {self.month}/{self.day}/{self.year}")

class birthday_manager:
    def __init__(self):
         self.birthday_book=[]
         self.echo_state=False
    def commands(self,argument):
        if argument=="":
               print("No command entered. Please enter a list of commands, or type 'help' for a list.")
        elif argument[0]=="add":
            self.add(argument)
        elif argument[0]=="help":
             self.print_help()
        elif argument[0]=="list":
             self.list()
        elif argument[0]=="delete":
             self.delete(argument)
        elif argument[0]=="search":
            self.search(argument)
        elif argument[0]=="save":
            self.save(argument)
        elif argument[0]=="load":
            self.load(argument)
        elif argument[0]=="quit":
            return False
        elif argument[0]=="echo":
            self.echo(argument)

        else:
            print("I am sorry, but that is not a recognized command, or")
            print("you have entered an incorrect number of arguments.")
            print("You may enter 'help' to see a list of commands.")
    
    def add(self,argument):
        if len(argument)!=6:
            print("I am sorry, but that is not a recognized command, or")
            print("you have entered an incorrect number of arguments.")
            print("You may enter 'help' to see a list of commands.")
            return
        try:
            firstname=argument[1]
            lastname=argument[2]
            month=int(argument[3])
            day=int(argument[4])
            year=int(argument[5])

            entry=Birthday(firstname,lastname, month, day, year)
            self.birthday_book.append(entry)
            print(f"Added \"{entry}\" to birthday book.")
        except:
             print("Unable to add birthday to book. Please use integers for dates.")

    def print_help(self): 
        """This function can be used to print out the help message."""
        print("Allowed commands:")
        print("add firstName lastName month day year")
        print("list") 
        print("delete number")
        print("search name")
        print("save filename")
        print("load filename")
        print("help")
        print("echo on")
        print("echo off")
        print("quit")
    
    def list(self):
        if not self.birthday_book: #this will reveal if the list if empty. if empty, it will become true
            print("The birthday book is empty.")
        else:
            for i in range(len(self.birthday_book)):
                print(f"{i + 1}. {self.birthday_book[i]}")
    
    def delete(self,argument):
        try: 
            index_to_delete=int(argument[1])-1
            if 0<= index_to_delete<len(self.birthday_book):
                firstname = self.birthday_book[index_to_delete].firstname
                lastname = self.birthday_book[index_to_delete].lastname
                decision=input(f"Really delete {firstname} {lastname} from the birthday book? (y/n) ")
                if decision=="y":
                    del self.birthday_book[index_to_delete]
                    self.list()
                while decision!="n" and decision!="y":
                    decision=input('Please enter "y" or "n" (y/n): ')      
            else:
                print("I'm sorry, but there is no such entry in the book.")
                    
        except(IndexError, ValueError):
            print("Error: Please specify the item to delete using an integer.")
    
    def search(self,argument):
        name=argument[1].lower()
        matches=[]
        for i in range(len(self.birthday_book)):
            entry=self.birthday_book[i]
            if name==entry.firstname.lower() or name==entry.lastname.lower():
                matches.append(i)
        if matches:
            print(f'Entries with a name of "{argument[1]}"')
            for j in range(len(matches)):
                print(self.birthday_book[matches[j]])
        else:
            print(f"I'm sorry, but there are no entries with a name of {argument[1]}.")
        
    def save(self,argument):
        filename=argument[1]
        outfile=open(filename,'w')
        outfile.write("List of Birthdays!")
        for i in range(len(self.birthday_book)):
            outfile.write(str(self.birthday_book[i])+"\n")
        print(f'Saved birthdays to "{filename}".')
    
    def load(self,argument):
        filename=argument[1]
        if os.path.exists(filename):
            infile=open(filename,'r')
            first_line=infile.readline().strip()
            if first_line!="List of Birthdays!":
                print(f"I'm sorry, but \"{filename}\" is not in the correct")
                print("format. You can only load files saved by this same program.")

            else:    
                for line in infile:
                    line=infile.readline().strip()
                    if line!="":
                        (name,date)=line.split(', ')
                        (firstname,lastname)=name.split()
                        date_parts=date.split('/')
                        month=int(date_parts[0])
                        day=int(date_parts[1])
                        year=int(date_parts[2])
                        self.birthday_book.append(Birthday(firstname,lastname,month,day,year))
            print(f"Birthdays in \"{filename}\" added to birthday book.")
            infile.close()
        else:
            print(f"I'm sorry, but \"{filename}\" is not in the correct format. You can only load files saved by this same program.")
            return
    
    def echo(self,argument):
        if argument[1] == "on":
            self.echo_state = True
            print("Echo turned on.")
        elif argument[1] == "off":
            self.echo_state = False
            print("Echo turned off.")

            


def main():
    """The main function of the Birthday Book program."""
    manager=birthday_manager()
    print("Welcome to the Birthday Book Manager")
    while True: #loop is so that input is continuous
        answer=input("> ").strip()
        if manager.echo_state==True:
            print(f"You entered: \"{answer}\"")
        argument=answer.split()
        if argument:
            should_continue=manager.commands(argument)
            if should_continue==False:
                break



    



if __name__ == "__main__":
    main()