import React, { useState, useEffect } from "react";
import { Box, Tabs, Tab, Paper, Button, Typography, CircularProgress, Stack, IconButton, Chip, Autocomplete, TextField, Accordion, AccordionSummary, AccordionDetails } from '@mui/material';

// --- Export CSV Handler ---
function handleExportCSV(contracts, months) {
  // Helper to safely format numbers (avoids NaN)
  const safe = (val, digits = 2) => {
    const num = Number(val);
    return isNaN(num) ? '0' : num.toFixed(digits);
  };

  // Build CSV header
  const headers = [
    'Contract/Associate', 'Associate Name/ID',
    ...months.map(m => [
      `${m} Revenue`,
      `${m} Leave FTE`,
      `${m} Total FTE`,
      `${m} Billed FTE`,
      `${m} Non-Billable FTE`
    ]).flat()
  ];
  let rows = [headers];

  // Build contract rows (summary row + all associates)
  contracts.forEach(contractObj => {
    const associates = Array.isArray(contractObj.associates) ? contractObj.associates : [];
    // Contract summary row
    const contractRow = [contractObj.contract, ''];
    months.forEach(m => {
      const totalRevenue = associates.reduce((sum, a) => sum + Number(a[`${m}_total_revenue`] || 0), 0);
      const leaveFte = associates.reduce((sum, a) => sum + Number(a[`${m}_leaveFte`] || 0), 0);
      const totalFte = associates.reduce((sum, a) => sum + Number(a[`${m}_fte`] || 0), 0);
      const billedFte = associates.reduce((sum, a) => sum + Number(a[`${m}_billedFte`] || 0), 0);
      const nonBillableFte = associates.reduce((sum, a) => sum + Number(a[`${m}_nonBillableFte`] || 0), 0);
      contractRow.push(
        safe(totalRevenue),
        safe(leaveFte),
        safe(totalFte),
        safe(billedFte),
        safe(nonBillableFte, 3)
      );
    });
    rows.push(contractRow);
    // Each associate row
    associates.forEach(a => {
      const assocRow = ['', a.name || a.empId || ''];
      months.forEach(m => {
        assocRow.push(
          safe(a[`${m}_total_revenue`]),
          safe(a[`${m}_leaveFte`]),
          safe(a[`${m}_fte`]),
          safe(a[`${m}_billedFte`]),
          safe(a[`${m}_nonBillableFte`], 3)
        );
      });
      rows.push(assocRow);
    });
  });

  // Convert to CSV string
  const csvContent = rows.map(r => r.join(',')).join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'fte_by_contract.csv';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}


import CloseIcon from '@mui/icons-material/Close';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import DownloadIcon from '@mui/icons-material/Download';
import * as XLSX from 'xlsx';
import LeaveSummaryTab from './LeaveSummaryTab';
import ContractMonthFilter from './ContractMonthFilter';
import { DataGrid, GridToolbar } from '@mui/x-data-grid';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Collapse
} from '@mui/material';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';

import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

