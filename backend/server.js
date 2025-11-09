const express = require('express');
const cors = require('cors');
const multer = require('multer');
const ExcelJS = require('exceljs');
const path = require('path');

const app = express();
const upload = multer({ storage: multer.memoryStorage() });
const PORT = 4000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../frontend/build')));

// Polyfill for fetch
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

// --- Data & Helper Functions ---

// Helper function to process Excel files with ExcelJS
async function processExcelBuffer(buffer) {
    const workbook = new ExcelJS.Workbook();
    await workbook.xlsx.load(buffer);
    
    const worksheet = workbook.getWorksheet(1);
    if (!worksheet) {
        throw new Error('No worksheet found');
    }
    
    const json = [];
    worksheet.eachRow((row, rowNumber) => {
        const values = [];
        row.eachCell((cell, colNumber) => {
            // Handle different cell types
            let value = cell.value;
            if (value && typeof value === 'object' && value.text) {
                value = value.text; // Rich text
            } else if (value instanceof Date) {
                value = value.toISOString().split('T')[0]; // Format dates
            }
            values[colNumber - 1] = value;
        });
        json.push(values);
    });
    
    return json;
}

// Helper function to process multi-sheet Excel files
async function processMultiSheetExcel(buffer) {
    const workbook = new ExcelJS.Workbook();
    await workbook.xlsx.load(buffer);
    
    const result = {};
    workbook.eachSheet((worksheet, sheetId) => {
        const sheetData = [];
        worksheet.eachRow((row, rowNumber) => {
            const rowData = {};
            row.eachCell((cell, colNumber) => {
                let value = cell.value;
                if (value && typeof value === 'object' && value.text) {
                    value = value.text;
                } else if (value instanceof Date) {
                    value = value.toISOString().split('T')[0];
                }
                
                // Use the header from first row as key, or column letter if no header
                const header = worksheet.getRow(1).getCell(colNumber).value || `Column${colNumber}`;
                rowData[header] = value !== undefined ? value : '';
            });
            if (rowNumber > 1) { // Skip header row
                sheetData.push(rowData);
            }
        });
        result[worksheet.name] = sheetData;
    });
    
    return result;
}

const holidaysCache = {};
/**
 * Fetches UK public holidays for a given year and caches the result.
 * @param {number} year - The year to fetch holidays for.
 * @returns {Promise<string[]>} A promise that resolves to an array of date strings ('YYYY-MM-DD').
 */
async function getUKPublicHolidays(year) {
  if (holidaysCache[year]) return holidaysCache[year];
  try {
    const res = await fetch(`https://date.nager.at/api/v3/PublicHolidays/${year}/GB`);
    if (!res.ok) throw new Error('Unable to fetch UK public holidays');
    const data = await res.json();
    // Only include holidays for England & Wales (counties == null or includes 'England')
    // Only include holidays for England & Wales (counties includes 'GB-ENG' or 'GB-WLS', or counties is null)
    const holidays = data
      .filter(h => h.counties === null ||
        (Array.isArray(h.counties) && (h.counties.includes('GB-ENG') || h.counties.includes('GB-WLS')))
      )
      .map(h => h.date);
    holidaysCache[year] = holidays;
    return holidays;
  } catch (error) {
    console.error(`Error fetching holidays for ${year}:`, error);
    return []; // Return an empty array on error to prevent the app from crashing
  }
}

/**
 * Checks if a row contains 'CWR' in any of the specified fields.
 * @param {object} row - The row object from the Excel sheet.
 * @returns {boolean} True if the row is a CWR row, otherwise false.
 */
function isCWRRow(row) {
  const fields = [
    'Contract Name', 'Contract', 'EMP ID', 'Associate ID', 'Name', 'Associate Name'
  ];
  return fields.some(f =>
    row[f] && row[f].toString().toUpperCase().includes('CWR')
  );
}

/**
 * Converts an Excel serial date number to a JavaScript Date object.
 * @param {number} serial - The Excel serial date number.
 * @returns {Date | null} The corresponding Date object or null if invalid.
 */
function excelSerialToDate(serial) {
  if (typeof serial !== 'number' || isNaN(serial)) return null;
  const excelEpoch = new Date(Date.UTC(1899, 11, 30));
  const date = new Date(excelEpoch.getTime() + serial * 86400000);
  return !isNaN(date.getTime()) ? date : null;
}

