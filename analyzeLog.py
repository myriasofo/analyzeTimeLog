# WHAT: Analyze how I spent my time
    # Two main functions:
    # 1. Print table of hrs spent - by day, by categ
    # 2. Print selected events - chosen by day/categ/keyword

# HOW: Takes in log, processes it, then prints tables
    # Below is info on the formatting of the time log
    # Check 'timeLog_example.txt' for a concrete example
    # 1. Must start with 'month year', eg. 'May 2015'
    # 2. Must proceed with 'day number', eg. 'Tues 5'
    # 3. First event for each day must be when woke up
    # 4. For each event: 'time desc_categ', eg. '940 wakeup_fff'
        # Note that '940' is '9:40am' and it's the END time
        # Special abbrev: after '940' a '50' means '9:50am'
        # Also use military time, so '2140' means '9:40pm'

# WHY: To work more on high priority tasks
    # To see how I spend my time, just like how I spend money
    # Each use of time is like a 'purchase'
    # Just tracking makes me aware of how I spend
    # 1. What events are fixed (eg. sleep) vs discretionary (eg. fb)?
        # Breaks are impt to avoid burnout - so they're inbetween
    # 2. How much value am I getting from each event?
        # What events are great and I should do more of?
        # What events are worthless and I should avoid?
    # 3. How long did I think it'd take? How long did it actually take?
    # 4. How much do I plan on working? How much do I actually work?
    # Overall.
        # Spend 1hr on exercising and meditation
        # Spend 1hr on breaks
        # Spend 5hr on great tasks (over lesser tasks)
        # Minimize time socializing

from datetime import datetime

class TimeTracker:
    def __init__(self):
        self.events = []
        self.table = {}


    def extractData(self,logLocation):
        ''' 
        1. Take in log, sep bw month/day/event
        2. If event, append to 'events' (with month/day, desc, categ, duration)
        '''

        # Instantiate vars for getDuration()
        hr = 0.0
        clock = 0.0

        # Crazy main for-loop
        f =  open(logLocation,"r")
        for line in f:
            line =line.strip()
            if line == 'log' or line == '':
                pass

            # Line is month/year info
            elif line[0] == '$':
                month = str(datetime.strptime(line,'$%b %Y').month)

            # Line is day info
            elif line[0] == '#':
                day = line[1:]

            # If line not month or day, means event
            else:
                # Get month/day from prev lines
                date = month + '/' + day

                # Event has 3 parts: timer, desc, categ
                # Use '_' as the delimiter.
                # Note: Manually change first space to delimiter
                line = line.replace(' ','_',1)
                line = line.split('_')

                # If categ is missing, add 'mis' 
                if len(line) < 3:
                    line.append('mis')

                # Grab each part
                timer = line[0]
                desc = line[1]
                categ = line[2]

                # Get duration. Tricky encapsulation bc relies on prev time
                duration, hr, clock = self.getDuration(timer, hr, clock)

                # Finally, append line to events
                self.events.append([date,duration,categ,desc])
        f.close()
        # Marks end (for makeTable later)
        self.events.append(['end',0,'na','na'])

    def getDuration(self, timer, prevHr, prevClock):
        ''' 
        'timer' is first # of each event. It's an abbrev:
            so '930' is '9:30am'
            and '2130' is '9:30pm'
            also '50' after '930' means '9:50am'
        For '50', need hr from prev line
        '''

        # Identify hr and mins:
        if len(timer) == 2:
            hr = prevHr
            mins = timer
        elif len(timer) == 3:
            hr = timer[0]
            mins = timer[1:]
        elif len(timer) == 4:
            hr = timer[0:2]
            mins = timer[2:]

        clock = float(hr) + float(mins)/60
        duration = clock - prevClock

        # For event that goes past midnight (eg. 2359 to 000)
        if duration < 0:
            duration += 24

        return (duration, hr, clock)


    def makeTable(self):
        '''
        1. Takes self.events, gathers all lines for a day
        2. Run stats on that day
        3. Appends those stats to self.table
        '''

        curr = ''
        dayData =[]
        for line in self.events:
            past = curr
            curr = line[0]
            if curr == past:
                dayData.append(line)
            elif dayData:
                # Now add to table
                dayStats = self.forDay_getStats(dayData)
                for key in dayStats:
                    if key in self.table:
                        self.table[key].append(dayStats[key])
                    else:
                        self.table[key] = [dayStats[key]]
                dayData = []

    def forDay_getStats(self,dayData):
        ''' Simply: Sum hrs for each categ '''

        # Fill with placeholder categs (in case, to fill out table)
        dayStats = {}
        for ch in ['t','b','f']:
            for i in (1,2,3):
                dayStats[ch*i] = 0
        dayStats['day'] = dayData[0][0]
        dayStats['mis'] = 0
        dayStats['org'] = 0
        dayStats['tot'] = 0

        # Stats: Time spent in each categ
        for event in dayData:
            duration = event[1]
            categ = event[2]
            desc = event[3]

            dayStats[categ] += duration
            dayStats['tot'] += duration

            # Special categ if event matches substr 'orgz'
            if 'orgz' in desc:
                dayStats['org'] += duration

        return dayStats


    def printTable(self):
        ''' Simply: Print data in table (nicely) '''

        # Print month/day
        print 'day',
        for i in self.table['day']:
            print "{:>5}".format(i),
        print
        print

        # Print each categ
        for ch in ['t','b','f']:
            for i in (1,2,3):
                categ = ch*i
                if categ != 'fff':
                    print format(categ,'3'),
                    for i in self.table[categ]:
                        print "{:5.1f}".format(i),
                    print
            print

        # Print extra categs
        for categ in ['org','tot','mis']:
            print categ,
            for i in self.table[categ]:
                print "{:5.1f}".format(i),
            print

        print

    def printEvents(self, day='', label='', include='', exclude=''):
        '''
        Prints lines in self.events
        Here are some options:
            'day' is month/day (same format as 'date')
            'label' is category (same format as 'categ')
            'include' and 'exclude' are any str to match
        '''
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
            print "{:>5}".format(date),
            print "{:4.1f}".format(dur),
            print "{:3}".format(categ),
            print desc
            total += dur

        print "TOTAL:","{:3.1f}".format(total)

def main():
    logDir = "C:/Users/Abe/Dropbox/CS/apps/analyzeLog/"
    logFile = "timeLog.txt"
    t = TimeTracker()
    t.extractData(logDir + logFile)
    t.makeTable()
    t.printTable()

    #t.printEvents()
    #t.printEvents(day='',label='',include='',exclude='')
    t.printEvents(day='5/9',label='t',include='',exclude='')

    #t.printEvents(day='5/9',label='tt')
    #t.printEvents(day='5/9',label='tt',exclude='analyzeLog')
    #t.printEvents(include='orgz')

main()

