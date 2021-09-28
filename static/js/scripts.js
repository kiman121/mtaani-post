$(document).ready(() => {
  $("#users_table tbody").on("click", "a.admin-edit-user", function (e) {
    // const userId = $(this).data("userid");
    const userId = $(this).parents(".edit-delete-user").data("userid");

    $.ajax({
      url: `/profile/${userId}/`,
      dataType: "json",
      success: function (data) {
        $("#id_first_name").val(data.first_name);
        $("#id_other_name").val(data.other_name);
        $("#id_email").val(data.email);
        $("#id_phone_number").val(data.phone_number);
        $("#id_username").val(data.username);
        $("#id_user_type").val(data.user_type).change();
        $("#id_neighbourhood").val(data.neighbourhood).change();
        $("#edit_user_profile").modal("show");
        $("#edit_user_profile form").attr(
          "href",
          `/edit-user/${userId}/?next=/users/`
        );
      },
    });
  });
  // /edit-user/88b4f671-5ddc-47ae-90ba-c5eb74b211a5/?next=/profile/
  // {% url 'edit-user' user.id %}?next={{request.path}}
  $("#neighbourhood_table tbody").on(
    "click",
    "a.edit-neighbourhood",
    function (e) {
      const neighbourhoodId = $(this)
        .parents(".edit-delete-neighbourhood")
        .data("neighbourhoodid");
      $.ajax({
        url: `/neighbourhood/neighbourhood/${neighbourhoodId}/`,
        dataType: "json",
        success: function (data) {
          console.log(data);
        },
      });
    }
  );
});
