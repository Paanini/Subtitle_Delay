#!/usr/bin/python
import argparse
import os
import re
import datetime

filename = ''
delay=0
no_replace=False


def apply_delay(time,delay):
    hour = int(time[0])
    minute = int(time[1])
    sec = int(time[2])
    milli = int(time[3])
    micro = milli*1000
    
    #Use a dummy date of 1/1/1000 so we can get a time delta
    initial_time = datetime.datetime(1000,1,1,hour,minute,sec,micro)
    delayed_time = initial_time + datetime.timedelta(milliseconds = milli)

    hour = delayed_time.hour
    minute = delayed_time.minute
    second = delayed_time.second
    milli = delayed_time.microsecond/1000

    if sec < 10: sec = '0'+str(sec)
    if minute < 10: minute = '0'+str(minute)
    if hour < 10: hour = '0'+str(hour)

    time_new = str(hour)+":"+str(minute)+":"+str(sec)+","+str(milli)
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
    with open(filename,"r") as f:
        text = f.read()

    times = re.findall(r'\d\d:\d\d:\d\d,\d\d\d',text)
    for t in times:
        # Ghastly hack to split up the timestamp properly without using regex groups.
        # Can't remember why I didn't want to use them - probably made parsing difficult.
        time_new = apply_delay(t.replace(',',':').split(':'),delay)
        text = text.replace(t,time_new)

    with open(filename,"w") as f:
        f.write(text)
    

if __name__=="__main__":
    main()
