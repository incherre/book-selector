'''The main file for the book club program.'''
import books_common
import google_api

class MenuItem:
    '''A selectable item in a text based menu.'''

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def get_name(self):
        '''Returns the display name of the item.'''
        return self.name

    def execute(self):
        '''Executes the item.'''
        return self.function()

class GoBackItem(MenuItem):
    '''An item to return to a higher menu level.'''

    def __init__(self, name):
        super().__init__(name, self.go_up)
        self.higher = None

    def set_higher(self, higher):
        '''Sets the higher level menu to return to.'''
        self.higher = higher

    def go_up(self):
        '''Returns to the higher level menu.'''
        self.higher.execute()

class HighLevelMenu(MenuItem):
    '''A list of menu items.'''

    def __init__(self, name, options):
        super().__init__(name, self.execute_choice)
        self.options = options

    def display_options(self):
        '''Displays the possible selections.'''
        print('\n%s:' % (self.name))
        option_num = 1
        for option in self.options:
            print('%2d) %s' % (option_num, option.get_name()))
            option_num += 1

    def execute_choice(self):
        '''Allows the user to choose and execute their choice.'''
        choice = 0
        while not (choice > 0 and choice <= len(self.options)):
            self.display_options()
            try:
                choice = int(input('Please enter the number of your choice: '))
            except ValueError:
                print('Please enter an integer')
                choice = 0
            else:
                if not (choice > 0 and choice <= len(self.options)):
                    print('Please enter a number that appears on the menu')
        self.options[choice - 1].execute()

class DynamicMenu(MenuItem):
    '''A menu that generates the items.'''

    def __init__(self, name, option_gen, other_options):
        super().__init__(name, self.execute_choice)
        self.option_gen = option_gen
        self.other_options = other_options
        self.options = None

    def display_options(self):
        '''Generates and displays the current opions.'''
        print('\n%s:' % (self.name))
        self.options = self.option_gen()
        option_num = 1
        for option in self.options:
            print('%2d) %s' % (option_num, option.get_name()))
            option_num += 1

        for option in self.other_options:
            print('%2d) %s' % (option_num, option.get_name()))
            option_num += 1

    def execute_choice(self):
        '''Allows the user to choose and execute their choice.'''
        choice = 0
        while not (choice > 0 and choice <= len(self.options) + len(self.other_options)):
            self.display_options()
            try:
                choice = int(input('Please enter the number of your choice: '))
            except ValueError:
                print('Please enter an integer')
                choice = 0
            else:
                if not (choice > 0 and choice <= len(self.options) + len(self.other_options)):
                    print('Please enter a number that appears on the menu')

        true_choice = choice - 1
        if true_choice < len(self.options):
            self.options[true_choice].execute()
        elif true_choice >= len(self.options):
            true_choice -= len(self.options)
            self.other_options[true_choice].execute()

def make_lambda(function, *args, **kwargs):
    '''Makes a static lambda fuction for some input.'''
    return lambda: function(*args, **kwargs)

