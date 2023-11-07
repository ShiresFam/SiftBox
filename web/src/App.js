import { useState } from 'react';
import { styled, ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import Header from './components/Header'; // Import Header
import { lightTheme, darkTheme } from './utils/theme';


const FlexWrapper = styled('div')(() => ({
  display: 'flex',
  flexDirection: 'column',
  width: '100%',
  height: '100vh',
}));


function App() {
  const [mode, setMode] = useState('light'); // Add state for mode

  const toggleTheme = () => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  };

  const theme = mode === 'light' ? lightTheme : darkTheme;

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline enableColorScheme />
      <FlexWrapper>
      <Header toggleTheme={toggleTheme}/>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </FlexWrapper>
    </ThemeProvider>
  );
}

export default App;
