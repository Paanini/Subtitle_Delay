#!/usr/bin/python
import argparse
import os
import re

filename = ''
delay=0
no_replace=False


def apply_delay(time,delay):
    hour = int(time[0])
    minute = int(time[1])
    second = int(time[2])
    mili = int(time[3])
    if (mili + delay) < 0:
        mili = mili + delay + 1000
        second-=1
        #Subtract minute
    if (mili + delay) > 1000:
        #Add minute
        mili = mili + delay - 1000
        second += 1
    time_new = str(hour)+":"+str(minute)+":"+str(second)+","+str(mili)
    return time_new


def arg_parse():
    global filename, delay, no_replace
    cur_path = os.getcwd()
    help_string = "A handy script to introduce a (+/-) delay in a subtitle (SRT) file\n(Since VLC does a shoddy job of adding delays)"

    # Parse the arguments from the command line
    parser = argparse.ArgumentParser(description=help_string)
    parser.add_argument("filename", help="Enter the name of the Subtitle file to be used",type=str)
    parser.add_argument("delay", help="Enter the delay to be introduced in ms",type=int)
    parser.add_argument("--no-replace", help="Create a new Subtitle file instead of modifying the existing one", action="store_true")
    args = parser.parse_args()
    filename = args.filename
    no_replace = args.no_replace
    delay = args.delay

    # Check if the subtitle_file is valid
    if not (os.path.isfile(filename) or os.path.isfile(os.path.join(cur_path,filename))):
        print "Invalid filename: %s \nExiting." %(filename)
        exit(-1)


def main():
    global filename, delay, no_replace
    arg_parse()
    print "Arguments parsed successfully - filename = %s, delay = %d, --no-replace=%s" %(filename, delay, no_replace)
    with open(filename,"r") as f:
        text = f.read()

    times = re.findall(r'\d\d:\d\d:\d\d,\d\d\d',text)
    for t in times:
        time_new = apply_delay(t.replace(',',':').split(':'),delay)
        text = text.replace(t,time_new)

    with open(filename,"w") as f:
        f.write(text)
    


if __name__=="__main__":
    main()
