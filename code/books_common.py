'''This file contains the shared classes used by the book-selector project.'''

import random
from abc import ABC, abstractmethod

class Book:
    '''A class representing a book recommended by a user.'''

    def __init__(self, title, author_first_name, author_last_name, location, data_io):
        if isinstance(title, str):
            self.title = title
        else:
            raise TypeError("Provided title not a string.")

        if isinstance(author_first_name, str):
            self.author_first_name = author_first_name
        else:
            raise TypeError("Provided author's first name not a string.")

        if isinstance(author_last_name, str):
            self.author_last_name = author_last_name
        else:
            raise TypeError("Provided author's last name not a string.")

        if isinstance(location, Location) or location is None:
            self.location = location
        else:
            raise TypeError("Provided location not a Location object.")

        if isinstance(data_io, DataIO):
            self.data_io = data_io
        else:
            raise TypeError("Provided data io interface not a DataIO object.")

    def delete(self):
        '''Removes this book from the database. Returns success.'''
        if self.location != None:
            return self.data_io.remove_book(self)

        return False

    def get_title(self):
        '''Returns the title of this book.'''
        return self.title

    def get_author_name(self):
        '''Returns the author's name.'''
        return self.author_first_name + " " + self.author_last_name

    def get_author_first_name(self):
        '''Returns the author's first name.'''
        return self.author_first_name

    def get_author_last_name(self):
        '''Returns the author's last name.'''
        return self.author_last_name

    def compare(self, other):
        '''Compares to another book. Books with the same title and author are considered equal.'''
        ret = isinstance(other, Book)

        #These next three lines rely on short circuit evalutation
        ret = ret and self.title.lower() == other.title.lower()
        ret = ret and self.author_first_name.lower() == other.author_first_name.lower()
        ret = ret and self.author_last_name.lower() == other.author_last_name.lower()
        return ret

class User:
    '''A class representing a book club participant.'''

    def __init__(self, user_name, user_email, books, form_link, data_io):
        if isinstance(user_name, str):
            self.user_name = user_name
        else:
            raise TypeError("Provided user name not a string.")

        if isinstance(user_email, str):
            self.user_email = user_email
        else:
            raise TypeError("Provided user email not a string.")

        if isinstance(books, list) and (not books or isinstance(books[0], Book)):
            self.books = books
            self.book_count = len(books)
        else:
            raise TypeError("Provided book list not a list of books.")

        if isinstance(form_link, str):
            self.form_link = form_link
        else:
            raise TypeError("Provided link to form not a string.")

        if isinstance(data_io, DataIO):
            self.data_io = data_io
        else:
            raise TypeError("Provided data io interface not a DataIO object.")

    def get_books(self):
        '''Returns the list of books suggested by this user.'''
        if not self.books:
            self.data_io.get_user_books(self)

        return self.books

    def get_user_name(self):
        '''Returns the user's username.'''
        return self.user_name

    def get_user_email(self):
        '''Returns the user's email address.'''
        return self.user_email

    def get_book_count(self):
        '''Returns the number of books a user has.'''
        return self.book_count

    def get_form_link(self):
        '''Returns the link to the form the user uses to input books.'''
        return self.form_link

    def replace_books(self, new_books):
        '''Replaces the book list with the one provided.'''
        if isinstance(new_books, list) and (not new_books or isinstance(new_books[0], Book)):
            self.books = new_books
            self.book_count = len(new_books)
        else:
            raise TypeError("Provided book list not a list of books.")

class Date:
    '''A class representing when a poll happened.'''

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

    def get_string_date(self):
        '''Returns a string representation of the date.'''
        return str(self.year) + "/" + str(self.month) + "/" + str(self.day)

    def get_year(self):
        '''Returns the year.'''
        return self.year

    def get_month(self):
        '''Returns the month.'''
        return self.month

    def get_day(self):
        '''Returns the day.'''
        return self.day

    def compare(self, other):
        '''Tests for equality between dates.'''
        ret = isinstance(other, Date)
        ret = ret and self.year == other.year
        ret = ret and self.month == other.month
        ret = ret and self.day == other.day
        return ret

