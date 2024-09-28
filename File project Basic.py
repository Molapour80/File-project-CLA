import argparse
import json
import sys
import datetime
import os



##############################################Define command-line arguments##################################
def setup():
    parser = argparse.ArgumentParser(description="weather forecast CLI")
    parser.add_argument("--list",type=str, help="Show the all file")
    parser.add_argument("--cd", type=str, help=" Change the working directory")
    parser.add_argument("--mkdir", help="Create a new directory")
    parser.add_argument("--rmdir", help="Remove the directory")
    parser.add_argument("--rm", help="Remove the file")
    parser.add_argument("--rm-r", help="Remove the directory")
    parser.add_argument("--cp",nargs=2, help=" Copy a file or directory")
    parser.add_argument("--mv",nargs=2, help="Move a file or directory from")
    parser.add_argument("--find",nargs=2, help="Search forfiles or directories ")
    parser.add_argument("--cat",type=str, help="Outputthe contents ofthe file")
    parser.add_argument("--show-logs",action="store_true", help="show all logs of the program")

    return parser

####################command to log file####################
def log(cmd):
    with open("commands.log", "a") as file:
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = f"{cmd}: {time_now}\n"
        file.write(text)

#################List the directory#######################

def ls(path="."):
    try:
        files = os.listdir(path)
        for f in files:
            print(f)
    except FileNotFoundError:
        print(f"Directory '{path}' not found.")

##################Change the directory####################

def ch_directory(path):
    try:
        os.chdir(path)
        print(f"Changed directory to {path}")
    except FileNotFoundError:
        print(f"Directory '{path}' not found.")
    except NotADirectoryError:
        print(f"'{path}' is not a directory.")
################## Create a new directory#################
def mk_directory(path):
    try:
        os.mkdir(path)
        print(f"Created directory '{path}'")
    except FileExistsError:
        print(f"Directory '{path}' already exists.")
    except Exception as e:
        print(f"Error creating directory: {e}")


###################Remove a  directory#####################

def re_directory(path):
    try:
        os.rmdir(path)
        print(f"Removed directory '{path}'")
    except FileNotFoundError:
        print(f"Directory '{path}' not found.")
    except OSError:
        print(f"Directory '{path}' is not empty or cannot be removed.")


###################Remove a file###########################

def re_file(file):
    try:
        os.remove(file)
        print(f"Removed file '{file}'")
    except FileNotFoundError:
        print(f"File '{file}' not found.")

#########################Remove a directory ####################################
def remove_directory_recursively(directory):
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isdir(file_path):
                remove_directory_recursively(file_path)
            else:
                os.remove(file_path)
        os.rmdir(directory)
        print(f"Removed directory '{directory}' and its contents")
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
########################### Copy a file or directory#####################3
def copy(source, destination):
    try:
        if os.path.isdir(source):
            os.mkdir(destination)
            for item in os.listdir(source):
                s = os.path.join(source, item)
                d = os.path.join(destination, item)
                copy(s, d)  
        else:
            with open(source, 'rb') as fsrc:
                with open(destination, 'wb') as fdst:
                    fdst.write(fsrc.read())
        print(f"Copied '{source}' to '{destination}'")
    except Exception as e:
        print(f"Error copying: {e}")

#################################Move a file or directory####################

def move(source, destination):
    try:
        copy(source, destination)
        re_file(source)
        print(f"Moved '{source}' to '{destination}'")
    except Exception as e:
        print(f"Error moving: {e}")
#####################################Search for files or directories matching a pattern###############################
def find(path, pattern):
    matches = []
    for rot, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(pattern):  
                matches.append(os.path.join(rot, name))
    if matches:
        print("Found files:")
        for match in matches:
            print(match)
    else:
        print(f"No files matching '{pattern}' found in '{path}'.")
###################################Display the contents of a file##################################
def display_file_contents(file):
    try:
        with open(file, "r") as f:
            contents = f.read()
            print(contents)
    except FileNotFoundError:
        print(f"File '{file}' not found.")
###################################Display the log of commands##################################

def show_log(file_name="commands.log"):
    try:
        with open(file_name, "r") as file:
            data = file.read()
        print(data)
    except FileNotFoundError:
        print("Log file not found.")

parser = setup()
args = parser.parse_args()

cmd = " ".join(sys.argv)
log(cmd)

if args.show_logs:
    show_log()
elif args.list:
    ls(args.list)
elif args.cd:
    ch_directory(args.cd)
elif args.mkdir:
    mk_directory(args.mkdir)
elif args.rmdir:
    re_directory(args.rmdir)
elif args.rm:
    re_file(args.rm)
elif args.rm_r:
    remove_directory_recursively(args.rm_r)
elif args.cp:
    copy(args.cp[0], args.cp[1])
elif args.mv:
    move(args.mv[0], args.mv[1])
elif args.find:
    find(args.find[0], args.find[1])
elif args.cat:
    display_file_contents(args.cat)
else:
    print("No valid command provided.")
