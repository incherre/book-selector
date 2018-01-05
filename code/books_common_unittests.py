'''This is the unit test file for the books-common.py file.'''

import unittest
import books_common

## These classes are implementations of abstract classes for testing purposes
class BaseLocationWithoutErrorInit(books_common.Location):
    def __init__(self):
        pass

class BaseDataIOWithoutErrorInit(books_common.DataIO):
    def __init__(self):
        pass

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

class DataIOAllSuccess(books_common.DataIO):
    '''Anything that returns a success returns true'''
    def __init__(self):
        pass

    def createUser(self, user):
        return True

    def removeBook(self, book):
        return True

    def newPoll(self, poll):
        return True

    def closePoll(self, poll):
        return True

    def addWinner(self, book):
        return True

class DataIOAllFail(books_common.DataIO):
    '''Anything that returns a success returns false'''
    def __init__(self):
        pass

    def createUser(self, user):
        return False

    def removeBook(self, book):
        return False

    def newPoll(self, poll):
        return False

    def closePoll(self, poll):
        return False

    def addWinner(self, book):
        return False

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

    def tearDown(self):
        del self.t_title
        del self.t_authorFname
        del self.t_authorLname
        del self.t_location
        del self.t_data_io

        del self.basicBook
        del self.succeedBook
        del self.failBook
    
    def test_init(self):
        testVar = books_common.Book(self.t_title, self.t_authorFname, self.t_authorLname, self.t_location, self.t_data_io)
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
            testVar = books_common.Book(self.t_title,  self.t_authorFname, self.t_authorLname, None, self.t_data_io)

    def test_init_fail_invalid_data_io(self):
        with self.assertRaises(TypeError):
            testVar = books_common.Book(self.t_title,  self.t_authorFname, self.t_authorLname, self.t_location, None)
        
    def test_delete(self):
        self.assertTrue(self.succeedBook.delete())
        self.assertFalse(self.failBook.delete())

    def test_getTitle(self):
        self.assertEqual(self.basicBook.getTitle(), self.t_title)

    def test_getAuthorName(self):
        author = self.t_authorFname + " " + self.t_authorLname
        self.assertEqual(self.basicBook.getAuthorName(), author)

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
        self.t_books = [abook]
        self.t_formLink = "www.example.com"

        self.t_user = books_common.User(self.t_userName, self.t_books, self.t_formLink)

    def tearDown(self):
        del self.t_userName
        del self.t_books
        del self.t_formLink

        del self.t_user
    
    def test_init(self):
        testVar = books_common.User(self.t_userName, self.t_books, self.t_formLink)
        self.assertIsInstance(testVar, books_common.User)

    def test_init_fail_invalid_userName(self):
        with self.assertRaises(TypeError):
            testVar = books_common.User(None, self.t_books, self.t_formLink)

    def test_init_fail_invalid_books(self):
        with self.assertRaises(TypeError):
            testVar = books_common.User(self.t_userName, None, self.t_formLink)

    def test_init_fail_invalid_formLink(self):
        with self.assertRaises(TypeError):
            testVar = books_common.User(self.t_userName, self.t_books, None)

    def test_getBooks(self):
        maybe_books = self.t_user.getBooks()
        self.assertIsInstance(maybe_books, list)
        self.assertEqual(len(maybe_books), 1)
        self.assertTrue(maybe_books[0].compare(self.t_books[0]))

    def test_getUserName(self):
        self.assertEqual(self.t_user.getUserName(), self.t_userName)

    def test_getNumBooks(self):
        self.assertEqual(self.t_user.getNumBooks(), len(self.t_books))

    def test_getFormLink(self):
        self.assertEqual(self.t_user.getFormLink(), self.t_formLink)

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

    def test_getStringDate(self):
        self.assertEqual(self.t_date.getStringDate(), self.t_strDate)

    def test_getYear(self):
        self.assertEqual(self.t_date.getYear(), self.t_year)

    def test_getMonth(self):
        self.assertEqual(self.t_date.getMonth(), self.t_month)

    def test_getDay(self):
        self.assertEqual(self.t_date.getDay(), self.t_day)

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
    def test_basic_init(self):
        pass #TODO

    def test_full_init(self):
        pass #TODO

    def test_getWinner(self):
        pass #TODO

    def test_closeVoting(self):
        pass #TODO

    def test_getFormLink(self):
        pass #TODO

    def test_getOptions(self):
        pass #TODO

    def test_getDate(self):
        pass #TODO

    def test_updateResults(self):
        pass #TODO

class TestLocationMethods(unittest.TestCase):
    def test_basic_init(self):
        with self.assertRaises(NotImplementedError):
            testVar = books_common.Location()

    def test_compare(self):
        testLoc1 = BaseLocationWithoutErrorInit()
        testLoc2 = BaseLocationWithoutErrorInit()
        with self.assertRaises(NotImplementedError):
            testLoc1.compare(testLoc2)     

class TestDataIOMethods(unittest.TestCase):
    def test_basic_init(self):
        with self.assertRaises(NotImplementedError):
            testVar = books_common.DataIO()

    def setUp(self):
        self.testIO = BaseDataIOWithoutErrorInit()
        self.testBook = books_common.Book("Title", "Sarah", "Smith", BaseLocationWithoutErrorInit(), BaseDataIOWithoutErrorInit())
        self.testPoll = books_common.Poll([self.testBook, self.testBook], [0, 0], "www.example.com", books_common.Date(2000, 1, 1), BaseDataIOWithoutErrorInit())

    def tearDown(self):
        del self.testIO
        del self.testBook
        del self.testPoll

    def test_getUserNames(self):
        self.assertRaises(NotImplementedError, self.testIO.getUserNames)

    def test_getUserInfo(self):
        self.assertRaises(NotImplementedError, self.testIO.getUserInfo, "uName")

    def test_getUserBooks(self):
        self.assertRaises(NotImplementedError, self.testIO.getUserBooks, "uName")

    def test_getHistory(self):
        self.assertRaises(NotImplementedError, self.testIO.getHistory)

    def test_getCurrentPoll(self):
        self.assertRaises(NotImplementedError, self.testIO.getCurrentPoll)

    def test_createUser(self):
        self.assertRaises(NotImplementedError, self.testIO.createUser, "uName")

    def test_removeBook(self):
        self.assertRaises(NotImplementedError, self.testIO.removeBook, self.testBook)

    def test_newPoll(self):
        self.assertRaises(NotImplementedError, self.testIO.newPoll, self.testPoll)

    def test_closePoll(self):
        self.assertRaises(NotImplementedError, self.testIO.closePoll, self.testPoll)

    def test_addWinner(self):
        self.assertRaises(NotImplementedError, self.testIO.addWinner, self.testBook)

if __name__ == '__main__':
    unittest.main()
