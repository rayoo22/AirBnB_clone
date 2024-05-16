#!/usr/bin/python3
"""console module"""
import cmd
import json
import shlex
import models
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """entry point of the command interpreter"""

    prompt = '(hbnb) '
    classes = {"BaseModel": BaseModel, "User": User, "State": State, "City": City, "Amenity": Amenity, "Place": Place, "Review": Review}

    def do_create(self, clsname=None):
        """ creates an instance of BaseModel """
        if not clsname:
            print("** class name missing **")

        elif not self.classes.get(clsname):
            print('** class doesn\'t exist **')

        else:
            obj = self.classes[clsname]()
            models.storage.save()
            print(obj.id)

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        clsname, objid = None, None
        args = arg.split(' ')
        if len(args) > 0:
            clsname = args[0]
        if len(args) > 1:
            objid = args[1]
        if not clsname:
            print("** class name missing **")
        elif not objid:
            print('** instance id missing **')
        elif not self.classes.get(clsname):
            print('** class doesn\'t exist **')
            
        else:
            k = clsname + "." + objid
            obj = models.storage.all().get(k)
            if not obj:
                print('**no instance found **')
            else:
                print(obj)
        

    def do_destroy(self, line):
        """ deletes an instance of BaseModel based on class name and id """
        clargs = line.split()
        if len(clargs) == 0:
            print("** class name missing **")
        elif clargs[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")
        elif len(clargs) == 1:
            print("** instance id missing **")
        else:
            key_id = "{}.{}".format(clargs[0], clargs[1])
            try:
                del models.storage.all()[key_id]
                models.storage.save()
            except KeyError:
                print("** no instance found **")

    def do_all(self, line):
        """ prints all string representation of BaseModel instances"""
        clargs = line.split()
        new_list = []

        if len(clargs) == 1:
            if clargs[0] not in HBNBCommand.classes.keys():
                print("** class doesn't exist **")
            else:
                for key in models.storage.all().keys():
                    name = key.split(".")
                    if name[0] == clargs[0]:
                        new_list.append(str(models.storage.all()[key]))
                    else:
                        continue
                print(new_list)

        else:
            for key, value in models.storage.all().items():
                new_list.append(str(models.storage.all()[key]))
            print(new_list)


    def do_update(self, arg):
        """Updates an instance of BaseModel based on name and id"""
        clargs = shlex.split(line)
        models.storage.reload()
        nova_dict = models.storage.all()
        if len(clargs) == 0:
            print("** class name missing **")
        elif clargs[0] not in HBNBCommand.classes.keys():
            print("** class doesn't exist **")
        elif len(clargs) == 1:
            print("** instance  id missing **")
        elif clargs[0] + "." + clargs[1] not in nova_dict.keys():
            print("** no instance found **")
        elif len(clargs) == 2:
            print("** attribute name missing **")
        elif len(clargs) == 3:
            print("** value missing **")
        else:
            key_id = "{}.{}".format(clargs[0], clargs[1])
            if hasattr(nova_dict[key_id], clargs[2]):
                binder = type(getattr(nova_dict[key_id], clargs[2]))
                setattr(nova_dict[key_id], clargs[2], binder(clargs[3]))
                models.storage.save()
            else:
                setattr(nova_dict[key_id], clargs[2], clargs[3])
                models.storage.save()

    def default(self, line):
        """ handles class commands """
        ln = line.split('.', 1)
        if len(ln) < 2:
            print('*** Unknown syntax:', ln[0])
            return False
        clsname, line = ln[0], ln[1]
        if clsname not in list(self.classes.keys()):
            print('** Unknown syntax: {}.{}'.format(clsname, line))
            return False
        ln = line.split('(', 1)
        if len(ln) < 2:
            print('*** Unknown syntax: {}.{}'.format(clsname, ln[0]))
            return False
        mthname, args = ln[0], ln[1].rstrip(')')
        if mthname not in ['all', 'count', 'show', 'destroy', 'update']:
            print('*** Unknown syntax: {}.{}'.format(clsname, line))
            return False
        if mthname == "all":
            self.do_all(clsname)
        elif mthname == "count":
            print(self.count_class(clsname))
        elif mthname == "show":
            self.do_show(clsname + " " + args.strip('"'))
        elif mthname == "destroy":
            self.do_destroy(clsname + " " + args.strip('"'))
        elif mthname == 'update':
            lb, rb = args.find('{'), args.find('}')
            d = None
            if args[lb:rb + 1] != '':
                d = eval(args[lb:rb + 1])
            ln = args.split(',', 1)
            objid, args = ln[0].strip('"'), ln[1]
            if d and type(d) is dict:
                self.handle_dict(clsname, objid, d)
            else:
                from shlex import shlex
                args = args.replace(',', ' ', 1)
                ln = list(shlex(args))
                ln[0] = ln[0].strip('"')
                self.do_update(" ".join([clsname, objid, ln[0], ln[1]]))

    @staticmethod
    def count_class(clsname):
        """count number of object of a certain class"""
        c = 0
        for key, value in models.storage.all().items():
            if type(value).__name__ == clsname:
                c += 1
        return (c)



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
