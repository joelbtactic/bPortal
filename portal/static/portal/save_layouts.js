function save_list_layout() {
  var selected_fields = $("#selected-fields li")
    .map(function() {
      return $(this).attr("id");
    })
    .get();

  var data = {
    selected_fields: selected_fields
  };

  $.ajax({
    type: "POST",
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    error: function(response) {
      alert(response.responseJSON.error);
    },
    success: function(response) {
      alert(response.msg);
    }
  });
}

function save_layout_layout() {
  var selected_fields = [];
  $("#selected-fields div.row").map(function() {
    selected_fields.push(
      $(this)
        .children("div.col.card.sortable-ul")
        .map(function() {
          var children = $(this).children();
          if (children.length > 0) {
            return children.attr("id");
          } else {
            return "";
          }
        })
        .get()
    );
  });

  var data = {
    selected_fields: selected_fields
  };

  $.ajax({
    type: "POST",
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    error: function(response) {
      alert(response.responseJSON.error);
    },
    success: function(response) {
      alert(response.msg);
    }
  });
}

function add_layout_row() {
  $("#selected_fields_list_group").append(
    '\
        <div class="list-group-item justify-content-between">\
            <div class="row">\
                <div class="col card sortable-ul selected-field ml-2"></div>\
                <div class="col col-2 text-center align-self-center">\
                    <a class="btn btn-danger" href="#" role="button" onclick="remove_layout_row($(this));">\
                        <span class="oi oi-x"></span>\
                    </a>\
                </div>\
            </div>\
        </div>\
    '
  );
  $(".selected-field, #available-fields")
    .sortable({
      connectWith: ".sortable-ul"
    })
    .disableSelection();
  $(".selected-field").each(function() {
    $(this).on("sortreceive", function(event, ui) {
      if ($(this).children().length > 1) {
        $(ui.sender).sortable("cancel");
        var el1 = $(this).children()[0];
        var el2 = $(ui.item)[0];
        $(this).append(el2);
        $(ui.sender).append(el1);
      }
    });
  });
}

function add_layout_row2() {
  $("#selected_fields_list_group").append(
    '\
        <div class="list-group-item justify-content-between">\
            <div class="row">\
                <div class="col card sortable-ul selected-field ml-2"></div>\
                <div class="col card sortable-ul selected-field ml-2"></div>\
                <div class="col col-2 text-center align-self-center">\
                    <a class="btn btn-danger" href="#" role="button" onclick="remove_layout_row($(this));">\
                        <span class="oi oi-x"></span>\
                    </a>\
                </div>\
            </div>\
        </div>\
    '
  );
  $(".selected-field, #available-fields")
    .sortable({
      connectWith: ".sortable-ul"
    })
    .disableSelection();
  $(".selected-field").each(function() {
    $(this).on("sortreceive", function(event, ui) {
      if ($(this).children().length > 1) {
        $(ui.sender).sortable("cancel");
        var el1 = $(this).children()[0];
        var el2 = $(ui.item)[0];
        $(this).append(el2);
        $(ui.sender).append(el1);
      }
    });
  });
}

function remove_layout_row(object) {
  var row = object.parent().parent();
  row.children("div.col.card.sortable-ul").map(function() {
    var children = $(this).children();
    if (children.length > 0) {
      $("#available-fields").append(children);
    }
  });
  row.parent().remove();
}
