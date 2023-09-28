
function progressFail() {
    jQuery("#progressMessage strong").text("Failed!");
    jQuery("#progressBar .progress-bar").removeClass('bg-primary').addClass('bg-danger').css('width', '100%');
}

function progressMover(text, percent) {
    jQuery("#progressMessage strong").text(text);
    jQuery("#progressBar .progress-bar").css('width', percent + '%');
}

function checkWifiStatus(targetAP) {
    var statusData_r = jQuery.get( configData.wifiStatus.endpoint, function(data) {
        wifiData = JSON.parse(data);
        console.log(wifiData);
    })
    .done(function(data) {
        wifiData = JSON.parse(data);
        if (wifiData.status == "success") {
            console.log("wifiData: " + wifiData);
        }
        else {
            //progressFail();
        }
    })
    .fail(function() {
        progressFail();
        alert("error loading wifi status data!");
    })
    .always(function() {
        //alert( "finished" );
    });
}