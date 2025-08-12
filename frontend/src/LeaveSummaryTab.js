import React, { useState } from "react";
import { Box, Paper, Typography, Button, TextField, Select, MenuItem, InputLabel, FormControl, OutlinedInput, Chip, Checkbox, ListItemText } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";

const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const monthNames = {
  Jan: 'January', Feb: 'February', Mar: 'March', Apr: 'April', May: 'May', Jun: 'June',
  Jul: 'July', Aug: 'August', Sep: 'September', Oct: 'October', Nov: 'November', Dec: 'December'
};

function LeaveSummaryTab({ leaveSummary, selectedCols, onSaveView }) {
  // --- Custom Multi-Column Filter State for LeaveSummaryTab ---
  const [leaveFilterCol, setLeaveFilterCol] = useState('');
  const [leaveFilterVals, setLeaveFilterVals] = useState([]); // array of values for current column
  const [leaveFilterText, setLeaveFilterText] = useState('');
  const [leaveColumnFilters, setLeaveColumnFilters] = useState([]); // [{ col, vals: [] }]

  const [pageSize, setPageSize] = useState(20);

  // Auto-generate columns from leaveSummary data
  let columns = [
    { field: 'empId', headerName: 'Associate ID', width: 120 },
    { field: 'name', headerName: 'Associate Name', width: 180 },
    ...months.map(m => ({
      field: `${m}_leaveDays`,
      headerName: `${monthNames[m]} Leave Days`,
      width: 120,
      type: 'number',
      align: 'right',
      headerAlign: 'right',
      filterable: true,
      sortable: true
    }))
  ];
  if (selectedCols && selectedCols.length) {
    columns = columns.filter(col => selectedCols.includes(col.field) || selectedCols.find(sel => sel.id === col.field));
  }

  // Debug logging
  console.log('LeaveSummaryTab leaveSummary:', leaveSummary);
  const rows = leaveSummary.map((row, idx) => ({ ...row, id: (row.empId || row.name) + '-' + idx }));
  console.log('LeaveSummaryTab rows:', rows);

  // Custom filter logic for LeaveSummaryTab
  const filteredRows = rows.filter(row => {
    if (!leaveColumnFilters.length) return true;
    return leaveColumnFilters.every(fil => {
      const cell = row[fil.col];
      return fil.vals.some(val => cell !== undefined && cell !== null && String(cell).toLowerCase().includes(String(val).toLowerCase()));
    });
  });

  // Get unique values for a column
  const getLeaveUniqueValues = (col) => {
    return Array.from(new Set(rows.map(row => row[col]).filter(v => v !== undefined && v !== null && String(v).trim() !== '')));
  };

  return (
    <Paper sx={{ p: 2, mb: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, gap: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 600 }}>Leave Summary</Typography>
      </Box>
      <Box sx={{ width: '100%', height: 480, bgcolor: '#fff', borderRadius: 2, boxShadow: 1, border: '1px solid #e0e0e0', p: 1 }}>
        <DataGrid
          columns={columns}
          rows={filteredRows}
          pageSize={pageSize}
          onPageSizeChange={setPageSize}
          rowsPerPageOptions={[20, 50, 100]}
          pagination
          disableSelectionOnClick
          density="compact"
          components={{ Toolbar: GridToolbar }}
          sx={{
            '& .MuiDataGrid-columnHeaders': { bgcolor: '#f2f6fc', fontWeight: 700 },
            '& .MuiDataGrid-cell': { whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' },
            '& .MuiDataGrid-row:hover': { bgcolor: '#e3f2fd' }
          }}
          initialState={{
            filter: { filterModel: { items: [] } }
          }}
        />
      </Box>
    </Paper>
  );
}

export default LeaveSummaryTab;
