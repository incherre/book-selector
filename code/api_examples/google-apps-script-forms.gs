/**
 * The function in this script will be called by the Apps Script Execution API.
 */

/**
 * Create a generic test form
 */

function makeTestForm(email_address) {
  var item = "Test Form";
  var form = FormApp.create(item);
  form.setTitle(item);
  
  item = "Preferred Book";  
  var choices = ["Book1", "Book2", "Book3", "Book4"];  
  var question = form.addMultipleChoiceItem();
  question.setTitle(item);
  question.setChoiceValues(choices);
  question.setRequired(true);
  
  var form_id = form.getId();
  var form_as_file = DriveApp.getFileById(form_id);
  form_as_file.addEditor(email_address);
  
  return form_id;
}

/**
 * Create a form used to enter new book suggestions.
 * Fixes https://issuetracker.google.com/issues/36763096
 */

function makeBooksForm(service_email, user_email, user_name) {
  var temp_str = user_name + "'s Book Suggestion Input";
  var input_form = FormApp.create(temp_str);
  input_form.setTitle(temp_str);
  
  temp_str = "New book title";
  var temp_question = input_form.addTextItem();
  temp_question.setTitle(temp_str);
  temp_question.setHelpText(temp_str);
  temp_question.setRequired(true);
  
  temp_str = "New book author's first name";
  temp_question = input_form.addTextItem();
  temp_question.setTitle(temp_str);
  temp_question.setHelpText(temp_str);
  temp_question.setRequired(true);
  
  temp_str = "New book author's last name";
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