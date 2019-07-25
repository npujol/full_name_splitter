# -*- coding: utf-8 -*-
import re

LAST_NAME_PREFIXES = [
    "de",
    "da",
    "la",
    "du",
    "del",
    "dei",
    "vda.",
    "dello",
    "della",
    "degli",
    "delle",
    "van",
    "von",
    "der",
    "den",
    "heer",
    "ten",
    "ter",
    "vande",
    "vanden",
    "vander",
    "voor",
    "ver",
    "aan",
    "mc",
]

RE_INITIAL = re.compile(r"^\w\.?$", re.IGNORECASE)
RE_APOSTROPHE = re.compile(r"\w{1}\'\w+", re.IGNORECASE)
RE_SUFFIX = re.compile(
    r"(i{1,3}|iv|vi{0,3}|s(enio)?r|j(unio)?r|phd|apr|rph|pe|md|ma|dmd|cme)$",
    re.IGNORECASE,
)
RE_SALUTATION = re.compile(
    r"^(mrs?|m[ia]ster|miss|ms|d(octo)?r|prof|rev|fr|judge|honorable|hon|lord|lady)\.?",
    re.IGNORECASE,
)


class Splitter(object):
    def __init__(self, full_name):
        self._full_name = full_name
        self._first_names = []
        self._last_names = []
        self.clean_fullname()
        self.split()

    def clean_fullname(self):
        # Remove more one space, "," prefix and salution
        full_name = re.sub(r"[\n\t,]*", "", re.sub(r" +", " ", self._full_name))

        self._full_name = " ".join(
            [
                part
                for part in full_name.split(" ")
                if not is_salutation(part) and not is_suffix(part) and part
            ]
        )

    def split(self):
        parts = self._full_name.split(" ")
        while parts:
            part = parts.pop(0)
            if (
                is_prefix(part)
                or has_apostrophe(part)
                or (
                    self._first_names
                    and not is_initial(part)
                    and len(self._first_names) >= 2
                )
            ):
                self._last_names.append(part)
                break
            else:
                self._first_names.append(part)
        self._last_names.extend(parts)

    @property
    def full_name(self):
        return " ".join(self._first_names + self._last_names)

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


def is_salutation(part):
    return RE_SALUTATION.match(part)


def is_suffix(part):
    return RE_SUFFIX.match(part)


# Adjusting exceptions like
# "Ludwig Mies van der Rohe" => ["Ludwig",  "Mies van der Rohe"   ]
# "Juan Martín de la Cruz Gómez" => ["Juan Martín", "de la Cruz Gómez"]
# "Javier Reyes de la Barrera" => ["Javier",  "Reyes de la Barrera" ]
# Rosa María Pérez Martínez Vda. de la Cruz => ["Rosa María", "Pérez Martínez Vda. de la Cruz"]
# def adjust_exceptions():
#     if re.search(r'^(van der|(vda\. )?de la \w+$)', self.last_names):
