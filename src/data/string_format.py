import re

def format_name(s):
    return s.replace("'s", "s").replace(' ,', ',').title().replace('St ', 'St. ').replace(' Rd', ' Road').replace('&', 'and').replace('Gun Makers', 'Gunmakers').replace(' Northside', ' North Side').replace(' And ', ' and ').strip()

to_short_name = lambda x: re.sub('\d*$', '', x.split(',')[0].strip()).strip()