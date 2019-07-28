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

# Regular expresions
RE_INITIAL = re.compile(r"^\w\.?$", re.IGNORECASE)
RE_APOSTROPHE = re.compile(r"\w{1}\'\w+", re.IGNORECASE)
RE_COMPOUSED = re.compile(r"\w+\-\w+", re.IGNORECASE)
RE_SUFFIX = re.compile(
    r",? +(i{1,3}|iv|vi{0,3}|s(enio)?r|j(unio)?r|phd|apr|rph|pe|md|ma|dmd|cme)$",
    re.IGNORECASE,
)
RE_SALUTATION = re.compile(
    r"^(mrs?|m[ia]ster|miss|ms|d(octo)?r|prof|rev|fr|judge|honorable|hon|lord|lady)\.?$",
    re.IGNORECASE,
)
RE_EXCEPTIONS = re.compile(r"^(van der|(vda\.)? ?de la \w+$)", re.IGNORECASE)
RE_SPACES = re.compile(r"\s+")


class Splitter:
    def __init__(self, full_name):
        self._full_name = full_name
        self._first_names = []
        self._last_names = []
        self.split(self.tokens_fullname())

    def tokens_fullname(self):
        # Remove more than one spaces and suffix
        full_name_clean = RE_SUFFIX.sub("", RE_SPACES.sub(" ", self._full_name.strip()))
        if "," in full_name_clean:
            return full_name_clean.split(",")[1::-1]
        return [part for part in full_name_clean.split(" ") if part]

    def split(self, parts):
        while parts:
            part = parts.pop(0).strip()
            if (
                is_prefix(part)
                or has_apostrophe(part)
                or (self._first_names and not parts and not is_initial(part))
            ):
                self._last_names.append(part)
                break
            else:
                self._first_names.append(part)
        self._last_names.extend(parts)

        if self._first_names:
            if is_salutation(self._first_names[0]):
                self._first_names.pop(0)

        self.adjust_exceptions()

    def adjust_exceptions(self):
        # Adjusting exceptions like
        # "Ludwig Mies van der Rohe"      => ["Ludwig", "Mies van der Rohe"]
        # "Juan Martín de la Cruz Gómez"  => ["Juan Martín", "de la Cruz Gómez"]
        # "Javier Reyes de la Barrera"    => ["Javier", "Reyes de la Barrera"]
        # "Rosa María Pérez Martínez Vda. de la Cruz"
        #   => ["Rosa María", "Pérez Martínez Vda. de la Cruz"]
        if (
            len(self._first_names) > 1
            and not is_initial(self._first_names[-1])
            and RE_EXCEPTIONS.match(" ".join(self._last_names))
        ):
            while True:
                self._last_names.insert(0, self._first_names.pop())
                if len(self._first_names) <= 2:
                    break

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
