/**
 * The function in this script will be called by the Apps Script Execution API.
 */

/**
 * Create a generic test form
 * Has a workaround for issue: https://issuetracker.google.com/issues/36763096
 */
function makeTestForm(email_address) {
  var item = "Test Form";
  var form = FormApp.create(item);
  form.setTitle(item);
  
  item = "Preferred Book";  
  var choices = ["Book1", "Book2", "Book3", "Book4"];  
  var question = form.addMultipleChoiceItem()  
  question.setTitle(item)  
  question.setChoiceValues(choices)  
  question.setRequired(true);
  
  var form_id = form.getId();
  var form_as_file = DriveApp.getFileById(form_id)
  form_as_file.addEditor(email_address)
}