
function progressFail() {
    jQuery("#progressMessage strong").text("Failed!");
    jQuery("#progressBar .progress-bar").removeClass('bg-primary').addClass('bg-danger').css('width', '100%');
}