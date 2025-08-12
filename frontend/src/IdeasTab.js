import React, { useState } from "react";
import { Box, Button, Typography, Paper, TextField, Select, MenuItem, InputLabel, FormControl, OutlinedInput, Chip, Autocomplete, Checkbox, ListItemText, IconButton, Tooltip } from "@mui/material";
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import SaveAltIcon from '@mui/icons-material/SaveAlt';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import { DataGrid, GridToolbar } from '@mui/x-data-grid';

function IdeasTab(props) {
  // --- Custom Multi-Column Filter State for IdeasTab ---
  const {
    ideasFilterCol, setIdeasFilterCol,
    ideasFilterVals, setIdeasFilterVals,
    ideasFilterText, setIdeasFilterText,
    ideasColumnFilters, setIdeasColumnFilters,
    columns, setColumns,
    data, setData,
    visibleCols, setVisibleCols,
    ideasViews, setIdeasViews,
    selectedIdeasView, setSelectedIdeasView,
    colSelectOpen, setColSelectOpen,
    sort, setSort,
    filters, setFilters,
    error, setError,
    selectedFile, setSelectedFile
  } = props;

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
      const res = await fetch("http://localhost:4000/api/ideas-upload", {
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
      // You can adjust below to use the relevant returned data as needed
      setColumns(json.columns || []);
      setData(json.data || []);
      setVisibleCols([]); // Do not load all columns by default
      setSelectedIdeasView('');
      setFilters({});
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

  const handleFilterChange = (colIdx, value) => {
    setFilters(f => ({ ...f, [colIdx]: value }));
  };

  const filteredData = data.filter(row => {
    if (!ideasColumnFilters.length) return true;
    return ideasColumnFilters.every(fil => {
      const colIdx = columns.indexOf(fil.col);
      if (colIdx === -1) return true;
      const cell = row[colIdx];
      return fil.vals.some(val => cell !== undefined && cell !== null && String(cell).toLowerCase().includes(String(val).toLowerCase()));
    });
  });

  const handleColCheck = (idx) => {
    setVisibleCols(cols =>
      cols.includes(idx) ? cols.filter(i => i !== idx) : [...cols, idx].sort((a, b) => a - b)
    );
  };

  const UPLOAD_VERSION = 2;

  // --- Old Single File Upload ---
  const SimpleUpload = (
  <Box sx={{ textAlign: 'center', maxWidth: 800, mx: 'auto', p: { xs: 1, md: 3 }, minHeight: 0 }}>
    <Paper  sx={{ mb: 3, p: 2, background: '#f8fafc', borderRadius: 2, boxShadow: 1}}>
      <form onSubmit={handleUpload} style={{ display: 'flex', alignItems: 'center', gap: 16, justifyContent: 'center' }}>
        <input
          type="file"
          accept=".xlsx,.xls"
          style={{ display: 'none' }}
          id="ideas-upload-input"
          onChange={e => setSelectedFile(e.target.files[0] || null)}
        />
        <label htmlFor="ideas-upload-input">
          <Button
            variant="contained"
            component="span"
            startIcon={<UploadFileIcon />}
            sx={{
              bgcolor: '#003366',
              color: '#fff',
              fontWeight: 300,
              borderRadius: 2,
              boxShadow: 1,
              textTransform: 'none',
              fontSize: 13,
              minWidth: 150,
              px: 3,
              py: 1.1,
              '&:hover': { bgcolor: '#002244' }
            }}
          >
            CHOOSE FILE
          </Button>
        </label>
        <Typography sx={{ minWidth: 120, fontSize: 13, color: '#333', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: 1 }}>
          {selectedFile ? selectedFile.name : 'No file chosen'}
        </Typography>
        <Button
          variant="contained"
          type="submit"
          sx={{
            bgcolor: '#003366',
            color: '#fff',
            fontWeight: 300,
            borderRadius: 2,
            boxShadow: 1,
            textTransform: 'none',
            fontSize: 13,
            minWidth: 120,
            px: 3,
            py: 1.1,
            '&:hover': { bgcolor: '#002244' }
          }}
        >
          UPLOAD
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
            setIdeasColumnFilters([]);
            setFilters({});
            setSort({ col: null, direction: 'asc' });
            setError("");
          }}
        >
          Reset
        </Button>
        {error && <Typography color="error" sx={{ fontSize: 14, ml: 2 }}>{error}</Typography>}
      </form>
    </Paper>
    </Box>
  );

  return (
  <Box>
      {/* Ideas Tracker Intro */}
      <Box sx={{ mb: 3 }}>
        {/* <Typography variant="h7" sx={{ fontWeight: 500, color: '#003366', mb: 1 }}>
          Ideas Tracker
        </Typography> */}
        <Typography variant="subtitle1" sx={{ color: '#888', fontSize: 13, mb: 1, textAlign: 'center' }} >
          Welcome to the Ideas Tracker. Upload your Excel (.xlsx or .xls) files to view, sort, and filter your ideas in an interactive table. Use the tools below to get started.
        </Typography>
      </Box>

      {/* Upload Controls Row */}
      {SimpleUpload}


      {/* Custom Multi-Column Filter Bar for IdeasTab */}
      {columns.length > 0 && (
        <Box sx={{ mb: 2, display: 'flex', alignItems: 'flex-end', gap: 3, flexWrap: 'nowrap' }}>
          <FormControl size="small" sx={{ minWidth: 180 }}>
            <InputLabel>Column</InputLabel>
            <Select
              value={ideasFilterCol}
              onChange={e => {
                setIdeasFilterCol(e.target.value);
                setIdeasFilterVals([]);
                setIdeasFilterText('');
              }}
              input={<OutlinedInput label="Column" />}
            >
              {columns
                .filter(col => !ideasColumnFilters.some(f => f.col === col))
                .map(col => (
                  <MenuItem value={col} key={col}>{col}</MenuItem>
                ))}
            </Select>
          </FormControl>
          <FormControl size="small" sx={{ minWidth: 220 }} disabled={!ideasFilterCol}>
            <InputLabel>Values</InputLabel>
            <Select
              multiple
              value={ideasFilterVals}
              onChange={e => setIdeasFilterVals(typeof e.target.value === 'string' ? e.target.value.split(',') : e.target.value)}
              input={<OutlinedInput label="Values" />}
              renderValue={selected => selected.join(', ')}
            >
              {ideasFilterCol && columns.includes(ideasFilterCol) && Array.from(new Set(data.map(row => row[columns.indexOf(ideasFilterCol)]).filter(v => v !== undefined && v !== null && String(v).trim() !== ''))).map(v => (
                <MenuItem key={String(v)} value={String(v)}>
                  <Checkbox checked={ideasFilterVals.indexOf(String(v)) > -1} />
                  <ListItemText primary={String(v)} />
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', minWidth: 260 }}>
            <TextField
              size="small"
              label="Press Enter Values or comma to add"
              disabled={!ideasFilterCol}
              value={ideasFilterText}
              onChange={e => setIdeasFilterText(e.target.value)}
              onKeyDown={e => {
                if ((e.key === 'Enter' || e.key === ',') && ideasFilterText.trim()) {
                  e.preventDefault();
                  if (!ideasFilterVals.includes(ideasFilterText.trim())) {
                    setIdeasFilterVals([...ideasFilterVals, ideasFilterText.trim()]);
                  }
                  setIdeasFilterText('');
                }
              }}
              sx={{ minWidth: 260 }}
            />
          </Box>
          <Button
            size="small"
            variant="contained"
            disabled={!ideasFilterCol || ideasFilterVals.length === 0}
            sx={{ minWidth: 120, fontWeight: 600 }}
            onClick={() => {
              if (!ideasFilterCol || ideasFilterVals.length === 0) return;
              setIdeasColumnFilters(prev => ([
                ...prev,
                { col: ideasFilterCol, vals: ideasFilterVals }
              ]));
              setIdeasFilterCol('');
              setIdeasFilterVals([]);
              setIdeasFilterText('');
            }}
          >
            Add Filter
          </Button>
        </Box>
      )}
      {/* Multi-Filter Chips Bar for IdeasTab */}
      {columns.length > 0 && ideasColumnFilters.length > 0 && (
        <Box sx={{ mb: 1, pl: 1, display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 1 }}>
          <Typography sx={{ fontWeight: 500, mr: 1, fontSize: 14, color: '#003366' }}>Active Filters:</Typography>
          {ideasColumnFilters.map((filter, fIdx) =>
            filter.vals.map((val, vIdx) => (
              <Chip
                key={filter.col + ':' + val}
                label={`${filter.col}: ${val}`}
                onDelete={() => {
                  setIdeasColumnFilters(prev => {
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

      {/* Saved Views and Select Columns UI for IdeasTab */}
      {columns.length > 0 && (
        <Box sx={{ mb: 2, display: 'flex', flexDirection: 'column', gap: 1 }}>
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 2,
              flexWrap: 'wrap',
              bgcolor: '#f7fafd',
              borderRadius: 3,
              p: 2.5,
              boxShadow: 2,
              border: '1.5px solid #e3eafc',
              minHeight: 72,
            }}
          >
            <FormControl sx={{ minWidth: 240, bgcolor: '#fff', borderRadius: 2, boxShadow: 0, fontWeight: 700 }} size="small">
              <InputLabel sx={{ fontWeight: 700, fontSize: 16, color: '#8a99b3' }}>Saved View</InputLabel>
              <Select
                value={selectedIdeasView}
                label="Saved View"
                onChange={e => {
                  setSelectedIdeasView(e.target.value);
                  window.localStorage.setItem('selectedIdeasView', e.target.value);
                  const view = ideasViews[e.target.value];
                  if (view) {
                    let colNames;
                    if (Array.isArray(view)) {
                      colNames = view;
                    } else {
                      colNames = view.columns || [];
                    }
                    setVisibleCols(Array.isArray(colNames) ? colNames.map(col => columns.indexOf(col)).filter(idx => idx !== -1) : []);
                  }
                }}
                sx={{ fontWeight: 700, borderRadius: 2, fontSize: 16, color: '#003366', bgcolor: '#fff', boxShadow: 0 }}
                MenuProps={{ PaperProps: { sx: { borderRadius: 2, boxShadow: 3 } } }}
              >
                {Object.keys(ideasViews).length === 0 && (
                  <MenuItem disabled>No views saved</MenuItem>
                )}
                {Object.keys(ideasViews).map(name => (
                  <MenuItem key={name} value={name} sx={{ fontWeight: 700, fontSize: 16 }}>{name}</MenuItem>
                ))}
              </Select>
            </FormControl>
            <Tooltip title="Add View">
              <IconButton color="primary" sx={{ mx: 0.5, bgcolor: '#fff', borderRadius: 2, border: '1.5px solid #003366', '&:hover': { bgcolor: '#e3f2fd' } }} onClick={() => {
                let name = prompt('Enter a name for this view:');
                if (!name) return;
                if (!visibleCols.length) {
                  alert('Please select columns to include in the view.');
                  return;
                }
                const newViews = { ...ideasViews, [name]: { columns: visibleCols.map(i => columns[i]) } };
                setIdeasViews(newViews);
                setSelectedIdeasView(name);
                window.localStorage.setItem('ideasViews', JSON.stringify(newViews));
                window.localStorage.setItem('selectedIdeasView', name);
              }}>
                <AddCircleOutlineIcon sx={{ fontSize: 16 }} />
              </IconButton>
            </Tooltip>
            <Tooltip title="Save View">
              <IconButton color="primary" sx={{ mx: 0.5, bgcolor: '#fff', borderRadius: 2, border: '1.5px solid #003366', '&:hover': { bgcolor: '#e3f2fd' } }} onClick={() => {
                if (!selectedIdeasView) return;
                if (!visibleCols.length) {
                  alert('Please select columns to include in the view.');
                  return;
                }
                const newViews = { ...ideasViews, [selectedIdeasView]: { columns: visibleCols.map(i => columns[i]) } };
                setIdeasViews(newViews);
                window.localStorage.setItem('ideasViews', JSON.stringify(newViews));
              }}>
                <SaveAltIcon sx={{ fontSize: 16 }} />
              </IconButton>
            </Tooltip>
            <Tooltip title="Edit View Name">
              <IconButton color="info" sx={{ mx: 0.5, bgcolor: '#fff', borderRadius: 2, border: '1.5px solid #1976d2', '&:hover': { bgcolor: '#e3f2fd' } }} onClick={() => {
                if (!selectedIdeasView) return;
                let name = prompt('Rename view:', selectedIdeasView);
                if (!name || name === selectedIdeasView) return;
                const newViews = { ...ideasViews };
                newViews[name] = newViews[selectedIdeasView];
                delete newViews[selectedIdeasView];
                setIdeasViews(newViews);
                setSelectedIdeasView(name);
                window.localStorage.setItem('ideasViews', JSON.stringify(newViews));
                window.localStorage.setItem('selectedIdeasView', name);
              }}>
                <EditOutlinedIcon sx={{ fontSize: 16 }} />
              </IconButton>
            </Tooltip>
            <Tooltip title="Delete View">
              <IconButton color="error" sx={{ mx: 0.5, bgcolor: '#fff', borderRadius: 2, border: '1.5px solid #d32f2f', '&:hover': { bgcolor: '#ffebee' } }} onClick={() => {
                if (!selectedIdeasView) return;
                if (!window.confirm(`Delete view '${selectedIdeasView}'?`)) return;
                const newViews = { ...ideasViews };
                delete newViews[selectedIdeasView];
                setIdeasViews(newViews);
                const keys = Object.keys(newViews);
                const next = keys.length ? keys[0] : '';
                setSelectedIdeasView(next);
                window.localStorage.setItem('ideasViews', JSON.stringify(newViews));
                window.localStorage.setItem('selectedIdeasView', next);
                if (!next) {
                  setVisibleCols([]);
                } else {
                  const view = newViews[next];
                  if (view) {
                    let colNames;
                    if (Array.isArray(view)) {
                      colNames = view;
                    } else {
                      colNames = view.columns || [];
                    }
                    setVisibleCols(Array.isArray(colNames) ? colNames.map(col => columns.indexOf(col)).filter(idx => idx !== -1) : []);
                  }
                }
              }}>
                <DeleteOutlineIcon sx={{ fontSize: 16 }} />
              </IconButton>
            </Tooltip>
          </Box>
          <Autocomplete
            multiple
            options={columns.map((col, idx) => ({ label: col, idx }))}
            value={visibleCols.map(i => ({ label: columns[i], idx: i })).filter(v => v.label)}
            onChange={(e, newValue) => setVisibleCols(newValue.map(v => v.idx))}
            filterSelectedOptions
            disableCloseOnSelect
            freeSolo={false}
            renderTags={(value, getTagProps) =>
              value.map((option, index) => (
                <Chip
                  variant="outlined"
                  label={option.label}
                  {...getTagProps({ index })}
                  key={option.label}
                />
              ))
            }
            renderInput={params => (
              <TextField {...params} variant="outlined" label="Select columns" placeholder="Type or select columns" size="small" />
            )}
            sx={{ mt: 1, minWidth: 350 }}
          />
        </Box>
      )}
      {columns.length > 0 && (
        <Paper sx={{ height: 520, width: '100%', overflow: 'auto', mb: 4, p: 2 }}>
           <DataGrid
            rows={filteredData.map((row, idx) => {
              const obj = { id: idx };
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
              renderHeader: (params) => (
                <Typography
                  variant="subtitle2"
                  sx={{
                    fontWeight: 600,
                    color: '#003366',
                    fontSize: 14,
                    letterSpacing: 0.2,
                    lineHeight: 1.2,
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                  }}
                >
                  {params.colDef.headerName}
                </Typography>
              ),
              filterOperators: [
                {
                  label: 'contains',
                  value: 'contains',
                  getApplyFilterFn: (filterItem) => {
                    if (!filterItem.value) return null;
                    return (params) =>
                      params.value && params.value.toString().toLowerCase().includes(filterItem.value.toString().toLowerCase());
                  },
                  InputComponent: (props) => (
                    <Autocomplete
                      size="small"
                      options={Array.from(new Set(data.map(row => row[i]).filter(v => v !== undefined && v !== null && v !== ''))).sort((a, b) => String(a).localeCompare(String(b)))}
                      value={props.item.value || ''}
                      onInputChange={(e, value) => props.applyValue({ ...props.item, value })}
                      renderInput={(params) => (
                        <TextField {...params}
                          placeholder="Type or select value"
                          variant="outlined"
                          size="small"
                          sx={{ fontSize: 13, bgcolor: '#f9fafb', borderRadius: 2, minWidth: 180 }}
                          InputProps={{ ...params.InputProps, style: { paddingRight: 32 } }}
                        />
                      )}
                      freeSolo
                      clearOnBlur={false}
                      sx={{ minWidth: 180, bgcolor: '#fff', borderRadius: 2 }}
                      popupIcon={null}
                      ChipProps={{ sx: { bgcolor: '#e3f2fd', color: '#003366', fontWeight: 500, fontSize: 13, m: 0.5 } }}
                    />
                  ),
                },
              ]
            }))}
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
    </Box>
  );
}

export default IdeasTab;
