from full_name_splitter import Splitter

CASE_SOLUTIONS = [
    # One name and only one lastname
    ["John Smith", ["John", "Smith"]],
    # Only name
    ["John", ["John", null]],
    ["George H. W.", ["George H. W.", null]],
    ["Van Helsing", [null, "Van Helsing"]],
    ["d'Artagnan", [null, "d'Artagnan"]],
    ["O'Connor", [null, "O'Connor"]],
    ["George", ["George", null]],
    ["Kevin J. ", ["Kevin J.", null]],
    # Name with abbreviation
    ["Kevin J. Connor", ["Kevin J.", "Connor"]],
    ["George W Bush", ["George W", "Bush"]],
    ["George H. W. Bush", ["George H. W.", "Bush"]],
    ["James K. Polk", ["James K.", "Polk"]],
    # Lastname with prefix
    ["Gabriel Van Helsing", ["Gabriel", "Van Helsing"]],
    ["Pierre de Montesquiou", ["Pierre", "de Montesquiou"]],
    ["Charles d'Artagnan", ["Charles", "d'Artagnan"]],
    ["Anne du Bourg", ["Anne", "du Bourg"]],
    # Compoused lastname
    ["Ben Butler-Sandwich", ["Ben", "Butler-Sandwich"]],
    ["Noda' bi-Yehudah", ["Noda'", "bi-Yehudah"]],
    ["Alessandro Del Piero", ["Alessandro", "Del Piero"]],
    # Two lastnames
    ["Maria del Carmen Menendez", ["Maria", "del Carmen, Menendez"]],
    ["Thomas G. Della Fave", ["Thomas G.", "Della Fave"]],
    # Two names
    ["William Henry Harrison", ["William Henry", "Harrison"]],
    ["John Quincy Adams", ["John Quincy", "Adams"]],
    ["John Quincy", ["John", "Quincy"]],
    # German
    ["Johann Wolfgang von Goethe", ["Johann Wolfgang", "von Goethe"]],
    # Spanish-speaking countries
    ["Juan Martín de la Cruz Gómez", ["Juan Martín", "de la Cruz Gómez"]],
    ["Javier Reyes de la Barrera", ["Javier", "Reyes de la Barrera"]],
    #Exceptions?
    ["Ludwig Mies van der Rohe", ["Ludwig", "Mies van der Rohe"]],
    # Test ignoring unnecessary whitespaces
    ["\t Ludwig  Mies\t van der Rohe ", ["Ludwig", "Mies van der Rohe"]],
    ["\t van  der Rohe,\t Ludwig  Mies ", ["Ludwig Mies", "van der Rohe"]],
    ["\t Ludwig      ", ["Ludwig", null]],
    ["  van  helsing ", [null, "van helsing"]],
    [", van  helsing ", ["van helsing", null]],
    ["\t van  der Rohe,\t Ludwig  Mies ", ["Ludwig Mies", "van der Rohe"]],
    #  Names with honorifics
    ['Mr. William R. Hearst, III', ['William R.', 'Hearst']],
    ['William Randolph Hearst', ['William Randolph', 'Hearst']],
    ['William R. De La Cruz', ['William R.', 'De La Cruz']],
    ['Mr. William R. De La Cruz III', ['William R.', 'De La Cruz']],
    ['William De Cruz', ['William', 'De Cruz']],
    ['William De La Cruz', ['William', 'De La Cruz']],
    ['William A. B. De La Cruz', ['William A. B.', 'De La Cruz']],
    ['James Hugh Calum Laurie', ['James Hugh Calum', 'Laurie']],
    [
        'Kiefer William Frederick Dempsey George Rufus Sutherland',
        ['Kiefer William Frederick Dempsey George Rufus', 'Sutherland']
    ],
    ['William Hearst', ['William', 'Hearst']],
    ['William Hearst Jr', ['William', 'Hearst']],
    ['Hearst, William Jr', ['William', 'Hearst']],
    ['Hearst, William Randolph', ['William Randolph', 'Hearst']],
    ['Hearst, William, M.D.', ['William', 'Hearst']],
    ['William', ['William', null]],
    ['', [null, null]],
]


def test_basic():
    t = Template('<% for u in users %>${u["username"]}\n<% endfor %>')
    result = t.render(users=[{'username': 'John'}, {'username': 'Jane'}])
    assert result == "John\nJane\n"


def test_split_simple_names():
    name = ["John Smith", ["John", "Smith"]]  # One name and only one lastname
    s = Splitter(name[0])
    result = s.split()
    assert result == name[1]
