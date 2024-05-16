#!/usr/bin/python3
"""console module"""
import cmd
import json
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """entry point of the command interpreter"""

    prompt = '(hbnb) '

    def do_create(self, arg):
        """ creates an instance of BaseModel """
        if not arg:
            print("** class name missing **")
            return

        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        if args[0] not in ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        storage = models.storage.all()
        if key in storage:
            print(storage[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """ deletes an instance of BaseModel based on class name and id """
        if not arg:
            print("** class name missing **")
            return
        
        args = arg.split()
        if args[0] not in ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        storage = models.storage.all()
        if key in storage:
            del storage[key]
            models.storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """ prints all string representation of BaseModel instances"""
        if not arg:
            print("** class name missing **")
            return
        
        class_name = arg.split()
        if class_name not in ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]:
            print("** class doesn't exist **")
            return

        try:
            all_instances = eval(class_name).all()
            objects = [str(obj) for obj in all_instances]
            print(objects)
        except NameError:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance of BaseModel based on name and id"""
        if not arg:
            print("** class name missing **")
            return

        args = arg.split()
        if args[0] not in ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        key = "{}.{}".format(args[0], args[1])
        storage = models.storage.all()
        if key in storage:
            obj = storage[key]
            setattr(obj, args[2], args[3])
            obj.save()
        else:
            print("** no instance found **")

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
