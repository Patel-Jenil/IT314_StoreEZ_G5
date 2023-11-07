$(function() {
  $('#date').datepicker({
    dateFormat: 'dd-M-yy',
    minDate: 1
  });
  
  $('.date-icon').on('click', function() {
    $('#date').focus();
  })
});