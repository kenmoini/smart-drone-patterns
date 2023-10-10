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

var historyFile = './data/history.txt';
var bkUpHistoryFile = './history.txt';

// Read in the history file
var history = [];
function readHistoryFile() {
  fs.readFile(historyFile, function(err, data) {
    if (err) {
      console.log("Error reading history file: " + err);
      // Try to read the backup history file
      fs.readFile(bkUpHistoryFile, function(err, data) {
        if (err) {
          console.log("Error reading backup history file: " + err);
        } else {
          console.log("Backup history file read successfully.");
          history = JSON.parse(data);
          // Set the history file to the backup history file
          historyFile = bkUpHistoryFile;
        }
      });
    } else {
      history = JSON.parse(data);
    }
  });
}
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