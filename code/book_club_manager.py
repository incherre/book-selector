'''The main file for the book club program.'''

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
                choice = 0
        self.options[choice - 1].execute()

if __name__ == '__main__':
    def view_poll_info():
        '''Displays the info for the current poll.'''
        print('poll info')

    def start_new_poll():
        '''Deletes the old poll and begins a new poll.'''
        print('new poll started')

    def close_poll():
        '''Stops the current poll from accepting new responses.'''
        print('poll closed')

    def add_new_user():
        '''Adds a new user.'''
        print('new user added')

    def view_history():
        '''Displays the history.'''
        print('history')

    VIEW_POLL = MenuItem('View poll info', view_poll_info)
    START_POLL = MenuItem('Start a new poll', start_new_poll)
    END_POLL = MenuItem('Close the current poll', close_poll)
    NEW_USER = MenuItem('Add a new user', add_new_user)
    HISTORY = MenuItem('View history', view_history)
    EXIT_OPTION = MenuItem('Exit', exit)

    TOP_LEVEL = HighLevelMenu('The Book Club', [VIEW_POLL, START_POLL, END_POLL,
                                                NEW_USER, HISTORY, EXIT_OPTION])

    while True:
        TOP_LEVEL.execute()
