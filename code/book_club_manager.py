'''The main file for the book club program.'''
import string

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

#----- Adapted from the work of Peter Norvig at http://norvig.com/spell-correct.html -----
def edits1(word, letters):
    "All edits that are one edit away from `word`."
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word, letters):
    "All edits that are two edits away from `word`."
    return set(e2 for e1 in edits1(word, letters) for e2 in edits1(e1, letters))
#----- End adapted spell check code

def get_conf(file_name):
    try:
        f = open(file_name)
    except IOError:
        print('Unable to open configuration file')
        return None

    conf = {}
    for line in f:
        if line and line[0] != '#':
            fields = line.strip().split(' : ')
            if len(fields) == 2:
                conf[fields[0]] = fields[1]
            else:
                print('Malformed configuration: %s' % line)

    f.close()
    return conf

if __name__ == '__main__':
    #----- Initialization -----
    CONF = get_conf('./book-club.conf')
    print(str(CONF))

    if 'CRED_PATH' in CONF:
        CRED_PATH = CONF['CRED_PATH']
    else:
        print('Missing configuration: CRED_PATH')
        exit()

    if 'CLINT_SECRET_PATH' in CONF:
        CLINT_SECRET_PATH = CONF['CLINT_SECRET_PATH']
    else:
        print('Missing configuration: CLINT_SECRET_PATH')
        exit()

    if 'APP_NAME' in CONF:
        APP_NAME = CONF['APP_NAME']
    else:
        print('Missing configuration: APP_NAME')
        exit()

    if 'CRED_NAME' in CONF:
        CRED_NAME = CONF['CRED_NAME']
    else:
        print('Missing configuration: CRED_NAME')
        exit()

    if 'SCRIPT_ID' in CONF:
        SCRIPT_ID = CONF['SCRIPT_ID']
    else:
        print('Missing configuration: SCRIPT_ID')
        exit()

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
            return

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
        possible_errors = (google_api.errors.HttpError,
                           google_api.AppsScriptError,
                           google_api.SpreadsheetFormatError)
        try:
            current_poll = BOOK_BOT.get_current_poll()
        except possible_errors:
            print('Failed to retrieve current poll')
            return False

        try:
            current_poll.delete()
        except possible_errors:
            print('Failed to remove the poll')
            return False
        else:
            print('Closed the current poll')
            return True

    def select_winner():
        '''Closes a poll and selects a winner. Emails the winner to everyone.'''
        if not close_poll():
            return

        print('winner selected')
        #TODO(incherre): Complete functionality

    def add_new_user():
        '''Adds a new user.'''
        possible_errors = (google_api.errors.HttpError,
                           google_api.AppsScriptError,
                           google_api.SpreadsheetFormatError)
        try:
            user_names = BOOK_BOT.get_user_names()
        except possible_errors:
            print('Failed to retrieve list of existing users')
            print('User creation can not proceed')
            return

        allowable_chars = string.ascii_letters + string.digits + '_-'
        valid = False
        while not valid:
            new_user_name = input("Enter the new user's username: ").strip()

            valid = True
            for char in new_user_name:
                if not char in allowable_chars:
                    valid = False
                    print('"%s" is not allowed in usernames' % (char))

            if valid: #don't check this if it's already been invalidated
                check_name = new_user_name.lower()
                one_edit = edits1(check_name, allowable_chars)
                two_edits = edits2(check_name, allowable_chars)
                for name in user_names:
                    l_name = name.lower()
                    if l_name == check_name or l_name in one_edit or l_name in two_edits:
                        valid = False
                        print('New username, %s, too similar' % (check_name),
                              'to existing username %s' % (name))

        valid = False
        while not valid:
            new_user_email = input("Enter the new user's email address: ").strip()

            split_email = new_user_email.split('@')
            if len(split_email) < 2:
                print('Malformed email address')
            else:
                split_domain = split_email[-1].split('.')
                if len(split_domain) < 2:
                    print('Malformed email adddress')
                else:
                    valid = True

        try:
            new_user = BOOK_BOT.create_user(new_user_name, new_user_email)
        except possible_errors:
            print('Failed to create user')
            return
        else:
            print('User created')

        subject = 'Welcome to %s' % (APP_NAME)
        body = 'You have been created an account for %s.\n' % (APP_NAME)
        body += 'Your username is %s.\n' % (new_user_name)
        body += 'The link to your book input form is %s.\n' % (new_user.get_form_link())

        try:
            BOOK_BOT.send_email(new_user_email, subject, body)
        except possible_errors:
            print("Failed to send account details to the user's email")
        else:
            print('Account details emailed')

    def view_history():
        '''Displays the history.'''
        possible_errors = (google_api.errors.HttpError,
                           google_api.AppsScriptError,
                           google_api.SpreadsheetFormatError)
        try:
            history = BOOK_BOT.get_history()
        except possible_errors:
            print('Failed to retrieve history')
            history = []

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
