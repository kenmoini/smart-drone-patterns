const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');
const qs = require('querystring');

const port = 6969;
const server = http.createServer(express);
const wss = new WebSocket.Server({ server })
const ext = /[\w\d_-]+\.[\w\d]+$/;

const wssClient = new WebSocket('ws://localhost:6969');

var historyFileName = 'history.json';
var historyFilePath = './data/';
var bkUpHistoryFilePath = './';
var historyFile = null;

// Read in the history file
var history = [{"nick": "ChanSrv", "message": "Welcome to OpenChat!  Please enter your nickname and start chatting!"}];

function readFileIntoHistory(historyFile) {
  //console.log("readFileIntoHistory: " + historyFile)
  fs.readFile(historyFile, function(err, data) {
    if (err) {
      console.log("Error reading history file: " + err);
    } else {
      //console.log("History file read successfully.");
      history = JSON.parse(data);
    }
  });
}
function determineHistoryFile() {
  //console.log("determineHistoryFile")
  // Check for the primary persistent history file
  if (fs.existsSync(historyFilePath + historyFileName)) {
    // Primary history file exists, read it into the history array
    //console.log("Primary history file exists.");
    historyFile = historyFilePath + historyFileName;
    readFileIntoHistory(historyFile);
  } 
  // Check to see if the persistent path exists, ie when a PVC is mounted but empty
  else if (fs.existsSync(historyFilePath)) {
    // Path exists but is empty so create the history file
    //console.log("History file path exists, creating history file.");
    fs.writeFile(historyFilePath + historyFileName, JSON.stringify(history), (error) => {
      // throw the error in case of a writing problem
      if (error) {
        console.error(error);
        throw error;
      }
      //console.log(historyFilePath + historyFileName + " written correctly");
      // Set the history file to the new history file
      historyFile = historyFilePath + historyFileName;
    });
  }
  // In case this is an ephemeral container, check for the backup history file
  else if (fs.existsSync(bkUpHistoryFilePath + historyFileName)) {
    // Backup history file exists, read it into the history array
    //console.log("Backup history file exists.");
    historyFile = bkUpHistoryFilePath + historyFileName;
    readFileIntoHistory(historyFile);
  }
  // All else has failed, thrown an error
  else {
    console.log("History file does not exist and cannot be created!");
  }
}

function readHistoryFile() {
  // If the history file is defined then read it
  //console.log("readHistoryFile")
  //console.log("historyFile: " + historyFile)
  if (historyFile != null) {
    // Double check to make sure the defined history file exists
    if (fs.existsSync(historyFile)) {
      //console.log("History file exists: " + historyFile);
      // Read the history file
      readFileIntoHistory(historyFile);
    } else {
      //console.log("Defined history file does not exist!");
      determineHistoryFile();
    }
  } else {
    // The history file variable is not defined so we need to step through the options
    determineHistoryFile();
  }
}
/*

  fs.readFile(historyFilePath + historyFileName, function(err, data) {
    if (err) {
      console.log("Error reading history file: " + err);
      // Check to see if the historyFilePath exists
      if (fs.existsSync(historyFilePath)) {
        console.log("History file path exists.");
        // Create the history file
        fs.writeFile(historyFilePath + historyFileName, JSON.stringify(history), (error) => {
          // throw the error in case of a writing problem
          if (error) {
            // logging the error
            console.error(error);
            throw error;
          }
          console.log(historyFilePath + historyFileName + " written correctly");
          // Set the history file to the new history file
          historyFile = historyFilePath + historyFileName;
        });
      }
    }
    else {
      // Try to read the backup history file
      fs.readFile(bkUpHistoryFilePath + historyFileName, function(err, data) {
        if (err) {
          console.log("Error reading backup history file: " + err);
        } else {
          console.log("Backup history file read successfully.");
          history = JSON.parse(data);
          // Set the history file to the backup history file
          historyFile = bkUpHistoryFilePath + historyFileName;
        }
      });
    } else {
      history = JSON.parse(data);
    }
  });
}*/
readHistoryFile();

wss.on('connection', function connection(ws) {
  // Send the history to the new client
  readHistoryFile();

  // Loop through the history and send each message to the client
  for (var i = 0; i < history.length; i++) {
    msg = history[i];
    ws.send(JSON.stringify(msg));
  }

  ws.on('message', function incoming(data) {
    // Read the file in asynchronusly
    try {
      const fData = fs.readFileSync(historyFile);
      // Parse the data
      const currentHistory = JSON.parse(fData);
      //console.log(currentHistory);
      
      // Append the new message to the history
      currentHistory.push(JSON.parse(data));
      //console.log(currentHistory);

      // Write the file
      fs.writeFile(historyFile, JSON.stringify(currentHistory), (error) => {
        // throwing the error
        // in case of a writing problem
        if (error) {
          // logging the error
          console.error(error);
          throw error;
        }
        readHistoryFile();
        //console.log(historyFile + " written correctly");
      });

    } catch (error) {
      console.error(error);
      throw error;
    }

    // Send data to each client
    wss.clients.forEach(function each(client) {
      if (client !== ws && client.readyState === WebSocket.OPEN) {
        client.send(data);
      }
    })
  })
})

