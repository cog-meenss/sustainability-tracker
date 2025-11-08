import React, { useState } from "react";
import { Box, Button, Typography, Paper, TextField, Select, MenuItem, InputLabel, FormControl, OutlinedInput, Chip, Autocomplete, Checkbox, ListItemText, IconButton, Tooltip, Dialog, DialogTitle, DialogContent, DialogActions, LinearProgress, Alert, Accordion, AccordionSummary, AccordionDetails, Slider, Grid } from "@mui/material";
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import SaveAltIcon from '@mui/icons-material/SaveAlt';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import PsychologyIcon from '@mui/icons-material/Psychology';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import AssessmentIcon from '@mui/icons-material/Assessment';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { DataGrid, GridToolbar } from '@mui/x-data-grid';
import { evaluateIdeas, evaluateIdea, getEvaluationParameters, validateParameters, formatEvaluationSummary } from './services/ideaEvaluationService';

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

  // --- AI Evaluation State ---
  const [evaluations, setEvaluations] = useState({});
  const [evaluationParams, setEvaluationParams] = useState(getEvaluationParameters());
  const [showEvaluationDialog, setShowEvaluationDialog] = useState(false);
  const [evaluationProgress, setEvaluationProgress] = useState(null);
  const [evaluationError, setEvaluationError] = useState('');
  const [selectedIdeaForEvaluation, setSelectedIdeaForEvaluation] = useState(null);
  const [evaluationResults, setEvaluationResults] = useState([]);

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
      const res = await fetch("/api/ideas-upload", {
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

  // --- AI Evaluation Functions ---
  const handleEvaluateAllIdeas = async () => {
    if (!data || data.length === 0) {
      setEvaluationError('No ideas to evaluate. Please upload data first.');
      return;
    }

    setShowEvaluationDialog(true);
    setEvaluationError('');
    setEvaluationProgress({ completed: 0, total: data.length, percentage: 0 });

    try {
      // Convert data rows to idea objects
      const ideasToEvaluate = data.map((row, index) => {
        const idea = {};
        columns.forEach((col, colIndex) => {
          idea[col] = row[colIndex];
        });
        idea.id = index;
        return idea;
      });

      const results = await evaluateIdeas(ideasToEvaluate, evaluationParams, (progress) => {
        setEvaluationProgress(progress);
      });

      // Store evaluations
      const evaluationsMap = {};
      results.forEach((result) => {
        evaluationsMap[result.ideaIndex] = result.evaluation;
      });
      
      setEvaluations(evaluationsMap);
      setEvaluationResults(results);
      setEvaluationProgress(null);
      
    } catch (error) {
      setEvaluationError(`Evaluation failed: ${error.message}`);
      setEvaluationProgress(null);
    }
  };

  const handleEvaluateSingleIdea = async (rowIndex) => {
    if (!data || !data[rowIndex]) {
      setEvaluationError('Invalid idea selected for evaluation.');
      return;
    }

    setSelectedIdeaForEvaluation(rowIndex);
    
    try {
      // Convert data row to idea object
      const idea = {};
      columns.forEach((col, colIndex) => {
        idea[col] = data[rowIndex][colIndex];
      });
      idea.id = rowIndex;

      const result = await evaluateIdea(idea, evaluationParams);
      
      if (result.success) {
        setEvaluations(prev => ({
          ...prev,
          [rowIndex]: result.evaluation
        }));
      } else {
        setEvaluationError(`Evaluation failed: ${result.error || 'Unknown error'}`);
      }
    } catch (error) {
      setEvaluationError(`Evaluation failed: ${error.message}`);
    }
    
    setSelectedIdeaForEvaluation(null);
  };

  const handleUpdateEvaluationParams = (newParams) => {
    const validation = validateParameters(newParams);
    if (!validation.valid) {
      setEvaluationError(validation.error);
      return;
    }
    setEvaluationParams(newParams);
    setEvaluationError('');
  };

  const handleCloseEvaluationDialog = () => {
    setShowEvaluationDialog(false);
    setEvaluationProgress(null);
    setEvaluationError('');
  };

  const getSortedDataWithEvaluations = () => {
    if (Object.keys(evaluations).length === 0) return filteredData;
    
    return [...filteredData].sort((a, b) => {
      const aIndex = data.indexOf(a);
      const bIndex = data.indexOf(b);
      const aEval = evaluations[aIndex];
      const bEval = evaluations[bIndex];
      
      if (!aEval && !bEval) return 0;
      if (!aEval) return 1;
      if (!bEval) return -1;
      
      return (bEval.overallScore || 0) - (aEval.overallScore || 0);
    });
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
        <>
          {/* AI Evaluation Section */}
          <Paper sx={{ mb: 3, p: 2, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', borderRadius: 3, boxShadow: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <PsychologyIcon sx={{ color: 'white', fontSize: 28 }} />
                <Typography variant="h6" sx={{ color: 'white', fontWeight: 600 }}>
                  AI Idea Evaluation & Ranking
                </Typography>
              </Box>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <Button
                  variant="contained"
                  startIcon={<AssessmentIcon />}
                  onClick={handleEvaluateAllIdeas}
                  disabled={!data.length || evaluationProgress !== null}
                  sx={{
                    bgcolor: 'rgba(255, 255, 255, 0.2)',
                    color: 'white',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255, 255, 255, 0.3)',
                    '&:hover': {
                      bgcolor: 'rgba(255, 255, 255, 0.3)',
                    }
                  }}
                >
                  {evaluationProgress ? 'Evaluating...' : 'Evaluate All Ideas'}
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<TrendingUpIcon />}
                  onClick={() => setShowEvaluationDialog(true)}
                  sx={{
                    color: 'white',
                    borderColor: 'rgba(255, 255, 255, 0.5)',
                    '&:hover': {
                      borderColor: 'white',
                      bgcolor: 'rgba(255, 255, 255, 0.1)',
                    }
                  }}
                >
                  View Results
                </Button>
              </Box>
            </Box>
            
            {/* Evaluation Progress */}
            {evaluationProgress && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" sx={{ color: 'white', mb: 1 }}>
                  Evaluating ideas: {evaluationProgress.completed} of {evaluationProgress.total} ({evaluationProgress.percentage}%)
                </Typography>
                <LinearProgress 
                  variant="determinate" 
                  value={evaluationProgress.percentage}
                  sx={{ 
                    height: 8, 
                    borderRadius: 4,
                    bgcolor: 'rgba(255, 255, 255, 0.2)',
                    '& .MuiLinearProgress-bar': {
                      bgcolor: 'white',
                      borderRadius: 4,
                    }
                  }}
                />
              </Box>
            )}

            {/* Evaluation Summary */}
            {Object.keys(evaluations).length > 0 && (
              <Box sx={{ mt: 2, p: 2, bgcolor: 'rgba(255, 255, 255, 0.1)', borderRadius: 2 }}>
                <Typography variant="body2" sx={{ color: 'white', mb: 1 }}>
                  <strong>Evaluation Summary:</strong> {Object.keys(evaluations).length} ideas evaluated
                </Typography>
                {evaluationResults.length > 0 && (
                  <Typography variant="body2" sx={{ color: 'white' }}>
                    <strong>Top Idea:</strong> {evaluationResults[0] && formatEvaluationSummary(evaluationResults[0].evaluation)}
                  </Typography>
                )}
              </Box>
            )}
            
            {evaluationError && (
              <Alert severity="error" sx={{ mt: 2, bgcolor: 'rgba(255, 255, 255, 0.9)' }}>
                {evaluationError}
              </Alert>
            )}
          </Paper>

          {/* Evaluation Results Dialog */}
          <Dialog 
            open={showEvaluationDialog} 
            onClose={handleCloseEvaluationDialog}
            maxWidth="lg"
            fullWidth
          >
            <DialogTitle>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <AssessmentIcon />
                AI Idea Evaluation Results
              </Box>
            </DialogTitle>
            <DialogContent>
              {evaluationProgress && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="body2" gutterBottom>
                    Progress: {evaluationProgress.completed} of {evaluationProgress.total} ideas evaluated
                  </Typography>
                  <LinearProgress variant="determinate" value={evaluationProgress.percentage} />
                </Box>
              )}
              
              {/* Evaluation Parameters */}
              <Accordion sx={{ mb: 2 }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="h6">Evaluation Parameters</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Grid container spacing={2}>
                    {Object.entries(evaluationParams).map(([key, param]) => (
                      <Grid item xs={12} sm={6} key={key}>
                        <Typography variant="body2" gutterBottom>
                          {key.charAt(0).toUpperCase() + key.slice(1)} ({(param.weight * 100).toFixed(0)}%)
                        </Typography>
                        <Typography variant="caption" color="textSecondary">
                          {param.description}
                        </Typography>
                        <Slider
                          value={param.weight * 100}
                          onChange={(_, value) => {
                            const newParams = {
                              ...evaluationParams,
                              [key]: { ...param, weight: value / 100 }
                            };
                            handleUpdateEvaluationParams(newParams);
                          }}
                          min={5}
                          max={50}
                          step={5}
                          marks
                          valueLabelDisplay="auto"
                          valueLabelFormat={(value) => `${value}%`}
                        />
                      </Grid>
                    ))}
                  </Grid>
                </AccordionDetails>
              </Accordion>

              {/* Evaluation Results */}
              {evaluationResults.length > 0 && (
                <Box>
                  <Typography variant="h6" gutterBottom>Results</Typography>
                  {evaluationResults.map((result, index) => {
                    const evaluation = result.evaluation;
                    if (!evaluation) return null;
                    
                    return (
                      <Accordion key={result.ideaIndex} sx={{ mb: 1 }}>
                        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                            <Typography variant="body1">
                              #{index + 1} - Score: {evaluation.overallScore?.toFixed(1)}/10
                            </Typography>
                            <Chip 
                              label={evaluation.overallRanking} 
                              color={evaluation.overallScore >= 8 ? 'success' : evaluation.overallScore >= 6 ? 'primary' : 'warning'}
                              size="small"
                            />
                            <Chip 
                              label={evaluation.implementationPriority} 
                              variant="outlined"
                              size="small"
                            />
                          </Box>
                        </AccordionSummary>
                        <AccordionDetails>
                          <Box sx={{ mb: 2 }}>
                            <Typography variant="body2" paragraph>
                              <strong>Summary:</strong> {evaluation.summary}
                            </Typography>
                            
                            <Typography variant="subtitle2" gutterBottom>Detailed Scores:</Typography>
                            <Grid container spacing={1} sx={{ mb: 2 }}>
                              {Object.entries(evaluation.scores || {}).map(([criterion, score]) => (
                                <Grid item xs={6} sm={4} key={criterion}>
                                  <Box sx={{ p: 1, bgcolor: 'grey.50', borderRadius: 1 }}>
                                    <Typography variant="caption" display="block">
                                      {criterion.charAt(0).toUpperCase() + criterion.slice(1)}
                                    </Typography>
                                    <Typography variant="body2" fontWeight="bold">
                                      {score.score}/10
                                    </Typography>
                                  </Box>
                                </Grid>
                              ))}
                            </Grid>

                            {evaluation.recommendations && evaluation.recommendations.length > 0 && (
                              <Box sx={{ mb: 2 }}>
                                <Typography variant="subtitle2" gutterBottom>Recommendations:</Typography>
                                <Box component="ul" sx={{ pl: 2, mb: 0 }}>
                                  {evaluation.recommendations.map((rec, i) => (
                                    <Typography component="li" variant="body2" key={i}>
                                      {rec}
                                    </Typography>
                                  ))}
                                </Box>
                              </Box>
                            )}

                            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                              <Chip label={`Effort: ${evaluation.estimatedEffort}`} size="small" />
                              <Chip label={`Timeline: ${evaluation.marketReadiness}`} size="small" />
                              {evaluation.isAutomated && (
                                <Chip label="Automated Assessment" color="info" size="small" />
                              )}
                            </Box>
                          </Box>
                        </AccordionDetails>
                      </Accordion>
                    );
                  })}
                </Box>
              )}
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseEvaluationDialog}>Close</Button>
              {!evaluationProgress && data.length > 0 && (
                <Button 
                  variant="contained" 
                  onClick={handleEvaluateAllIdeas}
                  startIcon={<AssessmentIcon />}
                >
                  Re-evaluate All
                </Button>
              )}
            </DialogActions>
          </Dialog>
        </>
      )}
      {columns.length > 0 && (
        <Paper sx={{ height: 520, width: '100%', overflow: 'auto', mb: 4, p: 2 }}>
           <DataGrid
            rows={getSortedDataWithEvaluations().map((row, idx) => {
              const originalIdx = data.indexOf(row);
              const obj = { id: originalIdx, _rowIndex: originalIdx };
              (visibleCols.length ? visibleCols : columns.map((_, i) => i)).forEach(i => { obj[columns[i]] = row[i]; });
              
              // Add evaluation data
              const evaluation = evaluations[originalIdx];
              if (evaluation) {
                obj['AI_Score'] = evaluation.overallScore ? evaluation.overallScore.toFixed(1) : 'N/A';
                obj['AI_Ranking'] = evaluation.overallRanking || 'N/A';
                obj['AI_Priority'] = evaluation.implementationPriority || 'N/A';
                obj['AI_Effort'] = evaluation.estimatedEffort || 'N/A';
                obj['AI_Summary'] = evaluation.summary || 'No evaluation';
              } else {
                obj['AI_Score'] = 'Not evaluated';
                obj['AI_Ranking'] = 'Not evaluated';
                obj['AI_Priority'] = 'Not evaluated';
                obj['AI_Effort'] = 'Not evaluated';
                obj['AI_Summary'] = 'Click to evaluate';
              }
              
              return obj;
            })}
            columns={[
              // Evaluation columns first (always visible when evaluations exist)
              ...(Object.keys(evaluations).length > 0 ? [
                {
                  field: 'AI_Score',
                  headerName: '🤖 AI Score',
                  width: 120,
                  sortable: true,
                  renderCell: (params) => (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="body2" fontWeight="bold">
                        {params.value}
                      </Typography>
                      {params.value !== 'Not evaluated' && params.value !== 'N/A' && (
                        <Typography variant="caption" color="textSecondary">
                          /10
                        </Typography>
                      )}
                    </Box>
                  )
                },
                {
                  field: 'AI_Ranking',
                  headerName: '📊 Ranking',
                  width: 120,
                  renderCell: (params) => {
                    if (params.value === 'Not evaluated') {
                      return (
                        <Button
                          size="small"
                          startIcon={<PsychologyIcon />}
                          onClick={() => handleEvaluateSingleIdea(params.row._rowIndex)}
                          disabled={selectedIdeaForEvaluation === params.row._rowIndex}
                        >
                          Evaluate
                        </Button>
                      );
                    }
                    const color = params.value === 'Excellent' ? 'success' : 
                                 params.value === 'Good' ? 'primary' : 
                                 params.value === 'Average' ? 'warning' : 'error';
                    return <Chip label={params.value} color={color} size="small" />;
                  }
                },
                {
                  field: 'AI_Priority',
                  headerName: '⚡ Priority',
                  width: 100,
                  renderCell: (params) => {
                    if (params.value === 'Not evaluated') return <Typography variant="caption">-</Typography>;
                    const color = params.value === 'High' ? 'error' : 
                                 params.value === 'Medium' ? 'warning' : 'default';
                    return <Chip label={params.value} color={color} size="small" variant="outlined" />;
                  }
                },
                {
                  field: 'AI_Summary',
                  headerName: '💭 AI Summary',
                  width: 300,
                  renderCell: (params) => (
                    <Tooltip title={params.value} placement="top">
                      <Typography 
                        variant="body2" 
                        sx={{ 
                          overflow: 'hidden', 
                          textOverflow: 'ellipsis', 
                          whiteSpace: 'nowrap',
                          cursor: params.value !== 'Click to evaluate' ? 'help' : 'pointer'
                        }}
                      >
                        {params.value}
                      </Typography>
                    </Tooltip>
                  )
                }
              ] : []),
              // Original data columns
              ...(visibleCols.length ? visibleCols : columns.map((_, i) => i)).map(i => ({
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
              ],
            }))
            ]}
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
