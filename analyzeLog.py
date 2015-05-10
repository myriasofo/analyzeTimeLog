# WHAT: Analyze how I spent my time
    # Two main functions:
    # 1. Print table of hrs spent - by day, by categ
    # 2. Print selected events - chosen by day/catg/keyword

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

# TODO:
    # Need a bit more cleaning up - esp. 'crazy main loop'
        # getDuration as its own fctn
        # find way to convert 'June' to '6'
    # Could use fancier datetime functions, just for practice
        #from datetime import datetime
        # ESP. for "June" to "5"

from datetime import datetime

class TimeTracker:
    def __init__(self):
        self.events = []
        self.table = {}


    def extractData(self,logLocation):
        hr = 0.0
        clock = 0.0

        ## Crazy main for-loop
        f =  open(logLocation,"r")
        for line in f:
            event = []
            line =line.strip()
            if line == 'log' or line == '':
                pass

            elif line[0] == '$':
                month = str(datetime.strptime(line,'$%b %Y').month)

            elif line[0] == '#':
                day = line[1:]

            else:
                event.append(month + '/' + day)

                # For events, use '_' as the delimiter. Change first space to '_'
                # Split events into 3 parts => time, desc, categ
                event += line.replace(' ','_',1).split('_',2)
                if len(event) < 4:
                    event.append('mis')

                duration, hr, clock = self.getDuration(event[1],hr,clock)
                event.append(duration)

                self.events.append(event)
        f.close()
        # Marks end (for makeTable later)
        self.events.append(['end','na','na','na',0])

    def getDuration(self, logged, prevHr, prevClock):
        # Identify hr and mins:
        # eg. '930' is '9:30am' and '2130' is '9:30pm'
        # while '50' after '930' means '9:50am'
        if len(logged) == 2:
            hr = prevHr
            mins = logged
        elif len(logged) == 3:
            hr = logged[0]
            mins = logged[1:]
        elif len(logged) == 4:
            hr = logged[0:2]
            mins = logged[2:]

        clock = float(hr) + float(mins)/60
        duration = clock - prevClock

        # For event that goes past midnight (eg. 2359 to 000)
        if duration < 0:
            duration += 24

        return (duration, hr, clock)


    def makeTable(self):
        #### Take data and tabulate by day & categ
        ## Make output table below

        self.table['day'] = []
        curr = ''
        daysData =[]
        for line in self.events:
            past = curr
            curr = line[0]
            if curr == past:
                daysData.append(line)
            elif daysData:
                self.table['day'].append(past)
                self.forTable_addData(daysData)
                daysData =[]

    def forTable_addData(self,daysData):
        ''' Grab stats for each day, then add to table '''

        # Fill with placeholder categs (in case, to fill out table)
        dct = {}
        for ch in ['t','b','f']:
            for i in (1,2,3):
                dct[ch*i] = 0
        dct['mis'] = 0
        dct['org'] = 0
        dct['sum'] = 0

        # Stats: Time spent in each categ
        # That is, for each event, add its dur to its categ
        # Note: Each event has only one categ => mutually exclusive
        for event in daysData:
            desc = event[2]
            categ = event[3]
            duration = event[4]

            dct[categ] += duration
            dct['sum'] += duration

            # Special categ if event matches substr 'orgz'
            # So *not* mutually excl with above
            if 'orgz' in desc:
                dct['org'] += duration

        # Now add to table
        for key in dct:
            if key in self.table:
                self.table[key].append(dct[key])
            else:
                self.table[key] = [dct[key]]


    def printTable(self):
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
        for categ in ['org','sum','mis']:
            print categ,
            for i in self.table[categ]:
                print "{:5.1f}".format(i),
            print

        print

    def printEvents(self, categ='',day='',include='',exclude=''):
        # Note: Dislike name 'day0' but best bad
        viewSum = 0
        for event in self.events:
            day0 = event[0]
            desc0 = event[2]
            categ0 = event[3]
            dur0 = event[4]

            # Enact options below
            if 'end' == day0:
                continue
            elif day and day != day0:
                continue
            elif categ and categ != categ0:
                continue
            elif include and include not in desc0:
                continue
            elif exclude and exclude in desc0:
                continue

            # Print day, dur, categ, desc
            print "{:>5}".format(day0),
            print "{:4.1f}".format(dur0),
            print "{:3}".format(categ0),
            print desc0
            viewSum += dur0

        print "SUM:","{:4.1f}".format(viewSum)

def main():
    logDir = "C:/Users/Abe/Dropbox/CS/apps/analyzeLog/"
    logFile = "timeLog.txt"
    t = TimeTracker()
    t.extractData(logDir + logFile)
    t.makeTable()
    t.printTable()

    t.printEvents()
    #t.printEvents(day='5/9',categ='tt')
    #t.printEvents(day='5/9',categ='tt',exclude='analyzeLog')
    #t.printEvents(include='orgz')

main()