if __name__ == '__main__':
    #----- Initialization -----
    CRED_PATH = './creds/book-selector-key.json'
    CLINT_SECRET_PATH = './creds/book-selector-userauth-key.json'
    APP_NAME = 'Book Club'
    CRED_NAME = 'bc-creds.json'
    SCRIPT_ID = 'MnjtpoV6LOWSqGbn-qvMxHji8zG_MrsiO'

    BOOK_BOT = google_api.GoogleDocsBot(CRED_PATH, CLINT_SECRET_PATH,
                                        CRED_NAME, SCRIPT_ID)

    USERS = {}
    #----- End Initialization -----

    #----- External Functionality -----
    def view_poll_info():
        '''Displays the info for the current poll.'''
        possible_errors = (google_api.errors.HttpError,
                           google_api.AppsScriptError,
                           google_api.SpreadsheetFormatError)
        try:
            current_poll = BOOK_BOT.get_current_poll()
        except possible_errors:
            print('Failed to retrieve current poll')
        else:
            if current_poll is None:
                print('There is no currently active poll')
            else:
                print('Current Poll:')
                print(' Date created: %s' % (current_poll.get_date().get_string_date()))
                print(' Options:')
                for book in current_poll.get_options():
                    print('  "%s" by %s' % (book.get_title(), book.get_author_name()))

    def start_new_poll():
        '''Deletes the old poll and begins a new poll.'''
        print('new poll started')
        #TODO(incherre): Add functionality

    def close_poll():
        '''Stops the current poll from accepting new responses.'''
        print('poll closed')
        #TODO(incherre): Add functionality

    def add_new_user():
        '''Adds a new user.'''
        print('new user added')
        #TODO(incherre): Add functionality

    def view_history():
        '''Displays the history.'''
        possible_errors = (google_api.errors.HttpError,
                           google_api.AppsScriptError,
                           google_api.SpreadsheetFormatError)
        try:
            history = BOOK_BOT.get_history()
        except possible_errors:
            print('Failed to retrieve history')
            histroy = []

        for record in history:
            print('%s: "%s" by %s %s' % tuple(record))

    def delete_user(user):
        '''Removes a user from the records.'''
        possible_errors = (google_api.errors.HttpError,
                           google_api.AppsScriptError,
                           google_api.SpreadsheetFormatError)

        try:
            BOOK_BOT.remove_user(user)
        except possible_errors:
            print('Failed to remove user')
        else:
            print(user.get_user_name() + ' removed')

    def remove_all_books(user):
        '''Removes all the books of a user.'''
        #TODO(incherre): Add functionality
        print(user.get_user_name() + "'s books removed")

    def remove_book(book):
        '''Removes the book from the records.'''
        possible_errors = (TypeError,
                           google_api.errors.HttpError,
                           google_api.AppsScriptError)
        try:
            book.delete()
        except possible_errors:
            print('Book deletion failed')
        else:
            print(book.get_title() + ' removed')
    #----- End External Functionality -----

    #----- Define Menu Structure -----
    def book_gen(go_up, user):
        '''Generates a list of book menu objects.'''
        possible_errors = (google_api.errors.HttpError,
                           google_api.AppsScriptError,
                           google_api.SpreadsheetFormatError)
        try:
            books = BOOK_BOT.get_user_books(user)
        except possible_errors:
            print('Failed to retrieve books')
            books = []

        book_delete_options = []

        for book in books:
            temp_option = MenuItem('Delete "%s" by %s' % (book.get_title(), book.get_author_name()),
                                   make_lambda(remove_book, book))
            book_delete_options.append(temp_option)

        return book_delete_options

    def user_gen(go_up):
        '''Generates a list of user menu objects.'''
        possible_errors = (google_api.errors.HttpError,
                           google_api.AppsScriptError,
                           google_api.SpreadsheetFormatError)
        try:
            user_names = BOOK_BOT.get_user_names()
        except possible_errors:
            print('Failed to retrieve user list')
            user_names = []

        user_menus = []

        for name in user_names:
            valid_user = True
            if not name in USERS:
                try:
                    USERS[name] = BOOK_BOT.get_user_info(name)
                except possible_errors:
                    print("Failed to retrieve %s's info" % (name))
                    valid_user = False

            if valid_user:
                gen_book_function = make_lambda(book_gen, go_up, USERS[name])
                temp_remove_book = DynamicMenu("Remove one of %s's books" % (name),
                                               gen_book_function, [go_up])

                remove_books_function = make_lambda(remove_all_books, USERS[name])
                temp_remove_books = MenuItem("Remove all of %s's books" % (name),
                                             remove_books_function)

                del_user_function = make_lambda(delete_user, USERS[name])
                temp_del_user = MenuItem('Delete %s' % (name), del_user_function)

                temp_menu = HighLevelMenu(name, [temp_remove_book, temp_remove_books,
                                                 temp_del_user, go_up])
                user_menus.append(temp_menu)

        return user_menus

    VIEW_POLL = MenuItem('View poll info', view_poll_info)
    START_POLL = MenuItem('Start a new poll', start_new_poll)
    END_POLL = MenuItem('Close the current poll', close_poll)
    NEW_USER = MenuItem('Add a new user', add_new_user)
    HISTORY = MenuItem('View history', view_history)
    RETURN_TL = MenuItem('Go back', lambda: None)
    RETURN_USER = GoBackItem('Go back')
    USER_OPTION = DynamicMenu('Manage users', make_lambda(user_gen, RETURN_USER), [RETURN_TL])
    RETURN_USER.set_higher(USER_OPTION)
    EXIT_OPTION = MenuItem('Exit', exit)

    TOP_LEVEL = HighLevelMenu('The Book Club', [VIEW_POLL, START_POLL, END_POLL,
                                                NEW_USER, USER_OPTION, HISTORY,
                                                EXIT_OPTION])
    #----- End Define Menu Structure -----

    while True:
        TOP_LEVEL.execute()
