'''This file contains the shared classes used by the book-selector project.'''

class Book:
    '''A class representing a book recommended by a user.'''

    def __init__(self):
        self.title = None
        self.authorFname = None
        self.location = None

    def __init__(self, title, authorFname, authorLname, location):
        #TODO

    def delete(self):
        #TODO

    def getTitle(self):
        #TODO

    def getAuthorName(self):
        #TODO

    def compare(self, other):
        #TODO

class User:
    '''A class representing a book club participant.'''

    def __init__(self):
        self.userName = None
        self.books = None
        self.numBooks = 0
        self.formLink = None

    def __init__(self, userName, books, formLink):
        #TODO

    def getBooks(self):
        #TODO

    def getUserName(self):
        #TODO

    def getNumBooks(self):
        #TODO

    def getFormLink(self):
        #TODO

class Date:
    '''A class representing when a poll happened.'''

    def __init__(self):
        self.year = None
        self.month = None
        self.day = None

    def __init__(self, year, month, day):
        #TODO

    def getStringDate(self):
        #TODO

    def getYear(self):
        #TODO

    def getMonth(self):
        #TODO

    def getDay(self):
        #TODO

    def compare(self, other):
        #TODO

class Poll:
    '''A class representing a preferred book poll.'''

    def __init__(self):
        self.options = None
        self.scores = None
        self.formLink = None
        self.dateCreated = None

    def __init__(self, options, scores, formLink, dateCreated):
        #TODO

    def getWinner(self):
        #TODO

    def closeVoting(self):
        #TODO

    def getFormLink(self):
        #TODO

    def getOptions(self):
        #TODO

    def getDate(self):
        #TODO

class Location:
    '''An abstract class representing where a book is stored'''

    def __init__(self):
        raise NotImplementedError('Abstract method "__init__" not implemented')

    def compare(self, other):
        raise NotImplementedError('Abstract method "compare" not implemented')
