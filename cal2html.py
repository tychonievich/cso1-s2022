import re, markdown, dateutil, json
from datetime import timedelta, datetime
from sys import stderr

TEXTBOOKS = {
    'MCS': 'files/mcs.pdf',
    u'\u2200x': 'files/forallx.pdf'
}
ANCHORS = ["chapter.","section.","subsection."]

def yamlfile(f):
    from yaml import load
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader

    if type(f) is str:
        with open(f) as stream:
            data = load(stream, Loader=Loader)
    else:
        data = load(f, Loader=Loader)
    return data


def dow(n):
    """string to int, with datetime's default 0=monday weekday numbering"""
    if type(n) is int: return n
    n = n.lower()
    if n.startswith('mo') or n == 'm': return 0
    if n.startswith('tu') or n == 't': return 1
    if n.startswith('we') or n == 'w': return 2
    if n.startswith('th') or n == 'h': return 3
    if n.startswith('fr') or n == 'f': return 4
    if n.startswith('sa') or n == 's': return 5
    if n.startswith('su') or n == 'u': return 6
    raise Exception("Unknown weekday: "+str(n))


def raw2cal(data, links):
    """Given the data from a cal.yaml, return a list of weeks,
    where each week is a list of seven days,
    where each day is either None or {"date":datetime.date, "events":[...]}
    
    An event is a title, kind, and some kind of day info:
        - from, to
        - day = all-day
        - date = one copy per section
    
    Location and office hours removed for now
    Section data not placed in ics
    """
    s = data['Special Dates']['Courses begin']
    beg = s
    e = data['Special Dates']['Courses end']
    end = e
    while s.weekday() != 6: s -= timedelta(1)
    e = max(e, data['meta']['final']['start'].date())
    
    data['meta']['days'] = [dow(dows) for dows in data['meta']['days']]
    
    data['sidx'] = 0
    
    def onday(d):
        dt = datetime.fromordinal(d.toordinal())
        isexam = False
        ans = []
        
        # handle metadata
        if d == data['meta']['final']['start'].date():
            final = data['meta']['final']
            ans.append({
                "title":"Final Exam",
                "kind":"exam",
                "from":final['start'],
                "to":final['start'] + timedelta(0,60*final['duration']),
            })
        for k,v in data['Special Dates'].items():
            if (v['start'] > d or v['end'] < d) if type(v) is dict else d not in v if type(v) is list else v != d:
                continue # does not apply
            if 'recess' in k or 'Reading' in k or 'break' in k:
                ans.append({
                    "title":k,
                    "kind":"special",
                    "day":d
                })
                return ans # no classes
            if 'exam' in k.lower() or 'test' in k.lower() or 'midterm' in k.lower():
                isexam = True
            else:
                ans.append({
                    "title":k,
                    "kind":"special",
                    "day":d
                })
        if d >= beg and d <= end:
            if d.weekday() in data['meta']['days']:
                # handle main calendar
                if isexam:
                    ans.append({
                        'title':'Exam',
                        "kind":'exam',
                        "date":dt,
                    })
                elif len(data['lectures']) <= data['sidx']:
                    ans.append({
                        'title':'Lecture',
                        "kind":'lecture',
                        "date":dt,
                    })
                else:
                    ans.append({
                        'title':data['lectures'][data['sidx']] or '',
                        "kind":'lecture',
                        "date":dt,
                    })
                    for subtitle in (ans[-1]['title'] if type(ans[-1]['title']) is list else [ans[-1]['title']]):
                        if subtitle in data['reading']:
                            tmp = data['reading'][subtitle]
                            if type(tmp) is not list: tmp = [tmp]

                            for (i, reading) in enumerate(tmp):
                                if type(reading) == str:
                                    for name, link in TEXTBOOKS.items():
                                        if name in reading:
                                            sect = re.search(r'\d+(?:\.\d+)*', reading)
                                            if sect and '#' not in link:
                                                sect = sect.group(0)
                                                anchor = '#'+ANCHORS[sect.count('.')]+sect
                                                link += anchor
                                            tmp[i] = {'txt': reading, 'lnk': link}

                            if 'reading' in ans[-1]:
                                ans[-1]['reading'].extend(tmp)
                            else:
                                ans[-1]['reading'] = tmp[:]
                    data['sidx'] += 1
                
                # handle links files
                for section, notes in links.items():
                    if d in notes:
                        ans.append({
                            'title':section,
                            'kind':'notes',
                            'date':dt,
                        })
                        for f in notes[d].get('files',[]):
                            if type(f) is dict:
                                ans[-1].setdefault('reading',[]).append(f)
                            else:
                                n = os.path.basename(f)
                                n = n[n.find('-')+1:]
                                n = re.sub('^([0-9]*-)*', '', n)
                                ans[-1].setdefault('reading',[]).append({'txt':n,'lnk':f})
                        if 'video' in notes[d]: ans[-1]['video'] = notes[d]['video']
                        if 'audio' in notes[d]: ans[-1]['audio'] = notes[d]['audio']


        # handle assignments
        for task,ent in data['assignments'].items():
            if task[0] == '.': continue
            if 'due' not in ent: continue
            if ent['due'].date() != d: continue
            group = ent.get('group', re.match('^[A-Za-z]*',task).group(0))
            tmp = dict(data['assignments'].get('.groups',{}).get(group,{}))
            tmp.update(ent)
            ent = tmp
            ans.append({
                'title':ent.get('title', task),
                'kind':'assignment',
                'group':group,
                'from':ent['due']-timedelta(0,900),
                'to':ent['due'],
                'slug':task,
            })
            if 'hide' in ent: ans[-1]['hide'] = ent['hide']
            if 'link' in ent: ans[-1]['link'] = ent['link']
        
        return ans

    ans = []
    while s <= e:
        if s.weekday() == 6: ans.append([])
        events = onday(s)
        if len(events):
            ans[-1].append({'date':s,'events':events})
        else:
            ans[-1].append(None)
        s += timedelta(1)
    return ans