// Format currency with commas and symbol
function formatCurrency(value, symbol) {
  if (value == null || value === '') return symbol + '0.00';
  let num = typeof value === 'string' ? parseFloat(value.replace(/[^0-9.-]+/g, "")) : value;
  if (isNaN(num)) num = 0;
  return symbol + num.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


const RevenueFteTab = (props) => {
  const { resetKey = 0 } = props;
  // Accordion expanded state
  const [accordionExpanded, setAccordionExpanded] = useState(() => {
    try {
      const val = localStorage.getItem('accordionExpanded');
      return val === null ? true : val === 'true';
    } catch { return true; }
  });
  React.useEffect(() => {
    localStorage.setItem('accordionExpanded', accordionExpanded);
  }, [accordionExpanded]);
  // --- Saved Views State (top-level only!) ---
  const [savedViews, setSavedViews] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('revenueFteSavedViews') || '{}');
    } catch { return {}; }
  });
  React.useEffect(() => {
    localStorage.setItem('revenueFteSavedViews', JSON.stringify(savedViews));
  }, [savedViews]);
  const [selectedViewName, setSelectedViewName] = useState('');
  const [viewNameInput, setViewNameInput] = useState('');

  // Save view handler
  const handleSaveView = () => {
    if (!viewNameInput.trim()) return;
    const newViews = {
      ...savedViews,
      [viewNameInput.trim()]: {
        people: peopleSelectedCols,
        leave: leaveSelectedCols,
      }
    };
    setSavedViews(newViews);
    setSelectedViewName(viewNameInput.trim());
    localStorage.setItem('revenueFteSavedViews', JSON.stringify(newViews));
  };
  // Load view handler
  const handleLoadView = (name) => {
    if (!name || !savedViews[name]) return;
    // Restore people columns by id
    const savedPeopleIds = (savedViews[name].people || []).map(c => c.id);
    setPeopleSelectedCols(peopleAvailableCols.filter(col => savedPeopleIds.includes(col.id)));
    setPeopleAvailableCols(peopleAvailableCols.filter(col => !savedPeopleIds.includes(col.id)));
    // Restore leave columns by id
    const savedLeaveIds = (savedViews[name].leave || []).map(c => c.id);
    setLeaveSelectedCols(leaveAvailableCols.filter(col => savedLeaveIds.includes(col.id)));
    setLeaveAvailableCols(leaveAvailableCols.filter(col => !savedLeaveIds.includes(col.id)));
    setSelectedViewName(name);
    setViewNameInput(name);
  };
  // Delete view handler
  const handleDeleteView = () => {
    if (!selectedViewName) return;
    const newViews = { ...savedViews };
    delete newViews[selectedViewName];
    setSavedViews(newViews);
    setSelectedViewName('');
    setViewNameInput('');
    localStorage.setItem('revenueFteSavedViews', JSON.stringify(newViews));
  };

  const {
    files, setFiles,
    processing, setProcessing,
    tabIdx, setTabIdx,
    tables, setTables,
    error, setError
  } = props;

  // --- Reset button visibility state ---
  const [showReset, setShowReset] = React.useState(false);

  // --- Dynamic Contract/Month Filter State (reset on new tables) ---
  const [selectedContracts, setSelectedContracts] = useState([]);
  const [selectedMonths, setSelectedMonths] = useState([]);
  React.useEffect(() => {
    setSelectedContracts([]);
    setSelectedMonths([]);
  }, [tables]);

  // --- Persist and restore tables ---
  React.useEffect(() => {
    if (tables && tables.length > 0) {
      localStorage.setItem('revenueTables', JSON.stringify(tables));
    } else {
      localStorage.removeItem('revenueTables');
    }
  }, [tables]);

  React.useEffect(() => {
    // On mount: clear uploads and tables, hide RESET, and remove revenueTables from localStorage
    setFiles([]); // Always clear uploaded files on mount
    setTables([]); // Always clear tables on mount
    setError(""); // Clear error on mount
    setShowReset(false); // Hide RESET button on tab entry
    localStorage.removeItem('revenueTables'); // Remove any saved tables so RESET never appears after reload
  }, []);

  // Show RESET after successful process (tables set)
  React.useEffect(() => {
    if (tables && tables.length > 0) {
      setShowReset(true);
    }
  }, [tables]);

  // Handle multi-file selection
  const handleFilesChange = (e) => {
    setFiles(Array.from(e.target.files));
    setTables([]); // reset tables on new upload
  };

  // Remove a file from the list
  const handleRemoveFile = (idx) => {
    setFiles(prev => prev.filter((_, i) => i !== idx));
  };

  // Parse Excel file to table data for DataGrid
  const extractTableData = async (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = new Uint8Array(e.target.result);
          const workbook = XLSX.read(data, { type: 'array' });
          const wsname = workbook.SheetNames[0];
          const ws = workbook.Sheets[wsname];
          const json = XLSX.utils.sheet_to_json(ws, { header: 1 });
          if (!json.length) return resolve({ name: file.name, columns: [], rows: [] });
          const columns = json[0].map((header, idx) => ({ field: String(header) || `col${idx}`, headerName: String(header) || `Column ${idx+1}`, flex: 1 }));
          const rows = json.slice(1).map((row, i) => {
            const rowObj = { id: i };
            (Array.isArray(columns) ? columns : []).forEach((col, j) => {
              rowObj[col.field] = row[j] || '';
            });
            return rowObj;
          });
          resolve({ name: file.name, columns, rows });
        } catch (err) {
          reject(err);
        }
      };
      reader.onerror = () => reject(reader.error);
      reader.readAsArrayBuffer(file);
    });
  };

  // --- Column selection state ---
  const [peopleAvailableCols, setPeopleAvailableCols] = useState([]);
  const [peopleSelectedCols, setPeopleSelectedCols] = useState([]);
  const [leaveAvailableCols, setLeaveAvailableCols] = useState([]);
  const [leaveSelectedCols, setLeaveSelectedCols] = useState([]);


  React.useEffect(() => {
    localStorage.setItem('peopleAvailableCols', JSON.stringify(peopleAvailableCols));
  }, [peopleAvailableCols]);
  React.useEffect(() => {
    localStorage.setItem('peopleSelectedCols', JSON.stringify(peopleSelectedCols));
  }, [peopleSelectedCols]);
  React.useEffect(() => {
    localStorage.setItem('leaveAvailableCols', JSON.stringify(leaveAvailableCols));
  }, [leaveAvailableCols]);
  React.useEffect(() => {
    localStorage.setItem('leaveSelectedCols', JSON.stringify(leaveSelectedCols));
  }, [leaveSelectedCols]);
  const [showColSelector, setShowColSelector] = useState(false);
  const [colSelectionConfirmed, setColSelectionConfirmed] = useState(false);

  // Persist and restore selected columns
  React.useEffect(() => {
    // Restore from localStorage if available after columns are loaded
    if (showColSelector && !colSelectionConfirmed) {
      const savedPeople = localStorage.getItem('peopleSelectedCols');
      const savedLeave = localStorage.getItem('leaveSelectedCols');
      if (savedPeople && peopleAvailableCols.length) {
        try {
          const arr = JSON.parse(savedPeople);
          // Only restore if all saved columns are in available
          if (arr.every(c => peopleAvailableCols.find(a => a.id === c.id))) {
            setPeopleSelectedCols(arr);
            setPeopleAvailableCols(peopleAvailableCols.filter(a => !arr.find(c => c.id === a.id)));
          }
        } catch {}
      }
      if (savedLeave && leaveAvailableCols.length) {
        try {
          const arr = JSON.parse(savedLeave);
          if (arr.every(c => leaveAvailableCols.find(a => a.id === c.id))) {
            setLeaveSelectedCols(arr);
            setLeaveAvailableCols(leaveAvailableCols.filter(a => !arr.find(c => c.id === a.id)));
          }
        } catch {}
      }
    }
  }, [showColSelector, peopleAvailableCols, leaveAvailableCols, colSelectionConfirmed]);

  React.useEffect(() => {
    if (colSelectionConfirmed) {
      localStorage.setItem('peopleSelectedCols', JSON.stringify(peopleSelectedCols));
      localStorage.setItem('leaveSelectedCols', JSON.stringify(leaveSelectedCols));
    }
  }, [colSelectionConfirmed, peopleSelectedCols, leaveSelectedCols]);

  // Helper to extract columns from backend response
  function extractColumnsFromData(data, key) {
    if (!Array.isArray(data) || !data.length) return [];
    return Object.keys(data[0]).map(col => ({ id: col, label: col }));
  }

  // Drag-and-drop handler
  function onDragEnd(result, tracker) {
    if (!result.destination) return;
    const sourceIdx = result.source.index;
    const destIdx = result.destination.index;
    let available, selected, setAvailable, setSelected;
    if (tracker === 'people') {
      available = Array.from(peopleAvailableCols);
      selected = Array.from(peopleSelectedCols);
      setAvailable = setPeopleAvailableCols;
      setSelected = setPeopleSelectedCols;
    } else {
      available = Array.from(leaveAvailableCols);
      selected = Array.from(leaveSelectedCols);
      setAvailable = setLeaveAvailableCols;
      setSelected = setLeaveSelectedCols;
    }
    // Drag from available to selected
    if (result.source.droppableId === 'available' && result.destination.droppableId === 'selected') {
      const [moved] = available.splice(sourceIdx, 1);
      selected.splice(destIdx, 0, moved);
    } else if (result.source.droppableId === 'selected' && result.destination.droppableId === 'available') {
      const [moved] = selected.splice(sourceIdx, 1);
      available.splice(destIdx, 0, moved);
    } else if (result.source.droppableId === 'selected' && result.destination.droppableId === 'selected') {
      const [moved] = selected.splice(sourceIdx, 1);
      selected.splice(destIdx, 0, moved);
    }
    setAvailable(available);
    setSelected(selected);
  }

  // After backend returns data, extract columns and show selector
  const handleProcess = async () => {
    setProcessing(true);
    setError("");
    setTables([]);
    try {
      const formData = new FormData();
      if (!files[0] || !files[1]) {
        setError("Please upload both Leave and People Tracker files.");
        setProcessing(false);
        return;
      }
      formData.append('leave', files[0]);
      formData.append('people', files[1]);
      formData.append('peopleSelectedCols', JSON.stringify(peopleSelectedCols.map(c => c.id)));
      formData.append('leaveSelectedCols', JSON.stringify(leaveSelectedCols.map(c => c.id)));
      const res = await fetch('http://localhost:4000/api/upload', {
        method: 'POST',
        body: formData,
      });
      let json;
      try {
        json = await res.json();
      } catch (parseErr) {
        throw new Error("Server response was not valid JSON. Possible server error or maintenance mode.");
      }
      if (!res.ok) throw new Error(json.error || "Upload failed");
      // Extract columns for selection UI
      setPeopleAvailableCols(extractColumnsFromData(json.people, 'people'));
      setPeopleSelectedCols([]);
      setLeaveAvailableCols(extractColumnsFromData(json.leaveSummary, 'leaveSummary'));
      setLeaveSelectedCols([]);
      setShowColSelector(true);
      setColSelectionConfirmed(false);

      // Build contract group rows with month-wise total FTE and leave FTE
      const contractGroups = {};
      (Array.isArray(json.people) ? json.people : []).forEach(p => {
        if (!contractGroups[p.contract]) contractGroups[p.contract] = [];
        contractGroups[p.contract].push(p);
      });
      // Build parent/child rows for true tree data
      const contractRows = Object.entries(contractGroups).map(([contract, associates], idx) => {
        const groupRow = { id: `contract-${contract}`, contract, isContractGroup: true, parentId: null };
        json.months.forEach(m => {
          groupRow[`${m}_fte`] = associates.reduce((sum, a) => sum + parseFloat(a[`${m}_fte`] || 0), 0).toFixed(2);
          groupRow[`${m}_leaveFte`] = associates.reduce((sum, a) => sum + parseFloat(a[`${m}_leaveFte`] || 0), 0).toFixed(2);
        });
        return groupRow;
      });
      setTables([json]);
      setTabIdx(0);
    } catch (err) {
      setError("Error processing files. Please check your upload and try again.");
    }
    setProcessing(false);
  };

  return (
    <>
      <Box sx={{ width: '100%', maxWidth: 1200, mx: 'auto', p: { xs: 1, md: 3 }, minHeight: 0 }}>
        <Typography variant="subtitle1" sx={{ color: '#555', mb: 2, fontSize: 14, textAlign: 'left', px: 0 }}>
          Welcome to the Revenue & FTE Tracker. Upload your Leave and People Tracker Excel files to process and analyze revenue and FTE data. Use the tools below to get started.
        </Typography>
        <Paper elevation={2} sx={{
          p: { xs: 2, md: 3 },
          mb: 3,
          borderRadius: 2,
          boxShadow: 1,
          background: '#f8fafc',
          width: '100%',
          maxWidth: '100%',
          mx: 'auto',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
        }}>
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              width: '100%',
              py: 2,
              border: '2px dashed',
              borderColor: files.length === 2 ? '#4caf50' : '#b0bec5',
              borderRadius: 3,
              background: files.length === 2 ? '#f1fdf4' : '#f8fafc',
              position: 'relative',
              transition: 'border-color 0.2s, background 0.2s',
              outline: 'none',
              '&:hover': { borderColor: '#003366', background: '#f0f7ff' },
              mb: 2,
            }}
            tabIndex={0}
            aria-label="File upload area"
            onKeyDown={e => {
              if ((e.key === 'Enter' || e.key === ' ') && !processing) {
                document.getElementById('dual-file-upload-input').click();
              }
            }}
          >
            <Button
              variant="contained"
              component="label"
              startIcon={<UploadFileIcon />}
              sx={{
                bgcolor: '#003366',
                color: '#fff',
                fontWeight: 400,
                borderRadius: 2,
                boxShadow: 2,
                textTransform: 'none',
                fontSize: 16,
                minWidth: 200,
                px: 3,
                py: 1.5,
                mb: 1.5,
                transition: 'transform 0.1s',
                '&:hover': { bgcolor: '#002244', transform: 'scale(1.04)' }
              }}
              aria-label="Choose Excel files"
            >
              Choose Files
              <input
                id="dual-file-upload-input"
                type="file"
                accept=".xlsx,.xls"
                hidden
                multiple
                onChange={e => setFiles(Array.from(e.target.files))}
              />
            </Button>
            <Typography sx={{ color: '#888', fontSize: 13, mb: 1, textAlign: 'center' }}>
              Upload both the 'Leave Tracker' and 'People Tracker' excel files (.xlsx or .xls)
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 1, justifyContent: 'center', width: '100%', minHeight: 38, transition: 'all 0.2s' }}>
              {files.length > 0
                ? files.map((file, idx) => (
                    <Chip
                      key={file.name + idx}
                      label={<span title={file.name} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                        <UploadFileIcon sx={{ fontSize: 17, mr: 0.5 }} />
                        <span style={{ maxWidth: 100, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{file.name}</span>
                      </span>}
                      onDelete={() => setFiles(prev => prev.filter((_, i) => i !== idx))}
                      size="medium"
                      sx={{ bgcolor: '#e3f2fd', color: '#003366', fontWeight: 500, fontSize: 14, borderRadius: 2, px: 1.5, py: 0.5, m: 0.25, maxWidth: 170, transition: 'all 0.2s' }}
                    />
                  ))
                : <Typography sx={{ fontSize: 13, color: '#888', minWidth: 110 }}>No file chosen</Typography>
              }
              {files.length === 2 && (
                <Box sx={{ display: 'flex', alignItems: 'center', ml: 2 }}>
                  <UploadFileIcon sx={{ color: '#4caf50', fontSize: 22, mr: 0.5 }} />
                  <Typography sx={{ color: '#388e3c', fontWeight: 600, fontSize: 14 }}>Ready</Typography>
                </Box>
              )}
            </Box>
            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', width: '100%' }}>
              <Button
                variant="contained"
                onClick={handleProcess}
                disabled={files.length < 2 || processing || tables.length > 0}
                sx={{
                  bgcolor: files.length < 2 || processing || tables.length > 0 ? '#bbb' : '#003366',
                  color: '#fff',
                  fontWeight: 500,
                  borderRadius: 2,
                  boxShadow: 2,
                  textTransform: 'none',
                  fontSize: 16,
                  minWidth: 200,
                  px: 3,
                  py: 1.4,
                  mt: 3,
                  transition: 'transform 0.1s',
                  '&:hover': { bgcolor: files.length < 2 || processing || tables.length > 0 ? '#bbb' : '#002244', transform: files.length < 2 || processing || tables.length > 0 ? 'none' : 'scale(1.04)' }
                }}
                aria-label="Process Files"
              >
                {processing ? <><CircularProgress size={20} sx={{ color: '#fff', mr: 1 }} />Processing...</> : 'Process Files'}
              </Button>
              {showReset && tables.length > 0 && (
                <Button
                  variant="outlined"
                  color="secondary"
                  onClick={() => {
                    setFiles([]);
                    setTables([]);
                    setError("");
                    setShowReset(false);
                    localStorage.removeItem('revenueTables');
                    // Do NOT clear saved views or column selections here
                  }}
                  sx={{ minWidth: 120, fontWeight: 600, fontSize: 15, ml: 2, mt: 3 }}
                >
                  Reset
                </Button>
              )}
            </Box>
          </Box>
          {error && <Typography color="error" sx={{ fontSize: 14, mt: 1 }}>{error}</Typography>}
          {processing && (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 120, width: '100%' }}>
              <CircularProgress size={40} sx={{ color: '#003366' }} />
            </Box>
          )}
        </Paper>
      </Box>

      {/* Column Selection UI */}
      {showColSelector && !processing && (
        <Box sx={{ width: '100%', maxWidth: 1100, mx: 'auto', mt: 3, mb: 2 }}>
          <Accordion
            expanded={accordionExpanded}
            onChange={(_, expanded) => setAccordionExpanded(expanded)}
            sx={{
              minWidth: 320,
              width: '100%',
              boxShadow: 2,
              bgcolor: '#f7fbff',
              borderRadius: 3,
              transition: 'all 0.3s cubic-bezier(.4,0,.2,1)',
              mx: 'auto'
            }}
          >
            <AccordionSummary
              expandIcon={<KeyboardArrowDownIcon />}
              aria-controls="col-select-content"
              id="col-select-header"
              sx={{
                minHeight: 56,
                px: 3,
                bgcolor: '#f7fbff',
                borderRadius: 3,
                fontWeight: 600,
                width: '100%',
                transition: 'all 0.3s cubic-bezier(.4,0,.2,1)'
              }}
            >
              <Typography variant="subtitle1" sx={{ fontWeight: 700 }}>
                Select Columns to Display
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
            <Box sx={{ display: 'flex', gap: 4, flexWrap: 'wrap', justifyContent: 'center' }}>
              {[{ label: 'People Tracker', available: peopleAvailableCols, selected: peopleSelectedCols, setSelected: setPeopleSelectedCols, setAvailable: setPeopleAvailableCols, tracker: 'people' },
                { label: 'Leave Tracker', available: leaveAvailableCols, selected: leaveSelectedCols, setSelected: setLeaveSelectedCols, setAvailable: setLeaveAvailableCols, tracker: 'leave' }].map((section, idx) => (
                <Box key={section.tracker} sx={{ minWidth: 340, maxWidth: 430, flex: 1, p: 2, bgcolor: '#fff', borderRadius: 2, boxShadow: 1 }}>
                  <Typography sx={{ fontWeight: 600, mb: 1, fontSize: 17 }}>{section.label}</Typography>
                  <DragDropContext onDragEnd={result => onDragEnd(result, section.tracker)}>
                    <Box sx={{ display: 'flex', gap: 2 }}>
                    {/* Available Columns */}
                    <Droppable droppableId="available">
  {(provided, snapshot) => (
    <Box ref={provided.innerRef} {...provided.droppableProps} sx={{ minWidth: 150, maxWidth: 200, minHeight: 180, bgcolor: '#f0f6fa', borderRadius: 2, p: 1, flex: 1, border: '1px dashed #b0c4d4', mr: 1, maxHeight: 260, overflowY: 'auto' }}>
      <Typography sx={{ fontSize: 13, color: '#888', mb: 1, textAlign: 'center' }}>Available</Typography>
      <Autocomplete
        size="small"
        options={section.available}
        getOptionLabel={opt => opt.label}
        filterSelectedOptions
        onChange={(_, value) => {
          if (value) {
            // Move to selected
            section.setAvailable(section.available.filter(c => c.id !== value.id));
            section.setSelected([ ...section.selected, value ]);
          }
        }}
        renderInput={params => <TextField {...params} label="Type to filter" variant="outlined" sx={{ mb: 1 }} />}
        sx={{ mb: 1 }}
      />
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
        {section.available.map((col, i) => (
          <Chip
            key={col.id}
            label={col.label}
            size="small"
            color="default"
            sx={{ bgcolor: '#e3f6fb', color: '#003366', fontWeight: 500, mb: 0.5, cursor: 'pointer', minWidth: 120, maxWidth: 180, whiteSpace: 'normal', textOverflow: 'ellipsis', overflow: 'hidden' }}
            onClick={() => {
              section.setAvailable(section.available.filter(c => c.id !== col.id));
              section.setSelected([ ...section.selected, col ]);
            }}
            {...provided.draggableProps}
            {...provided.dragHandleProps}
          />
        ))}
      </Box>
      {provided.placeholder}
    </Box>
  )}
</Droppable>
                    {/* Selected Columns */}
                    <Droppable droppableId="selected">
  {(provided, snapshot) => (
    <Box ref={provided.innerRef} {...provided.droppableProps} sx={{ minWidth: 150, maxWidth: 200, minHeight: 180, bgcolor: '#e8f5e9', borderRadius: 2, p: 1, flex: 1, border: '1px solid #4caf50', ml: 1, maxHeight: 260, overflowY: 'auto' }}>
      <Typography sx={{ fontSize: 13, color: '#388e3c', mb: 1, textAlign: 'center' }}>Selected</Typography>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
        {section.selected.map((col, i) => (
          <Chip
            key={col.id}
            label={col.label}
            size="small"
            color="success"
            sx={{ bgcolor: '#c8f8e5', color: '#003366', fontWeight: 600, mb: 0.5, cursor: 'pointer', minWidth: 120, maxWidth: 180, whiteSpace: 'normal', textOverflow: 'ellipsis', overflow: 'hidden' }}
            onDelete={() => {
              section.setSelected(section.selected.filter(c => c.id !== col.id));
              section.setAvailable([ ...section.available, col ]);
            }}
            {...provided.draggableProps}
            {...provided.dragHandleProps}
          />
        ))}
      </Box>
      {provided.placeholder}
    </Box>
  )}
</Droppable>
                  </Box>
                </DragDropContext>
              </Box>
            ))}
          </Box>
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 3, gap: 2 }}>
            {/* Saved Views UI */}
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%', maxWidth: 600 }}>
              <Autocomplete
                options={Object.keys(savedViews)}
                value={selectedViewName}
                onChange={(_, v) => handleLoadView(v)}
                renderInput={params => <TextField {...params} label="Saved Views" variant="outlined" size="small" />} 
                sx={{ minWidth: 180, flex: 1 }}
              />
              <TextField
                label="View Name"
                value={viewNameInput}
                onChange={e => setViewNameInput(e.target.value)}
                size="small"
                sx={{ minWidth: 160 }}
              />
              <Button variant="contained" color="success" size="small" sx={{ minWidth: 80 }} onClick={handleSaveView} disabled={!viewNameInput.trim()}>Save</Button>
              <Button variant="outlined" color="error" size="small" sx={{ minWidth: 80 }} onClick={handleDeleteView} disabled={!selectedViewName}>Delete</Button>
            </Box>
            <Button
              variant="contained"
              color="primary"
              onClick={() => {
                setColSelectionConfirmed(true);
                setAccordionExpanded(false);
              }}
              disabled={peopleSelectedCols.length === 0 && leaveSelectedCols.length === 0}
              sx={{ minWidth: 180, fontWeight: 600, fontSize: 16, borderRadius: 2, mt: 2 }}
            >
              Confirm Selection
            </Button>
          </Box>
        </AccordionDetails>
      </Accordion>
      </Box>
      )}

      {/* Table Tabs and Views */}
       {/* Show dynamic filter UI only after column selection is confirmed and closed */}
       {!processing && tables.length > 0 && colSelectionConfirmed && (
        <Box sx={{ width: '100%', maxWidth: 1200, mx: 'auto', mt: 0 }}>
          {/* Spacer between Select Columns and Filter */}
          <Box sx={{ height: 32 }} />
          {/* Dynamic Contract/Month Filter UI */}
          <ContractMonthFilter
            contracts={Array.from(new Set((tables[0]?.contractGroupedSummary || tables[0]?.summary || []).map(c => c.contract)))}
            months={Array.from(new Set((tables[0]?.contractGroupedSummary?.[0]?.months?.map(m => m.month) || tables[0]?.months || [])))}
            selectedContracts={selectedContracts || []}
            setSelectedContracts={setSelectedContracts}
            selectedMonths={selectedMonths || []}
            setSelectedMonths={setSelectedMonths}
          />
          <Tabs value={tabIdx} onChange={(_, v) => setTabIdx(v)} sx={{ mb: 2 }}>
            <Tab label="Total FTE" />
            <Tab label="Leave Summary" />
          </Tabs>
          {tabIdx === 0 && (
              <Paper sx={{ p: 2, mb: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, gap: 2 }}>
                  {/* Define contracts and months for export and table rendering */}
                  {(() => {
                    var contracts = Array.isArray(tables[0]?.contractGroupedSummary)
                      ? tables[0].contractGroupedSummary
                      : (Array.isArray(tables[0]?.summary) ? tables[0].summary : []);
                    var months = Array.isArray(tables[0]?.months) ? tables[0].months : [];
                    return (
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                        <Typography variant="h6" sx={{ fontWeight: 700, color: '#222', mb: 0, mt: 2, px: 0 }}>
                          Total FTE (by Contract)
                        </Typography>
                        <Button
                          variant="outlined"
                          startIcon={<DownloadIcon />}
                          sx={{ ml: 1, mt: 2, fontWeight: 600, borderRadius: 2, fontSize: 15 }}
                          onClick={() => handleExportCSV(contracts, months)}
                        >
                          EXPORT CSV
                        </Button>
                      </Box>
                    );
                  })()}
                </Box>
                <FteContractTable data={{
  ...tables[0],
  columns: (tables[0]?.columns || []).filter(col => peopleSelectedCols.find(sel => sel.id === col.field)),
  selectedContracts,
  selectedMonths
}} />
              </Paper>
            )}
          {tabIdx === 1 && (
             <LeaveSummaryTab leaveSummary={tables[0]?.leaveSummary || []} selectedCols={leaveSelectedCols} />
           )}
        </Box>
      )}
    </>
  );
}


