import React, { useRef } from 'react';
import { Box, IconButton, InputBase, Paper, Tooltip } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import UploadFileIcon from '@mui/icons-material/UploadFile';

export default function ChatInput({ value, onChange, onSend, onUpload, disabled }) {
  const inputRef = useRef();
  return (
    <Paper
      elevation={3}
      sx={{
        position: 'fixed',
        bottom: 0,
        left: { xs: 0, md: '240px' },
        right: 0,
        zIndex: 1201,
        mx: 'auto',
        maxWidth: 900,
        borderRadius: 4,
        boxShadow: '0 2px 16px 0 rgba(0,0,0,0.07)',
        bgcolor: 'rgba(255,255,255,0.88)',
        backdropFilter: 'blur(8px)',
        px: { xs: 1.5, md: 2.5 },
        py: 1,
        display: 'flex',
        alignItems: 'center',
        mb: { xs: 0, md: 3 },
        border: '1px solid #e3e6ee',
      }}
    >
      <InputBase
        inputRef={inputRef}
        value={value}
        onChange={onChange}
        onKeyDown={e => {
          if (e.key === 'Enter' && !e.shiftKey && !disabled) {
            e.preventDefault();
            onSend && onSend();
          }
        }}
        placeholder="Send a message..."
        sx={{
          flex: 1,
          px: 2,
          fontSize: 18,
          fontFamily: 'Montserrat, Arial, sans-serif',
          bgcolor: 'transparent',
        }}
        multiline
        minRows={1}
        maxRows={4}
        disabled={disabled}
      />
      <Tooltip title="Upload file">
        <span>
          <IconButton component="label" sx={{ mx: 0.5 }} disabled={disabled}>
            <UploadFileIcon sx={{ fontSize: 28 }} />
            <input type="file" hidden onChange={onUpload} />
          </IconButton>
        </span>
      </Tooltip>
      <Tooltip title="Send">
        <span>
          <IconButton onClick={onSend} sx={{ ml: 0.5, bgcolor: '#00b1e1', color: '#fff', '&:hover': { bgcolor: '#0094be' } }} disabled={disabled}>
            <SearchIcon sx={{ fontSize: 28 }} />
          </IconButton>
        </span>
      </Tooltip>
    </Paper>
  );
}
