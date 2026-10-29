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

function logout() {
  document.getElementById("settings-and-logout-form").submit();
}
