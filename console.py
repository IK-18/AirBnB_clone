#!/usr/bin/python3
"""Contains the entry point of the command interpreter"""
import cmd
from re import search
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


def parse_cmd(arg):
    """Parses a list of args"""
    curly = search(r"\{(.*?)\}", arg)
    braces = search(r"\[(.*?)\]", arg)
    if curly is None:
        if braces is None:
            return [token.strip(",") for token in split(arg)]
        else:
            tokens = split(arg[:braces.span()[0]])
            ret = [token.strip(",") for token in tokens]
            ret.append(braces.group())
            return ret
    else:
        tokens = split(arg[:curly.span()[0]])
        ret = [token.strip(",") for token in tokens]
        ret.append(curly.group())
        return ret


class HBNBCommand(cmd.Cmd):
    """HBNB command interpreter

    Attributes:
        __classes (set): set of classes supported by command interpreter
        prompt (str): The command prompt

    Methods:
        emptyline(self): does nothing upon recieving an empty line
        do_quit(self, arg): exits the program
        do_EOF(self, arg): exits the program
        do_create(self, arg): creates a new class instance, saves it
            and prints its id
        do_show(self, arg): prints the string representation of an instance
            based on the class name and id
        do_destroy(self, arg): deletes an instance based on the class name
            and id
        do_all(self, arg): prints all string representation of all instances
            based or not on the class name
        do_update(self, arg): updates an instance based on the class name
            and id by adding or updating attribute
    """

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    }
    prompt = "(hbnb) "

    def emptyline(self):
        """Do nothing upon receiving an empty line"""
        pass

    def default(self, arg):
        """Invalid input handling"""
        arg_dict = {
            "show": self.do_show,
            "destroy": self.do_destroy,
            "all": self.do_all,
            "update": self.do_update,
            "count": self.do_count
        }
        match = search(r"\.", arg)
        if match is not None:
            args = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = search(r"\((.*?)\)", args[1])
            if match is not None:
                cmnd = [args[1][:match.span()[0]], match.group()[1:-1]]
                if cmnd[0] in arg_dict.keys():
                    para = "{} {}".format(args[0], cmnd[1])
                    return arg_dict[cmnd[0]](para)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program"""
        print()
        return True

    def do_create(self, arg):
        """Usage: create <class name>
        Creates a new class instance, saves it and prints the id
        """
        args = parse_cmd(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(args[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class name> <id> or <class name>.show(<id>)
        Prints a string representation of the instance
        based on the class name and id
        """
        args = parse_cmd(arg)
        objs = storage.all()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in objs.keys():
            print("** no instance found **")
        else:
            print(objs["{}.{}".format(args[0], args[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class name> <id> or <class name>.destroy(<id>)
        Deletes an instance based on the class name and id
        """
        args = parse_cmd(arg)
        objs = storage.all()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in objs.keys():
            print("** no instance found **")
        else:
            del objs["{}.{}".format(args[0], args[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all <class name> or all or <class name>.all()
        Prints all string representations of all instances
        based or not on the class name
        """
        args = parse_cmd(arg)
        if len(args) > 0 and args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        objs = []
        for obj in storage.all().values():
            if len(args) == 0:
                objs.append(obj.__str__())
            elif args[0] == obj.__class__.__name__:
                objs.append(obj.__str__())
        if len(objs) > 0:
            print(objs)

    def do_update(self, arg):
        """Usage: update <class name> <id> <attribute name> "<attribute value>"
        or <class name>.update(<id>, <attribute_name>, <attribute_value>)
        or <class name>.update(<id>, <dict>)
        Updates an instance based on the class name
        and id by adding or updating attribute
        """
        args = parse_cmd(arg)
        objs = storage.all()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(args[0], args[1]) not in objs.keys():
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                type(eval(args[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(args) == 4:
            obj = objs["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__.keys():
                vtype = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = vtype(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
        elif type(eval(args[2])) == dict:
            obj = objs["{}.{}".format(args[0], args[1])]
            for k, v in eval(args[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    vtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = vtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def do_count(self, arg):
        """Usage: count <class name> or <class name>.count()
        Retrieves the number of instances of a class
        """
        args = parse_cmd(arg)
        num = 0
        for obj in storage.all().values():
            if args[0] == obj.__class__.__name__:
                num += 1
        print(num)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
