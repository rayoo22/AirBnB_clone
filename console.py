#!/usr/bin/python3
"""
Command interpreter for AirBnB clone
"""
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter class
    """
    prompt = "(hbnb) "
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        new_instance = self.classes[args[0]]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance based on the class
        name and id
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id (save the change
        into the JSON file)
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """
        Prints all string representation of all instances based or not on the
        class name
        """
        args = arg.split()
        if args and args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        objs = storage.all()
        obj_list = []
        for key, value in objs.items():
            if not args or key.startswith(args[0]):
                obj_list.append(str(value))
        print(obj_list)

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file)
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        instance = storage.all()[key]
        attr_name = args[2]
        attr_value = args[3].strip('\"')

        if hasattr(instance, attr_name):
            attr_type = type(getattr(instance, attr_name))
            setattr(instance, attr_name, attr_type(attr_value))
        else:
            setattr(instance, attr_name, attr_value)
        instance.save()

    def default(self, line):
        """Method to handle default case where command is not found"""
        match = re.fullmatch(r"(\w+)\.(\w+)\((.*)\)", line)
        if match:
            class_name, method_name, method_args = match.groups()
            if class_name in self.classes:
                if method_name == "all":
                    self.do_all(class_name)
                elif method_name == "count":
                    count = len([key for key in storage.all()
                                if key.startswith(class_name)])
                    print(count)
                elif method_name == "show":
                    self.do_show(f"{class_name} {method_args.strip('\"')}")
                elif method_name == "destroy":
                    self.do_destroy(f"{class_name} {method_args.strip('\"')}")
                elif method_name == "update":
                    args_match = re.fullmatch(r"\"(.+?)\", (.+)", method_args)
                    if args_match:
                        instance_id, update_args = args_match.groups()
                        if (update_args.startswith("{")
                                and update_args.endswith("}")):
                            update_dict = eval(update_args)
                            for attr, value in update_dict.items():
                                self.do_update(
                                    f"{class_name} {instance_id} {attr} "
                                    f"{value}"
                                )
                        else:
                            attr_name, attr_value = update_args.split(", ")
                            self.do_update(
                                f"{class_name} {instance_id} "
                                f"{attr_name.strip('\"')} "
                                f"{attr_value.strip('\"')}"
                            )
            else:
                print("** class doesn't exist **")
        else:
            print(f"*** Unknown syntax: {line}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
