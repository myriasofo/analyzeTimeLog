'''
WHAT: Analyze how I spend my time
    Two main uses:
    1. Print table of hrs spent on each category, each day
    2. Print selected events (can choose by day/categ/keyword)

HOW: Takes in log, processes it, then prints tables
    The log is plain-text, but in a special style (for ease of entry)
    Check 'timeLog_example.txt' for a concrete example
    1. First line should be 'log'
    2. Next line should be '$month year', eg. '$May 2015'
    3. Then '#dayNumber', eg. '#5'
    4. First event for each day must be waking up (makes sense)
    5. For each event: 'time desc_categ', eg. '940 wakeup_fff'
        Note that '940' is '9:40am' and it's the end time
        Special abbrev: after '940', a '50' means '9:50am'
        Also use military time, so '2140' means '9:40pm'

WHY: To work more on high priority tasks
    To see how I spend my time, just like how I spend money
    Each use of time is like a 'purchase'
    Just tracking makes me aware of how I spend
    1. What events are fixed (eg. sleep) vs discretionary (eg. fb)?
        Breaks are impt to avoid burnout - so they're inbetween
    2. How much value am I getting from each event?
        What events are great and I should do more of?
        What events are worthless and I should avoid?
    3. How long did I think it'd take? How long did it actually take?
    4. How much do I plan on working? How much do I actually work?
    Overall.
        Spend 1hr on exercising and meditation
        Spend 1hr on breaks
        Spend 5hr on great tasks (over lesser tasks)
        Control time socializing
'''

from datetime import datetime
from math import floor
import os

