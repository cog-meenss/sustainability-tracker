// Simple Express backend for Excel file upload and column extraction/sorting
const express = require('express');
const fileUpload = require('express-fileupload');
const cors = require('cors');
const xlsx = require('xlsx');

const app = express();
const PORT = 4000;

app.use(cors());
app.use(fileUpload());

// Upload and extract columns
app.post('/upload', (req, res) => {
    if (!req.files || !req.files.excel) {
        return res.status(400).json({ error: 'No file uploaded' });
    }
    const workbook = xlsx.read(req.files.excel.data, { type: 'buffer' });
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];
    const json = xlsx.utils.sheet_to_json(sheet, { header: 1 });
    if (json.length === 0) {
        return res.status(400).json({ error: 'Empty sheet' });
    }
    const columns = json[0];
    const data = json.slice(1);
    res.json({ columns, data });
});

// Sort extracted data
app.post('/sort', express.json(), (req, res) => {
    const { data, columnIndex, order } = req.body;
    if (!Array.isArray(data) || typeof columnIndex !== 'number' || !order) {
        return res.status(400).json({ error: 'Invalid payload' });
    }
    const sorted = [...data].sort((a, b) => {
        if (a[columnIndex] === b[columnIndex]) return 0;
        if (order === 'asc') return a[columnIndex] > b[columnIndex] ? 1 : -1;
        return a[columnIndex] < b[columnIndex] ? 1 : -1;
    });
    res.json({ sorted });
});

app.listen(PORT, () => {
    console.log(`Excel backend running on http://localhost:${PORT}`);
});
