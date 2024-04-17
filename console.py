#!/usr/bin/python3
"""
 contains the entry point of the command interpreter
"""

import cmd
import sys
import shlex
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
    -Command interpreter for the AirBnB console
    -Accepts commands via interactive mode & non-interactive mode
    """
    prompt = "(hbnb) "
    classes = {"BaseModel", "User", "State", "City", "Amenity", "Place",
               "Review"}

    def emptyline(self):
        '''overide default of running last command when prompt cmd is empty'''
        return

    def do_quit(self, line):
        '''Quits the command interpreter\n'''
        return True

    def do_EOF(self, line):
        '''exit program on EOF command - Ctrl-D(linux), Ctrl-Z(Windows)'''
        print()
        return True

    def do_create(self, arg):
        '''
        Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id. Ex: $ create BaseModel
        '''
        if len(arg) == 0:
            print("** class name missing **")
            return
        try:
            args = shlex.split(arg)
            new_instance = eval(args[0])()
            for i in args[1:]:
                try:
                    key = i.split("=")[0]
                    value = i.split("=")[1]
                    if hasattr(new_instance, key):
                        value = value.replace("-", " ")
                        try:
                            value = eval(value)
                        except Exception:
                            pass
                        setattr(new_instance, key, value)
                except(ValueError, IndexError):
                    pass
            new_instance.save()
            print(new_instance.id)
        except Exception:
            print("** class doesn't exist **")
            return

    def do_show(self, line):
        '''
        Prints the string representation of an instance based on the
        class name and id. Ex: $ show BaseModel 1234-1234-1234
        '''
        args = shlex.split(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            obj_id = "{}.{}".format(args[0], args[1])
            if obj_id not in storage.all().keys():
                print("** no instance found **")
            else:
                print(storage.all()[obj_id])

    def do_destroy(self, line):
        '''
        Deletes an instance based on the class name and id.
        Save the change into the JSON file.
        Ex: $ destroy BaseModel 1234-1234-1234
        '''
        if len(line) == 0:
            print("** class name missing **")
            return
        args = shlex.split(line)
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            obj_id = "{}.{}".format(args[0], args[1])
            if obj_id not in storage.all().keys():
                print("** no instance found **")
            else:
                del storage.all()[obj_id]
                storage.save()

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)

    def do_update(self, line):
        '''
        Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        '''
        if len(line) == 0:
            print("** class name missing **")
            return
        args = shlex.split(line)
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            obj_id = "{}.{}".format(args[0], args[1])
            if obj_id not in storage.all().keys():
                print("** no instance found **")
            elif len(args) < 3:
                print("** attribute name missing **")
            elif len(args) < 4:
                print("** value missing **")
            else:
                obj_key = "{}.{}".format(args[0], args[1])
                pattern1 = r'^\d+$'
                pattern2 = re.compile(r'^[-+]?(\d+(\.\d*)?|\.\d+)\
                        ([eE][-+]?\d+)?$')
                if re.match(pattern1, args[3]):
                    args[3] = int(args[3])
                elif pattern2.match(args[3]):
                    args[3] = float(args[3])

                setattr(storage.all()[obj_key], args[2], args[3])
                storage.all()[obj_key].save()

    def default(self, line):
        '''retrieve all instances of a class using <class name>.all()'''
        match = re.search(r"all()", line)
        if match:
            for cls_name in self.classes:
                if line == "{}.all()".format(cls_name):
                    self.do_all(cls_name)
                    return

        '''retrieve # of instances of a class using <class name>.count()'''
        match = re.search(r"count()", line)
        if match:
            cls_name = line.split('.')[0]
            if cls_name in HBNBCommand.classes:
                obj_count = 0
                for key in storage.all().keys():
                    if cls_name in key:
                        obj_count += 1
                print("{}".format(obj_count))
                return

        line_list = line.split('.')
        cls_name = line_list[0]
        obj_id = line_list[1].split('(')[1].split(')')[0]
        '''retrieve an instance based on its ID: <class name>.show(<id>)'''
        if line == "{}.show({})".format(cls_name, obj_id):
            line = "{} {}".format(cls_name, obj_id)
            self.do_show(line)
            return
        '''destroy an instance based on his ID: <class name>.destroy(<id>)'''
        if line == "{}.destroy({})".format(cls_name, obj_id):
            line = "{} {}".format(cls_name, obj_id)
            self.do_destroy(line)
            return

        '''
        update an instance based on his ID:
        <class name>.update(<id>, <attribute name>, <attribute value>)
        eg. User.update("2993..", "first_name", "John")
        '''
        match = re.search(r".update()", line)
        if match:
            for i in range(len(line)):
                if line[i] == '(':
                    idx1 = i
                elif line[i] == ')':
                    idx2 = i
            arg_str = line[idx1+1:idx2]
            arg_list = arg_str.split(', ')
            obj_id = arg_list[0]
            '''check if attribute is in dict
            <class name>.update(<id>, <dictionary representation>)
            eg. User.update("38f22813-2753-4d42-b37c-57a17f1e4f88",\
                    {'first_name': "John", "age": 89})
            '''
            match1 = re.search(r"{", line)
            if not match1:
                attr_name = arg_list[1]
                attr_val = arg_list[2]
                line = "{} {} {} {}".format(cls_name, obj_id,
                                            attr_name, attr_val)
                self.do_update(line)
            else:
                for j in range(len(arg_str)):
                    if arg_str[j] == '{':
                        j1 = j
                    elif arg_str[j] == '}':
                        j2 = j
                attr = arg_str[j1:j2+1]
                attr_dict = eval(attr)
                for attr_name, attr_val in attr_dict.items():
                    line = "{} {} {} {}".format(cls_name, obj_id,
                                                attr_name, attr_val)
                    self.do_update(line)
            return


if __name__ == '__main__':
    HBNBCommand().cmdloop()
