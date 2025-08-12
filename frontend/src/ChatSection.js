import React, { useEffect, useRef } from 'react';
import { Box, Typography, IconButton, Tooltip } from '@mui/material';
import RestartAltIcon from '@mui/icons-material/RestartAlt';

export default function ChatSection({ messages, aiTyping, onClearChat }) {
  const endRef = useRef();
  useEffect(() => {
    if (endRef.current) endRef.current.scrollIntoView({ behavior: 'smooth' });
  }, [messages, aiTyping]);

  return (
    <Box
      sx={{
        flex: 1,
        width: '100%',
        maxWidth: 900,
        mx: 'auto',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'stretch',
        justifyContent: 'flex-end',
        py: { xs: 1, md: 4 },
        px: { xs: 1, md: 2 },
        minHeight: '60vh',
        position: 'relative',
        overflowY: 'auto',
        bgcolor: 'rgba(255,255,255,0.97)',
        borderRadius: 4,
        boxShadow: '0 2px 16px 0 rgba(0,0,0,0.03)',
      }}
    >
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 1 }}>
        {messages && messages.length > 0 && (
          <Tooltip title="Clear chat">
            <IconButton onClick={onClearChat} size="small" sx={{ color: '#b0c4d4', bgcolor: '#fff', border: '1px solid #e3e6ee', '&:hover': { bgcolor: '#e3f6fb', color: '#00b1e1' }, mr: 0.5 }}>
              <RestartAltIcon />
            </IconButton>
          </Tooltip>
        )}
      </Box>
      {(!messages || messages.length === 0) ? (
        <Box sx={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: 0.55 }}>
          <Typography variant="h5" sx={{ fontWeight: 400, color: '#003366', textAlign: 'center', fontFamily: 'Montserrat, Arial, sans-serif' }}>
            Start a new conversation
            <br />
            <Typography variant="body1" sx={{ mt: 1, color: '#6d7a8c', fontWeight: 300 }}>
              Ask anything, upload a file, or search for insights.
            </Typography>
          </Typography>
        </Box>
      ) : (
        <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 2, mt: 2, mb: 8 }}>
          {messages.map((msg, i) => (
            <Box
              key={i}
              sx={{
                display: 'flex',
                justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                alignItems: 'flex-end',
                width: '100%',
              }}
            >
              <Box
                sx={{
                  maxWidth: '80%',
                  bgcolor: msg.role === 'user' ? '#e3f6fb' : '#fff',
                  color: '#003366',
                  px: 2.2,
                  py: 1.3,
                  borderRadius: 3,
                  borderTopLeftRadius: msg.role === 'user' ? 12 : 3,
                  borderTopRightRadius: msg.role === 'user' ? 3 : 12,
                  boxShadow: msg.role === 'user' ? '0 1px 6px 0 rgba(0,177,225,0.07)' : '0 1px 8px 0 rgba(0,49,102,0.06)',
                  fontSize: 17,
                  fontFamily: 'Montserrat, Arial, sans-serif',
                  mb: 0.5,
                  wordBreak: 'break-word',
                  textAlign: 'left',
                }}
              >
                {msg.text}
              </Box>
            </Box>
          ))}
          {aiTyping && (
            <Box sx={{ display: 'flex', justifyContent: 'flex-start', alignItems: 'center', pl: 1, mt: 1 }}>
              <Box sx={{
                bgcolor: '#fff',
                color: '#00b1e1',
                px: 2.2,
                py: 1.3,
                borderRadius: 3,
                borderTopRightRadius: 12,
                boxShadow: '0 1px 8px 0 rgba(0,49,102,0.06)',
                fontSize: 17,
                fontFamily: 'Montserrat, Arial, sans-serif',
                display: 'flex',
                alignItems: 'center',
                minWidth: 48,
                minHeight: 32,
              }}>
                <TypingDots />
              </Box>
            </Box>
          )}
          <div ref={endRef} />
        </Box>
      )}
    </Box>
  );
}

function TypingDots() {
  // Animated three dots ...
  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
      <Dot delay={0} />
      <Dot delay={0.15} />
      <Dot delay={0.3} />
    </Box>
  );
}
function Dot({ delay }) {
  return (
    <Box
      sx={{
        width: 8,
        height: 8,
        borderRadius: '50%',
        background: '#00b1e1',
        mx: 0.2,
        animation: 'typing-bounce 1s infinite',
        animationDelay: `${delay}s`,
        '@keyframes typing-bounce': {
          '0%, 80%, 100%': { transform: 'scale(0.7)' },
          '40%': { transform: 'scale(1.2)' },
        },
      }}
    />
  );
}
