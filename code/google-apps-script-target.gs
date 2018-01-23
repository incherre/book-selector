/**
 * The functions in this script will be called by the Apps Script Execution API.
 */

new_book_title_prompt = "New book title"
new_book_authorfn_prompt = "New book author's first name"
new_book_authorln_prompt = "New book author's last name"

/**
 * Retrieves the user's email
 */

function getEmail() {
  return Session.getActiveUser().getEmail();
}

/**
 * Create a form used to enter new book suggestions.
 * Fixes https://issuetracker.google.com/issues/36763096
 */

function makeBooksForm(service_email, user_name) {
  var temp_str = user_name + "'s Book Suggestion Input";
  var input_form = FormApp.create(temp_str);
  input_form.setTitle(temp_str);
  
  temp_str = new_book_title_prompt;
  var temp_question = input_form.addTextItem();
  temp_question.setTitle(temp_str);
  temp_question.setHelpText(temp_str);
  temp_question.setRequired(true);
  
  temp_str = new_book_authorfn_prompt;
  temp_question = input_form.addTextItem();
  temp_question.setTitle(temp_str);
  temp_question.setHelpText(temp_str);
  temp_question.setRequired(true);
  
  temp_str = new_book_authorln_prompt;
  temp_question = input_form.addTextItem();
  temp_question.setTitle(temp_str);
  temp_question.setHelpText(temp_str);
  temp_question.setRequired(true);
  
  // Emails can't be delivered to a service account.
  // There's an annoying "failed to deliver email" email that is sent to the user if it tries.
  var form_id = input_form.getId();
  Drive.Permissions.insert(
    {
      'role': 'writer',
      'type': 'user',
      'value': service_email
    },
    form_id,
    {
      'sendNotificationEmails': 'false' //The normal way of adding editors doesn't have this option
    }
  );
  
  var form_url = input_form.getPublishedUrl();
  
  return {form_id: form_id, form_url: form_url};
}

/**
 * Create a form used as a poll.
 * Fixes https://issuetracker.google.com/issues/36763096
 */

function makePollForm(service_email, options) {
  var temp_str = "Next Month's Book Poll";
  var input_form = FormApp.create(temp_str);
  input_form.setTitle(temp_str);
  input_form.setLimitOneResponsePerUser(true)
  
  var question = input_form.addMultipleChoiceItem();
  question.setTitle("Which book would you prefer to read?");
  question.setChoiceValues(options)
  question.showOtherOption(false);
  question.setRequired(true);
  
  // Emails can't be delivered to a service account.
  // There's an annoying "failed to deliver email" email that is sent to the user if it tries.
  var form_id = input_form.getId();
  Drive.Permissions.insert(
    {
      'role': 'writer',
      'type': 'user',
      'value': service_email
    },
    form_id,
    {
      'sendNotificationEmails': 'false' //The normal way of adding editors doesn't have this option
    }
  );
  
  var form_url = input_form.getPublishedUrl();
  
  return {form_id: form_id, form_url: form_url};
}

/**
 * Reads responses from a book form
 */

function getBookList(form_id) {
  var books = [];
  
  var form = FormApp.openById(form_id);
  var formResponses = form.getResponses();
  for (var i = 0; i < formResponses.length; i++) {
    var temp_book = {};
    
    var formResponse = formResponses[i];
    temp_book['formResponseId'] = formResponse.getId();
    
    var itemResponses = formResponse.getItemResponses();
    for (var j = 0; j < itemResponses.length; j++) {
      var itemResponse = itemResponses[j];
      var itemTitle = itemResponse.getItem().getTitle();
      
      if (itemTitle == new_book_title_prompt) {
        temp_book['title'] = itemResponse.getResponse().toString();
      } else if (itemTitle == new_book_authorfn_prompt) {
        temp_book['authorFirstName'] = itemResponse.getResponse().toString();
      } else if (itemTitle == new_book_authorln_prompt) {
        temp_book['authorLastName'] = itemResponse.getResponse().toString();
      }
    }
    
    books.push(temp_book);
  }
  
  return books;
}
