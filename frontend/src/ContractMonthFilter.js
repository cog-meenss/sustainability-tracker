import React from "react";
import { Box, FormControl, InputLabel, Select, MenuItem, Chip, OutlinedInput } from "@mui/material";

export default function ContractMonthFilter({
  contracts = [],
  months = [],
  selectedContracts = [],
  setSelectedContracts,
  selectedMonths = [],
  setSelectedMonths
}) {
  // Handle contract selection/deselection
  const handleContractChange = (event) => {
    const value = event.target.value;
    // If clicking an already selected item, remove it
    if (selectedContracts.includes(value)) {
      setSelectedContracts(selectedContracts.filter(c => c !== value));
    } else {
      setSelectedContracts([...selectedContracts, value]);
    }
  };

  // Remove a contract chip
  const handleDeleteContract = (contract) => {
    setSelectedContracts(selectedContracts.filter(c => c !== contract));
  };
  
  // Handle month selection/deselection
  const handleMonthChange = (event) => {
    const value = event.target.value;
    // If clicking an already selected item, remove it
    if (selectedMonths.includes(value)) {
      setSelectedMonths(selectedMonths.filter(m => m !== value));
    } else {
      setSelectedMonths([...selectedMonths, value]);
    }
  };
  
  // Remove a month chip
  const handleDeleteMonth = (month) => {
    setSelectedMonths(selectedMonths.filter(m => m !== month));
  };
  return (
    <Box sx={{ display: 'flex', gap: 4, alignItems: 'center', mb: 2 }}>
      <FormControl sx={{ minWidth: 220 }} size="small">
        <InputLabel id="contract-filter-label">Select Contract</InputLabel>
        <Select
          labelId="contract-filter-label"
          multiple
          value={selectedContracts}
          onChange={(e) => setSelectedContracts(e.target.value)}
          onClose={(e) => e.stopPropagation()}
          input={<OutlinedInput label="Select Contract" />}
          renderValue={selected => (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {selected.map(value => (
                <Chip
                  key={value}
                  label={value}
                  size="small"
                  sx={{ m: 0.25 }}
                  onMouseDown={e => e.stopPropagation()}
                  onDelete={() => handleDeleteContract(value)}
                />
              ))}
            </Box>
          )}

          MenuProps={{ PaperProps: { sx: { maxHeight: 320 } } }}
        >
          {contracts.map(contract => (
            <MenuItem 
              key={contract} 
              value={contract}
              onClick={(e) => {
                e.preventDefault();
                if (selectedContracts.includes(contract)) {
                  setSelectedContracts(selectedContracts.filter(c => c !== contract));
                } else {
                  setSelectedContracts([...selectedContracts, contract]);
                }
              }}
              sx={selectedContracts.includes(contract) ? { backgroundColor: 'rgba(25, 118, 210, 0.08)' } : {}}
            >
              {contract}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl sx={{ minWidth: 180 }} size="small">
        <InputLabel id="month-filter-label">Select Month</InputLabel>
        <Select
          labelId="month-filter-label"
          multiple
          value={selectedMonths}
          onChange={(e) => setSelectedMonths(e.target.value)}
          onClose={(e) => e.stopPropagation()}
          input={<OutlinedInput label="Select Month" />}
          renderValue={selected => (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {selected.map(value => (
                <Chip
                  key={value}
                  label={value}
                  size="small"
                  sx={{ m: 0.25 }}
                  onMouseDown={e => e.stopPropagation()}
                  onDelete={() => handleDeleteMonth(value)}
                />
              ))}
            </Box>
          )}

          MenuProps={{ PaperProps: { sx: { maxHeight: 320 } } }}
        >
          {months.map(month => (
            <MenuItem 
              key={month} 
              value={month}
              onClick={(e) => {
                e.preventDefault();
                if (selectedMonths.includes(month)) {
                  setSelectedMonths(selectedMonths.filter(m => m !== month));
                } else {
                  setSelectedMonths([...selectedMonths, month]);
                }
              }}
              sx={selectedMonths.includes(month) ? { backgroundColor: 'rgba(25, 118, 210, 0.08)' } : {}}
            >
              {month}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  );
}