function FteContractTable({ data }) {
  // Defensive copy for filter safety
  const selectedContracts = data.selectedContracts || [];
  const selectedMonths = data.selectedMonths || [];
  const [open, setOpen] = useState({});
  // Use summary from backend
  let contracts = Array.isArray(data.contractGroupedSummary) ? data.contractGroupedSummary : (Array.isArray(data.summary) ? data.summary : []);
  // Apply contract filter if any selected
  if (selectedContracts.length > 0) {
    contracts = contracts.filter(c => selectedContracts.includes(c.contract));
  }
  // Normalize months to 'Jan', 'Feb', ... 'Dec' for key access
  let months = (contracts[0]?.months?.map(m => m.month) || (Array.isArray(data.months) ? data.months : []))
    .map(m => m.charAt(0).toUpperCase() + m.slice(1,3).toLowerCase());
  // Apply month filter if any selected
  if (selectedMonths.length > 0) {
    months = months.filter(m => selectedMonths.includes(m));
  }

  // Compute totals for each month
  const totalPerMonth = months.map(m => {
    let sumRevenue = 0;
    let sumLeaveFte = 0;
    contracts.forEach(contractObj => {
      const associates = Array.isArray(contractObj.associates) ? contractObj.associates : [];
      // Sum revenue for this contract/month
      const contractRevenue = associates.reduce((sum, a) => {
        let val = a[`${m}_total_revenue`] || "0";
        val = parseFloat(typeof val === 'string' ? val.replace(/[^0-9.-]+/g, "") : val);
        return sum + (isNaN(val) ? 0 : val);
      }, 0);
      sumRevenue += contractRevenue;
      // Sum leave FTE for this contract/month
      const contractLeaveFte = associates.reduce((sum, a) => sum + parseFloat(a[`${m}_leaveFte`] || 0), 0);
      sumLeaveFte += contractLeaveFte;
    });
    return { revenue: sumRevenue, leaveFte: sumLeaveFte };
  });

  return (
    <TableContainer>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell />
            <TableCell sx={{ fontWeight: 700 }}>Contract</TableCell>
            {months.map(m => [
              <TableCell key={m+"usd"} align="right" sx={{ fontWeight: 700 }}>{m} Revenue</TableCell>,
              <TableCell key={m+"leaveFte"} align="right" sx={{ fontWeight: 700 }}>{m} Leave FTE</TableCell>,
              <TableCell key={m+"totalFte"} align="right" sx={{ fontWeight: 700, bgcolor: '#e3f2fd' }}>{m} Revenue FTE</TableCell>,
              <TableCell key={m+"billedFte"} align="right" sx={{ fontWeight: 700, bgcolor: '#fffde7' }}>{m} Billed FTE</TableCell>,
              <TableCell key={m+"nonBillable"} align="right" sx={{ fontWeight: 700, bgcolor: '#fff3e0' }}>{m} Non-Billable FTE</TableCell>
            ])}
          </TableRow>
        </TableHead>
        <TableBody>
          {contracts.map(contractObj => (
            <React.Fragment key={contractObj.contract}>
              {/* Collapsed: Contract-level monthly summary */}
              <TableRow sx={{ bgcolor: '#f2f6fc', fontWeight: 700 }}>
                <TableCell>
                  <IconButton size="small" onClick={() => setOpen(o => ({ ...o, [contractObj.contract]: !o[contractObj.contract] }))}>
                    {open[contractObj.contract] ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                  </IconButton>
                </TableCell>
                <TableCell sx={{ fontWeight: 700 }}>{contractObj.contract}</TableCell>
                {months.map((m, idx) => {
                  const associates = Array.isArray(contractObj.associates) ? contractObj.associates : [];
                  const totalRevenue = associates.reduce((sum, a) => {
                    let val = a[`${m}_total_revenue`] || "0";
                    val = parseFloat(typeof val === 'string' ? val.replace(/[^0-9.-]+/g, "") : val);
                    return sum + (isNaN(val) ? 0 : val);
                  }, 0).toFixed(2);
                  const totalLeaveFte = associates.reduce((sum, a) => sum + parseFloat(a[`${m}_leaveFte`] || 0), 0).toFixed(2);
                  // Calculate total billed FTE directly from associates
                  const totalBilledFte = associates.reduce((sum, a) => sum + parseFloat(a[`${m}_billedFte`] || 0), 0).toFixed(2);
                  // Calculate total non-billable FTE directly from associates
                  const totalNonBillableFte = associates.reduce((sum, a) => sum + parseFloat(a[`${m}_nonBillableFte`] || 0), 0).toFixed(3);
                  // Calculate total FTE directly from associates
                  const totalFteSum = associates.reduce((sum, a) => sum + parseFloat(a[`${m}_fte`] || 0), 0).toFixed(2);
                  // Pull contract-level summary for this month
                  const monthSummary = (contractObj.months || []).find(ms => ms.month === m) || {};
                  return [
                    <TableCell key={m+"usd"} align="right" sx={{ fontWeight: 700 }}>{formatCurrency(totalRevenue, '$')}</TableCell>,
                    <TableCell key={m+"leaveFte"} align="right" sx={{ fontWeight: 700 }}>{totalLeaveFte}</TableCell>,
                    <TableCell key={m+"totalFte"} align="right" sx={{ fontWeight: 700, bgcolor: '#e3f2fd' }}>{totalFteSum}</TableCell>,
                    <TableCell key={m+"billedFte"} align="right" sx={{ fontWeight: 700, bgcolor: '#fffde7' }}>{totalBilledFte}</TableCell>,
                    <TableCell key={m+"nonBillable"} align="right" sx={{ fontWeight: 700, bgcolor: '#fff3e0' }}>{totalNonBillableFte}</TableCell>
                  ];
                })}
              </TableRow>
              {/* Expanded: Per-associate/month breakdown */}
              <TableRow>
                <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={2 + months.length*5}>
                  <Collapse in={!!open[contractObj.contract]} timeout="auto" unmountOnExit>
                    <Box sx={{ m: 1 }}>
                      <Table size="small" sx={{ width: '100%' }}>
                        <TableHead>
                          <TableRow>
                            <TableCell sx={{ fontWeight: 600 }}>Associate ID</TableCell>
                            {months.map(m => [
                              <TableCell key={m+"costRevenue"} align="right">{m} Revenue (GBP)</TableCell>,
                              <TableCell key={m+"totalRevenue"} align="right">{m} Revenue (USD)</TableCell>,
                              <TableCell key={m+"leaveFte"} align="right">{m} Leave FTE</TableCell>,
                              <TableCell key={m+"billedFte"} align="right" sx={{ bgcolor: '#fffde7' }}>{m} Billed FTE</TableCell>,
                              <TableCell key={m+"nonBillable"} align="right" sx={{ bgcolor: '#fff3e0' }}>{m} Non-Billable FTE</TableCell>
                            ])}
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {(Array.isArray(contractObj.associates) ? contractObj.associates : []).map((a, idx) => (
                            <TableRow key={`assoc-${a.empId}-${contractObj.contract}-${idx}`}> 
                              <TableCell>{a.empId}</TableCell>
                              {months.map((m, colIdx) => {
                                // Debug: Log fields for first associate of first contract for first month
                                if (idx === 0 && contractObj.contract && colIdx === 0) {
                                  // Only log for first associate, first contract, first month
                                  // eslint-disable-next-line no-console
                                  console.log('DEBUG associate fields:', a);
                                }
                                return [
                                  <TableCell key={`cell-${a.empId}-${contractObj.contract}-${m}-costRevenue`} align="right">{formatCurrency(a[`${m}_cost_revenue`], '£')}</TableCell>,
                                  <TableCell key={`cell-${a.empId}-${contractObj.contract}-${m}-totalRevenue`} align="right">{formatCurrency(a[`${m}_total_revenue`], '$')}</TableCell>,
                                  <TableCell key={`cell-${a.empId}-${contractObj.contract}-${m}-leaveFte`} align="right">{a[`${m}_leaveFte`] ?? '0.00'}</TableCell>,
                                  <TableCell key={`cell-${a.empId}-${contractObj.contract}-${m}-billedFte`} align="right" sx={{ bgcolor: '#fffde7' }}>{a[`${m}_billedFte`] ?? '0.00'}</TableCell>,
                                  <TableCell key={`cell-${a.empId}-${contractObj.contract}-${m}-nonBillable`} align="right" sx={{ bgcolor: (parseFloat(a[`${m}_nonBillableFte`] || 0) > 0 ? '#fff3e0' : undefined) }}>
  {parseFloat(a[`${m}_nonBillableFte`] || 0) > 0 ? <span style={{ fontWeight: 600 }}>{parseFloat(a[`${m}_nonBillableFte`]).toFixed(3)}</span> : '0.000'}
</TableCell>
                                ];
                              })}
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </Box>
                  </Collapse>
                </TableCell>
              </TableRow>
            </React.Fragment>
          ))}
          {/* Total row */}
          <TableRow sx={{ bgcolor: '#e3f2fd', fontWeight: 700 }}>
            <TableCell />
            <TableCell sx={{ fontWeight: 700 }}>Total</TableCell>
            {months.map((m, idx) => {
              // Sum all columns for each month
              const revenue = contracts.reduce((sum, c) => {
                const associates = Array.isArray(c.associates) ? c.associates : [];
                return sum + associates.reduce((s, a) => {
                  let val = a[`${m}_total_revenue`] || "0";
                  val = parseFloat(typeof val === 'string' ? val.replace(/[^0-9.-]+/g, "") : val);
                  return s + (isNaN(val) ? 0 : val);
                }, 0);
              }, 0);
              const leaveFte = contracts.reduce((sum, c) => {
                const associates = Array.isArray(c.associates) ? c.associates : [];
                return sum + associates.reduce((s, a) => s + parseFloat(a[`${m}_leaveFte`] || 0), 0);
              }, 0);
              const totalFte = contracts.reduce((sum, c) => {
                const associates = Array.isArray(c.associates) ? c.associates : [];
                return sum + associates.reduce((s, a) => s + parseFloat(a[`${m}_fte`] || 0), 0);
              }, 0);
              const billedFte = contracts.reduce((sum, c) => {
                const associates = Array.isArray(c.associates) ? c.associates : [];
                return sum + associates.reduce((s, a) => s + parseFloat(a[`${m}_billedFte`] || 0), 0);
              }, 0);
              const nonBillableFte = contracts.reduce((sum, c) => {
  const associates = Array.isArray(c.associates) ? c.associates : [];
  return sum + associates.reduce((s, a) => s + parseFloat(a[`${m}_nonBillableFte`] || 0), 0);
}, 0);
              return [
                <TableCell key={m+"usd-total"} align="right" sx={{ fontWeight: 700 }}>{formatCurrency(revenue, '$')}</TableCell>,
                <TableCell key={m+"leaveFte-total"} align="right" sx={{ fontWeight: 700 }}>{leaveFte.toFixed(2)}</TableCell>,
                <TableCell key={m+"totalFte-total"} align="right" sx={{ fontWeight: 700, bgcolor: '#e3f2fd' }}>{totalFte.toFixed(2)}</TableCell>,
                <TableCell key={m+"billedFte-total"} align="right" sx={{ fontWeight: 700, bgcolor: '#fffde7' }}>{billedFte.toFixed(2)}</TableCell>,
                <TableCell key={m+"nonBillable-total"} align="right" sx={{ fontWeight: 700, bgcolor: '#fff3e0' }}>{nonBillableFte.toFixed(3)}</TableCell>
              ];
            })}
          </TableRow>
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default RevenueFteTab;
