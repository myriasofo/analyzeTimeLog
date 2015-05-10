# WHAT: Analyze how I spent my time
    # Two main functions:
    # 1. Print table of hrs spent - by day, by categ
    # 2. Print selected events - chosen by day/catg/keyword

# HOW: Takes in log, processes, then prints tables
    # Below is info on the formatting of the time log
    # Check 'timeLog_example.txt' for a concrete example
    # 1. Must start with 'month year', eg. 'May 2015'
    # 2. Must proceed with 'day number', eg. 'Tues 5'
    # 3. First event for each day must be when woke up
    # 4. For each event: 'time desc_categ', eg. '940 wakeup_fff'
        # Note that '940' is '9:40am' and it's the END time
        # Special abbrev: after '940' a '50' means '9:50am'
        # Also use military time, so '2140' means '9:40pm'
    # That's it!

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
        # Spend 5hr on tasks
        # Minimize time socializing
        # Do more higher priority tasks over low


# NOTE: Ugly right now, but works. Will refactor later
# TODO:
    # Refactor, turn this whole thing into a class (no more globals)
    # Could use fancier datetime functions, just for practice
        #from datetime import datetime
        # ESP. for "June" to "5"


def addData_toTable(dayData):
    # Use a dict, fill with placeholders for table later
    dct = {}
    for ch in ['t','b','f']:
        for i in (1,2,3):
            dct[ch*i] = 0
    dct['mis'] = 0
    dct['org'] = 0

    for event in dayData:
        categ = event[3]
        duration = event[4]
        if categ not in dct:
            dct[categ] = duration
        else:
            dct[categ] += duration
        desc = event[2]
        if 'orgz' in desc:
            dct['org'] += duration

    daySum = 0
    for key in dct:
        if key in table:
            table[key].append(dct[key])
        else:
            table[key] =[dct[key]]
        if key != 'org':
            daySum += dct[key]
    table['sum'].append(daySum)

def printTable(table):
    # Print day
    print 'day,',
    for i in table['day']:
        print '%04s'%i + ',',
    print
    print

    # Print each categ
    for ch in ['t','b','f']:
        for i in (1,2,3):
            categ = ch*i
            if categ != 'fff':
                print format(categ,'3') + ',',
                for i in table[categ]:
                    print "{:4.1f}".format(i) + ',',
                print
        print

    # Print extra categ
    for label in ['org','sum','mis']:
        print label + ',',
        for i in table[label]:
            print "{:4.1f}".format(i) + ',',
        print

    print


#### Grab raw data and put into form I want!
logDir = "C:/Users/Abe/Dropbox/CS/apps/analyzeLog/"
#logFile = "timeLog.txt"
logFile = "timeLog_quick.txt"
#logFile = "timeLog_example.txt"
f =  open(logDir + logFile,"r")
curr = 0.0
events = []
## Crazy main for-loop
for line in f:
    event = []
    line =line.strip()
    if line == 'log' or line == '':
        pass
    elif line[0] == '$':
        #strMonthYear = line[1:]
        strMonth =line[1:].split(' ')[0]
        #TODO: do this automatically, yo
        if strMonth == 'May':
            strMonth = '5'
        elif strMonth == 'June':
            strMonth = '6'
    elif line[0] == '#':
        # Grab just number of the day (ie. '5' instead of 'Tues')
        strDay = line[1:].split(' ')[1]
    else:
        # Split events into 3 parts => time, desc, categ
        # Use '_' as the delimiter. Change first space to '_'
        event.append('/'.join([strMonth,strDay]))
        event += line.replace(' ','_',1).split('_',2)
        if len(event) < 4:
            event.append('mis')

        # Get duration
        # Start with hours and mins
        time = event[1]
        if len(time) == 2:
            currMin = time
        elif len(time) == 3:
            currHour = time[0]
            currMin = time[1:]
        elif len(time) == 4:
            currHour = time[0:2]
            currMin = time[2:]
        past = curr
        curr = float(currHour) + float(currMin)/60
        duration = curr - past

        # Deal with times that cross over days
        if duration < 0:
            duration += 24
        event.append(duration)

        events.append(event)
f.close()
# Marks end (for making table later)
events.append(['end','','','',''])

#### Take data and tabulate by day & categ
## Make output table below
table = {}
table['day'] = []
table['sum'] = []
curr = ''
dayData =[]
#TODO: Could shorten this using a range, or a while loop?
    # Like maybe take out need for 'end' above
    # Maybe a dumb idea
for line in events:
    past = curr
    curr = line[0]
    if curr != past:
        if len(dayData) > 0:
            table['day'].append(past)
            addData_toTable(dayData)
            dayData =[]
    else:
        dayData.append(line)

printTable(table)

