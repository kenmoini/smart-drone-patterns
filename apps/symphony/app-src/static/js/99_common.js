
function progressFail() {
    jQuery("#progressMessage strong").text("Failed!");
    jQuery("#progressBar .progress-bar").removeClass('bg-primary').addClass('bg-danger').css('width', '100%');
}

function progressMover(text, percent) {
    jQuery("#progressMessage strong").text(text);
    jQuery("#progressBar .progress-bar").css('width', percent + '%');
}