class Poll:
    '''A class representing a preferred book poll.'''

    def __init__(self, options, scores, form_link, form_id, date_created, data_io):
        self.winner = None

        if isinstance(options, list) and (not options or isinstance(options[0], Book)):
            self.options = options
        else:
            raise TypeError("Provided options list not a list of books.")

        is_scores = isinstance(scores, list)
        is_scores = is_scores and len(scores) == len(options)
        is_scores = is_scores and (not scores or isinstance(scores[0], int))
        if is_scores:
            self.scores = scores
        else:
            raise TypeError("Provided scores list not a valid list of numbers.")

        if isinstance(form_link, str):
            self.form_link = form_link
        else:
            raise TypeError("Provided link to form not a string.")

        if isinstance(form_id, str):
            self.form_id = form_id
        else:
            raise TypeError("Provided form identification not a string.")

        if isinstance(date_created, Date):
            self.date_created = date_created
        else:
            raise TypeError("Provided date not a date object.")

        if isinstance(data_io, DataIO):
            self.data_io = data_io
        else:
            raise TypeError("Provided data io interface not a DataIO object.")

    def get_winner(self):
        '''Returns the winner of the poll.'''
        if self.winner is None:
            winning_threshold = max(self.scores)
            potential_winners = [i for i in range(len(self.scores))
                                 if self.scores[i] == winning_threshold]

            #deal with ties and make sure the result is consistent
            self.winner = self.options[random.choice(potential_winners)]
        return self.winner

    def close_voting(self):
        '''Closes the poll for voting. Returns success.'''
        return self.data_io.close_poll(self)

    def get_form_link(self):
        '''Returns the link used to vote.'''
        return self.form_link

    def get_options(self):
        '''Returns the list of options used in the poll.'''
        return self.options

    def get_date(self):
        '''Returns the date the poll was created.'''
        return self.date_created

    def update_results(self):
        '''Changes the results to those of the current poll.
        Removes the cached winner if it exists.'''
        current_poll = self.data_io.get_current_poll()
        self.scores = current_poll.scores

        if hasattr(self, 'winner'):
            self.winner = None

    def delete(self):
        '''Removes this poll from the database.'''
        return self.data_io.delete_poll(self.form_id)

class Location(ABC):
    '''An abstract class representing where a book is stored'''

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def compare(self, other):
        '''Abstract method. Returns whether two locations represent the same place or not.'''
        raise NotImplementedError('Abstract method "compare" not implemented')

class DataIO(ABC):
    '''An abstract class representing the functions to communicate with a DB.'''

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_user_names(self):
        '''Abstract method. Returns a list of user names.'''
        raise NotImplementedError('Abstract method "get_user_names" not implemented')

    @abstractmethod
    def get_user_info(self, username):
        '''Abstract method. Returns a populated (except for the books) User object.'''
        raise NotImplementedError('Abstract method "get_user_info" not implemented')

    @abstractmethod
    def get_user_books(self, user):
        '''Abstract method. Returns the list of books that belong to a user.
        Also updates the user object's books.'''
        raise NotImplementedError('Abstract method "get_user_books" not implemented')

    @abstractmethod
    def get_history(self):
        '''Abstract method. Returns the list of books that have won in the past.'''
        raise NotImplementedError('Abstract method "get_history" not implemented')

    @abstractmethod
    def get_current_poll(self):
        '''Abstract method. Returns the ongoing poll.'''
        raise NotImplementedError('Abstract method "get_current_poll" not implemented')

    @abstractmethod
    def create_user(self, username, user_email):
        '''Abstract method. Creates a new user and returns it.'''
        raise NotImplementedError('Abstract method "create_user" not implemented')

    @abstractmethod
    def remove_book(self, book):
        '''Abstract method. Deletes a book, wherever it is stored.'''
        raise NotImplementedError('Abstract method "remove_book" not implemented')

    @abstractmethod
    def remove_all_books(self, user):
        '''Abstract method. Deletes all user's books wherever it is stored.'''
        raise NotImplementedError('Abstract method "remove_all_books" not implemented')

    @abstractmethod
    def new_poll(self, options):
        '''Abstract method. Creates a new poll.'''
        raise NotImplementedError('Abstract method "new_poll" not implemented')

    @abstractmethod
    def close_poll(self, poll):
        '''Abstract method. Stops a poll from accepting new responses.'''
        raise NotImplementedError('Abstract method "close_poll" not implemented')

    @abstractmethod
    def add_winner(self, book):
        '''Abstract method. Adds a book to the winner history.'''
        raise NotImplementedError('Abstract method "add_winner" not implemented')

    @abstractmethod
    def send_email(self, destination_address, subject, body):
        '''Abstract method. Sends an email, used to convey account info.'''
        raise NotImplementedError('Abstract method "send_email" not implemented')

    @abstractmethod
    def remove_user(self, user):
        '''Abstract method. Removes all record of a user.'''
        raise NotImplementedError('Abstract method "remove_user" not implemented')

    @abstractmethod
    def delete_poll(self, poll_id):
        '''Abstract method. Removes a poll.'''
        raise NotImplementedError('Abstract method "delete_poll" not implemented')
