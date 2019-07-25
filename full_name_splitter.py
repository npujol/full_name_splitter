# -*- coding: utf-8 -*-
import re

LAST_NAME_PREFIXES = [
    'de', 'da', 'la', 'du', 'del', 'dei', 'vda.', 'dello', 'della', 'degli',
    'delle', 'van', 'von', 'der', 'den', 'heer', 'ten', 'ter', 'vande',
    'vanden', 'vander', 'voor', 'ver', 'aan', 'mc'
]

RE_INITIAL = re.compile(r'^\w\.?$')
RE_APOSTROPHE = re.compile(r'\w{1}\'\w+')


class Splitter(object):
    def __init__(self, full_name):
        self.full_name = full_name
        self._first_names = []
        self._last_names = []
        self.split()

    def split(self):
        parts = self.full_name.split(" ")
        while parts:
            part = parts.pop(0)
            #  if prefix? or with_apostrophe? or (first_name? and last_unit? and not initial?)
            print(
                is_prefix(part), has_apostrophe(part), self._first_names,
                not is_initial(part)
            )
            if is_prefix(part) or has_apostrophe(part) or (
                self._first_names and not is_initial(part)
            ):
                self._last_names.append(part)
                break
            else:
                self._first_names.append(part)
        self._last_names.extend(parts)

    @property
    def first_names(self):
        return " ".join(self._first_names)

    @property
    def last_names(self):
        return " ".join(self._last_names)


def is_prefix(part):
    return part.lower() in LAST_NAME_PREFIXES


def is_initial(part):
    return RE_INITIAL.match(part)


def has_apostrophe(part):
    return RE_APOSTROPHE.match(part)

# Adjusting exceptions like
# "Ludwig Mies van der Rohe" => ["Ludwig",  "Mies van der Rohe"   ]
# "Juan Martín de la Cruz Gómez" => ["Juan Martín", "de la Cruz Gómez"]
# "Javier Reyes de la Barrera" => ["Javier",  "Reyes de la Barrera" ]
# Rosa María Pérez Martínez Vda. de la Cruz => ["Rosa María", "Pérez Martínez Vda. de la Cruz"]
# def adjust_exceptions():
#     if re.search(r'^(van der|(vda\. )?de la \w+$)', self.last_names):
