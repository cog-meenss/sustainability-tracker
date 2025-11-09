import React, { useRef, useState } from "react";
import { Box, Button, Typography, Paper, TextField, Select, MenuItem, InputLabel, FormControl, OutlinedInput, Chip, Autocomplete, Checkbox, ListItemText, Stack, IconButton } from "@mui/material";
import UploadFileIcon from '@mui/icons-material/UploadFile';
import { DataGrid, GridToolbar } from '@mui/x-data-grid';

import { Tabs, Tab } from '@mui/material';

function TrainingTab(props) {
  // --- Custom Multi-Column Filter State ---
  const {
    multiFilterCol, setMultiFilterCol,
    multiFilterVals, setMultiFilterVals,
    multiFilterText, setMultiFilterText,
    multiColumnFilters, setMultiColumnFilters,
    views, setViews,
    selectedView, setSelectedView,
    columns, setColumns,
    data, setData,
    visibleCols, setVisibleCols,
    colSelectOpen, setColSelectOpen,
    sort, setSort,
    error, setError,
    selectedFile, setSelectedFile,
    filterModel, setFilterModel,
    chartColumns, setChartColumns,
    selectedCol, setSelectedCol,
    selectedValue, setSelectedValue,
  } = props;

  // --- Saved Views Handlers ---
  const handleSelectView = (name) => {
    setSelectedView(name);
    window.localStorage.setItem('selectedView', name);
    const view = views[name];
    if (view) {
      let colNames, filters, sort;
      if (Array.isArray(view)) {
        colNames = view;
        filters = undefined;
        sort = undefined;
      } else {
        colNames = view.columns || [];
        filters = view.filters;
        sort = view.sort;
      }
      setVisibleCols(Array.isArray(colNames) ? colNames.map(col => columns.indexOf(col)).filter(idx => idx !== -1) : []);
      if (filters) setFilterModel(filters);
      if (sort) setSort(sort);
    }
  };

  const handleSaveView = () => {
    let name = prompt('Enter a name for this view:', selectedView || '');
    if (!name) return;
    const newViews = { ...views, [name]: { columns: visibleCols.map(i => columns[i]), filters: filterModel, sort } };
    setViews(newViews);
    setSelectedView(name);
    window.localStorage.setItem('columnViews', JSON.stringify(newViews));
    window.localStorage.setItem('selectedView', name);
  };

  const handleEditView = () => {
    if (!selectedView) return;
    let name = prompt('Rename view:', selectedView);
    if (!name || name === selectedView) return;
    const newViews = { ...views };
    newViews[name] = newViews[selectedView];
    delete newViews[selectedView];
    setViews(newViews);
    setSelectedView(name);
    window.localStorage.setItem('columnViews', JSON.stringify(newViews));
    window.localStorage.setItem('selectedView', name);
  };

  const handleDeleteView = () => {
    if (!selectedView) return;
    if (!window.confirm(`Delete view '${selectedView}'?`)) return;
    const newViews = { ...views };
    delete newViews[selectedView];
    setViews(newViews);
    const keys = Object.keys(newViews);
    const next = keys.length ? keys[0] : '';
    setSelectedView(next);
    window.localStorage.setItem('columnViews', JSON.stringify(newViews));
    window.localStorage.setItem('selectedView', next);
    // Optionally clear columns/filters if no view left
    if (!next) {
      setVisibleCols([]);
      setFilterModel({ items: [] });
      setSort({ col: null, direction: 'asc' });
    } else {
      handleSelectView(next);
    }
  };

  const fileInput = useRef();

  const handleUpload = async (e) => {
    e.preventDefault();
    setError("");
    if (!selectedFile) {
      setError("Please select an Excel file.");
      return;
    }
    const formData = new FormData();
    formData.append("excel", selectedFile);
    try {
      const res = await fetch("/api/training-upload", {
        method: "POST",
        body: formData,
      });
      let json;
      try {
        json = await res.json();
      } catch (parseErr) {
        throw new Error("Server response was not valid JSON. Possible server error or maintenance mode.");
      }
      if (!res.ok) throw new Error(json.error || "Upload failed");
      setColumns(json.columns);
      setData(json.data);
      // On upload, if a saved view is selected, apply it
      const selectedView = window.localStorage.getItem('selectedView') || '';
      const views = JSON.parse(window.localStorage.getItem('columnViews') || '{}');
      if (selectedView && views[selectedView]) {
        let colNames, filters;
        if (Array.isArray(views[selectedView])) {
          // Legacy: just columns array
          colNames = views[selectedView];
          filters = undefined;
        } else {
          colNames = views[selectedView].columns || [];
          filters = views[selectedView].filters;
        }
        setVisibleCols(Array.isArray(colNames) ? colNames.map(col => json.columns.indexOf(col)).filter(idx => idx !== -1) : []);
        if (filters) setFilterModel(filters);
      } else {
        setVisibleCols([]);
      }
      setFilterModel({ items: [] });
      setSort({ col: null, direction: 'asc' });
    } catch (err) {
      setError(err.message);
    }
  };

  const handleSort = (colIdx) => {
    let direction = 'asc';
    if (sort.col === colIdx && sort.direction === 'asc') direction = 'desc';
    setSort({ col: colIdx, direction });
    setData(prev => {
      const sorted = [...prev].sort((a, b) => {
        const valA = a[colIdx] ?? '';
        const valB = b[colIdx] ?? '';
        if (!isNaN(valA) && !isNaN(valB) && valA !== '' && valB !== '') {
          return direction === 'asc' ? (valA - valB) : (valB - valA);
        }
        return direction === 'asc'
          ? String(valA).localeCompare(String(valB), undefined, { numeric: true, sensitivity: 'base' })
          : String(valB).localeCompare(String(valA), undefined, { numeric: true, sensitivity: 'base' });
      });
      return sorted;
    });
  };

  // Compute filteredData using custom multi-column filter logic
  const filteredData = (data && Array.isArray(data)) ? data.filter(row => {
    if (!multiColumnFilters || !multiColumnFilters.length) return true;
    return multiColumnFilters.every(fil => {
      const colIdx = columns ? columns.indexOf(fil.col) : -1;
      if (colIdx === -1) return true;
      const cell = row[colIdx];
      return fil.vals.some(val => cell !== undefined && cell !== null && String(cell).toLowerCase().includes(String(val).toLowerCase()));
    });
  }) : [];

  // --- Customizable Completion Chart State and Logic ---
  

  // Get unique values for a given column
  const getUniqueValues = (col) => {
    if (!columns || !filteredData) return [];
    const colIdx = columns.indexOf(col);
    if (colIdx === -1) return [];
    return Array.from(new Set(filteredData.map(row => row[colIdx]).filter(v => v !== undefined && v !== null && String(v).trim() !== '')));
  };

  // Calculate completion percent for a column+value
  const getCompletionPercent = (col, value) => {
    if (!columns || !filteredData) return 0;
    const colIdx = columns.indexOf(col);
    if (colIdx === -1) return 0;
    const total = filteredData.length;
    if (total === 0) return 0;
    const matched = filteredData.filter(row => String(row[colIdx]) === String(value)).length;
    return Math.round((matched / total) * 100);
  };

  // Add a new column+value to the chart
  const handleAddChartCol = () => {
    if (selectedCol && selectedValue && !chartColumns.find(c => c.col === selectedCol && c.value === selectedValue)) {
      setChartColumns([...chartColumns, { col: selectedCol, value: selectedValue }]);
    }
  };

  // Remove a column+value from the chart
  const handleRemoveChartCol = (col, value) => {
    setChartColumns(chartColumns.filter(c => !(c.col === col && c.value === value)));
  };


  const handleColCheck = (idx) => {
    setVisibleCols(cols =>
      cols.includes(idx) ? cols.filter(i => i !== idx) : [...cols, idx].sort((a, b) => a - b)
    );
  };

  // Toggle which upload version to show
  const UPLOAD_VERSION = 2; // 1: Simple, 2: Professional Card, 3: Stepper

  // --- Version 1: Simple Upload ---
  const SimpleUpload = (
    <Box sx={{ mb: 3 }}>
      <form onSubmit={handleUpload} style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <input
          type="file"
          accept=".xlsx,.xls"
          style={{ display: 'none' }}
          ref={fileInput}
          onChange={e => {
            setSelectedFile(e.target.files[0] || null);
            setError("");
          }}
        />
        <Button
          variant="contained"
          startIcon={<UploadFileIcon />}
          onClick={() => fileInput.current && fileInput.current.click()}
        >
          Choose File
        </Button>
        <Typography sx={{ minWidth: 120, fontSize: 14, color: '#333', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: 1 }}>
          {selectedFile ? selectedFile.name : 'No file chosen'}
        </Typography>
        <Button variant="contained" type="submit" color="primary">
          Upload
        </Button>
        <Button
          variant="outlined"
          color="secondary"
          sx={{ minWidth: 100, ml: 2, fontWeight: 600, fontSize: 13 }}
          onClick={() => {
            setSelectedFile(null);
            setColumns([]);
            setData([]);
            setVisibleCols([]);
            setMultiColumnFilters([]);
            setFilterModel({ items: [] });
            setSort({ col: null, direction: 'asc' });
            setError("");
          }}
        >
          Reset
        </Button>
      </form>
      {error && <Typography color="error" sx={{ fontSize: 14, mt: 1 }}>{error}</Typography>}
    </Box>
  );

  // --- Version 2: Professional Card ---
  const ProfessionalUpload = (
    <>
       <Box sx={{ mb: 3 }}>
         <Typography variant="subtitle1" sx={{ color: '#888', fontSize: 13, mb: 1, textAlign: 'center' }}>
           Welcome to the Training Tracker. Upload your Excel (.xlsx or .xls) files to view, sort, and filter your training data in an interactive table. Use the tools below to get started.
         </Typography>
       </Box>
       <Box sx={{
         mb: 3,
         p: 2,
         background: '#f8fafc',
         borderRadius: 2,
         boxShadow: 1,
         minWidth: 900,
         maxWidth: 1200,
         mx: 'auto',
         display: 'flex',
         alignItems: 'center',
         justifyContent: 'center',
         overflow: 'visible',
       }}>
         <form onSubmit={handleUpload} style={{ display: 'flex', alignItems: 'center', gap: 24, width: '100%', justifyContent: 'center', minWidth: 800, overflow: 'visible' }}>
           <input
             type="file"
             accept=".xlsx,.xls"
             style={{ display: 'none' }}
             ref={fileInput}
             onChange={e => {
               setSelectedFile(e.target.files[0] || null);
               setError("");
             }}
           />
           <Button
             variant="contained"
             component="span"
             startIcon={<UploadFileIcon />}
             onClick={() => fileInput.current && fileInput.current.click()}
             sx={{
               bgcolor: '#003366',
               color: '#fff',
               fontWeight: 500,
               borderRadius: 2,
               boxShadow: 1,
               textTransform: 'none',
               fontSize: 15,
               minWidth: 150,
               px: 3,
               py: 1.3,
               '&:hover': { bgcolor: '#002244' }
             }}
           >
             CHOOSE FILE
           </Button>
           <Typography
             sx={{
               flex: 1,
               minWidth: 0,
               fontSize: 15,
               color: '#333',
               overflow: 'hidden',
               textOverflow: 'ellipsis',
               whiteSpace: 'nowrap',
               textAlign: 'center'
             }}
           >
             {selectedFile ? selectedFile.name : 'No file chosen'}
           </Typography>
           <Button
             variant="contained"
             type="submit"
             sx={{
               bgcolor: '#003366',
               color: '#fff',
               fontWeight: 500,
               borderRadius: 2,
               boxShadow: 1,
               textTransform: 'none',
               fontSize: 15,
               minWidth: 120,
               px: 3,
               py: 1.3,
               '&:hover': { bgcolor: '#002244' }
             }}
           >
             UPLOAD
           </Button>
           <Button
             variant="outlined"
             color="secondary"
             sx={{
               minWidth: 100,
               fontWeight: 600,
               fontSize: 15,
               borderRadius: 2,
               px: 3,
               py: 1.3,
               borderColor: '#00b1e1',
               color: '#00b1e1',
               ml: 2,
               '&:hover': { borderColor: '#0094be', color: '#0094be', background: '#f0fcff' }
             }}
             onClick={() => {
               setSelectedFile(null);
               setColumns([]);
               setData([]);
               setVisibleCols([]);
               setMultiColumnFilters([]);
               setFilterModel({ items: [] });
               setSort({ col: null, direction: 'asc' });
               setError("");
             }}
           >
             RESET
           </Button>
         </form>
         {error && <Typography color="error" sx={{ fontSize: 14, mt: 1 }}>{error}</Typography>}
       </Box>
    </>
  );

  // --- Version 3: Stepper Upload ---
  const [activeStep, setActiveStep] = useState(0);
  const StepperUpload = (
    <Box sx={{ mb: 3, maxWidth: 900 }}>
      {/* <Typography variant="h5" sx={{ fontWeight: 700, color: '#003366', mb: 2 }}>
        Training Tracker
      </Typography> */}
      <Box sx={{ mb: 2 }}>
        <Typography variant="subtitle1" sx={{ color: '#555' }}>
          Step-by-step upload:
        </Typography>
      </Box>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        {/* Step 1: Select File */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Button
            variant="contained"
            startIcon={<UploadFileIcon />}
            onClick={() => fileInput.current && fileInput.current.click()}
            sx={{ minWidth: 120, whiteSpace: 'nowrap' }}
            disabled={activeStep !== 0}
          >
            Choose File
          </Button>
          <input
            type="file"
            accept=".xlsx,.xls"
            style={{ display: 'none' }}
            ref={fileInput}
            onChange={e => {
              setSelectedFile(e.target.files[0] || null);
              setError("");
              setActiveStep(1);
            }}
          />
          <Typography sx={{ flex: 1, minWidth: 0, fontSize: 14, color: '#333', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', px: 1 }}>
            {selectedFile ? selectedFile.name : 'No file chosen'}
          </Typography>
        </Box>
        {/* Step 2: Upload Button */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Button
            variant="contained"
            color="primary"
            type="button"
            sx={{ minWidth: 100, whiteSpace: 'nowrap' }}
            disabled={!selectedFile || activeStep !== 1}
            onClick={e => {
              setActiveStep(2);
              handleUpload(e);
            }}
          >
            Upload
          </Button>
          <Button
             variant="outlined"
             color="secondary"
             sx={{
               minWidth: 100,
               fontWeight: 600,
               fontSize: 15,
               borderRadius: 2,
               px: 3,
               py: 1.3,
               borderColor: '#00b1e1',
               color: '#00b1e1',
               ml: 2,
               '&:hover': { borderColor: '#0094be', color: '#0094be', background: '#f0fcff' }
             }}
             onClick={() => {
               setSelectedFile(null);
               setColumns([]);
               setData([]);
               setVisibleCols([]);
               setMultiColumnFilters([]);
               setFilterModel({ items: [] });
               setSort({ col: null, direction: 'asc' });
               setError("");
             }}
           >
             RESET
           </Button>
        </Box>
        {error && <Typography color="error" sx={{ fontSize: 14, mt: 1 }}>{error}</Typography>}
      </Box>
    </Box>
  );

  return (
    <Box>
      {/* Professional Training Tracker Intro */}
      <Box sx={{ mb: 3, textAlign: 'center' }}>
        {/* <Typography variant="h8" sx={{ fontWeight: 700, color: '#003366', mb: 1 }}>
          Training Tracker
        </Typography> */}
        <Typography variant="subtitle1" sx={{ color: '#888', fontSize: 13, mb: 1, textAlign: 'center' }}>
          Welcome to the Training Tracker. Upload your Excel (.xlsx or .xls) files to view, sort, and filter your training data in an interactive table. Use the tools below to get started.
        </Typography>
      </Box>

      {/* Instructions Card */}
      {/* <Box sx={{
        mb: 3,
        p: 2,
        background: '#f2f6fb',
        borderRadius: 2,
        boxShadow: 2,
        border: '1px solid #e0e7ef',
        maxWidth: 600,
      }}>
        <Typography variant="h6" sx={{ color: '#003366', mb: 1, fontWeight: 600 }}>
          Instructions
        </Typography>
        <Typography variant="body1" sx={{ color: '#333', mb: 0 }}>
          1. Click <b>Choose File</b> to select an Excel file (.xlsx or .xls) containing your training data.<br/>
          2. Review the selected file name.<br/>
          3. Click <b>Upload</b> to load your data into the tracker.<br/>
          4. Once uploaded, you can sort and filter the data using the table below.
        </Typography>
      </Box> */}



      {/* Upload Controls Row */}
    <Box sx={{display: 'flex', justifyContent: 'center', textAlign: 'center' }}>
      <Box component="form" onSubmit={handleUpload} sx={{
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        gap: 2,
        mb: 3,
        maxWidth: 600,
        width: '100%',
        background: '#f8fafd',
        borderRadius: 2,
        boxShadow: 1,
        p: 2
      }}>
        <input
          type="file"
          accept=".xlsx,.xls"
          style={{ display: 'none' }}
          ref={fileInput}
          onChange={e => {
            setSelectedFile(e.target.files[0] || null);
            setError("");
          }}
        />
        <Button
          variant="contained"
          startIcon={<UploadFileIcon />}
          onClick={() => fileInput.current && fileInput.current.click()}
          sx={{ minWidth: 120, whiteSpace: 'nowrap' }}
        >
          Choose File
        </Button>
        <Typography
          sx={{
            flex: 1,
            minWidth: 0,
            fontSize: 14,
            color: '#333',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            px: 1
          }}
        >
          {selectedFile ? selectedFile.name : 'No file chosen'}
        </Typography>
        <Button variant="contained" type="submit" color="primary" sx={{ minWidth: 100, whiteSpace: 'nowrap' }}>
          Upload
        </Button>
        {error && <Typography color="error" sx={{ fontSize: 14, ml: 2 }}>{error}</Typography>}
        <Button
          variant="outlined"
          color="secondary"
          sx={{ minWidth: 100, ml: 2, fontWeight: 600, fontSize: 13 }}
          onClick={() => {
            setSelectedFile(null);
            setColumns([]);
            setData([]);
            setVisibleCols([]);
            setMultiColumnFilters([]);
            setFilterModel({ items: [] });
            setSort({ col: null, direction: 'asc' });
            setError("");
          }}
        >
          Reset
        </Button>
        
      </Box>
      </Box>
      {columns && columns.length > 0 && (
        <Box sx={{ mb: 2, width: 400 }}>
          {/* Saved Views Dropdown */}
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1, gap: 1 }}>
            <FormControl size="small" sx={{ minWidth: 180 }}>
              <InputLabel id="saved-view-label">Saved View</InputLabel>
              <Select
                labelId="saved-view-label"
                value={selectedView}
                label="Saved View"
                onChange={e => {
                  if (e.target.value === '__add__') {
                    let name = prompt('Enter a name for the new view:');
                    if (!name) return;
                    if (views[name]) {
                      alert('A view with this name already exists.');
                      return;
                    }
                    const newViews = { ...views, [name]: { columns: visibleCols.map(i => columns[i]), filters: filterModel } };
                    setViews(newViews);
                    setSelectedView(name);
                    window.localStorage.setItem('columnViews', JSON.stringify(newViews));
                    window.localStorage.setItem('selectedView', name);
                  } else {
                    setSelectedView(e.target.value);
                    window.localStorage.setItem('selectedView', e.target.value);
                    const view = views[e.target.value];
                    if (view) {
                      const { columns: colNames, filters } = view;
                      setVisibleCols(colNames.map(col => columns.indexOf(col)).filter(idx => idx !== -1));
                      if (filters) setFilterModel(filters);
                    }
                  }
                }}
              >
                <MenuItem value="__add__" sx={{ fontStyle: 'italic', color: '#1976d2', fontWeight: 500 }}>
                  <span role="img" aria-label="add">➕</span> Add...
                </MenuItem>
                {Object.keys(JSON.parse(window.localStorage.getItem('columnViews') || '{}')).map(name => (
                  <MenuItem key={name} value={name}>
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
                      <span>{name}</span>
                      <Box>
                        <IconButton size="small" color="info" onClick={e => {
                          e.stopPropagation();
                          const newName = prompt('Rename view:', name);
                          if (!newName || newName === name) return;
                          const views = JSON.parse(window.localStorage.getItem('columnViews') || '{}');
                          views[newName] = views[name];
                          delete views[name];
                          window.localStorage.setItem('columnViews', JSON.stringify(views));
                          if (window.localStorage.getItem('selectedView') === name) {
                            window.localStorage.setItem('selectedView', newName);
                          }
                          setVisibleCols(v => [...v]);
                        }}><span role="img" aria-label="rename">✏️</span></IconButton>
                        <IconButton size="small" color="error" onClick={e => {
                          e.stopPropagation();
                          if (!window.confirm('Delete this view?')) return;
                          const views = JSON.parse(window.localStorage.getItem('columnViews') || '{}');
                          delete views[name];
                          window.localStorage.setItem('columnViews', JSON.stringify(views));
                          if (window.localStorage.getItem('selectedView') === name) {
                            window.localStorage.setItem('selectedView', '');
                          }
                          setVisibleCols(v => [...v]);
                        }}><span role="img" aria-label="delete">🗑️</span></IconButton>
                      </Box>
                    </Box>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <Button
              size="small"
              variant="outlined"
              sx={{ height: 36, whiteSpace: 'nowrap' }}
              onClick={() => {
                const name = prompt('Save current columns as view (name):');
                if (!name) return;
                const views = JSON.parse(window.localStorage.getItem('columnViews') || '{}');
                const selectedCols = visibleCols.map(idx => columns[idx]);
                views[name] = { columns: selectedCols, filters: filterModel };
                window.localStorage.setItem('columnViews', JSON.stringify(views));
                window.localStorage.setItem('selectedView', name);
                setVisibleCols([...visibleCols]);
              }}
            >Save View</Button>
          </Box>
          <Autocomplete
            multiple
            options={columns.map((col, i) => ({ label: col, idx: i }))}
            getOptionLabel={option => option.label}
            value={columns
              .map((col, i) => ({ label: col, idx: i }))
              .filter(option => visibleCols.includes(option.idx))}
            onChange={(e, value) => setVisibleCols(value.map(opt => opt.idx))}
            renderOption={(props, option, { selected }) => (
              <li {...props} key={option.idx} style={{ display: 'flex', alignItems: 'center' }}>
                <Checkbox
                  style={{ marginRight: 8 }}
                  checked={selected}
                />
                {option.label}
              </li>
            )}
            renderTags={(value, getTagProps) =>
              value.map((option, index) => (
                <Chip
                  variant="filled"
                  label={option.label}
                  {...getTagProps({ index })}
                  key={option.label}
                />
              ))
            }
            renderInput={params => (
              <TextField {...params} variant="outlined" label="Select columns" placeholder="Select columns" />
            )}
            disableCloseOnSelect
            sx={{ minWidth: 300 }}
            ListboxProps={{ style: { maxHeight: 400, overflow: 'auto' } }}
          />
        </Box>
      )}

      {/* Custom Multi-Column Filter Bar */}
      {columns && columns.length > 0 && (
        <Box sx={{ mb: 2, display: 'flex', alignItems: 'flex-end', gap: 3, flexWrap: 'nowrap' }}>
          <FormControl size="small" sx={{ minWidth: 180 }}>
            <InputLabel>Column</InputLabel>
            <Select
              value={multiFilterCol}
              onChange={e => {
                setMultiFilterCol(e.target.value);
                setMultiFilterVals([]);
                setMultiFilterText('');
              }}
              input={<OutlinedInput label="Column" />}
            >
              {columns
                .filter(col => !multiColumnFilters.some(f => f.col === col))
                .map(col => (
                  <MenuItem value={col} key={col}>{col}</MenuItem>
                ))}
            </Select>
          </FormControl>
          <FormControl size="small" sx={{ minWidth: 220 }} disabled={!multiFilterCol}>
            <InputLabel>Values</InputLabel>
            <Select
              multiple
              value={multiFilterVals}
              onChange={e => setMultiFilterVals(typeof e.target.value === 'string' ? e.target.value.split(',') : e.target.value)}
              input={<OutlinedInput label="Values" />}
              renderValue={selected => selected.join(', ')}
            >
              {multiFilterCol && getUniqueValues(multiFilterCol).map(v => (
                <MenuItem key={String(v)} value={String(v)}>
                  <Checkbox checked={multiFilterVals.indexOf(String(v)) > -1} />
                  <ListItemText primary={String(v)} />
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', minWidth: 260 }}>
            <TextField
              size="small"
              label="Press Enter Values or comma to add"
              disabled={!multiFilterCol}
              value={multiFilterText}
              onChange={e => setMultiFilterText(e.target.value)}
              onKeyDown={e => {
                if ((e.key === 'Enter' || e.key === ',') && multiFilterText.trim()) {
                  e.preventDefault();
                  if (!multiFilterVals.includes(multiFilterText.trim())) {
                    setMultiFilterVals([...multiFilterVals, multiFilterText.trim()]);
                  }
                  setMultiFilterText('');
                }
              }}
              sx={{ minWidth: 260 }}
            />
          </Box>
          <Button
            size="small"
            variant="contained"
            disabled={!multiFilterCol || multiFilterVals.length === 0}
            sx={{ minWidth: 120, fontWeight: 600 }}
            onClick={() => {
              if (!multiFilterCol || multiFilterVals.length === 0) return;
              setMultiColumnFilters(prev => ([
                ...prev,
                { col: multiFilterCol, vals: multiFilterVals }
              ]));
              setMultiFilterCol('');
              setMultiFilterVals([]);
              setMultiFilterText('');
            }}
          >
            Add Filter
          </Button>
        </Box>
      )}

      {/* Multi-Filter Chips Bar */}
      {columns && columns.length > 0 && multiColumnFilters && multiColumnFilters.length > 0 && (
        <Box sx={{ mb: 1, pl: 1, display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 1 }}>
          <Typography sx={{ fontWeight: 500, mr: 1, fontSize: 14, color: '#003366' }}>Active Filters:</Typography>
          {multiColumnFilters.map((filter, fIdx) =>
            filter.vals.map((val, vIdx) => (
              <Chip
                key={filter.col + ':' + val}
                label={`${filter.col}: ${val}`}
                onDelete={() => {
                  setMultiColumnFilters(prev => {
                    const newFilters = prev.map((f, idx) => idx === fIdx ? { ...f, vals: f.vals.filter((_, i) => i !== vIdx) } : f)
                      .filter(f => f.vals.length > 0);
                    return newFilters;
                  });
                }}
                sx={{ bgcolor: '#e3f2fd', color: '#003366', fontWeight: 500, fontSize: 13 }}
              />
            ))
          )}
        </Box>
      )}

      {/* Data Table */}
      {columns && columns.length > 0 && (
        <Paper sx={{ height: 520, width: '100%', overflow: 'auto', mb: 4, p: 2 }}>
           <DataGrid
            rows={filteredData.map((row, idx) => {
              const obj = { id: idx };
              // If no columns selected, show all columns
              (visibleCols.length ? visibleCols : columns.map((_, i) => i)).forEach(i => { obj[columns[i]] = row[i]; });
              return obj;
            })}
            columns={(visibleCols.length ? visibleCols : columns.map((_, i) => i)).map(i => ({
              field: columns[i],
              headerName: columns[i],
              flex: 1,
              sortable: true,
              filterable: true,
              minWidth: 120,
              resizable: true,
              pinnable: true,
            }))}
            filterModel={filterModel}
            onFilterModelChange={setFilterModel}
            pageSize={10}
            rowsPerPageOptions={[10, 20, 50, 100]}
            disableSelectionOnClick
            sx={{ fontSize: 13 }}
            components={{ Toolbar: GridToolbar }}
            density="comfortable"
            checkboxSelection
            disableColumnMenu={false}
            experimentalFeatures={{ newEditingApi: true }}
          />
        </Paper>
      )}
      {columns && columns.length > 0 && filteredData && filteredData.length > 0 && (
        <Box sx={{ mt: 2, mb: 4, maxWidth: 700, p: 2, background: '#f4f7fa', borderRadius: 2, boxShadow: 1 }}>
          {visibleCols.length > 0 && (() => {
            const chartCol = columns[visibleCols[0]];
            const colIdx = columns.indexOf(chartCol);
            if (colIdx === -1) return null;
            let valueCounts = {};
            let total = 0;
            filteredData.forEach(row => {
              const val = row[colIdx] ?? '';
              valueCounts[val] = (valueCounts[val] || 0) + 1;
              total++;
            });
            const values = Object.keys(valueCounts);
            const colors = ['#2196f3', '#4caf50', '#ff9800', '#e91e63', '#9c27b0', '#009688', '#ff5722', '#607d8b', '#ffc107', '#8bc34a'];
            let startAngle = 0;
            return (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                <svg width="120" height="120" viewBox="0 0 120 120">
                  {values.map((val, idx) => {
                    const percent = (valueCounts[val] / total) * 100;
                    const angle = (percent / 100) * 360;
                    const largeArc = angle > 180 ? 1 : 0;
                    const endAngle = startAngle + angle;
                    const x1 = 60 + 50 * Math.cos(Math.PI * (startAngle - 90) / 180);
                    const y1 = 60 + 50 * Math.sin(Math.PI * (startAngle - 90) / 180);
                    const x2 = 60 + 50 * Math.cos(Math.PI * (endAngle - 90) / 180);
                    const y2 = 60 + 50 * Math.sin(Math.PI * (endAngle - 90) / 180);
                    const pathData = `M60,60 L${x1},${y1} A50,50 0 ${largeArc},1 ${x2},${y2} Z`;
                    const slice = (
                      <path
                        key={val+idx}
                        d={pathData}
                        fill={colors[idx % colors.length]}
                        stroke="#fff"
                        strokeWidth={2}
                        style={{ opacity: percent === 0 ? 0.15 : 1 }}
                      />
                    );
                    startAngle += angle;
                    return slice;
                  })}
                </svg>
                <Box>
                  {values.map((val, idx) => (
                    <Box key={val+idx} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <Box sx={{ width: 16, height: 16, background: colors[idx % colors.length], borderRadius: '50%', mr: 1 }} />
                      <Typography sx={{ fontSize: 15 }}>
                        <b>{val === '' ? '[Empty]' : val}</b>: {valueCounts[val]} ({((valueCounts[val]/total)*100).toFixed(1)}%)
                      </Typography>
                    </Box>
                  ))}
                </Box>
              </Box>
            );
          })()}
        </Box>
      )}

    </Box>
  );
}

export default TrainingTab;