/**
 * Parses various date formats from Excel and returns a Date object.
 * @param {any} dateValue - The value to parse as a date.
 * @returns {Date | null} The parsed Date object or null if parsing fails.
 */
function parseExcelDate(dateValue) {
  if (!dateValue) return null;
  if (typeof dateValue === 'number') {
    // Treat as Excel serial number
    return excelSerialToDate(dateValue);
  }
  const dateStr = String(dateValue).trim();
  // Try ISO format
  let d = new Date(dateStr);
  if (!isNaN(d.getTime())) return d;
  // Try DD/MM/YYYY or DD-MMM-YY
  const parts = dateStr.split(/[\/-]/);
  if (parts.length === 3) {
    let day = parseInt(parts[0], 10);
    let month = parseInt(parts[1], 10);
    let year = parseInt(parts[2], 10);

    // Handle DD-MMM-YY format
    if (isNaN(month) && /^[A-Za-z]{3}$/.test(parts[1])) {
      const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      month = monthNames.findIndex(m => m.toLowerCase() === parts[1].toLowerCase()) + 1;
      year = (year < 100) ? 2000 + year : year;
      if (month > 0) d = new Date(year, month - 1, day);
      if (!isNaN(d.getTime())) return d;
    }
    // Handle DD/MM/YYYY
    if (!isNaN(day) && !isNaN(month) && !isNaN(year)) {
      if (year < 100) year = 2000 + year; // Handle YY format
      d = new Date(year, month - 1, day);
      if (!isNaN(d.getTime())) return d;
    }
  }
  return null;
}

/**
 * Parses a rate card value, removing non-numeric characters.
 * @param {any} val - The value to parse.
 * @returns {number} The parsed number or 0 if invalid.
 */
function parseRateCard(val) {
  if (!val) return 0;
  return parseFloat(String(val).replace(/[^0-9.]/g, '')) || 0;
}

// --- API Endpoints ---
// Single-file upload for Ideas tab
app.post('/api/ideas-upload', upload.single('excel'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const json = await processExcelBuffer(req.file.buffer);

    if (json.length === 0) {
      return res.status(400).json({ error: 'The Excel file is empty or has no data.' });
    }

    res.json({ 
      data: json,
      message: 'Ideas data uploaded successfully' 
    });
  } catch (error) {
    console.error('Ideas upload error:', error);
    res.status(500).json({ error: 'Error processing ideas file: ' + error.message });
  }
});

// Single-file upload for Training tab
app.post('/api/training-upload', upload.single('excel'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const json = await processExcelBuffer(req.file.buffer);

    if (json.length === 0) {
      return res.status(400).json({ error: 'The Excel file is empty or has no data.' });
    }

    const columns = json.length > 0 ? json[0] : [];
    const data = json.length > 1 ? json.slice(1) : [];

    res.json({ 
      columns,
      data,
      message: 'Training data uploaded successfully' 
    });
  } catch (error) {
    console.error('Training upload error:', error);
    res.status(500).json({ error: 'Error processing training file: ' + error.message });
  }
});

