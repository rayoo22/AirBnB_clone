#!/usr/bin/python3
"""console module"""
import cmd


class HBNBCommand(cmd.Cmd):
    """entry point of the command interpreter"""

    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """implemeting quit and EOF to exit program"""
        print() # prints a new line before exiting
        return True

    def emptyline(self):
        """called when an empty line is entered"""
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()
