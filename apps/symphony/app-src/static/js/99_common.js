
function progressFail(message) {
    jQuery("#progressMessage strong").text("Failed! " + message);
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
        if (wifiData.activeNetwork.length > 0) {
            if (wifiData.activeNetwork[0][2] == targetAP) {
                console.log("Connected to " + targetAP);
                jQuery("#wifiStatus").removeClass('red').addClass('green');
            } else {
                console.log("Connected to " + wifiData.activeNetwork[0][2]);
                jQuery("#wifiStatus").removeClass('green').addClass('orange');
            }
        } else {
            console.log("Not connected to any AP!");
            jQuery("#wifiStatus").removeClass('green').addClass('red');
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