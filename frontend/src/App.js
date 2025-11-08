import React, { useState } from "react";
import TrainingTab from "./TrainingTab";
import IdeasTab from "./IdeasTab";
import RevenueFteTab from "./RevenueFteTab";
import ChatSection from "./ChatSection";
import ChatInput from "./ChatInput";
import { getChatResponse } from "./services/openaiService";
import { Box, Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Typography, Toolbar, Divider, Avatar, IconButton } from "@mui/material";
import SchoolIcon from '@mui/icons-material/School';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import MonetizationOnIcon from '@mui/icons-material/MonetizationOn';
import MenuBookIcon from '@mui/icons-material/MenuBook';

const drawerWidth = 240; // Sidebar width (expanded)
const drawerCollapsedWidth = 64; // Sidebar width (collapsed)
const mobileDrawerWidth = 200; // More compact sidebar for mobile
const sidebarTabs = [
  { label: 'Training', icon: <SchoolIcon />, idx: 0 },
  { label: 'Ideas', icon: <LightbulbIcon />, idx: 1 },
  { label: 'Revenue & FTE', icon: <MonetizationOnIcon />, idx: 2 },
];


import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import MenuIcon from '@mui/icons-material/Menu';
import HistoryToggleOffIcon from '@mui/icons-material/HistoryToggleOff';
import ViewListIcon from '@mui/icons-material/ViewList';
import Tooltip from '@mui/material/Tooltip';

import useMediaQuery from '@mui/material/useMediaQuery';
import SwipeableDrawer from '@mui/material/SwipeableDrawer';

