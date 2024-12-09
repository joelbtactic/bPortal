function saveListLayout() {
  var selectedFields = $("#selected-fields li")
    .map(function () {
      return $(this).attr("id");
    })
    .get();

  var data = {
    selectedFields
  };

  $.ajax({
    type: "POST",
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    error(response) {
      alert(response.responseJSON.error);
    },
    success(response) {
      alert(response.msg);
    }
  });
}

function save_layout_layout() {
  var selectedFields = [];

  $("#selected-fields div.row").map(function () {
    selectedFields.push(
      $(this)
        .children("div.col.sortable-ul")
        .map(function () {
          var dropdown = $(this).find("select"); // Find the <select> element
          if (dropdown.length > 0) {
            // Extract the value of the selected option
            return dropdown.val() || "";
          } else {
            return "";
          }
        })
        .get()
    );
  });

  var data = {
    selectedFields
  };

  $.ajax({
    type: "POST",
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    error(response) {
      alert(response.responseJSON.error);
    },
    success(response) {
      alert(response.msg);
    }
  });
}

function remove_layout_row(object) {
  var row = object.parent().parent();
  row.children("div.col.card.sortable-ul").map(function () {
    var children = $(this).children();
    if (children.length > 0) {
      $("#available-fields").append(children);
    }
  });
  row.parent().remove();
}