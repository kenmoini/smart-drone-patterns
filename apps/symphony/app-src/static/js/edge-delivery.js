var configData = {};

const goodStatuses = [200, 202, 301, 302, 304, 307, 308];

function processInferenceJSONData(jsonDataEndpoint) {
    jQuery.get( jsonDataEndpoint, function(data) {
        predictionJSONData = JSON.parse(data);
        console.log(predictionJSONData);

        jQuery("#rawJsonContainer").removeClass('d-none');
        jQuery("#detectedItemCountContainer").removeClass('d-none');
        // Loop through the frames
        objectCounts = {};
        frames = predictionJSONData.frames;
        for(let i = 0; i < frames.length; i++) {
            let obj = frames[i];
            // Assuming that the video is 15 seconds long and 30 frames per second,
            // we can calculate the delay of feedback output as:
            // 15 seconds * 30 frames per second = 450 frames
            // 15000 milliseconds / 450 frames = 33.333 milliseconds per frame
            
            // Append the raw JSON data
            setTimeout(() => {
                jQuery("pre#rawJson").append( JSON.stringify(obj['objects']) + ',\n' );
            }, 33 );

            // Now we'll loop through the objects and increase the individual counts
            for(let o = 0; o < obj.objects.length; o++) {
                let objName = obj.objects[o].class;
                if (objectCounts[objName] == undefined) {
                    objectCounts[objName] = 1;
                } else {
                    objectCounts[objName] = objectCounts[objName] + 1;
                }
            }

            // Now we'll loop through the object counts and display them
            itemCountHTML = '';
            for (const [key, value] of Object.entries(objectCounts)) {
                itemCountHTML = itemCountHTML + '<li><strong id="' + key + '">' + key + ':</strong> ' + value + '</li>';
            }
            jQuery("#detectedItemCountHolder").html(itemCountHTML);
        }
    });
}

//function curlUntilSuccess(endpoint) {
//    jQuery.get( endpoint )
//    .always(function(data, textStatus, xhr) {
//
//        console.log("curlLoop textStatus: " + textStatus);
//        if (goodStatuses.includes(xhr.status)) {
//            if (textStatus == "success") {
//                // The data is finally available, let's display it
//                progressMover("Model inference complete!", 80);
//                setTimeout(() => {
//                    console.log("Delayed for 1 second.");
//                }, "1000");
//
//                // Display the video
//                inferredVideoHTML = '<video id="inferredVideo" class="card-img-top" controls autoplay muted playsinline><source src="' + configData.s3PublicEndpoint + '/'+ configData.goproControl.targetBucket +'-predictions/pred_' + goproData.video_file + '" type="video/mp4"></video>';
//                jQuery("#inferredVideoContainer").removeClass('d-none');
//                jQuery("#inferredVideoHolder").html(inferredVideoHTML);
//
//                // Get the endpoint for the JSON data
//                jsonDataEndpoint = predictionEndpoint.replace(/\.[^/.]+$/, "") + '.json';
//
//                // Load the prediction data
//                processInferenceJSONData(jsonDataEndpoint);
//                progressMover("Output complete!", 100);
//            }
//        } else {
//            setTimeout(function() {
//                curlUntilSuccess(endpoint);
//            }, 1000);
//        }
//    });
//}

