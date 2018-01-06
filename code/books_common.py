'''This file contains the shared classes used by the book-selector project.'''

import random

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
            self.data_io = data_io
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

    def __init__(self, userName, books, formLink):
        if isinstance(userName, str):
            self.userName = userName
        else:
            raise TypeError("Provided user name not a string.")

        if isinstance(books, list) and (len(books) == 0 or isinstance(books[0], Book)):
            self.books = books
            self.numBooks = len(books)
        else:
            raise TypeError("Provided book list not a list of books.")

        if isinstance(formLink, str):
            self.formLink = formLink
        else:
            raise TypeError("Provided link to form not a string.")

    def getBooks(self):
        '''Returns the list of books suggested by this user.'''
        return self.books

    def getUserName(self):
        '''Returns the user's username.'''
        return self.userName

    def getNumBooks(self):
        '''Returns the number of books a user has.'''
        return self.numBooks

    def getFormLink(self):
        '''Returns the link to the form the user uses to input books.'''
        return self.formLink

class Date:
    '''A class representing when a poll happened.'''

    def __init__(self):
        self.year = None
        self.month = None
        self.day = None

    def __init__(self, year, month, day):
        if isinstance(year, int):
            self.year = year
        else:
            raise TypeError("Provided year not a number.")

        if isinstance(month, int) and month > 0 and month <= 12:
            self.month = month
        else:
            raise TypeError("Provided month not a valid number.")

        if isinstance(day, int) and day > 0 and day <= 31:
            self.day = day
        else:
            raise TypeError("Provided day not a valid number.")

    def getStringDate(self):
        '''Returns a string representation of the date.'''
        return str(self.year) + "/" + str(self.month) + "/" + str(self.day)

    def getYear(self):
        '''Returns the year.'''
        return self.year

    def getMonth(self):
        '''Returns the month.'''
        return self.month

    def getDay(self):
        '''Returns the day.'''
        return self.day

    def compare(self, other):
        '''Tests for equality between dates.'''
        return isinstance(other, Date) and self.year == other.year and self.month == other.month and self.day == other.day

class Poll:
    '''A class representing a preferred book poll.'''

    def __init__(self):
        self.options = None
        self.scores = None
        self.formLink = None
        self.dateCreated = None
        self.data_io = None

    def __init__(self, options, scores, formLink, dateCreated, data_io):
        if isinstance(options, list) and (len(options) == 0 or isinstance(options[0], Book)):
            self.options = options
        else:
            raise TypeError("Provided options list not a list of books.")

        if isinstance(scores, list) and len(scores) == len(options) and (len(scores) == 0 or isinstance(scores[0], int)):
            self.scores = scores
        else:
            raise TypeError("Provided scores list not a valid list of numbers.")

        if isinstance(formLink, str):
            self.formLink = formLink
        else:
            raise TypeError("Provided link to form not a string.")

        if isinstance(dateCreated, Date):
            self.dateCreated = dateCreated
        else:
            raise TypeError("Provided date not a date object.")

        if isinstance(data_io, DataIO):
            self.data_io = data_io
        else:
            raise TypeError("Provided data io interface not a DataIO object.")

    def getWinner(self):
        '''Returns the winner of the poll.'''
        if not hasattr(self, 'winner'):
            winning_threshold = max(self.scores)
            potential_winners = [i for i in range(len(self.scores)) if self.scores[i] == winning_threshold]
            self.winner = self.options[random.choice(potential_winners)] #deal with ties and make sure the result is consistent
        return self.winner            

    def closeVoting(self):
        '''Closes the poll for voting. Returns success.'''
        return self.data_io.closePoll(self)

    def getFormLink(self):
        '''Returns the link used to vote.'''
        return self.formLink

    def getOptions(self):
        '''Returns the list of options used in the poll.'''
        return self.options

    def getDate(self):
        '''Returns the date the poll was created.'''
        return self.dateCreated

    def updateResults(self):
        '''Changes the results to those of the current poll. Removes the cached winner if it exists.'''
        current_poll = self.data_io.getCurrentPoll()
        self.scores = current_poll.scores

        if hasattr(self, 'winner'):
            del self.winner

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

    def closePoll(self, poll):
        raise NotImplementedError('Abstract method "closePoll" not implemented')

    def addWinner(self, book):
        raise NotImplementedError('Abstract method "addWinner" not implemented')
