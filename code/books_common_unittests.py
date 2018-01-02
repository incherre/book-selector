'''This is the unit test file for the books-common.py file.'''

import unittest
import books_common

class TestBookMethods(unittest.TestCase):
    def test_basic_init(self):
        pass #TODO

    def test_full_init(self):
        pass #TODO

    def test_delete(self):
        pass #TODO

    def test_getTitle(self):
        pass #TODO

    def test_getAuthorName(self):
        pass #TODO

    def test_compare(self):
        pass #TODO

class TestUserMethods(unittest.TestCase):
    def test_basic_init(self):
        pass #TODO

    def test_full_init_(self):
        pass #TODO

    def test_getBooks(self):
        pass #TODO

    def test_getUserName(self):
        pass #TODO

    def test_getNumBooks(self):
        pass #TODO

    def test_getFormLink(self):
        pass #TODO

class TestDateMethods(unittest.TestCase):
    def test_basic_init(self):
        pass #TODO

    def test_full_init(self):
        pass #TODO

    def test_getStringDate(self):
        pass #TODO

    def test_getYear(self):
        pass #TODO

    def test_getMonth(self):
        pass #TODO

    def test_getDay(self):
        pass #TODO

    def test_compare(self):
        pass #TODO

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

class BaseLocationWithoutErrorInit(books_common.Location):
    def __init__(self):
        pass

class BaseDataIOWithoutErrorInit(books_common.DataIO):
    def __init__(self):
        pass

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
