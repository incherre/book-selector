'''This is the unit test file for the books-common.py file.'''

import unittest
import books_common

## These classes are implementations of abstract classes for testing purposes
class BaseLocationWithoutErrorInit(books_common.Location):
    def __init__(self):
        pass

    def compare(self, other):
        return super().compare(other)

class BaseDataIOWithoutErrorInit(books_common.DataIO):
    def __init__(self):
        pass

    def add_winner(self, book):
        return super().add_winner(book)

    def close_poll(self, poll):
        return super().close_poll(poll)

    def create_user(self, username, user_email):
        return super().create_user(username, user_email)

    def get_current_poll(self):
        return super().get_current_poll()

    def get_history(self):
        return super().get_history()

    def get_user_books(self, user):
        return super().get_user_books(user)

    def get_user_info(self, username):
        return super().get_user_info(username)

    def get_user_names(self):
        return super().get_user_names()

    def new_poll(self, options):
        return super().new_poll(options)

    def remove_book(self, book):
        return super().remove_book(book)

    def send_email(self, destination_address, subject, body):
        return super().send_email(destination_address, subject, body)

    def remove_user(self, user):
        return super().remove_user(user)

    def delete_poll(self, doc_id):
        return super().delete_poll(doc_id)

class LocationAllTrue(books_common.Location):
    def __init__(self):
        pass

    def compare(self, other):
        return True

class LocationAllFalse(books_common.Location):
    def __init__(self):
        pass

    def compare(self, other):
        return False

class DataIOAllSuccess(BaseDataIOWithoutErrorInit):
    '''Anything that returns a success returns true'''

    def create_user(self, user):
        return True

    def remove_book(self, book):
        return True

    def new_poll(self, poll):
        return True

    def close_poll(self, poll):
        return True

    def add_winner(self, book):
        return True

    def send_email(self, destination_address, subject, body):
        return True

    def remove_user(self, user):
        return True

    def delete_poll(self, doc_id):
        return True

class DataIOAllFail(BaseDataIOWithoutErrorInit):
    '''Anything that returns a success returns false'''

    def create_user(self, user):
        return False

    def remove_book(self, book):
        return False

    def new_poll(self, poll):
        return False

    def close_poll(self, poll):
        return False

    def add_winner(self, book):
        return False

    def send_email(self, destination_address, subject, body):
        return False

    def remove_user(self, user):
        return False

    def delete_poll(self, doc_id):
        return False

class BaseDataIOReturnPoll(BaseDataIOWithoutErrorInit):
    def __init__(self, poll):
        self.poll = poll

    def get_current_poll(self):
        return self.poll

## End test implementations

