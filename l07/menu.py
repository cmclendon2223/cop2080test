import os

def run_bash_cmd(some_choice):
    print('-' * 80, '\n')
    print('You entered #', some_choice)
    if (some_choice == 1):
        print('The available memory is ')
        os.system('free -tmh')
    elif (some_choice == 2):
        print('The current network connections include: ')
        os.system('netstat -an | grep -i Estab | cut -d \':\' -f 2,3 | gawk \'{print $2}\' | grep [0-9] | uniq')
    elif (some_choice == 3):
        print('Available file space is: ')
        os.system('df -h | grep \"Filesystem\\|root\"')
    return

# a menu displayed in the termanal that is used to run linux functions 
class Menu:
    # construct menu with no options
    def __init__(self):
        self._options = []

    # add an option to the menu
    def addOption(self, option):
        self._options.append(option)

    # display menu with list of options, run 
    def getInput(self):
        print()
        for i in range(1, len(self._options) + 1):
            print(str(i) + " " + self._options[i - 1])

        choice = int(input())

        if choice > 0 and choice <= len(self._options):
            if (choice == 4):
                return
            else:
                run_bash_cmd(choice)
                self.getInput()
        else:
            print("Unvalid selection")
            self.getInput()
