var configData = {};

jQuery( document ).ready(function() {
  // Disable dollar sign shortcut handling
  jQuery.noConflict();

  // Call out to internal configuration endpoint
  var configData_r = jQuery.get( "/config", function(data) {
      configData = JSON.parse(data);
      // Set the upload target
      jQuery("#upload_image_background").attr('data-post-url', configData.roboflowRobotEndpoint + "/inference");
  })
  .done(function() {
    //alert( "finished probably successfully" );
  })
  .fail(function() {
      alert( "error loading configuration data!" );
  })
  .always(function() {
      // Handle WAN Status Light
      wanStatusInterval = setInterval(checkWANStatus, 2000);
  });


  (function () {

    'use strict';
    
    // Four objects of interest: drop zones, input elements, gallery elements, and the files.
    // dataRefs = {files: [image files], input: element ref, gallery: element ref}
  
    const preventDefaults = event => {
      event.preventDefault();
      event.stopPropagation();
    };
  
    const highlight = event =>
      event.target.classList.add('highlight');
    
    const unhighlight = event =>
      event.target.classList.remove('highlight');
  
    const getInputAndGalleryRefs = element => {
      const zone = element.closest('.upload_dropZone') || false;
      const gallery = zone.querySelector('.upload_gallery') || false;
      const input = zone.querySelector('input[type="file"]') || false;
      return {input: input, gallery: gallery};
    }
  
    const handleDrop = event => {
      const dataRefs = getInputAndGalleryRefs(event.target);
      dataRefs.files = event.dataTransfer.files;
      handleFiles(dataRefs);
    }
  
  
    const eventHandlers = zone => {
  
      const dataRefs = getInputAndGalleryRefs(zone);
      if (!dataRefs.input) return;
  
      // Prevent default drag behaviors
      ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
        zone.addEventListener(event, preventDefaults, false);
        document.body.addEventListener(event, preventDefaults, false);
      });
  
      // Highlighting drop area when item is dragged over it
      ;['dragenter', 'dragover'].forEach(event => {
        zone.addEventListener(event, highlight, false);
      });
      ;['dragleave', 'drop'].forEach(event => {
        zone.addEventListener(event, unhighlight, false);
      });
  
      // Handle dropped files
      zone.addEventListener('drop', handleDrop, false);
  
      // Handle browse selected files
      dataRefs.input.addEventListener('change', event => {
        dataRefs.files = event.target.files;
        handleFiles(dataRefs);
      }, false);
  
    }
  
  
    // Initialise ALL dropzones
    const dropZones = document.querySelectorAll('.upload_dropZone');
    for (const zone of dropZones) {
      eventHandlers(zone);
    }


    // No 'image/gif' or PDF or webp allowed here, but it's up to your use case.
    // Double checks the input "accept" attribute
    const isImageFile = file => 
      ['image/jpeg', 'image/png', 'image/svg+xml'].includes(file.type);


    function previewFiles(dataRefs) {
      if (!dataRefs.gallery) return;
      for (const file of dataRefs.files) {
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function() {
          let img = document.createElement('img');
          img.className = 'upload_img mt-2';
          img.setAttribute('alt', file.name);
          img.src = reader.result;
          dataRefs.gallery.appendChild(img);
        }
      }
    }

    // Based on: https://flaviocopes.com/how-to-upload-files-fetch/
    const imageUpload = dataRefs => {

      // Multiple source routes, so double check validity
      if (!dataRefs.files || !dataRefs.input) return;

      const url = dataRefs.input.getAttribute('data-post-url');
      if (!url) return;

      const name = dataRefs.input.getAttribute('data-post-name');
      if (!name) return;

      const formData = new FormData();
      formData.append(name, dataRefs.files);


      var form = document.getElementById('uploadImage');
      // prepare data
      console.log(form);
      var newFormData = new FormData(form);

      jQuery.ajax({
        type: 'POST',
        url: url,
        data: newFormData,
        beforeSend: function(xhr) {
          //xhr.setRequestHeader('Accept-Encoding', 'gzip, deflate, br');
          //xhr.setRequestHeader('Connection', 'keep-alive');
          //xhr.setRequestHeader('Accept', '*/*');
        },
        processData: false,
        contentType: false
      }).done(function(data) {
        console.log(data);
        // Show the results
        jQuery("#inferredImageContainer").removeClass('d-none')
        .find("#inferredImageHolder")
        .html('<img src="' + url + '?imageName=' + data.inference + '" class="card-img-top">');

        // Show the JSON data
        jQuery("#rawJsonContainer").removeClass('d-none')
        .find("#rawJson").html(data.data);

        // Set up the counts

        // Send an alert if there was danger found
        
      }).fail(function() {
        console.log("failed to send request!");
      });

      /*
      fetch(url, {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        console.log('posted: ', data);
        if (data.success === true) {
          previewFiles(dataRefs);
        } else {
          console.log('URL: ', url, '  name: ', name)
        }
      })
      .catch(error => {
        console.error('errored: ', error);
      });
      */
    }
  
  
    // Handle both selected and dropped files
    const handleFiles = dataRefs => {
  
      let files = [...dataRefs.files];
  
      // Remove unaccepted file types
      files = files.filter(item => {
        if (!isImageFile(item)) {
          console.log('Not an image, ', item.type);
        }
        return isImageFile(item) ? item : null;
      });
  
      if (!files.length) return;
      dataRefs.files = files;
  
      previewFiles(dataRefs);
      imageUpload(dataRefs);
    }
  
  })();


});