def cal2html(cal):
    """Uses divs only, with no week-level divs"""
    ans = ['<div id="schedule" class="calendar">']
    ldat = None
    for week in cal:
        newweek = True
        for day in week:
            if day is not None and not all(_.get('kind') == 'oh' for _ in day['events']):
                ldat = day['date']
                ans.append('<div class="day {}" date="{}">'.format(day['date'].strftime('%a') + (' newweek' if newweek else ''), day['date'].strftime('%Y-%m-%d')))
                newweek = False
                ans.append('<span class="date w{1}">{0}</span>'.format(day['date'].strftime('%d %b').strip('0'), day['date'].strftime('%w')))
                ans.append('<div class="events">')
                for e in day['events']:
                    if e.get('kind') == 'oh': continue
                    if e.get('hide'): continue
                    classes = [e[k] for k in ('section','kind','group') if k in e]
                    title = e.get('title','TBA')
                    if type(title) is list: title = ' <small>and</small> '.join(title)
                    more = []
                    if 'link' in e:
                        title = '<a target="_blank" href="{}">{}</a>'.format(e['link'], title)
                    for media in ('video', 'audio'):
                        if media in e:
                            more.append('<a target="_blank" href="{}">{}{}</a>'.format(
                                'player.html#'+e[media][e[media].rfind('/')+1:] if e[media].endswith('.webm') and e[media].startswith('lecture') else e[media],
                                media,
                                e[media][e[media].rfind('.',e[media].rfind('/')+1):] if e[media].rfind('.',e[media].rfind('/')+1) > 0 else ''
                            ))
                    for reading in e.get('reading',[]):
                        if type(reading) is str:
                            more.append(reading)
                        else:
                            more.append('<a target="_blank" href="{}">{}</a>'.format(reading['lnk'], reading['txt']))
                    if more:
                        ans.append('<details class="{}">'.format(' '.join(classes)))
                        ans.append('<summary>{}</summary>'.format(title))
                        ans.append(' <small>and</small> '.join(more))
                        ans.append('</details>')
                    else:
                        ans.append('<div class="{}">{}</div>'.format(' '.join(classes), title))
                ans.append('</div>')
                ans.append('</div>')
            elif day is None and ldat is not None:
                ldat += timedelta(1)
                ans.append('<div class="empty day {}" date="{}"></div>'.format(ldat.strftime('%a') + (' newweek' if newweek else ''), ldat.strftime('%Y-%m-%d')))
                newweek = False
    ans.append('</div>')
    external = '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"><path fill="#fff" stroke="#36c" d="M1.5 4.518h5.982V10.5H1.5z"/><path fill="#36c" d="M5.765 1H11v5.39L9.427 7.937l-1.31-1.31L5.393 9.35l-2.69-2.688 2.81-2.808L4.2 2.544z"/><path fill="#fff" d="M9.995 2.004l.022 4.885L8.2 5.07 5.32 7.95 4.09 6.723l2.882-2.88-1.85-1.852z"/></svg>'
    return re.sub(r'(<a[^>]*href="[^"]*//[^"]*"[^<]*)</a>', r'\1'+external+'</a>', '\n'.join(ans))


