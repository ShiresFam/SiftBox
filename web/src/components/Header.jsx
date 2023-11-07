import React from 'react';
import { Typography, IconButton } from '@mui/material';
import { styled } from '@mui/system';
import Logo from '../resources/siftbox_logo.png';
import Brightness4Icon from '@mui/icons-material/Brightness4';

const StyledDiv = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    padding: theme.spacing(2),
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.primary.contrastText,
    boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
}));

const Header = ({ toggleTheme }) => (
    <StyledDiv>
        <img src={Logo} alt="Siftbox Logo" width="50" height="50" style={{ marginRight: '20px' }} />
        <Typography variant="h4" component="div" style={{ flexGrow: 1 }}>
            Siftbox
        </Typography>
        <IconButton onClick={toggleTheme} color="inherit">
            <Brightness4Icon />
        </IconButton>
    </StyledDiv>
);

export default Header;