class TestBookMethods(unittest.TestCase):
    def setUp(self):
        self.t_title = "title"
        self.t_authorFname = "fName"
        self.t_authorLname = "lName"
        self.t_location = BaseLocationWithoutErrorInit()
        self.t_data_io = BaseDataIOWithoutErrorInit()

        self.basicBook = books_common.Book(self.t_title, self.t_authorFname, self.t_authorLname, self.t_location, self.t_data_io)
        self.succeedBook = books_common.Book(self.t_title, self.t_authorFname, self.t_authorLname, self.t_location, DataIOAllSuccess())
        self.failBook = books_common.Book(self.t_title, self.t_authorFname, self.t_authorLname, self.t_location, DataIOAllFail())
        self.noLocBook = books_common.Book(self.t_title, self.t_authorFname, self.t_authorLname, None, self.t_data_io)

    def tearDown(self):
        del self.t_title
        del self.t_authorFname
        del self.t_authorLname
        del self.t_location
        del self.t_data_io

        del self.basicBook
        del self.succeedBook
        del self.failBook
        del self.noLocBook

    def test_init(self):
        testVar = books_common.Book(self.t_title, self.t_authorFname, self.t_authorLname, self.t_location, self.t_data_io)
        self.assertIsInstance(testVar, books_common.Book)

    def test_init_no_location(self):
        testVar = books_common.Book(self.t_title, self.t_authorFname, self.t_authorLname, None, self.t_data_io)
        self.assertIsInstance(testVar, books_common.Book)

    def test_init_fail_invalid_title(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Book(None,  self.t_authorFname, self.t_authorLname, self.t_location, self.t_data_io)

    def test_init_fail_invalid_author_fname(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Book(self.t_title,  None, self.t_authorLname, self.t_location, self.t_data_io)

    def test_init_fail_invalid_author_lname(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Book(self.t_title,  self.t_authorFname, None, self.t_location, self.t_data_io)

    def test_init_fail_invalid_location(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Book(self.t_title,  self.t_authorFname, self.t_authorLname, 'Not_a_location', self.t_data_io)

    def test_init_fail_invalid_data_io(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Book(self.t_title,  self.t_authorFname, self.t_authorLname, self.t_location, None)

    def test_delete(self):
        self.assertTrue(self.succeedBook.delete())
        self.assertFalse(self.failBook.delete())
        self.assertFalse(self.noLocBook.delete())

    def test_get_title(self):
        self.assertEqual(self.basicBook.get_title(), self.t_title)

    def test_get_author_name(self):
        author = self.t_authorFname + " " + self.t_authorLname
        self.assertEqual(self.basicBook.get_author_name(), author)

    def test_getAuthorFName(self):
        self.assertEqual(self.basicBook.get_author_first_name(), self.t_authorFname)

    def test_getAuthorLName(self):
        self.assertEqual(self.basicBook.get_author_last_name(), self.t_authorLname)

    def test_compare(self):
        other = books_common.Book(self.t_title, self.t_authorFname, self.t_authorLname, self.t_location, self.t_data_io)
        self.assertTrue(self.basicBook.compare(other))

        other = books_common.Book("different", self.t_authorFname, self.t_authorLname, self.t_location, self.t_data_io)
        self.assertFalse(self.basicBook.compare(other))

        other = books_common.Book(self.t_title, "different", self.t_authorLname, self.t_location, self.t_data_io)
        self.assertFalse(self.basicBook.compare(other))

        other = books_common.Book(self.t_title, self.t_authorFname, "different", self.t_location, self.t_data_io)
        self.assertFalse(self.basicBook.compare(other))

class TestUserMethods(unittest.TestCase):
    def setUp(self):
        abook = books_common.Book("title", "fName", "lName", BaseLocationWithoutErrorInit(), BaseDataIOWithoutErrorInit())

        self.t_userName = "uName"
        self.t_userEmail = "an.email@example.com"
        self.t_books = [abook]
        self.t_formLink = "www.example.com"

        self.t_user = books_common.User(self.t_userName, self.t_userEmail, self.t_books, self.t_formLink)

    def tearDown(self):
        del self.t_userName
        del self.t_userEmail
        del self.t_books
        del self.t_formLink

        del self.t_user

    def test_init(self):
        testVar = books_common.User(self.t_userName, self.t_userEmail, self.t_books, self.t_formLink)
        self.assertIsInstance(testVar, books_common.User)

    def test_init_fail_invalid_userName(self):
        with self.assertRaises(TypeError):
            testVar = books_common.User(None, self.t_userEmail, self.t_books, self.t_formLink)

    def test_init_fail_invalid_userEmail(self):
        with self.assertRaises(TypeError):
            testVar = books_common.User(self.t_userName, None, self.t_books, self.t_formLink)

    def test_init_fail_no_books(self):
        with self.assertRaises(TypeError):
            testVar = books_common.User(self.t_userName, self.t_userEmail, None, self.t_formLink)

    def test_init_fail_bad_books(self):
        with self.assertRaises(TypeError):
            testVar = books_common.User(self.t_userName, self.t_userEmail, [None], self.t_formLink)

    def test_init_fail_invalid_formLink(self):
        with self.assertRaises(TypeError):
            testVar = books_common.User(self.t_userName, self.t_userEmail, self.t_books, None)

    def test_get_books(self):
        maybe_books = self.t_user.get_books()
        self.assertIsInstance(maybe_books, list)
        self.assertEqual(len(maybe_books), 1)
        self.assertTrue(maybe_books[0].compare(self.t_books[0]))

    def test_get_user_name(self):
        self.assertEqual(self.t_user.get_user_name(), self.t_userName)

    def test_get_user_email(self):
        self.assertEqual(self.t_user.get_user_email(), self.t_userEmail)

    def test_get_book_count(self):
        self.assertEqual(self.t_user.get_book_count(), len(self.t_books))

    def test_get_form_link(self):
        self.assertEqual(self.t_user.get_form_link(), self.t_formLink)

    def test_replace_books(self):
        self.t_user.replace_books([])

        self.assertEqual(self.t_user.books, [])
        self.assertEqual(self.t_user.book_count, 0)

    def test_replace_books_fail_no_books(self):
        with self.assertRaises(TypeError):
            self.t_user.replace_books(None)

    def test_replace_books_fail_bad_books(self):
        with self.assertRaises(TypeError):
            self.t_user.replace_books([None])

class TestDateMethods(unittest.TestCase):
    def setUp(self):
        self.t_year = 2000
        self.t_month = 1
        self.t_day = 1
        self.t_strDate = "2000/1/1"

        self.t_date = books_common.Date(self.t_year, self.t_month, self.t_day)

    def tearDown(self):
        del self.t_year
        del self.t_month
        del self.t_day
        del self.t_strDate

        del self.t_date

    def test_init(self):
        testVar = books_common.Date(self.t_year, self.t_month, self.t_day)
        self.assertIsInstance(testVar, books_common.Date)

    def test_init_fail_no_year(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Date(None, self.t_month, self.t_day)

    def test_init_fail_no_month(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Date(self.t_year, None, self.t_day)

    def test_init_fail_small_month(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Date(self.t_year, 0, self.t_day)

    def test_init_fail_big_month(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Date(self.t_year, 13, self.t_day)

    def test_init_fail_no_day(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Date(self.t_year, self.t_month, None)

    def test_init_fail_small_day(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Date(self.t_year, self.t_month, 0)

    def test_init_fail_big_day(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Date(self.t_year, self.t_month, 32)

    def test_get_string_date(self):
        self.assertEqual(self.t_date.get_string_date(), self.t_strDate)

    def test_get_year(self):
        self.assertEqual(self.t_date.get_year(), self.t_year)

    def test_get_month(self):
        self.assertEqual(self.t_date.get_month(), self.t_month)

    def test_get_day(self):
        self.assertEqual(self.t_date.get_day(), self.t_day)

    def test_compare(self):
        other = books_common.Date(self.t_year, self.t_month, self.t_day)
        self.assertTrue(self.t_date.compare(other))

        other = books_common.Date(2001, self.t_month, self.t_day)
        self.assertFalse(self.t_date.compare(other))

        other = books_common.Date(self.t_year, 2, self.t_day)
        self.assertFalse(self.t_date.compare(other))

        other = books_common.Date(self.t_year, self.t_month, 2)
        self.assertFalse(self.t_date.compare(other))

class TestPollMethods(unittest.TestCase):
    def setUp(self):
        data_io = BaseDataIOWithoutErrorInit()
        location = BaseLocationWithoutErrorInit()

        self.t_book1 = books_common.Book("opt1", "fn", "ln", location, data_io)
        self.t_book2 = books_common.Book("opt2", "fn", "ln", location, data_io)
        self.t_book3 = books_common.Book("opt3", "fn", "ln", location, data_io)

        self.t_options = [self.t_book1, self.t_book2, self.t_book3]
        self.t_scores = [0, 0, 0]
        self.t_formLink = "www.example.com"
        self.t_formId = "4800063"
        self.t_dateCreated = books_common.Date(2000, 1, 1)
        self.t_data_io = data_io

        self.t_poll = books_common.Poll(self.t_options, self.t_scores, self.t_formLink, self.t_formId, self.t_dateCreated, data_io)
        self.t_succeed_poll = books_common.Poll(self.t_options, self.t_scores, self.t_formLink, self.t_formId, self.t_dateCreated, DataIOAllSuccess())
        self.t_fail_poll = books_common.Poll(self.t_options, self.t_scores, self.t_formLink, self.t_formId, self.t_dateCreated, DataIOAllFail())


    def tearDown(self):
        del self.t_options
        del self.t_scores
        del self.t_formLink
        del self.t_formId
        del self.t_dateCreated
        del self.t_data_io

        del self.t_poll
        del self.t_succeed_poll
        del self.t_fail_poll

    def test_init(self):
        testVar = books_common.Poll(self.t_options, self.t_scores, self.t_formLink, self.t_formId, self.t_dateCreated, self.t_data_io)
        self.assertIsInstance(testVar, books_common.Poll)

    def test_init_fail_no_options(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Poll(None, self.t_scores, self.t_formLink, self.t_formId, self.t_dateCreated, self.t_data_io)

    def test_init_fail_invalid_options(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Poll([None, None], self.t_scores, self.t_formLink, self.t_formId, self.t_dateCreated, self.t_data_io)

    def test_init_fail_no_scores(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Poll(self.t_options, None, self.t_formLink, self.t_formId, self.t_dateCreated, self.t_data_io)

    def test_init_fail_invalid_scores(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Poll(self.t_options, [None, None], self.t_formLink, self.t_formId, self.t_dateCreated, self.t_data_io)

    def test_init_fail_wrong_num_scores(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Poll(self.t_options, [0], self.t_formLink, self.t_formId, self.t_dateCreated, self.t_data_io)

    def test_init_fail_no_link(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Poll(self.t_options, self.t_scores, None, self.t_formId, self.t_dateCreated, self.t_data_io)

    def test_init_fail_no_id(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Poll(self.t_options, self.t_scores, self.t_formLink, None, self.t_dateCreated, self.t_data_io)

    def test_init_fail_no_date(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Poll(self.t_options, self.t_scores, self.t_formLink, self.t_formId, None, self.t_data_io)

    def test_init_fail_no_data_io(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Poll(self.t_options, self.t_scores, self.t_formLink, self.t_formId, self.t_dateCreated, None)

    def test_get_winner(self):
        self.t_poll.scores = [0, 0, 1]
        self.assertTrue(self.t_book3.compare(self.t_poll.get_winner()))
        self.t_poll.winner = None

        self.t_poll.scores = [0, 1, 1]
        winner = self.t_poll.get_winner()
        self.assertTrue(self.t_book3.compare(winner) or self.t_book2.compare(winner))
        for i in range(10):
            self.assertTrue(winner.compare(self.t_poll.get_winner()))
        del self.t_poll.winner

    def test_close_voting(self):
        testPoll = books_common.Poll(self.t_options, self.t_scores, self.t_formLink, self.t_formId, self.t_dateCreated, DataIOAllSuccess())
        self.assertTrue(testPoll.close_voting())

        testPoll = books_common.Poll(self.t_options, self.t_scores, self.t_formLink, self.t_formId, self.t_dateCreated, DataIOAllFail())
        self.assertFalse(testPoll.close_voting())

    def test_get_form_link(self):
        self.assertEqual(self.t_poll.get_form_link(), self.t_formLink)

    def test_get_options(self):
        options = self.t_poll.get_options()
        for i in range(len(options)):
            self.assertTrue(options[i].compare(self.t_options[i]))

    def test_get_date(self):
        self.assertTrue(self.t_dateCreated.compare(self.t_poll.get_date()))

    def test_update_results(self):
        newScores = [100, 101, 102]
        bigPoll = books_common.Poll(self.t_options, newScores, self.t_formLink, self.t_formId, self.t_dateCreated, self.t_data_io)
        testPoll = books_common.Poll(self.t_options, [1, 0, 0], self.t_formLink, self.t_formId, self.t_dateCreated, BaseDataIOReturnPoll(bigPoll))

        testPoll.winner = self.t_book1
        testPoll.update_results()
        self.assertFalse(hasattr(testPoll, 'winner'))
        for i in range(len(testPoll.scores)):
            self.assertEqual(newScores[i], testPoll.scores[i])

    def test_delete(self):
        self.assertTrue(self.t_succeed_poll.delete())
        self.assertFalse(self.t_fail_poll.delete())

class TestLocationMethods(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Location()

    def test_compare(self):
        testLoc1 = BaseLocationWithoutErrorInit()
        testLoc2 = BaseLocationWithoutErrorInit()
        with self.assertRaises(NotImplementedError):
            testLoc1.compare(testLoc2)

class TestDataIOMethods(unittest.TestCase):

    def setUp(self):
        self.testIO = BaseDataIOWithoutErrorInit()
        self.testBook = books_common.Book("Title", "Sarah", "Smith", BaseLocationWithoutErrorInit(), BaseDataIOWithoutErrorInit())
        self.testPoll = books_common.Poll([self.testBook, self.testBook], [0, 0], "www.example.com", "4800063", books_common.Date(2000, 1, 1), BaseDataIOWithoutErrorInit())

    def tearDown(self):
        del self.testIO
        del self.testBook
        del self.testPoll

    def test_init(self):
        with self.assertRaises(TypeError):
            testVar = books_common.DataIO()

    def test_get_user_names(self):
        self.assertRaises(NotImplementedError, self.testIO.get_user_names)

    def test_get_user_info(self):
        self.assertRaises(NotImplementedError, self.testIO.get_user_info, "uName")

    def test_get_user_books(self):
        self.assertRaises(NotImplementedError, self.testIO.get_user_books, "uName")

    def test_get_history(self):
        self.assertRaises(NotImplementedError, self.testIO.get_history)

    def test_get_current_poll(self):
        self.assertRaises(NotImplementedError, self.testIO.get_current_poll)

    def test_create_user(self):
        self.assertRaises(NotImplementedError, self.testIO.create_user, "uName", "user@email.com")

    def test_remove_book(self):
        self.assertRaises(NotImplementedError, self.testIO.remove_book, self.testBook)

    def test_new_poll(self):
        self.assertRaises(NotImplementedError, self.testIO.new_poll, self.testPoll)

    def test_close_poll(self):
        self.assertRaises(NotImplementedError, self.testIO.close_poll, self.testPoll)

    def test_add_winner(self):
        self.assertRaises(NotImplementedError, self.testIO.add_winner, self.testBook)

    def test_send_email(self):
        self.assertRaises(NotImplementedError, self.testIO.send_email, 'test@email.com', 'subject', 'body')

    def test_remove_user(self):
        self.assertRaises(NotImplementedError, self.testIO.remove_user, 'some user')

    def test_delete_poll(self):
        self.assertRaises(NotImplementedError, self.testIO.delete_poll, 'doc_id')

if __name__ == '__main__':
    unittest.main()
