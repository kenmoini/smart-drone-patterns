jQuery( document ).ready(function() {
    // Disable dollar sign shortcut handling
    jQuery.noConflict();

    // Call out to internal configuration endpoint
    var configData_r = jQuery.get( "/config", function(data) {
        configData = JSON.parse(data);
    })
    .done(function() {
        //alert( "second success" );
    })
    .fail(function() {
        alert( "error loading configuration data!" );
    })
    .always(function() {
        //alert( "finished" );
    });

    // Handle onclick for the start button
    jQuery( "#startBtn" ).on( "click", function() {
        // Show the workzone
        jQuery("#workZone").removeClass('d-none');
        jQuery("#progressMessage strong").text("Starting...");
        jQuery("#progressBar .progress-bar").css('width', '10%');
        jQuery("#progressMessage strong").text("Starting...");
        setTimeout(() => {
            console.log("Delayed for 0.5 second.");
        }, "500");

        jQuery("#progressMessage strong").text("Initializing camera...");
        jQuery("#progressBar .progress-bar").css('width', '15%');
        
        // Call out to the gopro-control service
        // Swich upon the status, if successful then call out to the s3-shipper service
        var goproData_r = jQuery.get( configData.goproControl.endpoint, function(data) {
            goproData = JSON.parse(data);
            console.log(goproData);

            alert( "success" );
        })
        .done(function() {
            //alert( "second success" );
        })
        .fail(function() {
            progressFail();
        })
        .always(function() {
            //alert( "finished" );
        });
    });
});