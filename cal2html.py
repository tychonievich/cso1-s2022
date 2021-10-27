import re, markdown, dateutil, json
from datetime import timedelta, datetime
from sys import stderr


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

# external link icon
external = '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"><path fill="#fff" stroke="#36c" d="M1.5 4.518h5.982V10.5H1.5z"/><path fill="#36c" d="M5.765 1H11v5.39L9.427 7.937l-1.31-1.31L5.393 9.35l-2.69-2.688 2.81-2.808L4.2 2.544z"/><path fill="#fff" d="M9.995 2.004l.022 4.885L8.2 5.07 5.32 7.95 4.09 6.723l2.882-2.88-1.85-1.852z"/></svg>'

def parseReading(data,topic):
    """Given "git" or ["git","hex editor"] and parsed cal.yaml,
    returns list of (text,locallink,abslink) triples"""
    def localfix(text,link):
        if '://' in link:
            return (text,link,link)
        else:
            if link[0] == '/': return (text, link, data['meta']['home'][:data['meta']['home'].find('/',9)+1].rstrip('/')+'/'+link)
            else: return (text, link, data['meta']['home'].rstrip('/')+'/'+link)
    
    if type(topic) is str: topic = [topic]
    ans = []
    for t in topic:
        if type(t) is list: ans.extend(parseReading(data, t))
        elif t in data['reading']:
            rs = data['reading'][t]
            if type(rs) is not list: rs = [rs]
            for r in rs:
                if type(r) is str: ans.append(localfix(t,r))
                else: ans.append(localfix(
                    r.get('txt',r.get('text', t)),
                    r.get('lnk',r.get('link'))
                ))
        elif t in data['assignments']:
            group = t
            while len(group) and group not in data['assignments'].get('.groups'):
                group = group[:-1]
            adat = data['assignments'][t]
            gdat = data['assignments'].get('.groups').get(group,{})
            name = adat.get('title',t)
            link = adat.get('link',gdat.get('link',None))
            if link is None: ans.append((name,None,None))
            else: ans.append(localfix(name,link))
        else:
            ans.append((t,None,None))
    return ans

def parseLinks(entry,name=None):
    if type(entry) is str: return [(entry if name is None else name,entry,entry)]
    if type(entry) is dict:
        lnk = entry.get('lnk',entry.get('link',None))
        if lnk: return [(entry.get('txt',entry.get('text',lnk if name is None else name)), lnk, lnk)]
        ans = []
        if 'video' in entry: ans.extend(parseLinks(entry['video'],'video'))
        if 'audio' in entry: ans.extend(parseLinks(entry['audio'],'audio'))
        ans.extend(parseLinks(entry.get('files',[])))
        return ans
    if type(entry) is list:
        ans = []
        for e in entry:
            ans.extend(parseLinks(e))
        return ans
    return []

def icescape(s):
    s = s.replace('"', '').replace(':', '')
    s = s.replace('\\', '\\\\')
    s = s.replace('\n', '\\n')
    s = s.replace(r',', r'\,')
    s = s.replace(r',', r'\;')
    return s

