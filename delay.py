#!/usr/bin/python
import argparse
import os

filename = ''
delay=0
no_replace=False


def arg_parse():
    global filename, delay, no_replace
    cur_path = os.getcwd()

    # Parse the arguments from the command line
    parser = argparse.ArgumentParser(description="A handy script to introduce a (+/-) delay in a subtitle (SRT) file")
    parser.add_argument("filename", help="Enter the name of the Subtitle file to be used",type=str)
    parser.add_argument("delay", help="Enter the delay to be introduced in ms",type=int)
    parser.add_argument("--no-replace", help="Create a new Subtitle file instead of modifying the existing one", action="store_true")
    args = parser.parse_args()
    filename = args.filename
    no_replace = args.no_replace

    # Check if the arguments are valid
    if not (os.path.isfile(filename) or os.path.isfile(os.path.join(cur_path,filename))):
        print "Invalid filename: %s \nExiting." %(filename)
        exit(-1)


def main():
    global filename, delay, no_replace
    arg_parse()
    print "Arguments parsed successfully - filename = %s, delay = %d, --no-replace=%s" %(filename, delay, no_replace)

if __name__=="__main__":
    main()
