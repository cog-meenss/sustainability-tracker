// Simple Express backend for Excel file upload and column extraction/sorting
const express = require('express');
const fileUpload = require('express-fileupload');
const cors = require('cors');
const ExcelJS = require('exceljs');

const app = express();
const PORT = 4000;

app.use(cors());
app.use(fileUpload());

// Upload and extract columns
app.post('/upload', async (req, res) => {
    if (!req.files || !req.files.excel) {
        return res.status(400).json({ error: 'No file uploaded' });
    }
    
    try {
        const workbook = new ExcelJS.Workbook();
        await workbook.xlsx.load(req.files.excel.data);
        
        const worksheet = workbook.getWorksheet(1); // Get first worksheet
        if (!worksheet) {
            return res.status(400).json({ error: 'No worksheet found' });
        }
        
        const json = [];
        worksheet.eachRow((row, rowNumber) => {
            const values = [];
            row.eachCell((cell, colNumber) => {
                values[colNumber - 1] = cell.value;
            });
            json.push(values);
        });
        
        if (json.length === 0) {
            return res.status(400).json({ error: 'Empty sheet' });
        }
        
        const columns = json[0];
        const data = json.slice(1);
        res.json({ columns, data });
    } catch (error) {
        console.error('Error processing Excel file:', error);
        res.status(500).json({ error: 'Failed to process Excel file' });
    }
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
