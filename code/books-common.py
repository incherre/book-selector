'''This file contains the shared classes used by the book-selector project.'''

class Book:
    '''A class representing a book recommended by a user.'''

    def __init__(self):
        self.title = None
        self.authorFname = None
        self.authorLname = None
        self.location = None
        self.data_io = None

    def __init__(self, title, authorFname, authorLname, location, data_io):
        if isinstance(title, str):
            self.title = title
        else:
            raise TypeError("Provided title not a string.")

        if isinstance(authorFname, str):
            self.authorFname = authorFname
        else:
            raise TypeError("Provided author's first name not a string.")

        if isinstance(authorLname, str):
            self.authorLname = authorLname
        else:
            raise TypeError("Provided author's last name not a string.")

        if isinstance(location, Location):
            self.location = location
        else:
            raise TypeError("Provided location not a Location object.")

        if isinstance(data_io, DataIO):
            self.title = title
        else:
            raise TypeError("Provided data io interface not a DataIO object.")
        

    def delete(self):
        '''Removes this book from the database. Returns success.'''
        return self.data_io.removeBook(self)

    def getTitle(self):
        '''Returns the title of this book.'''
        return self.title

    def getAuthorName(self):
        '''Returns the author's name.'''
        return self.authorFname + " " + self.authorLname

    def compare(self, other):
        '''Compares to another book. Books with the same title and author are considered equal.'''
        ret = isinstance(other, Book)

        #These next three lines rely on short circuit evalutation
        ret = ret and self.title.lower() == other.title.lower()
        ret = ret and self.authorFname.lower() == other.authorFname.lower()
        ret = ret and self.authorLname.lower() == other.authorLname.lower()
        return ret 

class User:
    '''A class representing a book club participant.'''

    def __init__(self):
        self.userName = None
        self.books = None
        self.numBooks = 0
        self.formLink = None
        self.data_io = None

    def __init__(self, userName, books, formLink, data_io):
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
        self.data_io = None

    def __init__(self, options, scores, formLink, dateCreated, data_io):
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

class DataIO:
    '''An abstract class representing the functions to communicate with a DB.'''

    def __init__(self):
        raise NotImplementedError('Abstract method "__init__" not implemented')

    def getUserNames(self):
        raise NotImplementedError('Abstract method "getUserNames" not implemented')

    def getUserInfo(self, user):
        raise NotImplementedError('Abstract method "getUserInfo" not implemented')

    def getUserBooks(self, user):
        raise NotImplementedError('Abstract method "getUserBooks" not implemented')

    def getHistory(self):
        raise NotImplementedError('Abstract method "getHistory" not implemented')

    def getCurrentPoll(self):
        raise NotImplementedError('Abstract method "getCurrentPoll" not implemented')

    def createUser(self, user):
        raise NotImplementedError('Abstract method "createUser" not implemented')

    def removeBook(self, book):
        raise NotImplementedError('Abstract method "removeBook" not implemented')

    def newPoll(self, poll):
        raise NotImplementedError('Abstract method "newPoll" not implemented')

    def addWinner(self, book):
        raise NotImplementedError('Abstract method "addWinner" not implemented')
