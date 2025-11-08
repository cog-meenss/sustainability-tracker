import OpenAI from 'openai';

// Initialize OpenAI client
let openai = null;

const initializeOpenAI = () => {
  const apiKey = process.env.REACT_APP_OPENAI_API_KEY;
  
  if (!apiKey) {
    console.warn('OpenAI API key not found. Please set REACT_APP_OPENAI_API_KEY in your .env file');
    return null;
  }

  if (!openai) {
    openai = new OpenAI({
      apiKey: apiKey,
      dangerouslyAllowBrowser: true // Note: In production, API calls should go through your backend
    });
  }
  
  return openai;
};

// System prompt that gives context about the Tracker application
const SYSTEM_PROMPT = `You are a helpful assistant for the Tracker application, a React-based business data management tool. 

The Tracker app has the following features:
- **Training Tab**: Upload and analyze Excel files containing training records. Users can filter, sort, and export training data.
- **Ideas Tab**: Track and manage business ideas with filtering and analysis capabilities.
- **Revenue & FTE Tab**: Calculate revenue and FTE (Full Time Equivalent) metrics from uploaded leave and people data files.
- **Chat System**: Built-in help system (that's you!) to assist users with app functionality.

Key functionality:
- Excel file uploads in all tabs using Material-UI file inputs
- Data display using MUI DataGrid with custom filtering/sorting
- Saved views system for column configurations (stored in localStorage)
- CSV export functionality for all data tables
- Working days calculations for UK business calendar
- Mobile-responsive design with collapsible sidebar
- Multi-file upload support in Revenue & FTE tab

Navigation:
- Sidebar contains tabs for Training, Ideas, Revenue & FTE, and Chat
- Each tab maintains its own state and data independently
- Views and filters persist across browser sessions

Common user tasks:
- Uploading Excel files for data processing
- Switching between different tabs/modules
- Filtering and sorting data in tables
- Exporting results as CSV files
- Saving and managing custom column views
- Understanding working days calculations

Please provide helpful, specific answers about using the Tracker application. Focus on practical guidance for the features mentioned above.`;

// Main function to get chat completion from OpenAI
export const getChatResponse = async (messages) => {
  const client = initializeOpenAI();
  
  if (!client) {
    return {
      success: false,
      error: 'OpenAI API key not configured. Please check your environment setup.',
      fallbackResponse: getFallbackResponse(messages[messages.length - 1]?.content || '')
    };
  }

  try {
    const completion = await client.chat.completions.create({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        ...messages.map(msg => ({
          role: msg.role,
          content: msg.text || msg.content
        }))
      ],
      max_tokens: 500,
      temperature: 0.7,
    });

    return {
      success: true,
      response: completion.choices[0].message.content
    };
  } catch (error) {
    console.error('OpenAI API Error:', error);
    
    let errorMessage = 'Failed to get AI response. ';
    if (error.status === 401) {
      errorMessage += 'Invalid API key.';
    } else if (error.status === 429) {
      errorMessage += 'Rate limit exceeded.';
    } else if (error.status === 500) {
      errorMessage += 'OpenAI service error.';
    } else {
      errorMessage += 'Please try again.';
    }

    return {
      success: false,
      error: errorMessage,
      fallbackResponse: getFallbackResponse(messages[messages.length - 1]?.content || messages[messages.length - 1]?.text || '')
    };
  }
};

