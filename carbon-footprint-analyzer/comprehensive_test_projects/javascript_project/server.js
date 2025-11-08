
const express = require('express');
const _ = require('lodash');
const axios = require('axios');

const app = express();
const port = 3000;

// Inefficient route handler
app.get('/api/data', async (req, res) => {
    const data = [];
    
    // Inefficient loop
    for (let i = 0; i < 1000; i++) {
        const item = {
            id: i,
            value: Math.random(),
            processed: processValue(i)
        };
        data.push(item);
    }
    
    res.json(data);
});

function processValue(value) {
    // Inefficient processing
    let result = value;
    for (let i = 0; i < 100; i++) {
        result = Math.sqrt(result + 1);
    }
    return result;
}

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