jQuery( document ).ready(function() {
    // Disable dollar sign shortcut handling
    jQuery.noConflict();

    // Call out to internal configuration endpoint
    var configData_r = jQuery.get( "/config", function(data) {
        configData = JSON.parse(data);
    })
    .done(function() {
        //alert( "second success" );

        // Handle Wifi Status light
        wifiStatusInterval = setInterval(checkWifiStatus, 2000, configData.goproControl.targetAP);
    })
    .fail(function() {
        alert( "error loading configuration data!" );
    })
    .always(function() {
        //alert( "finished" );
    });

    // Handle onclick for the start button
    jQuery( "#startBtn" ).on( "click", function() {
        // Hide the start button
        jQuery("#startBtn").addClass('d-none');
        
        loaderHTML = jQuery("#hiddenLoader").html();

        // Show the workzone
        jQuery("#workZone").removeClass('d-none');
        progressMover("Starting...", 10);
        setTimeout(() => {
            console.log("Delayed for 0.5 second.");
        }, "500");

        progressMover("Initializing camera recording...", 15);
        
        // Call out to the gopro-control service
        // Swich upon the status, if successful then call out to the s3-shipper service
        var goproData_r = jQuery.get( configData.goproControl.endpoint, function(data) {
            goproData = JSON.parse(data);
            console.log(goproData);
        })
        .done(function(data) {
            goproData = JSON.parse(data);
            if (goproData.status == "success") {
                console.log("goproData: " + goproData);
                progressMover("Video captured!", 20);

                // Next, we upload to S3
                setTimeout(() => {
                    console.log("Delayed for 0.5 second.");
                }, "1000");
                progressMover("Uploading to S3...", 30);
                
                //data: { bucket: configData.goproControl.targetBucket, filename: goproData.video_file, filepath: goproData.path },
                var s3Data_r = jQuery.ajax({
                    type: "POST",
                    url: configData.s3Shipper.endpoint,
                    data: { bucket: configData.goproControl.targetBucket, filename: goproData.video_file, filepath: '/opt/gopro-control/videos/' + goproData.video_file },
                    dataType: 'html'
                }).done(function(data) {
                    s3Data = JSON.parse(data);
                    console.log(s3Data);
                    if (s3Data.status == "success") {
                        progressMover("File uploaded to S3 successfully!", 40);

                        // Next, access the external S3 link and display the video
                        capturedVideoHTML = '<video id="capturedVideo" class="card-img-top" controls autoplay muted playsinline><source src="' + configData.s3PublicEndpoint + '/'+ configData.goproControl.targetBucket +'/' + goproData.video_file + '" type="video/mp4"></video>';
                        jQuery("#capturedVideoContainer").removeClass('d-none');
                        jQuery("#capturedVideoHolder").html(capturedVideoHTML);

                        // Next, we'll check on the inferrence status
                        setTimeout(() => {
                            console.log("Delayed for 1 second.");
                        }, "1000");
                        progressMover("Waiting for model inference...", 60);

                        // Check for the inference data at the prediction bucket
                        predictionEndpoint = configData.s3PublicEndpoint + '/' + configData.goproControl.targetBucket + '-predictions/pred_' + goproData.video_file;
                        predictionEndpointMKV = predictionEndpoint.replace(/\.[^/.]+$/, "") + '.mkv';
                        scrapeLoopDelay = 1000;

                        (function loop() {
                            setTimeout(() => {
                                // Your logic here
                                jQuery.get( predictionEndpointMKV )
                                .always(function(data, textStatus, xhr) {

                                    console.log("curlLoop textStatus: " + textStatus);
                                    if (goodStatuses.includes(xhr.status)) {
                                        if (textStatus == "success") {
                                            // The data is finally available, let's display it
                                            progressMover("Model inference complete!", 80);
                                            setTimeout(() => {
                                                console.log("Delayed for 1 second.");
                                            }, "1000");

                                            // Display the video
                                            inferredVideoHTML = '<video id="inferredVideo" class="card-img-top" controls autoplay muted playsinline><source src="' + predictionEndpointMKV + '" type="video/mp4"></video>';
                                            jQuery("#inferredVideoContainer").removeClass('d-none');
                                            jQuery("#inferredVideoHolder").html(inferredVideoHTML);

                                            // Get the endpoint for the JSON data
                                            jsonDataEndpoint = predictionEndpoint.replace(/\.[^/.]+$/, "") + '.json';

                                            // Load the prediction data
                                            processInferenceJSONData(jsonDataEndpoint);
                                            progressMover("Output complete!", 100);
                                        }
                                    } else {
                                        loop();
                                    }
                                });
                                
                            }, scrapeLoopDelay);
                        })();

                        //predictionData = curlUntilSuccess(predictionEndpoint);

                    } else {
                        progressFail(s3Data.message);
                    }
                }).fail(function() {
                    progressFail('Error uploading to S3!');
                }).always(function() {
                    //alert( "finished" );
                });
            }
            else {
                progressFail(goproData.msg);
            }
        })
        .fail(function() {
            progressFail('Error loading gopro control data!');
        })
        .always(function() {
            //alert( "finished" );
        });
    });
});