// Fallback response system (enhanced version of the original keyword-based system)
const getFallbackResponse = (input) => {
  const relevantKeywords = [
    'training', 'ideas', 'revenue', 'fte', 'upload', 'tab', 'sidebar', 'switch', 'filter', 
    'view', 'column', 'file', 'data', 'export', 'search', 'tracker', 'app', 'application', 
    'feature', 'functionality', 'leave', 'people', 'summary', 'contract', 'associate', 
    'table', 'download', 'sort', 'profile', 'settings', 'responsive', 'mobile', 'chat', 
    'conversation', 'excel', 'csv', 'working days', 'calendar'
  ];

  const lower = input.toLowerCase();
  const isRelevant = relevantKeywords.some(kw => lower.includes(kw));

  if (isRelevant) {
    // Enhanced context-aware replies
    if (lower.includes('upload')) {
      return 'You can upload Excel files in any of the three main tabs:\n• **Training Tab**: Upload training records\n• **Ideas Tab**: Upload ideas data\n• **Revenue & FTE Tab**: Upload both leave and people files\n\nSimply click the upload button and select your Excel file.';
    }
    if (lower.includes('switch') || lower.includes('navigate')) {
      return 'Use the sidebar on the left to switch between different sections:\n• **Training** - Training records analysis\n• **Ideas** - Ideas tracking\n• **Revenue & FTE** - Revenue calculations\n• **Chat** - This help system\n\nOn mobile, tap the menu icon to access the sidebar.';
    }
    if (lower.includes('export') || lower.includes('download') || lower.includes('csv')) {
      return 'Most tabs have an export feature:\n• Look for the **Export CSV** button in the data table toolbar\n• This will download your filtered and sorted data as a CSV file\n• The export includes only the currently visible columns and applied filters.';
    }
    if (lower.includes('filter') || lower.includes('search')) {
      return 'Each tab offers powerful filtering options:\n• Use the **column filters** in the data grid headers\n• Apply **multi-column filters** for complex queries\n• **Save custom views** to preserve your filter configurations\n• Filters persist between browser sessions.';
    }
    if (lower.includes('view') || lower.includes('column')) {
      return 'Manage your data views easily:\n• **Show/hide columns** using the column visibility controls\n• **Save custom views** with your preferred column setup\n• **Switch between saved views** using the view selector\n• Views are automatically saved to your browser.';
    }
    if (lower.includes('working days') || lower.includes('calendar')) {
      return 'The app includes UK working days calculations:\n• **Excludes weekends** (Saturday & Sunday)\n• **Excludes UK public holidays** for England & Wales\n• Used in Revenue & FTE calculations\n• Based on official UK government holiday calendar.';
    }
    if (lower.includes('mobile') || lower.includes('responsive')) {
      return 'The Tracker app is fully mobile-friendly:\n• **Responsive design** adapts to your screen size\n• **Collapsible sidebar** for mobile navigation\n• **Touch-friendly** controls and interactions\n• **Auto-hide sidebar** when scrolling on mobile.';
    }
    if (lower.includes('revenue') || lower.includes('fte')) {
      return 'The Revenue & FTE tab helps with workforce calculations:\n• Upload **leave data** and **people data** files\n• Calculates **FTE (Full Time Equivalent)** metrics\n• Processes **revenue calculations** based on working days\n• Supports **multi-file analysis** for comprehensive reporting.';
    }
    
    // Generic relevant response
    return 'The Tracker app helps you manage business data across three main areas:\n\n• **Training Records** - Upload and analyze training data\n• **Ideas Management** - Track and filter business ideas\n• **Revenue & FTE** - Calculate workforce and revenue metrics\n\nEach section supports Excel uploads, data filtering, and CSV exports. What specific feature would you like help with?';
  }

  return '🤖 I\'m here to help with the Tracker application! I can assist with:\n\n• Uploading and managing Excel files\n• Navigating between Training, Ideas, and Revenue & FTE tabs\n• Using filters and data views\n• Exporting data as CSV\n• Understanding app features\n\nWhat would you like to know about using the Tracker app?';
};

// Helper function to check if OpenAI is configured
export const isOpenAIConfigured = () => {
  return !!process.env.REACT_APP_OPENAI_API_KEY;
};

// Helper function to get configuration status
export const getConfigurationStatus = () => {
  const apiKey = process.env.REACT_APP_OPENAI_API_KEY;
  
  return {
    configured: !!apiKey,
    hasKey: !!apiKey,
    keyPreview: apiKey ? `${apiKey.substring(0, 8)}...` : null
  };
};