def cal2fullcal(cal, keep=lambda x:True):
    """see https://fullcalendar.io/docs/event-object"""
    ans = []
    for week in cal:
        for day in week:
            if day is not None:
                for event in day['events']:
                    if event.get('hide'): continue
                    if keep(event):
                        ans.append({
                            'id':'evt'+str(len(ans)),
                            'start':event['from'].strftime('%Y-%m-%dT%H:%M:%S'),
                            'end':event['to'].strftime('%Y-%m-%dT%H:%M:%S'),
                            'title':event['title'],
                            'classNames':['cal-'+event['kind']],
                            'editable':False,
                            # 'location':event['where'],
                        })
                        if 'link' in event: ans[-1]['url'] = event['link']
    ans.sort(key=lambda x:x['start'])
    return ans

def cal2ical(cal, course, home, tz=None, sections=None):
    if tz is None: tz = 'America/New_York'
    now = datetime.utcnow().strftime('%Y%m%dT%H%M%S')
    
    ans = ['''BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//University of Virginia//{0}//EN
CALSCALE:GREGORIAN
NAME:{0}'''.format(course)]
    def icescape(s):
        s = s.replace('"', '').replace(':', '')
        s = s.replace('\\', '\\\\')
        s = s.replace('\n', '\\n')
        s = s.replace(r',', r'\,')
        s = s.replace(r',', r'\;')
        return s
    def fixlinks(l):
        for i in range(len(l)):
            l[i] = l[i].replace('<//','<https://')
            l[i] = re.sub(r'<([^><:]*)>', r'<{}\1>'.format(home.replace('\\','\\\\')), l[i])
    def encode(event):
        details = []
        if 'link' in event: details.append('see <' + event.get('link')+'>')
        if 'details' in event: details.append(event.get('details'))
        if 'reading' in event:
            for r in event['reading']:
                if type(r) is str: details.append(r)
                else: details.append('{txt} <{lnk}>'.format(**r))
        for media in ('video', 'audio'):
            if media in event:
                details.append('{}: <{}>'.format(media, event[media]))
        title = event.get('title','TBA')
        if type(title) is list: title = ' and '.join(title)
        if 'group' in event and event['group'] not in title:
            title = event['group']+' '+title
        if 'day' in event:
            dts = [':{}'.format(event['day'].strftime('%Y%m%d'))]
            dte = [':{}'.format((event['day'] + timedelta(1)).strftime('%Y%m%d'))]
        elif 'from' in event and 'to' in event:
            dts = [';TZID={}:{}'.format(tz, event['from'].strftime('%Y%m%dT%H%M%S'))]
            dte = [';TZID={}:{}'.format(tz, event['to'].strftime('%Y%m%dT%H%M%S'))]
        elif 'date' in event:
            dts = [';TZID={}:{}'.format(tz, (event['date']+timedelta(0,sec['start'])).strftime('%Y%m%dT%H%M%S')) for sec in sections.values()]
            dte = [';TZID={}:{}'.format(tz, (event['date']+timedelta(0,sec['start']+sec['duration']*60)).strftime('%Y%m%dT%H%M%S')) for sec in sections.values()]
            title = [sec+' -- ' + title for sec in sections.keys()]
        else:
            raise Exception("Event without time: "+str(event))
        if type(title) is not list: title = [title]
        fixlinks(details)
        return ''.join('''BEGIN:VEVENT
SUMMARY:{title}
DESCRIPTION:{notes}{location}
DTSTART{dts}
DTEND{dte}
DTSTAMP:{now}Z
UID:{uid}@{course}.cs.virginia.edu
END:VEVENT'''.format(
            title=title[i], dts=dts[i], dte=dte[i], course=course, now=now,
            notes=icescape('\n'.join(details)),
            location='' if 'where' not in event else '\nLOCATION:{}'.format(event['where']),
            uid='{}-{}'.format(dts[i],title[i]),
        ) for i in range(len(dts)))
    for week in cal:
        for day in week:
            if day:
                for event in day['events']:
                    if event.get('hide'): continue
                    if 'section' in event and sections and event['section'] not in sections: continue
                    ans.append(encode(event))
    ans.append('END:VCALENDAR\r\n')
    return '\r\n'.join(_.replace('\n','\r\n') for _ in ans)

