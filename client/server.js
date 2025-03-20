const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');
const setupKafkaConsumer = require('./kafkaConsumer'); // Import Kafka consumer module

const app = express();
const port = 3000;

const server = http.createServer(app);
const io = new Server(server);

// Serve static files from the 'client' directory
app.use(express.static(path.join(__dirname, 'client')));

// Define routes for various pages
app.get('/licence.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'licence', 'licence.html'));
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'login', 'login.html'));
});

app.get('/licence/licence.js', (req, res) => {
    res.set('Content-Type', 'application/javascript');
    res.sendFile(path.join(__dirname, 'licence', 'licence.js'));
});

app.get('/licence/licence.css', (req, res) => {
    res.set('Content-Type', 'text/css');
    res.sendFile(path.join(__dirname, 'licence', 'licence.css'));
});

app.get('/submeter_page.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'submeter', 'main.html'));
});

app.get('/main.css', (req, res) => {
    res.sendFile(path.join(__dirname, 'submeter', 'main.css'));
});

app.get('/main.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'submeter', 'main.js'));
});

app.get('/login.css', (req, res) => {
    res.sendFile(path.join(__dirname, 'login', 'login.css'));
});

app.get('/login.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'login', 'login.html'));
});

app.get('/login.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'login', 'login.js'));
});

app.get('/home.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'home', 'home.html'));
});

app.get('/dashboard.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'home', 'dashboard.js'));
});

app.get('/support.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'home', 'support.html'));
});

app.get('/home.css', (req, res) => {
    res.sendFile(path.join(__dirname, 'home', 'home.css'));
});

app.get('/home.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'home', 'home.js'));
});

app.get('/wether.css', (req, res) => {
    res.sendFile(path.join(__dirname, 'home', 'wether.css'));
});

app.get('/licencepage.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'home', 'licencepage.html'));
});

app.use('/client/images', express.static(path.join(__dirname, 'images')));

app.get('/electric.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'electric', 'electric.html'));
});

app.get('/electric.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'electric', 'electric.js'));
});

app.get('/electric.css', (req, res) => {
    res.sendFile(path.join(__dirname, 'electric', 'electric.css'));
});

app.get('/wether.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'home', 'wether.js'));
});

io.on('connection', (socket) => {
    console.log('A user connected');

    socket.on('clientMessage', (data) => {
        console.log('Received from client:', data);
    });

    socket.on('disconnect', () => {
        console.log('User disconnected');
    });
});

// Start Kafka consumer (independent from the server)
setupKafkaConsumer(io);

server.listen(port, () => {
    console.log(`Server is listening on http://localhost:${port}`);
});