server.listen(port, function() {
  console.log(`Server is listening on ${port}!`)
})

http.createServer(function(request, response){
  // Set CORS headers
  response.setHeader('Access-Control-Allow-Origin', '*');
  response.setHeader('Access-Control-Request-Method', '*');
  response.setHeader('Access-Control-Allow-Methods', 'OPTIONS, GET');
  response.setHeader('Access-Control-Allow-Headers', '*');
  if ( request.method === 'OPTIONS' ) {
    response.writeHead(200);
    response.end();
    return;
  }

  var filePath =  '.' + request.url;
  if (filePath == './')
      filePath = './index.html';

  var extname = path.extname(filePath);
  var contentType = 'text/html';

  switch (extname) {
    case '.js':
        contentType = 'text/javascript';
        break;
    case '.css':
        contentType = 'text/css';
        break;
    case '.json':
        contentType = 'application/json';
        break;
    case '.png':
        contentType = 'image/png';
        break;      
    case '.jpg':
        contentType = 'image/jpg';
        break;
    case '.wav':
        contentType = 'audio/wav';
        break;
  }

  // See if the start of the request is for the RESTful service
  if (request.url.startsWith('/api')) {
    // Process POST messages
    if (request.method === 'POST') {
      if (request.url === '/api/sendMessage') {
        // Process messages sent from the client
        let body = '';
        request.on('data', chunk => {
            body += chunk.toString(); // convert Buffer to string
        });
        request.on('end', () => {
          pdata = qs.parse(body);
          // Assemble JSON object
          var msgData = {"nick": pdata.nick, "message": pdata.message};

          // Send the message to the websocket via the internal socket
          wssClient.send(JSON.stringify(msgData));
          response.end('ok');
        });
      }

      if (request.url === '/api/alertmanagerReceiver') {
        // https://gist.github.com/mobeigi/5a96f326bc06c7d6f283ecb7cb083f2b
        // Process messages sent from the client
        let body = '';
        request.on('data', chunk => {
            body += chunk.toString(); // convert Buffer to string
        });
        request.on('end', () => {
          //console.log("body: " + body);
          //console.log(JSON.parse(body));
          message = JSON.parse(body);

          var msgData = {"nick": "OCP Alertmanager", "message": (message.alerts.length) + " alert(s) firing on the " + message.receiver + " receiver!  Visit <a href='" + message.externalURL + "'>" + message.externalURL + "</a> for more information."};

          // Send the message to the websocket via the internal socket
          wssClient.send(JSON.stringify(msgData));
          response.end('ok');
        });
      }
    }
  } else {
    fs.readFile(filePath, function(error, content) {
      if (error) {
          if(error.code == 'ENOENT'){
              fs.readFile('./404.html', function(error, content) {
                  response.writeHead(404, { 'Content-Type': contentType });
                  response.end(content, 'utf-8');
              });
          }
          else {
              response.writeHead(500);
              response.end('Sorry, check with the site admin for error: '+error.code+' ..\n');
              response.end(); 
          }
      }
      else {
          response.writeHead(200, { 'Content-Type': contentType });
          response.end(content, 'utf-8');
      }
    });
  }
  /*
  if (request.url === '/') {
    response.writeHead(200, {'Content-Type': 'text/html'});
      fs.createReadStream('index.html').pipe(response);
  } else if (ext.test(request.url)) {
      fs.exists(path.join(__dirname, request.url), function (exists) {
          if (exists) {
            response.writeHead(200, {'Content-Type': 'text/html'});
              fs.createReadStream('index.html').pipe(response);
          } else {
            response.writeHead(404, {'Content-Type': 'text/html'});
              fs.createReadStream('404.html').pipe(response);
      }
    });
  } else {
      //  add a RESTful service
  }*/
}).listen(7979, function() {
  console.log(`Client server is listening on 7979!`)
});

/*  
fs.readFile('./index.html', function (err, html) {
  if (err) {
      throw err; 
  }       
  http.createServer(function(request, response) {
    // Set CORS headers
    response.setHeader('Access-Control-Allow-Origin', '*');
    response.setHeader('Access-Control-Request-Method', '*');
    response.setHeader('Access-Control-Allow-Methods', 'OPTIONS, GET');
    response.setHeader('Access-Control-Allow-Headers', '*');
    if ( request.method === 'OPTIONS' ) {
      response.writeHead(200);
      response.end();
      return;
    }
      response.writeHeader(200, {"Content-Type": "text/html"});  
      response.write(html);  
      response.end();  
  }).listen(7979, function() {
    console.log(`Client server is listening on 7979!`)
  });
});

*/