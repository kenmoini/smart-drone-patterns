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

    // Handle Wifi Status light
    //wifiStatusInterval = setInterval(wifiStatus, 1000);


    // Handle onclick for the start button
    jQuery( "#startBtn" ).on( "click", function() {
        // Show the workzone
        jQuery("#workZone").removeClass('d-none');
        progressMover("Starting...", 10);
        setTimeout(() => {
            console.log("Delayed for 0.5 second.");
        }, "500");

        progressMover("Initializing camera...", 15);
        
        // Call out to the gopro-control service
        // Swich upon the status, if successful then call out to the s3-shipper service
        var goproData_r = jQuery.get( configData.goproControl.endpoint, function(data) {
            goproData = JSON.parse(data);
            console.log(goproData);
        })
        .done(function(data) {
            goproData = JSON.parse(data);
            if (data.status == "success") {
                console.log("goproData: " + goproData);
                progressMover("Video captured!", 20);
                setTimeout(() => {
                    console.log("Delayed for 0.5 second.");
                }, "500");
                progressMover("Uploading to S3...", 30);
                var s3Data_r = jQuery.get( configData.s3Shipper.endpoint, function(data) {
                    s3Data = JSON.parse(data);
                    console.log(s3Data);
                })
            }
            else {
                progressFail();
            }
        })
        .fail(function() {
            progressFail();
        })
        .always(function() {
            //alert( "finished" );
        });
    });
});