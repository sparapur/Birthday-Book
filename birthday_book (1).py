import os
from datetime import datetime, date

class Birthday:
    def __init__(self, firstname, lastname, month, day, year):
        self.firstname = firstname
        self.lastname = lastname
        # Validate date before setting
        try:
            test_date = date(year, month, day)
            self.month = month
            self.day = day
            self.year = year
        except ValueError:
            raise ValueError(f"Invalid date: {month}/{day}/{year}")
            
    def get_age(self):
        today = date.today()
        birthday = date(self.year, self.month, self.day)
        age = today.year - birthday.year
        if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
            age -= 1
        return age
        
    def days_until_birthday(self):
        today = date.today()
        next_birthday = date(today.year, self.month, self.day)
        if next_birthday < today:
            next_birthday = date(today.year + 1, self.month, self.day)
        return (next_birthday - today).days

    def __str__(self):
        return f"{self.firstname} {self.lastname}, {self.month}/{self.day}/{self.year}"

class BirthdayManager:
    def __init__(self):
        self.birthday_book = []
        self.echo_state = False

    def commands(self,argument):
        if argument=="":
               print("No command entered. Please enter a list of commands, or type 'help' for a list.")
        elif argument[0]=="add":
            self.add(argument)
        elif argument[0]=="help":
             self.print_help()
        elif argument[0]=="list":
             self.list_entries()
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
        elif argument[0]=="update":
            self.update(argument)
        else:
            print("I am sorry, but that is not a recognized command, or")
            print("you have entered an incorrect number of arguments.")
            print("You may enter 'help' to see a list of commands.")    
    
    def add(self, argument):
        if len(argument) != 6:
            print("Error: add command requires firstname, lastname, month, day, year")
            return
            
        try:
            firstname, lastname = argument[1], argument[2]
            month, day, year = map(int, argument[3:6])
            
            entry = Birthday(firstname, lastname, month, day, year)
            self.birthday_book.append(entry)
            
            # Sort the book by date
            self.birthday_book.sort(key=lambda x: (x.month, x.day))
            
            print(f"Added \"{entry}\" to birthday book.")
            
            # Show upcoming birthday if within 30 days
            days_until = entry.days_until_birthday()
            if days_until <= 30:
                print(f"Upcoming birthday in {days_until} days!")
                
        except ValueError as e:
            print(f"Error: {str(e)}")

    def search(self, argument):
        if len(argument) < 2:
            print("Error: Search term required")
            return
            
        name = argument[1].lower()
        matches = []
        
        for entry in self.birthday_book:
            if name in entry.firstname.lower() or name in entry.lastname.lower():
                matches.append(entry)
                
        if matches:
            print(f'Entries matching "{argument[1]}":')
            for match in matches:
                age = match.get_age()
                days_until = match.days_until_birthday()
                print(f"{match} (Age: {age}, Next birthday in: {days_until} days)")
        else:
            print(f"No entries found matching '{argument[1]}'")

    def save(self, argument):
        if len(argument) != 2:
            print("Error: Filename required for save command")
            return
            
        filename = argument[1]
        try:
            with open(filename, 'w') as outfile:
                outfile.write("List of Birthdays!\n")
                for entry in self.birthday_book:
                    outfile.write(f"{entry}\n")
            print(f'Saved birthdays to "{filename}"')
        except IOError as e:
            print(f"Error saving file: {str(e)}")

    def load(self, argument):
        if len(argument) != 2:
            print("Error: Filename required for load command")
            return
            
        filename = argument[1]
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found")
            return
            
        try:
            with open(filename, 'r') as infile:
                first_line = infile.readline().strip()
                if first_line != "List of Birthdays!":
                    print("Error: Invalid file format")
                    return
                    
                for line in infile:
                    line = line.strip()
                    if line:
                        try:
                            name, date_str = line.split(', ')
                            firstname, lastname = name.split()
                            month, day, year = map(int, date_str.split('/'))
                            self.birthday_book.append(Birthday(firstname, lastname, month, day, year))
                        except (ValueError, IndexError):
                            print(f"Warning: Skipping invalid line: {line}")
                
            print(f"Successfully loaded birthdays from {filename}")
            self.birthday_book.sort(key=lambda x: (x.month, x.day))
            
        except IOError as e:
            print(f"Error loading file: {str(e)}")

    def stats(self):
        """Display statistics about the birthday book"""
        if not self.birthday_book:
            print("No entries in birthday book")
            return
            
        total = len(self.birthday_book)
        ages = [entry.get_age() for entry in self.birthday_book]
        avg_age = sum(ages) / len(ages)
        
        upcoming = [entry for entry in self.birthday_book 
                   if entry.days_until_birthday() <= 30]
        
        print(f"Total entries: {total}")
        print(f"Average age: {avg_age:.1f} years")
        print(f"Upcoming birthdays (next 30 days): {len(upcoming)}")
        
        if upcoming:
            print("\nUpcoming birthdays:")
            for entry in upcoming:
                days = entry.days_until_birthday()
                print(f"- {entry.firstname} {entry.lastname}: {days} days")
    
    def delete(self, argument):
        try:
            index_to_delete = int(argument[1]) - 1
            if 0 <= index_to_delete < len(self.birthday_book):
                firstname = self.birthday_book[index_to_delete].firstname
                lastname = self.birthday_book[index_to_delete].lastname
                decision = input(f"Really delete {firstname} {lastname} from the birthday book? (y/n) ")
                while decision not in ("y", "n"):
                    decision = input('Please enter "y" or "n" (y/n): ')
                if decision == "y":
                    del self.birthday_book[index_to_delete]
                    print("Entry deleted. Updated birthday book:")
                    self.list([])  # Call list with an empty argument list
            else:
                print("I'm sorry, but there is no such entry in the book.")
        except (IndexError, ValueError):
            print("Error: Please specify the item to delete using an integer.")
    
    def update(self, argument):
        """Update an existing birthday entry"""
        if len(argument) != 7:  # command + 6 arguments = 7 total
            print("Error: Update command format:")
            print("update entryNumber newFirstName newLastName newMonth newDay newYear")
            return
        
        try:
            index = int(argument[1]) - 1  # Convert from 1-based to 0-based indexing
            if 0 <= index < len(self.birthday_book):
                old_entry = self.birthday_book[index]
                new_firstname = argument[2]
                new_lastname = argument[3]
                new_month = int(argument[4])
                new_day = int(argument[5])
                new_year = int(argument[6])
                
                # Show the current and new values
                print(f"Current entry: {old_entry}")
                new_entry = Birthday(new_firstname, new_lastname, new_month, new_day, new_year)
                print(f"New entry will be: {new_entry}")
                
                # Confirm the update
                decision = input("Do you want to update this entry? (y/n) ")
                while decision.lower() not in ['y', 'n']:
                    decision = input('Please enter "y" or "n" (y/n): ')
                
                if decision.lower() == 'y':
                    self.birthday_book[index] = new_entry
                    print(f"Updated entry {index + 1}")
                    self.list_entries()  # Using new method name
                else:
                    print("Update cancelled")
            else:
                print("Error: Invalid entry number")
        except ValueError:
            print("Error: Please use integers for entry number, month, day, and year")
        except IndexError:
            print("Error: Invalid entry number")
    
    def echo(self,argument):
        if argument[1] == "on":
            self.echo_state = True
            print("Echo turned on.")
        elif argument[1] == "off":
            self.echo_state = False
            print("Echo turned off.")
    
    def list_entries(self):  # Renamed method and removed argument parameter
        """List all entries in the birthday book"""
        if not self.birthday_book:
            print("The birthday book is empty.")
        else:
            for i in range(len(self.birthday_book)):
                print(f"{i + 1}. {self.birthday_book[i]}")

    def print_help(self): 
        print("Allowed commands:")
        print("add firstName lastName month day year")
        print("update entryNumber newFirstName newLastName newMonth newDay newYear")
        print("list") 
        print("delete number")
        print("search name")
        print("save filename")
        print("load filename")
        print("help")
        print("echo on")
        print("echo off")
        print("quit")

def main():
    manager = BirthdayManager()
    print("Welcome to the Enhanced Birthday Book Manager")
    print("Type 'help' for available commands")
    
    while True:
        try:
            answer = input("> ").strip()
            if manager.echo_state:
                print(f"You entered: \"{answer}\"")
                
            args = answer.split()
            should_continue = manager.commands(args)
            if should_continue is False:
                break
                
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()