function App() {
  // --- RevenueFteTab persistent state ---
  const [revenueFiles, setRevenueFiles] = useState([]); // Always clear files on load
  const [revenueProcessing, setRevenueProcessing] = useState(false);
  const [revenueTabIdx, setRevenueTabIdx] = useState(() => {
    try {
      return Number(localStorage.getItem('revenueTabIdx')) || 0;
    } catch { return 0; }
  });
  const [revenueTables, setRevenueTables] = useState(() => {
    try {
      const val = localStorage.getItem('revenueTables');
      return val ? JSON.parse(val) : [];
    } catch { return []; }
  }); // Persisted
  const [revenueError, setRevenueError] = useState('');


  // Persist RevenueFteTab state
  // Do NOT persist revenueFiles to localStorage; always clear on reload
  React.useEffect(() => {
    localStorage.setItem('revenueTabIdx', revenueTabIdx);
  }, [revenueTabIdx]);
  React.useEffect(() => {
    localStorage.setItem('revenueTables', JSON.stringify(revenueTables));
  }, [revenueTables]);
  // Error is not persisted to avoid stale state

  const [tab, setTab] = useState(0);

  // --- Chatbot state ---
  const [showChat, setShowChat] = useState(false);
  const [chatInput, setChatInput] = useState("");
  // Each conversation: { id, title, messages: [ {role, text} ] }
  const [chats, setChats] = useState([]);
  const [activeChatId, setActiveChatId] = useState(null);
  const [showHistory, setShowHistory] = useState(true);
  const [aiTyping, setAiTyping] = useState(false);

  // Helper: get active chat object
  const activeChat = chats.find(c => c.id === activeChatId) || null;

  // Start a new chat (does not create chat until user sends)
  const handleNewChat = () => {
    setActiveChatId(null);
    setShowChat(true);
    setChatInput("");
    setAiTyping(false);
  };
  // Switch chat
  const handleSelectChat = (id) => {
    setActiveChatId(id);
    setShowChat(true);
    setChatInput("");
    setAiTyping(false);
  };
  // Clear/reset chat
  const handleClearChat = () => {
    if (activeChatId) {
      setChats(chats => chats.filter(c => c.id !== activeChatId));
      setActiveChatId(null);
      setChatInput("");
      setAiTyping(false);
    }
  };

  // Enhanced chatbot logic using OpenAI with fallback
  const getBotResponse = async (messages) => {
    try {
      const result = await getChatResponse(messages);
      
      if (result.success) {
        return result.response;
      } else {
        // If OpenAI fails, use fallback response
        console.warn('OpenAI API failed:', result.error);
        return result.fallbackResponse || 'I apologize, but I\'m having trouble connecting to my AI service. Please try again in a moment.';
      }
    } catch (error) {
      console.error('Unexpected error in chat response:', error);
      return 'I\'m experiencing technical difficulties. Please try again.';
    }
  };

  // Chat send handler with OpenAI integration
  const handleChatSend = async () => {
    const trimmed = chatInput.trim();
    if (!trimmed) return;
    
    setAiTyping(true);
    let chatId = activeChatId;
    let currentMessages = [];
    
    // If no active chat, create one
    if (!chatId) {
      chatId = (Math.max(0, ...chats.map(c => c.id)) + 1);
      const newChat = { 
        id: chatId, 
        title: trimmed.slice(0, 32), 
        messages: [{ role: 'user', text: trimmed }] 
      };
      setChats([newChat, ...chats]);
      setActiveChatId(chatId);
      currentMessages = newChat.messages;
    } else {
      // Add user message to existing chat
      setChats(chats => chats.map(chat => {
        if (chat.id === chatId) {
          const updatedChat = { ...chat, messages: [...chat.messages, { role: 'user', text: trimmed }] };
          currentMessages = updatedChat.messages;
          return updatedChat;
        }
        return chat;
      }));
      // Get current messages from the existing chat
      const existingChat = chats.find(c => c.id === chatId);
      if (existingChat) {
        currentMessages = [...existingChat.messages, { role: 'user', text: trimmed }];
      }
    }
    
    setChatInput("");
    
    // Get AI response
    try {
      const botResponse = await getBotResponse(currentMessages);
      
      setChats(chats => chats.map(chat =>
        chat.id === chatId
          ? { ...chat, messages: [...chat.messages, { role: 'assistant', text: botResponse }] }
          : chat
      ));
    } catch (error) {
      console.error('Error getting bot response:', error);
      setChats(chats => chats.map(chat =>
        chat.id === chatId
          ? { ...chat, messages: [...chat.messages, { role: 'assistant', text: 'I apologize, but I encountered an error. Please try again.' }] }
          : chat
      ));
    } finally {
      setAiTyping(false);
    }
  };

  // Persist sidebar collapsed state
  const getInitialSidebarCollapsed = () => {
    const stored = localStorage.getItem('sidebarCollapsed');
    return stored === 'true';
  };
  const [sidebarCollapsed, setSidebarCollapsed] = useState(getInitialSidebarCollapsed);
  React.useEffect(() => {
    localStorage.setItem('sidebarCollapsed', sidebarCollapsed);
  }, [sidebarCollapsed]);

  // Responsive: detect mobile
  const isMobile = useMediaQuery('(max-width: 600px)');
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  // Auto-hide sidebar on mobile scroll down
  React.useEffect(() => {
    if (!isMobile) return;
    let lastScroll = window.scrollY;
    const onScroll = () => {
      const curr = window.scrollY;
      if (curr > lastScroll + 30 && mobileSidebarOpen) setMobileSidebarOpen(false);
      lastScroll = curr;
    };
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, [isMobile, mobileSidebarOpen]);

  // Toggle handler
  const handleSidebarToggle = () => {
    if (isMobile) setMobileSidebarOpen((v) => !v);
    else setSidebarCollapsed((v) => !v);
  };


  // --- TrainingTab persistent state ---
  const [training_multiFilterCol, setTraining_multiFilterCol] = useState('');
  const [training_multiFilterVals, setTraining_multiFilterVals] = useState([]);
  const [training_multiFilterText, setTraining_multiFilterText] = useState('');
  const [training_multiColumnFilters, setTraining_multiColumnFilters] = useState([]);
  const [training_views, setTraining_views] = useState(() => {
    try {
      return JSON.parse(window.localStorage.getItem('columnViews') || '{}');
    } catch {
      return {};
    }
  });
  const [training_selectedView, setTraining_selectedView] = useState(() => window.localStorage.getItem('selectedView') || '');
  const [training_columns, setTraining_columns] = useState([]);
  const [training_data, setTraining_data] = useState([]);
  const [training_visibleCols, setTraining_visibleCols] = useState([]);
  const [training_colSelectOpen, setTraining_colSelectOpen] = useState(false);
  const [training_sort, setTraining_sort] = useState({ col: null, direction: 'asc' });
  const [training_error, setTraining_error] = useState("");
  const [training_selectedFile, setTraining_selectedFile] = useState(null);
  const [training_filterModel, setTraining_filterModel] = useState({ items: [] });

  const trainingTabState = {
    multiFilterCol: training_multiFilterCol, setMultiFilterCol: setTraining_multiFilterCol,
    multiFilterVals: training_multiFilterVals, setMultiFilterVals: setTraining_multiFilterVals,
    multiFilterText: training_multiFilterText, setMultiFilterText: setTraining_multiFilterText,
    multiColumnFilters: training_multiColumnFilters, setMultiColumnFilters: setTraining_multiColumnFilters,
    views: training_views, setViews: setTraining_views,
    selectedView: training_selectedView, setSelectedView: setTraining_selectedView,
    columns: training_columns, setColumns: setTraining_columns,
    data: training_data, setData: setTraining_data,
    visibleCols: training_visibleCols, setVisibleCols: setTraining_visibleCols,
    colSelectOpen: training_colSelectOpen, setColSelectOpen: setTraining_colSelectOpen,
    sort: training_sort, setSort: setTraining_sort,
    error: training_error, setError: setTraining_error,
    selectedFile: training_selectedFile, setSelectedFile: setTraining_selectedFile,
    filterModel: training_filterModel, setFilterModel: setTraining_filterModel,
  };

  // --- IdeasTab persistent state ---
  const [ideas_ideasFilterCol, setIdeas_ideasFilterCol] = useState('');
  const [ideas_ideasFilterVals, setIdeas_ideasFilterVals] = useState([]);
  const [ideas_ideasFilterText, setIdeas_ideasFilterText] = useState('');
  const [ideas_ideasColumnFilters, setIdeas_ideasColumnFilters] = useState([]);
  const [ideas_columns, setIdeas_columns] = useState([]);
  const [ideas_data, setIdeas_data] = useState([]);
  const [ideas_visibleCols, setIdeas_visibleCols] = useState([]);
  const [ideas_ideasViews, setIdeas_ideasViews] = useState(() => {
    try {
      return JSON.parse(window.localStorage.getItem('ideasViews') || '{}');
    } catch {
      return {};
    }
  });
  const [ideas_selectedIdeasView, setIdeas_selectedIdeasView] = useState(() => window.localStorage.getItem('selectedIdeasView') || '');
  const [ideas_colSelectOpen, setIdeas_colSelectOpen] = useState(false);
  const [ideas_sort, setIdeas_sort] = useState({ col: null, direction: 'asc' });
  const [ideas_filters, setIdeas_filters] = useState({});
  const [ideas_error, setIdeas_error] = useState("");
  const [ideas_selectedFile, setIdeas_selectedFile] = useState(null);

  const ideasTabState = {
    ideasFilterCol: ideas_ideasFilterCol, setIdeasFilterCol: setIdeas_ideasFilterCol,
    ideasFilterVals: ideas_ideasFilterVals, setIdeasFilterVals: setIdeas_ideasFilterVals,
    ideasFilterText: ideas_ideasFilterText, setIdeasFilterText: setIdeas_ideasFilterText,
    ideasColumnFilters: ideas_ideasColumnFilters, setIdeasColumnFilters: setIdeas_ideasColumnFilters,
    columns: ideas_columns, setColumns: setIdeas_columns,
    data: ideas_data, setData: setIdeas_data,
    visibleCols: ideas_visibleCols, setVisibleCols: setIdeas_visibleCols,
    ideasViews: ideas_ideasViews, setIdeasViews: setIdeas_ideasViews,
    selectedIdeasView: ideas_selectedIdeasView, setSelectedIdeasView: setIdeas_selectedIdeasView,
    colSelectOpen: ideas_colSelectOpen, setColSelectOpen: setIdeas_colSelectOpen,
    sort: ideas_sort, setSort: setIdeas_sort,
    filters: ideas_filters, setFilters: setIdeas_filters,
    error: ideas_error, setError: setIdeas_error,
    selectedFile: ideas_selectedFile, setSelectedFile: setIdeas_selectedFile,
  };

  // --- RevenueFteTab persistent state ---
  const [revenue_files, setRevenue_files] = useState([]);
  const [revenue_processing, setRevenue_processing] = useState(false);
  const [revenue_tabIdx, setRevenue_tabIdx] = useState(0);
  const [revenue_tables, setRevenue_tables] = useState([]);
  const [revenue_error, setRevenue_error] = useState("");

  const revenueTabState = {
    files: revenue_files, setFiles: setRevenue_files,
    processing: revenue_processing, setProcessing: setRevenue_processing,
    tabIdx: revenue_tabIdx, setTabIdx: setRevenue_tabIdx,
    tables: revenue_tables, setTables: setRevenue_tables,
    error: revenue_error, setError: setRevenue_error,
  };

  return (
    <Box sx={{ display: 'flex', height: '100vh', bgcolor: '#f5f7fb' }}>
      {/* Sidebar */}
      {/* Desktop/Tablet Sidebar */}
      {!isMobile && (
        <Drawer
          variant="permanent"
          sx={{
            width: sidebarCollapsed ? drawerCollapsedWidth : drawerWidth,
            flexShrink: 0,
            transition: 'width 0.3s cubic-bezier(0.4,0,0.2,1)',
            [`& .MuiDrawer-paper`]: {
              width: sidebarCollapsed ? drawerCollapsedWidth : drawerWidth,
              boxSizing: 'border-box',
              bgcolor: '#17223b',
              color: '#fff',
              borderRight: 'none',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'stretch',
              pt: 0,
              transition: 'width 0.3s cubic-bezier(0.4,0,0.2,1)',
              overflowX: 'hidden',
            },
          }}
        >
          <Toolbar sx={{ minHeight: 80, px: 2, py: 2, display: 'flex', alignItems: 'center', gap: sidebarCollapsed ? 0 : 2, bgcolor: 'transparent', justifyContent: sidebarCollapsed ? 'center' : 'space-between' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: sidebarCollapsed ? 0 : 2, width: '100%', justifyContent: sidebarCollapsed ? 'center' : 'flex-start' }}>
              <Avatar src={require('./assets/logo.png')} alt="Logo" sx={{ width: 44, height: 44, borderRadius: 2, boxShadow: '0 2px 12px rgba(0,49,102,0.10)', mx: sidebarCollapsed ? 'auto' : 0, transition: 'all 0.3s' }} />
              <Typography
                variant="h5"
                sx={{
                  fontWeight: 700,
                  letterSpacing: 2,
                  fontFamily: 'Montserrat, Arial, sans-serif',
                  color: '#fff',
                  ml: 1,
                  opacity: sidebarCollapsed ? 0 : 1,
                  transition: 'opacity 0.3s',
                  whiteSpace: 'nowrap',
                  pointerEvents: sidebarCollapsed ? 'none' : 'auto',
                }}
              >
                Trackify
              </Typography>
            </Box>
            <Tooltip title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'} placement="right">
              <IconButton
                aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
                onClick={handleSidebarToggle}
                sx={{
                  color: sidebarCollapsed ? '#003366' : '#fff',
                  background: sidebarCollapsed ? '#fff' : '#00b1e1',
                  boxShadow: sidebarCollapsed ? 2 : 0,
                  ml: sidebarCollapsed ? 0 : 1,
                  transition: 'all 0.3s',
                  borderRadius: '50%',
                  width: 44,
                  height: 44,
                  '&:hover': {
                    background: sidebarCollapsed ? '#e3f2fd' : '#0094be',
                    color: '#003366',
                  },
                  ...(sidebarCollapsed && { position: 'absolute', left: 10, top: 20, zIndex: 10 }),
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
                size="large"
              >
                {sidebarCollapsed ? <MenuIcon sx={{ fontSize: 32 }} /> : <ChevronLeftIcon sx={{ fontSize: 32 }} />}
              </IconButton>
            </Tooltip>
          </Toolbar>
          <Divider sx={{ bgcolor: 'rgba(255,255,255,0.08)' }} />
          <List sx={{ flex: 1, py: 2 }}>
            {sidebarTabs.map(({ label, icon, idx }) => (
              <ListItem key={label} disablePadding sx={{ display: 'block' }}>
                <ListItemButton
                  selected={tab === idx && !showChat}
                  onClick={() => { setTab(idx); setShowChat(false); }}
                  sx={{
                    borderRadius: 2,
                    mx: 2,
                    mb: 1.2,
                    bgcolor: tab === idx && !showChat ? 'rgba(0,177,225,0.14)' : 'transparent',
                    '&:hover': { bgcolor: 'rgba(0,177,225,0.10)' },
                    color: tab === idx && !showChat ? '#00b1e1' : '#fff',
                    fontWeight: tab === idx && !showChat ? 700 : 400,
                    minHeight: 48,
                    justifyContent: sidebarCollapsed ? 'center' : 'flex-start',
                    px: sidebarCollapsed ? 1 : 2,
                    transition: 'all 0.3s',
                  }}
                >
                  <ListItemIcon sx={{ color: tab === idx && !showChat ? '#00b1e1' : '#fff', minWidth: 0, mr: sidebarCollapsed ? 0 : 2, justifyContent: 'center', transition: 'all 0.3s' }}>{icon}</ListItemIcon>
                  <Box
                    sx={{
                      opacity: sidebarCollapsed ? 0 : 1,
                      width: sidebarCollapsed ? 0 : 'auto',
                      transition: 'opacity 0.3s, width 0.3s',
                      pointerEvents: sidebarCollapsed ? 'none' : 'auto',
                      overflow: 'hidden',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    <ListItemText primary={label} primaryTypographyProps={{ fontSize: 16, fontWeight: tab === idx ? 700 : 500 }} />
                  </Box>
                </ListItemButton>
              </ListItem>
            ))}
            {/* Dotted divider */}
            <Divider sx={{ borderStyle: 'dotted', borderColor: '#b0c4d4', mx: 2, my: 1.5, opacity: 0.6 }} />
            {/* Chat section */}
            <Box sx={{ px: 0, pb: 2, pt: 0, userSelect: 'none' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: sidebarCollapsed ? 'center' : 'space-between', px: sidebarCollapsed ? 0 : 2, mb: 1 }}>
                <ListItemButton
                  selected={!activeChatId}
                  onClick={handleNewChat}
                  sx={{
                    borderRadius: 2,
                    bgcolor: !activeChatId ? 'rgba(0,177,225,0.16)' : 'transparent',
                    color: '#00b1e1',
                    fontWeight: 600,
                    minHeight: 40,
                    justifyContent: sidebarCollapsed ? 'center' : 'flex-start',
                    px: sidebarCollapsed ? 1 : 2,
                    transition: 'all 0.3s',
                  }}
                >
                  <ListItemIcon sx={{ color: '#00b1e1', minWidth: 0, mr: sidebarCollapsed ? 0 : 2, justifyContent: 'center' }}>
                    <ChatBubbleOutlineIcon sx={{ fontSize: 22 }} />
                  </ListItemIcon>
                  <Box sx={{ opacity: sidebarCollapsed ? 0 : 1, width: sidebarCollapsed ? 0 : 'auto', transition: 'opacity 0.3s, width 0.3s', pointerEvents: sidebarCollapsed ? 'none' : 'auto', overflow: 'hidden', whiteSpace: 'nowrap' }}>
                    <ListItemText primary={'New Chat'} primaryTypographyProps={{ fontSize: 14, fontWeight: 600 }} />
                  </Box>
                </ListItemButton>
                {!sidebarCollapsed && (
                  <Tooltip title={showHistory ? 'Hide chat history' : 'Show chat history'} placement="top">
                    <IconButton size="small" onClick={() => setShowHistory(h => !h)} sx={{ ml: 1, color: '#b0c4d4', border: '1px solid #e3e6ee', bgcolor: '#fff', '&:hover': { bgcolor: '#e3f6fb', color: '#00b1e1' } }}>
                      {showHistory ? <HistoryToggleOffIcon sx={{ fontSize: 20 }} /> : <ViewListIcon sx={{ fontSize: 20 }} />}
                    </IconButton>
                  </Tooltip>
                )}
              </Box>
              {/* Chat history */}
              {showHistory && (
                <List sx={{ py: 0, maxHeight: 220, overflowY: 'auto', pr: 0.5 }}>
                  {chats.filter(chat => chat.messages.length > 0).map(chat => (
                    <ListItem key={chat.id} disablePadding sx={{ display: 'block' }}>
                      <ListItemButton
                        selected={showChat && activeChatId === chat.id}
                        onClick={() => handleSelectChat(chat.id)}
                        sx={{
                          borderRadius: 2,
                          mx: 2,
                          mb: 0.5,
                          bgcolor: showChat && activeChatId === chat.id ? 'rgba(0,177,225,0.12)' : 'transparent',
                          '&:hover': { bgcolor: 'rgba(0,177,225,0.08)' },
                          color: showChat && activeChatId === chat.id ? '#00b1e1' : '#fff',
                          fontWeight: showChat && activeChatId === chat.id ? 600 : 400,
                          minHeight: 38,
                          justifyContent: sidebarCollapsed ? 'center' : 'flex-start',
                          px: sidebarCollapsed ? 1 : 2,
                          transition: 'all 0.3s',
                          alignItems: 'center',
                        }}
                      >
                        <ListItemIcon sx={{ color: showChat && activeChatId === chat.id ? '#00b1e1' : '#b0c4d4', minWidth: 0, mr: sidebarCollapsed ? 0 : 2, justifyContent: 'center', transition: 'all 0.3s' }}>
                          <ChatBubbleOutlineIcon sx={{ fontSize: 18 }} />
                        </ListItemIcon>
                        <Box
                          sx={{
                            opacity: sidebarCollapsed ? 0 : 1,
                            width: sidebarCollapsed ? 0 : 'auto',
                            transition: 'opacity 0.3s, width 0.3s',
                            pointerEvents: sidebarCollapsed ? 'none' : 'auto',
                            overflow: 'hidden',
                            whiteSpace: 'nowrap',
                          }}
                        >
                          <ListItemText
                            primary={chat.messages.length > 0 ? chat.title : 'New Chat'}
                            primaryTypographyProps={{ fontSize: 13, fontWeight: 500, color: showChat && activeChatId === chat.id ? '#00b1e1' : '#b0c4d4', maxWidth: 120, textOverflow: 'ellipsis', overflow: 'hidden' }}
                          />
                        </Box>
                      </ListItemButton>
                    </ListItem>
                  ))}
                </List>
              )}
            </Box>
          </List>
          <Box sx={{ p: 2, pb: 3, color: '#b0c4d4', fontSize: 13, textAlign: 'center', minHeight: 32, opacity: sidebarCollapsed ? 0 : 1, transition: 'opacity 0.3s' }}>
            {!sidebarCollapsed && '© 2025 Trackify'}
          </Box>
        </Drawer>
      )}

      {/* Mobile Sidebar */}
      {isMobile && (
        <SwipeableDrawer
          anchor="left"
          open={mobileSidebarOpen}
          onClose={() => setMobileSidebarOpen(false)}
          onOpen={() => setMobileSidebarOpen(true)}
          disableDiscovery
          sx={{
            transition: 'all 0.35s cubic-bezier(.4,0,.2,1)',
            [`& .MuiDrawer-paper`]: {
              width: isMobile ? mobileDrawerWidth : drawerWidth,
              minWidth: isMobile ? mobileDrawerWidth : drawerWidth,
              boxSizing: 'border-box',
              bgcolor: '#17223b',
              color: '#fff',
              borderRight: 'none',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'stretch',
              pt: 0,
              overflowX: 'hidden',
              transition: 'width 0.35s cubic-bezier(.4,0,.2,1), min-width 0.35s cubic-bezier(.4,0,.2,1)',
            },
          }}
        >
          <Toolbar sx={{ minHeight: isMobile ? 56 : 80, px: isMobile ? 1 : 2, py: isMobile ? 1 : 2, display: 'flex', alignItems: 'center', gap: isMobile ? 1 : 2, bgcolor: 'transparent', justifyContent: 'space-between', transition: 'all 0.3s' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: isMobile ? 1 : 2, width: '100%', justifyContent: 'flex-start' }}>
              <Avatar src={require('./assets/logo.png')} alt="Logo" sx={{ width: isMobile ? 32 : 44, height: isMobile ? 32 : 44, borderRadius: 2, boxShadow: '0 2px 12px rgba(0,49,102,0.10)', transition: 'all 0.3s' }} />
              <Typography variant={isMobile ? "h6" : "h5"} sx={{ fontWeight: 700, letterSpacing: 2, fontFamily: 'Montserrat, Arial, sans-serif', color: '#fff', ml: 1, fontSize: isMobile ? 18 : 24, transition: 'all 0.3s' }}>
                Trackify
              </Typography>
            </Box>
            <Tooltip title="Close sidebar" placement="right">
              <IconButton
                aria-label="Close sidebar"
                onClick={() => setMobileSidebarOpen(false)}
                sx={{ color: '#003366', background: '#fff', boxShadow: 2, borderRadius: '50%', width: 44, height: 44, ml: 1 }}
                size="large"
              >
                <ChevronLeftIcon sx={{ fontSize: 32 }} />
              </IconButton>
            </Tooltip>
          </Toolbar>
          <Divider sx={{ bgcolor: 'rgba(255,255,255,0.08)' }} />
          <List sx={{ flex: 1, py: 2 }}>
            {sidebarTabs.map(({ label, icon, idx }) => (
              <ListItem key={label} disablePadding sx={{ display: 'block' }}>
                <ListItemButton
                  selected={tab === idx}
                  onClick={() => { setTab(idx); setMobileSidebarOpen(false); }}
                  sx={{
                    borderRadius: 2,
                    mx: 2,
                    mb: 1.2,
                    bgcolor: tab === idx ? 'rgba(0,177,225,0.14)' : 'transparent',
                    '&:hover': { bgcolor: 'rgba(0,177,225,0.10)' },
                    color: tab === idx ? '#00b1e1' : '#fff',
                    fontWeight: tab === idx ? 700 : 400,
                    minHeight: 48,
                    justifyContent: 'flex-start',
                    px: 2,
                    transition: 'all 0.3s',
                  }}
                >
                  <ListItemIcon sx={{ color: tab === idx ? '#00b1e1' : '#fff', minWidth: 0, mr: 2, justifyContent: 'center', transition: 'all 0.3s' }}>{icon}</ListItemIcon>
                  <ListItemText primary={label} primaryTypographyProps={{ fontSize: 16, fontWeight: tab === idx ? 700 : 500 }} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
          <Box sx={{ p: 2, pb: 3, color: '#b0c4d4', fontSize: 13, textAlign: 'center', minHeight: 32 }}>
            © 2025 Trackify
          </Box>
        </SwipeableDrawer>
      )}

      {/* Main content area */}
      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        {/* Top bar (minimal, optional) */}
        {isMobile && (
          <Box sx={{ height: 48, display: 'flex', alignItems: 'center', px: 1, bgcolor: '#f5f7fb', borderBottom: '1px solid #e0e0e0', boxShadow: 1 }}>
            <IconButton
              aria-label="Open sidebar"
              onClick={() => setMobileSidebarOpen(true)}
              sx={{ color: '#003366', bgcolor: '#fff', boxShadow: 1, borderRadius: '50%', width: 40, height: 40 }}
              size="large"
            >
              <MenuIcon sx={{ fontSize: 28 }} />
            </IconButton>
            <Typography variant="h6" sx={{ ml: 2, fontWeight: 700, color: '#003366', fontFamily: 'Montserrat, Arial, sans-serif', fontSize: 18 }}>
              Trackify
            </Typography>
          </Box>
        )}
        <Box sx={{ height: isMobile ? 0 : 24 }} />
        <Box sx={{ flex: 1, p: { xs: 2, md: 4 }, overflowY: 'auto', bgcolor: '#f5f7fb', borderRadius: 0, position: 'relative' }}>
          {!showChat && tab === 0 && <TrainingTab {...trainingTabState} />}
          {!showChat && tab === 1 && <IdeasTab {...ideasTabState} />}
          {/* RevenueFteTab persistent state */}
          {!showChat && tab === 2 && (
            <RevenueFteTab
              files={revenueFiles}
              setFiles={setRevenueFiles}
              processing={revenueProcessing}
              setProcessing={setRevenueProcessing}
              tabIdx={revenueTabIdx}
              setTabIdx={setRevenueTabIdx}
              tables={revenueTables}
              setTables={setRevenueTables}
              error={revenueError}
              setError={setRevenueError}
            />
          )}

          {showChat && <ChatSection messages={activeChat ? activeChat.messages : []} />}
        </Box>
        {showChat && (
          <ChatInput
            value={chatInput}
            onChange={e => setChatInput(e.target.value)}
            onSend={handleChatSend}
            onUpload={e => {/* handle upload */}}
          />
        )}
      </Box>
    </Box>
  );
}


export default App;