class TimeTracker:
    def __init__(self):
        self.events = []
        self.table = {}


    def extractData(self,logLocation):
        ''' 
        This fctn takes in log and returns desired parts
        1. Take in log, sep bw month/day/event
        2. If event, add line to self.events with 4 parts:
            date (ie. month/day)
            duration of event
            category
            text description
        '''

        # Instantiate vars in case missing month/day
        month = ''
        day = ''
        self.nDays = 0

        # Crazy main for-loop
        f = open(logLocation, "r")
        for line in f:
            line = line.strip()

            # Note: an equal '=' indicates a comment to ignore
            if line == '' or line[0] == '=' or line == 'log' or line == '(':
                pass

            # Line begin w '$' means month/year info
            elif line[0] == '$':
                month = str(datetime.strptime(line,'$ %b %Y').month)

            # Line begin w '#' means day info
            elif line[0] == '#':
                day = str(datetime.strptime(line,'# %a %d').day)
                self.nDays += 1

            # If not info on date, then info on event
            else:
                # Get month/day from prev lines
                date = month + '/' + day

                # Event has 3 parts: loggedTime, desc, categ
                # Use '_' as the delimiter.

                # If categ is missing, add 'mis' 
                if '_' not in line:
                    line += '_mis'

                # Change first space to delimiter
                line = line.replace(' ', '_', 1)

                # Get each part wanted
                loggedTime, desc, categ = line.split('_')
                dur = self.getDuration(loggedTime)

                # Finally, append line to events
                self.events.append([date, dur, categ, desc])
        f.close()

    def getDuration(self, loggedTime):
        ''' 
        This is a helper fctn for extractData()
        It takes a time entry (ie. loggedTime) and returns length of event
        'loggedTime' is in military time:
            so '930' is '9:30am'
            and '2130' is '9:30pm'
        Some entries are abbrev to 2 numbers - so use hr from prev line
            a '45' after '930' means '945am'
        To get duration, I subtract curr from prev
        Each is in the format of 'clock', ie. hrs from midnight
            so '930' is 9.5
            and '2130' is 21.5
        '''

        # Identify hr and mins:
        logChars = len(loggedTime)
        if logChars == 4:
            hr = loggedTime[0:2]
            mins = loggedTime[2:]
        elif logChars == 3:
            hr = loggedTime[0]
            mins = loggedTime[1:]
        elif logChars == 2:
            hr = floor(self.clock)
            mins = loggedTime

        # Note: 'clock' is hours since midnight
        if not hasattr(self,'clock'):
            self.clock = 0.0
        prev = self.clock
        self.clock = float(hr) + (float(mins) / 60)
        dur = self.clock - prev

        # For event that goes past midnight (eg. 2359 to 000)
        if dur < 0:
            dur += 24

        return dur

    def makeTable(self):
        '''
        This fctn takes in self.events and returns table of stats
        1. Make table of placeholders
        2. For each event, add dur to approp cell
        3. Determine cell by categ (row) and day (column)
        NOTE: categ is row bc need same number format for print later
        '''

        # Gather up all categs desired
        categList = []
        categList += ['day', 'tot', 'mis', 'org']
        categList += ['tsk', 'brk', 'fxd']
        for ch in ['t', 'b', 'f']:
            for i in (1, 2, 3):
                categList.append(ch * i)

        # Fill table with placeholder zeros for each categ
        for categ in categList:
            self.table[categ] = [0] * self.nDays

        # For each event, add its dur to approp cell
        col = -1
        date = ''
        for line in self.events:
            prev = date
            date = line[0]
            dur = line[1]
            categ = line[2]
            desc = line[3]

            # For first event of each day
            # Note: first should always be wakeup, so don't count
            if date != prev:
                col += 1
                self.table['day'][col] = date

            # Now get stats!
            else:
                self.table[categ][col] += dur
                self.table['tot'][col] += dur

                # Special categs
                if 'orgz' in desc:
                    self.table['org'][col] += dur

                # Not just hours, but also freq
                for i,j in [('t', 'tsk'), ('b', 'brk'), ('f', 'fxd')]:
                    if categ[0] == i:
                        self.table[j][col] += 1


    def printTable(self, recent=False, raw=False, day='', start='', end=''):
        '''
        Print table of stats (nicely)
        Options:
            'day' is for a single day
            'start' and 'end' are for a range
            'recent' is just the most recent (single) day
            'raw' takes out all labels, so just raw data
        '''

        # Pick out categs and their formatting to print
        sections = []
        if not raw:
            sections.append((['day'], '{:>6}'))
        sections.append((['t','tt','ttt'], '{:6.1f}'))
        sections.append((['b','bb','bbb'], '{:6.1f}'))
        sections.append((['f','ff'], '{:6.1f}'))
        sections.append((['tsk','brk','fxd'], '{:6}'))
        sections.append((['org','tot','mis'], '{:6.1f}'))
        #sections.append(([],''))


        # Set default days to print
        iStart = 0
        iEnd = self.nDays - 1

        # Option 'day', 'start', 'end' - Find arr pos of dates that match
        for i in range(self.nDays):
            if day == self.table['day'][i]:
                iStart = i
                iEnd = i
            if start == self.table['day'][i]:
                iStart = i
            if end == self.table['day'][i]:
                iEnd = i

        # Option 'recent' take highest precedent
        if recent:
            iStart = self.nDays - 1
            iEnd = iStart


        # Final forloop to print all
        for (categs,fmt) in sections:
            for categ in categs:
                line = ''
                if not raw:
                    line += '{:3}'.format(categ)
                for i in range(iStart, iEnd+1):
                    line += fmt.format(self.table[categ][i])
                print(line)
            print('')

    def printEvents(self, recent=False, day='', label='', include='', exclude=''):
        '''
        Prints selected lines in self.events
        Here are some options:
            'day' is month/day (same format as 'date')
            'label' is category (same format as 'categ')
            'include' and 'exclude' are str matches
            'recent' is only for most recent day (overrides 'day')
        '''
        if recent:
            day = self.events[-2][0]

        total = 0
        for event in self.events:
            date = event[0]
            dur = event[1]
            categ = event[2]
            desc = event[3]

            # Enact options below
            if 'end' == date:
                continue
            elif day and day != date:
                continue
            elif label and label != categ:
                continue
            elif include and include not in desc:
                continue
            elif exclude and exclude in desc:
                continue

            # Print day, dur, categ, desc
            line = ''
            line += "{:>5}".format(date) + ' '
            line += "{:4.1f}".format(dur) + ' '
            line += "{:3}".format(categ) + ' '
            line += desc
            print(line)

            total += dur

        print("TOTAL:", "{:3.1f}".format(total))

def main():
    # Setting up
    #logPath = os.path.expanduser('~/dev/analyzeLog/timeLog_example')
    logPath = os.path.expanduser('~/Dropbox/Tasks/_gitignore/timeLog.to')

    t = TimeTracker()
    t.extractData(logPath)
    t.makeTable()

    # Print out results
    t.printTable()
    #t.printTable(recent=1,raw=1)
    #t.printTable(recent=0,raw=1,day='7/8',start='',end='')

    #t.printEvents()
    #t.printEvents(label='f')
    #t.printEvents(label='b')
    #t.printEvents(label='bb')
    #t.printEvents(label='bbb')
    #t.printEvents(label='t')
    #t.printEvents(label='tt')

main()

