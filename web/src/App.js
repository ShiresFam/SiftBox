import { styled, ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Routes, Route } from 'react-router-dom';
import Home from './components/Home';

const FlexWrapper = styled('div')(() => ({
  display: 'flex',
  flexDirection: 'column',
  width: '100%',
  height: '100vh',
}));

const theme = createTheme();

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline enableColorScheme />
      <FlexWrapper>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </FlexWrapper>
    </ThemeProvider>
  );
}

export default App;
