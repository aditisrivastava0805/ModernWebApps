// Requirement 5.2
function validate_data() {
  var search_select = document.getElementById("search_select").value;
  var search_input = document.getElementById("search_input").value.trim();

  if (search_select === "Date" && !/^\d{2}\/\d{2}\/\d{4}$/.test(search_input)) {
    alert("Date format should be MM/DD/YYYY");
    return false;
  }
  if (search_select === "Name" && search_input === "") {
    alert("Name should not be empty");
    return false;
  }
  if (search_select === "Tags" && search_input === "") {
    alert("Tags should not be empty");
    return false;
  }
  return true;
}

function show_photo_details(photo_name, date_taken, tags) {
  alert("Photo:" + photo_name + " date_taken:" + date_taken + " tags:" + tags);
}

var slide_show_timer = null;
var slide_show_photo_names = [];
var slide_show_index = 0;

function display_photo(photo_names, index) {
  if (!photo_names || photo_names.length === 0) {
    document.getElementById("slideshow-display").innerHTML = "";
    return;
  }

  var photo_name = photo_names[index];
  document.getElementById("slideshow-display").innerHTML =
    '<img src="/static/images/photos/' + photo_name + '" style="max-width:100%; max-height:250px;">';
}

function start_slide_show() {
  fetch("/photos")
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      var photo_rows = data.photos || [];
      slide_show_photo_names = photo_rows.map(function (row) {
        return JSON.parse(row).name;
      });

      if (slide_show_photo_names.length === 0) {
        document.getElementById("slideshow-display").innerHTML = "";
        return;
      }

      slide_show_index = 0;
      display_photo(slide_show_photo_names, slide_show_index);

      if (slide_show_timer) {
        clearInterval(slide_show_timer);
      }

      slide_show_timer = setInterval(function () {
        slide_show_index = (slide_show_index + 1) % slide_show_photo_names.length;
        display_photo(slide_show_photo_names, slide_show_index);
      }, 3000);
    });
}

function stop_slide_show() {
  if (slide_show_timer) {
    clearInterval(slide_show_timer);
    slide_show_timer = null;
  }
}


// Requirement 4.3 - Implement the preview_photo method that displays the photo in modal
function preview_photo(photo_name) {
  document.getElementById("image-modal-body").innerHTML =
    '<img src="/static/images/photos/' + photo_name + '" class="img-fluid">';
  $('#imageModal').modal('show');
}


function show_settings() {
  alert("Settings called.");
}

function open_update_tags_modal() {
  var selected_photo = document.querySelector('input[name="selected_photo"]:checked');
  if (!selected_photo) {
    return;
  }

  var photo_name = selected_photo.value;
  fetch("/photos/" + encodeURIComponent(photo_name) + "/tags")
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      var current_tags = data.tags || "";
      document.getElementById("update_tags_photo_name").value = photo_name;
      document.getElementById("new_tags").value = current_tags;
      document.getElementById("update-tags-current").textContent =
        photo_name + " Current tags: " + current_tags;
      $('#updateTagsModal').modal('show');
    });
}

function delete_selected_photo() {
  var selected_photo = document.querySelector('input[name="selected_photo"]:checked');
  if (!selected_photo) {
    return;
  }

  document.getElementById("delete_photo_name").value = selected_photo.value;
  document.getElementById("delete-photo-form").submit();
}

function logout() {
  document.getElementById("settings-and-logout-form").submit();
}