def slug2asgn(slug, group, raw):
    ans = {}
    ans.update(raw['assignments'].get('.groups').get(group,{}))
    ans.update(raw['assignments'][slug])
    return ans
    

def cal2assigments(cal,raw):
    ans = {}
    for week in cal:
        for day in week:
            if day is not None:
                for event in day['events']:
                    if event.get('kind') == 'assignment':
                        s = event['slug']
                        g = event['group']
                        dat = slug2asgn(s,g,raw)
                        dat['group'] = g
                        ans[s] = dict(**dat)
    return ans

def coursegrade_json(data):
    groups = data['assignments'].get('.groups', {})
    weights, drops, inc, exc, excuse = {}, {}, {}, {}, {}
    for k,v in groups.items():
        if 'portion' in v:
            weights[k] = v['portion']
        else:
            weights[k] = 0
        if type(weights[k]) is str:
            try:
                weights[k] = eval(weights[k].replace('%','/100'))
            except: pass
        if 'drop' in v:
            drops[k] = v['drop']
        if 'include' in v:
            inc[k] = v['include']
        if 'exclude' in v:
            exc[k] = v['exclude']
        if 'excuse' in v:
            excuse[k] = v['excuse']
    for k,v in drops.items():
        if type(v) is str:
            v = eval(v.replace('%','/100'))
        if v < 1:
            cnt = 0
            for k,v in assignments_json(data).items():
                if v.get('group','') == k: cnt += 1
            v *= cnt
        drops[k] = int(round(v))
    return {'letters':[
        # {'A+':0.98},
        {'A' :0.93},
        {'A-':0.90},
        {'B+':0.86},
        {'B' :0.83},
        {'B-':0.80},
        {'C+':0.76},
        {'C' :0.73},
        {'C-':0.70},
        {'D+':0.66},
        {'D' :0.63},
        {'D-':0.60},
        {'F' :0.00},
    ],'weights':weights,'drops':drops,'includes':inc,'excludes':exc, 'excuse':excuse}


if __name__ == '__main__':
    import os, os.path, glob
    here = os.path.realpath(os.path.dirname(__file__))
    os.chdir(here)
    course = os.path.basename(here)


    import json, sys, yaml
    raw = yamlfile('cal.yaml')
    links = {fn[:-11]:yamlfile(fn) for fn in glob.glob('*links.yaml')}
    cal = raw2cal(raw, links)
    with open('schedule.html', 'w') as fh:
        fh.write(cal2html(cal))

    with open('markdown/cal.ics', 'w') as fh:
        fh.write(cal2ical(cal, course, raw['meta']['home'], tz=raw['meta']['timezone'], sections=raw['sections']))

    import pjson

    with open('assignments.json', 'w') as fh:
        print(pjson.prettyjson(cal2assigments(cal, raw)), file=fh)

    with open('coursegrade.json', 'w') as f:
        f.write(pjson.prettyjson(coursegrade_json(raw), maxinline=16))
