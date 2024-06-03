// Example using Express.js
const express = require('express');
const app = express();

// Middleware to set CORS headers
app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', 'http://localhost:3000');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    res.setHeader('Access-Control-Allow-Credentials', 'true');
    next();
});

// Your routes and other middleware here

app.listen(5000, () => {
    console.log('Server is running on port 5000');
});