// Dual-file upload for Revenue & FTE
app.post('/api/upload', upload.fields([{ name: 'leave' }, { name: 'people' }]), async (req, res) => {
  // Parse selected columns from frontend
  let peopleSelectedCols = [];
  let leaveSelectedCols = [];
  try {
    peopleSelectedCols = JSON.parse(req.body.peopleSelectedCols || '[]');
    leaveSelectedCols = JSON.parse(req.body.leaveSelectedCols || '[]');
  } catch (e) {
    peopleSelectedCols = [];
    leaveSelectedCols = [];
  }

  // Helper to filter array of objects by selected columns
  function filterColumns(arr, selectedCols) {
    if (!Array.isArray(arr) || !selectedCols?.length) return arr;
    return arr.map(row => {
      const filtered = {};
      selectedCols.forEach(col => { if (row.hasOwnProperty(col)) filtered[col] = row[col]; });
      if (row.hasOwnProperty('id')) filtered.id = row.id;
      return filtered;
    });
  }

  try {
    const files = req.files;
    if (!files || !files.leave || !files.people) {
      return res.status(400).json({ error: 'Both Leave and People Tracker files are required.' });
    }

    // Parse Excel files with ExcelJS
    async function parseSheets(file) {
      const workbook = new ExcelJS.Workbook();
      await workbook.xlsx.load(file.buffer);
      
      const result = {};
      workbook.eachSheet((worksheet, sheetId) => {
        const sheetData = [];
        worksheet.eachRow((row, rowNumber) => {
          if (rowNumber === 1) return; // Skip header row
          
          const rowData = {};
          row.eachCell((cell, colNumber) => {
            let value = cell.value;
            if (value && typeof value === 'object' && value.text) {
              value = value.text;
            } else if (value instanceof Date) {
              value = value.toISOString().split('T')[0];
            }
            
            // Get header from first row
            const header = worksheet.getRow(1).getCell(colNumber).value || `Column${colNumber}`;
            rowData[header] = value !== undefined ? value : '';
          });
          sheetData.push(rowData);
        });
        result[worksheet.name] = sheetData;
      });
      return result;
    }
    const leaveSheets = await parseSheets(files.leave[0]);
    const peopleSheets = await parseSheets(files.people[0]);

    // Define constants
    const currentYear = 2025;
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const holidays = await getUKPublicHolidays(currentYear);

    // --- Leave Data Processing ---
    // Extract leave days by associate and month (filtered for CWR)
    const leaveDaysByEmpMonth = {};
    Object.values(leaveSheets).forEach(sheet => {
      if (!Array.isArray(sheet)) return;
      sheet.forEach(row => {
        if (isCWRRow(row)) return;
        const empId = row['EMP ID'] || row['Employee ID'] || row['ID'] || row['Associate ID'] || row['Name'] || row['Associate Name'] || row['Associate'];
        if (!empId) return;
        Object.keys(row).forEach(col => {
          const match = col.match(/^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*Leave Days/i);
          if (match) {
            const month = match[1];
            const val = parseFloat(row[col]) || 0;
            if (!leaveDaysByEmpMonth[empId]) leaveDaysByEmpMonth[empId] = {};
            leaveDaysByEmpMonth[empId][month] = (leaveDaysByEmpMonth[empId][month] || 0) + val;
          }
        });
      });
    });

    // --- People Tracker Data Processing ---
    const people = [];
    const workingDaysByMonth = {};
    const leaveSummaryMap = {};
    const peopleTrackerRawData = [];

    // First pass: Populate leaveSummaryMap and peopleTrackerRawData
    // This allows for clean lookups in the next pass.
    Object.entries(leaveSheets).forEach(([sheetName, rows]) => {
      if (!Array.isArray(rows)) return;
      const lowerSheet = sheetName.toLowerCase();
      const month = months.find(m => lowerSheet.includes(m.toLowerCase()));
      if (!month) return;
      rows.forEach(row => {
        const empId = row['ID'] || row['Emp ID'] || row['Employee ID'] || row['Associate ID'] || '';
        const name = row['Name'] || row['Associate Name'] || row['Associate'] || '';
        if (!empId && !name) return;
        const key = String(empId).trim();
        if (!leaveSummaryMap[key]) leaveSummaryMap[key] = { empId, name };
        const leaveCol = Object.keys(row).find(
          c => c.trim().toLowerCase() === `${month.toLowerCase()} leave days`
        );
        const leaveDays = leaveCol ? Number(row[leaveCol]) || 0 : 0;
        leaveSummaryMap[key][`${month}_leaveDays`] = leaveDays;
      });
    });

    // Ensure all months have a leave days entry (default to 0)
    Object.values(leaveSummaryMap).forEach(obj => {
      months.forEach(m => {
        if (typeof obj[`${m}_leaveDays`] === 'undefined') {
          obj[`${m}_leaveDays`] = 0;
        }
      });
    });

    // Second pass: Process people data, calculate FTE, revenue etc.
    Object.values(peopleSheets).forEach(sheet => {
      if (!Array.isArray(sheet)) return;
      sheet.forEach(row => {
        if (isCWRRow(row)) return;
        
        // Extract and parse key fields
        const empId = row['EMP ID'] || row['Employee ID'] || row['ID'] || row['Associate ID'] || row['Name'] || row['Associate Name'] || row['Associate'];
        const name = row['Name'] || row['Associate Name'] || row['Associate'] || '';
        const contract = row['Contract Name'] || row['Contract'] || '';
        const rateCard = parseRateCard(row['Rate Card'] || row['RateCard'] || '');
        const assignmentStart = parseExcelDate(row['Assignment Start Date'] || row['Assignment Start']);
        const billableStart = parseExcelDate(row['Billing Start Date'] || row['Billing Start'] || row['Billable Start Date']);
        const billableEnd = parseExcelDate(row['Billing End Date'] || row['Billing End'] || row['Billable End Date']);

        if (!empId || !contract) return;

        const p = { empId, name, contract, rateCard, assignmentStart, billableStart, billableEnd };
        
        months.forEach((m, i) => {
          const monthIdx = i;
          const monthStart = new Date(Date.UTC(currentYear, monthIdx, 1));
          const monthEnd = new Date(Date.UTC(currentYear, monthIdx + 1, 0));

          // Assignment/billing windows (use billing end as assignment end)
          // Defensive: ensure all dates are valid Date objects
          const safeDate = d => (d instanceof Date && !isNaN(d)) ? d : null;
          let asgStart = safeDate(assignmentStart) && safeDate(assignmentStart) > monthStart ? safeDate(assignmentStart) : monthStart;
          let asgEnd = safeDate(billableEnd) && safeDate(billableEnd) < monthEnd ? safeDate(billableEnd) : monthEnd; // use billing end as assignment end
          let billStart = safeDate(billableStart) && safeDate(billableStart) > monthStart ? safeDate(billableStart) : monthStart;
          let billEnd = safeDate(billableEnd) && safeDate(billableEnd) < monthEnd ? safeDate(billableEnd) : monthEnd;

          // Initialize month-specific data
          p[`${m}_totalWorkingDays`] = 0;
          p[`${m}_leaveDays`] = 0;
          p[`${m}_actualWorkingDays`] = 0;
          p[`${m}_cost_revenue`] = '0.00';
          p[`${m}_total_revenue`] = '0.00';
          p[`${m}_fte`] = '0.00';
          p[`${m}_leaveFte`] = '0.00';

          // Gather leave days for this associate/month (dates as YYYY-MM-DD)
          let leaveDates = [];
          if (leaveSummaryMap[String(empId).trim()] && leaveSummaryMap[String(empId).trim()][`${m}_leaveDates`]) {
            leaveDates = Array.isArray(leaveSummaryMap[String(empId).trim()][`${m}_leaveDates`]) ? leaveSummaryMap[String(empId).trim()][`${m}_leaveDates`] : [];
          }

          // Helper: is working day
          function isWorkingDay(d) {
            const day = d.getUTCDay();
            const dateStr = d.toISOString().slice(0, 10);
            return day !== 0 && day !== 6 && !holidays.includes(dateStr);
          }

          // Helper: count working days in a window
          function countWorkingDays(start, end) {
            let count = 0;
            for (let d = new Date(start); d <= end; d.setUTCDate(d.getUTCDate() + 1)) {
              if (isWorkingDay(d)) count++;
            }
            return count;
          }

          // Helper: count leave days in a window
          function countLeaveDaysInWindow(start, end) {
            return leaveDates.filter(ld => {
              const d = new Date(ld);
              return d >= start && d <= end && isWorkingDay(d);
            }).length;
          }

          // 1. Pre-billing NBL window (clamped to current month)
          let preNBLStart = asgStart;
          let preNBLEnd = billStart > asgStart ? 
            new Date(Math.min(billStart.getTime() - 86400000, monthEnd.getTime())) : 
            new Date(Math.min(asgStart.getTime(), monthEnd.getTime()));
          let preNBLDays = 0, leaveInPreNBL = 0;
          if (preNBLEnd >= preNBLStart) {
            preNBLDays = countWorkingDays(preNBLStart, preNBLEnd);
            leaveInPreNBL = countLeaveDaysInWindow(preNBLStart, preNBLEnd);
          }

          // 2. Post-billing NBL window (clamped to current month)
          let postNBLStart = billEnd < asgEnd ? 
            new Date(Math.max(billEnd.getTime() + 86400000, monthStart.getTime())) : 
            new Date(Math.max(asgEnd.getTime(), monthStart.getTime()));
          let postNBLEnd = asgEnd;
          let postNBLDays = 0, leaveInPostNBL = 0;
          if (postNBLEnd >= postNBLStart) {
            postNBLDays = countWorkingDays(postNBLStart, postNBLEnd);
            leaveInPostNBL = countLeaveDaysInWindow(postNBLStart, postNBLEnd);
          }

          // 3. Total NBL days and FTE
          const nblDays = (preNBLDays - leaveInPreNBL) + (postNBLDays - leaveInPostNBL);
          const totalMonthWorkingDays = countWorkingDays(monthStart, monthEnd);
          const nonBillableFte = totalMonthWorkingDays > 0 ? nblDays / totalMonthWorkingDays : 0;
          p[`${m}_nonBillableLeaveDays`] = nblDays;
          p[`${m}_nonBillableFte`] = nonBillableFte.toFixed(3);

          if (asgStart <= asgEnd) {
            // Calculate non-billable leave days for this month
            let nonBillableLeaveDays = 0;
            let billedDays = 0;
            let totalMonthWorkingDays = 0;
            
            // For billed days, only count days between billingStart and billingEnd (capped to month)
            let billedStart = billableStart && billableStart > monthStart ? billableStart : monthStart;
            let billedEnd = billableEnd && billableEnd < monthEnd ? billableEnd : monthEnd;
            
            for (let d = new Date(monthStart); d <= monthEnd; d.setUTCDate(d.getUTCDate() + 1)) {
              const day = d.getUTCDay();
              const dateStr = d.toISOString().slice(0, 10);
              if (day !== 0 && day !== 6 && !holidays.includes(dateStr)) {
                totalMonthWorkingDays++;
                // Non-billable leave: in assignment window, but outside billing window
                const inAssignment = (!assignmentStart || d >= assignmentStart) && (!billableEnd || d <= billableEnd);
                const inBilling = (d >= billedStart && d <= billedEnd);
                if (inAssignment && !inBilling) {
                  nonBillableLeaveDays++;
                }
                if (inBilling) {
                  billedDays++;
                }
              }
            }
            
            // Save per-associate/month
            p[`${m}_nonBillableLeaveDays`] = nonBillableLeaveDays;
            // Billed FTE logic - subtract leave days that fall within billing period
            const leaveDaysInBillingPeriod = leaveDates.filter(ld => {
              const d = new Date(ld);
              return d >= billedStart && d <= billedEnd && isWorkingDay(d);
            }).length;
            const actualBilledDays = Math.max(0, billedDays - leaveDaysInBillingPeriod);
            const billedFte = (totalMonthWorkingDays > 0) ? (actualBilledDays / totalMonthWorkingDays) : 0;
            p[`${m}_billedFte`] = billedFte.toFixed(2);
          } else {
            // Always assign billedFte if asgStart > asgEnd
            p[`${m}_billedFte`] = '0.00';
            p[`${m}_nonBillableLeaveDays`] = 0;
          }
          
          // Ensure billedFte is always set
          if (typeof p[`${m}_billedFte`] === 'undefined') {
            p[`${m}_billedFte`] = '0.00';
          }

          // Print holidays for the month for debugging
          console.log(`HOLIDAYS FOR ${m}:`, holidays.filter(h => h.startsWith(`2025-${(monthIdx + 1).toString().padStart(2, '0')}`)));
          const leaveRow = leaveSummaryMap[String(empId).trim()];
          const leaveDays = leaveRow ? (Number(leaveRow[`${m}_leaveDays`]) || 0) : 0;

          let totalWorkingDays = 0;
          for (let d = new Date(asgStart); d <= asgEnd; d.setUTCDate(d.getUTCDate() + 1)) {
            const day = d.getUTCDay();
            const dateStr = d.toISOString().slice(0, 10);
            if (day !== 0 && day !== 6 && !holidays.includes(dateStr)) {
              totalWorkingDays++;
            }
          }

          const actualWorkingDays = Math.max(0, totalWorkingDays - leaveDays);
          const monthlyCost = rateCard * actualWorkingDays;
          const totalFte = (totalWorkingDays > 0) ? (actualWorkingDays / totalWorkingDays) : 0;
          const leaveFte = (totalWorkingDays > 0) ? (leaveDays / totalWorkingDays) : 0;
          const totalRevenue = monthlyCost * 1.29;

          p[`${m}_totalWorkingDays`] = totalWorkingDays;
          p[`${m}_leaveDays`] = leaveDays;
          p[`${m}_actualWorkingDays`] = actualWorkingDays;
          p[`${m}_cost_revenue`] = `£${monthlyCost.toFixed(2)}`;
          p[`${m}_total_revenue`] = `$${totalRevenue.toFixed(2)}`;
          p[`${m}_fte`] = totalFte.toFixed(2);
          // Enhanced debug log for tracing calculation
          console.log(`DEBUG: empId=${empId}, name=${name}, month=${m}, rateCard=${rateCard}, totalWorkingDays=${totalWorkingDays}, leaveDays=${leaveDays}, actualWorkingDays=${actualWorkingDays}, monthlyCost=${monthlyCost}, assignmentStart=${assignmentStart}, billableStart=${billableStart}, billableEnd=${billableEnd}, asgStart=${asgStart}, asgEnd=${asgEnd}`);
          p[`${m}_leaveFte`] = leaveFte.toFixed(2);
          p[`${m}_total_fte`] = totalFte.toFixed(2);
        }); // End months.forEach
        
        people.push(p);
        peopleTrackerRawData.push(p);
      }); // End sheet.forEach
    }); // End Object.values(peopleSheets).forEach

    // Group by contract for summary
    const contractGroups = people.reduce((acc, p) => {
      if (!acc[p.contract]) acc[p.contract] = [];
      acc[p.contract].push(p);
      return acc;
    }, {});

    // Build contract summary for frontend
    const contractSummary = Object.entries(contractGroups).map(([contract, rows]) => {
      const sumRateCard = rows.reduce((a, b) => a + (parseFloat(b.rateCard) || 0), 0);
      const monthsSummary = months.map((m) => {
        // Total FTE: count of associates for this contract/month
        const totalFte = rows.length;
        // Billed FTE: sum of billedFte for all associates
        const billedFte = rows.reduce((a, b) => a + (parseFloat(b[`${m}_billedFte`] || 0)), 0);
        // Non-billable leave: count of associates with any nonBillableLeaveDays > 0
        const nonBillableLeaveCount = rows.reduce((a, b) => a + ((parseFloat(b[`${m}_nonBillableLeaveDays`] || 0) > 0 ? 1 : 0)), 0);
        return {
          month: m,
          usd: rows.reduce((a, b) => a + (parseFloat(b[`${m}_total_revenue`]) || 0), 0).toFixed(2),
          leaveFte: rows.reduce((a, b) => a + (parseFloat(b[`${m}_leaveFte`] || 0)), 0).toFixed(2),
          totalFte,
          billedFte: billedFte.toFixed(2),
          nonBillableLeaveCount
        };
      });
      return {
        contract,
        sumRateCard: sumRateCard.toFixed(2),
        months: monthsSummary,
        associates: rows
      };
    });

    const leaveSummary = Object.values(leaveSummaryMap);

    // Restore flat totalFteBreakdown structure (one row per associate/month)
    const totalFteBreakdown = [];
    if (Array.isArray(people)) {
      people.forEach(p => {
        months.forEach(m => {
          totalFteBreakdown.push({
            contract: p.contract,
            empId: p.empId,
            name: p.name,
            month: m,
            fte: p[`${m}_fte`] || '0.00',
            leaveFte: p[`${m}_leaveFte`] || '0.00',
            costRevenue: p[`${m}_cost_revenue`] || '0.00'
          });
        });
      });
    }

    // Build contractGroupedSummary: [{ contract, associates: [ ... ] }]
    const contractGroupedSummary = Object.entries(contractGroups).map(([contract, associates]) => ({
      contract,
      associates
    }));

    res.json({
      months: Array.isArray(months) ? months : [],
      people: filterColumns(people, peopleSelectedCols),
      leaveSummary: filterColumns(leaveSummary, leaveSelectedCols),
      contractSummary: Array.isArray(contractSummary) ? contractSummary : [],
      summary: Array.isArray(contractSummary) ? contractSummary : [], // legacy, keep for compatibility
      groupedSummary: Array.isArray(contractSummary) ? contractSummary : [], // legacy, keep for compatibility
      contractGroupedSummary,
      totalFteBreakdown: Array.isArray(totalFteBreakdown) ? totalFteBreakdown : []
    });
  } catch (err) {
    console.error('API upload error:', err);
    res.status(500).json({ error: err.message || 'An unexpected error occurred during file processing.' });
  }
});

// Serve React app for any other route (after API routes)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/build', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Excel fullstack app running on http://localhost:${PORT}`);
});
