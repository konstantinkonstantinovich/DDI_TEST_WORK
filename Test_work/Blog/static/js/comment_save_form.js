$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#comment-create .modal-content").html("");
        $("#comment-create").modal("show");
      },
      success: function (data) {
        $("#comment-create .modal-content").html(data.html_form);
      }
    });
  };

    var sendForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#comment-create").modal("hide");
        }
        else {
          $("#comment-create .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // make contact
  $(".js-comment-create").click(loadForm);
  $("#comment-create").on("submit", ".js-comment-create-form", sendForm);

});