class CourseSchedule:
    def __init__(self, data, **kargs):
        """CourseSechedule(yamlfile('cal.yaml'), Sec1=yamlfile('sec1-links.yaml'), ...)"""
        self.raw = data
        self.name = data['meta']['name']
        d = data['Special Dates']
        self.start = d['Courses begin']
        while self.start.weekday() != 6: self.start -= timedelta(1)
        self.stop = max(_.date() for _ in d['Final exams'].values())
        self.final = d['Final exams']
        while self.stop.weekday() != 5: self.stop += timedelta(1)
        end = d['Courses end']
        self.extra = {}
        self.breaks = {}
        for key in d:
            if 'break' in key.lower() or 'recess' in key.lower():
                b = d[key]
                if type(b) is dict:
                    d1 = b['start']
                    while d1 <= b['end']:
                        self.breaks[d1] = key
                        d1 += timedelta(1)
                else:
                    self.breaks[b] = key
            elif 'deadline' in key.lower():
                self.extra[d[key]] = key
            elif key in ('Courses begin', 'Courses end', 'Final exams'):
                continue
            else:
                print('WARNING: ignoring',key)
        lect = data['meta']['lecture']
        lect['w'] = [dow(_) for _ in lect['days']]
        lab = data['meta'].get('lab',{})
        lab['w'] = [dow(_) for _ in lab.get('days',[])] # note: requires all labs on same weekday
        self.lects = {}
        self.labs = {}
        b = self.start
        while b <= end:
            if b in self.breaks: 
                b += timedelta(1)
                continue
            if b.weekday() in lect['w']:
                idx = len(self.lects)
                if idx < len(data['lectures']): topic = data['lectures'][idx]
                else: topic = 'TBA'
                if type(topic) is not list: topic = [topic]
                self.lects[b] = {None: parseReading(data,topic),False:topic}
                for k,v in kargs.items():
                    if b in v:
                        self.lects[b][k] = parseLinks(v[b])
            if b.weekday() in lab['w']:
                idx = len(self.labs)
                if idx < len(data['labs']): topic = data['labs'][idx]
                else: topic = 'TBA'
                if type(topic) is not list: topic = [topic]
                self.labs[b] = {None: parseReading(data,topic),False:topic}
            b += timedelta(1)
    def toHTML(self):
        ans = []
        ans.append('<div id="schedule">')
        d = self.start
        while d <= self.stop:
            empty = True
            if d in self.extra:
                if empty:
                    ans.append('<div class="day {0:%a}" date="{0:%Y-%m-%d}"><span class="date w{0:%w}">{0:%d %b}</span><div class="events">'.format(d))
                    empty = False
                ans.append('<div class="special">{}</div>'.format(self.extras[d]))
            if d in self.lects:
                if empty:
                    ans.append('<div class="day {0:%a}" date="{0:%Y-%m-%d}"><span class="date w{0:%w}">{0:%d %b}</span><div class="events">'.format(d))
                    empty = False
                # shared
                e = self.lects[d]
                if not any(_[1] for _ in e[None]):
                    ans.append('<div class="lecture">{}</div>'.format(' <small>and</small> '.join(e[False])))
                else:
                    ans.append('<details class="lecture"><summary>{}</summary>{}</details>'.format(
                        ' <small>and</small> '.join(e[False]),
                        ' <small>and</small> '.join((_[0] if not _[1] else '<a href="{1}">{0}</a>'.format(*_)) for _ in e[None]),
                    ))
                # sections
                for k,v in e.items():
                    if type(k) is str:
                        ans.append('<details class="lecture"><summary>{}</summary>{}</details>'.format(
                            k,
                            ' <small>and</small> '.join('<a href="{1}">{0}</a>'.format(*_) for _ in v),
                        ))
            if d in self.labs:
                if empty:
                    ans.append('<div class="day {0:%a}" date="{0:%Y-%m-%d}"><span class="date w{0:%w}">{0:%d %b}</span><div class="events">'.format(d))
                    empty = False
                e = self.labs[d]
                if not any(_[1] for _ in e[None]):
                    ans.append('<div class="lab">{}</div>'.format(' <small>and</small> '.join(e[False])))
                else:
                    ans.append('<details class="lab"><summary>{}</summary>{}</details>'.format(
                        ' <small>and</small> '.join(e[False]),
                        ' <small>and</small> '.join((_[0] if not _[1] else '<a href="{1}">{0}</a>'.format(*_)) for _ in e[None]),
                    ))
            for s,d2 in self.final.items():
                if d2.date() == d:
                    if empty:
                        ans.append('<div class="day {0:%a}" date="{0:%Y-%m-%d}"><span class="date w{0:%w}">{0:%d %b}</span><div class="events">'.format(d))
                        empty = False
                    ans.append('<div class="special">Final for {} at {:%H:%M}</div>'.format(s,d2))
            if not empty: ans.append('</div></div>')
            else: ans.append('<div class="empty day {0:%a}" date="{0:%Y-%m-%d}"></div>'.format(d))
            d += timedelta(1)
        ans.append('</div>')
        return '\n'.join(ans)
    def toICal(self, lectures, labs):
        tz = 'America/New_York'
        now = datetime.utcnow().strftime('%Y%m%dT%H%M%S')
        ans = ['''BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//University of Virginia//{0}//EN
CALSCALE:GREGORIAN
NAME:{0}'''.format(self.name)]
        
        if lectures is True:
            lectures = self.raw['meta']['lecture']['sections']
        elif lectures:
            lectures = {k:v for k,v in self.raw['meta']['lecture']['sections'].items() if k in lectures}
        else: lectures = {}
        
        if labs is True:
            labs = self.raw['meta']['lab']['sections']
        elif labs:
            labs = {k:v for k,v in self.raw['meta']['lab']['sections'].items() if k in labs}
        else: labs = {}
        
        for r in lectures,labs:
            for k in tuple(r.keys()):
                if type(r[k]['start']) is int:
                    minutes = r[k]['start']//60
                else:
                    start = [int(_) for _ in r[k]['start'].split(':')]
                    minutes = start[0] + 60*start[1]
                def m2s(m):
                    return '{:02d}{:02d}00'.format(m//60,m%60)
                r[k]['st'] = m2s(minutes)
                r[k]['et'] = m2s(minutes+r.get('duration',15))
        
        d = self.start
        while d <= self.stop:
            if lectures and (d in self.lects):
                for k,v in lectures.items():
                    ans.append('''BEGIN:VEVENT
SUMMARY:{title}
DESCRIPTION:{notes}
LOCATION:{location}
DTSTART;TZID={zone}:{date:%Y%m%d}T{start}
DTEND;TZID={zone}:{date:%Y%m%d}T{end}
DTSTAMP:{now}Z
UID:{uid}@{course}.cs.virginia.edu
END:VEVENT'''.format(
                    course=self.name,
                    title=icescape(k),
                    notes=icescape(' and '.join(self.lects[d][False])),
                    location=icescape(v['location']),
                    zone=tz, date=d, start=v['st'], end=v['et'],
                    now=now,
                    uid='{}-{}'.format(icescape(k),d)
                ))

            if labs and (d in self.labs):
                for k,v in labs.items():
                    ans.append('''BEGIN:VEVENT
SUMMARY:{title}
DESCRIPTION:{notes}
LOCATION:{location}
DTSTART;TZID={zone}:{date:%Y%m%d}T{start}
DTEND;TZID={zone}:{date:%Y%m%d}T{end}
DTSTAMP:{now}Z
UID:{uid}@{course}.cs.virginia.edu
END:VEVENT'''.format(
                    course=self.name,
                    title=icescape(k),
                    notes=icescape(' and '.join(self.labs[d][False])),
                    location=icescape(v['location']),
                    zone=tz, date=d, start=v['st'], end=v['et'],
                    now=now,
                    uid='{}-{}'.format(icescape(k),d)
                ))
            for sec in list(lectures) + list(labs):
                if sec in self.final and self.final[sec].date() == d:
                    ans.append('''BEGIN:VEVENT
SUMMARY:Final Exam - {sec}
DTSTART;TZID={zone}:{start:%Y%m%dT%H%M%S}
DTEND;TZID={zone}:{end:%Y%m%dT%H%M%S}
DTSTAMP:{now}Z
UID:final-exam-{sec}@{course}.cs.virginia.edu
END:VEVENT'''.format(sec=sec,
                     start=self.final[sec],
                     end=self.final[sec]+timedelta(0,3*60*60),
                     course=self.name,
                     zone=tz,
                     now=now
                    ))
            d += timedelta(1)

        ans.append('END:VCALENDAR')
        return '\n'.join(ans)


if __name__ == '__main__':
    import os, os.path, glob
    here = os.path.realpath(os.path.dirname(__file__))
    os.chdir(here)
    course = os.path.basename(here)


    import json, sys, yaml
    raw = yamlfile('cal.yaml')
    links = {fn[:-11]:yamlfile(fn) for fn in glob.glob('*-links.yaml')}
    
    cal = CourseSchedule(raw, **links)

    with open('schedule.html', 'w') as fh:
        fh.write(cal.toHTML())

    with open('markdown/all.ics', 'w') as fh:
        fh.write(cal.toICal(True,True))
    
    for sect in cal.raw['meta'].get('lecture',{}).get('sections',{}):
        with open('markdown/{}.ics'.format(sect), 'w') as fh:
            fh.write(cal.toICal([sect],False))
    for sect in cal.raw['meta'].get('lab',{}).get('sections',{}):
        with open('markdown/{}.ics'.format(sect), 'w') as fh:
            fh.write(cal.toICal(False,[sect]))
        

