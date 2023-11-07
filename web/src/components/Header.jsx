import { useState, useEffect } from 'react';
import { Typography, IconButton, Button } from '@mui/material';
import { styled } from '@mui/system';
import Logo from '../resources/siftbox_logo.png';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import { getUser, logout } from '../apis/auth';

const StyledDiv = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    padding: theme.spacing(2),
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.primary.contrastText,
    boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
}));

const Header = ({ toggleTheme }) => {
    const [displayName, setDisplayName] = useState('');
    useEffect(() => {
        const handleAuth = async () => {
            const name = await getUser();
            const dispName = name === " " ? 'User' : name;
            setDisplayName(dispName);
        }

        handleAuth();
    }, []);

    const handleLogout = async () => {
        await logout();
        window.location.href = '/';
    }
    return (
        <StyledDiv>
            <img src={Logo} alt="Siftbox Logo" width="50" height="50" style={{ marginRight: '20px' }} />
            <Typography variant="h4" component="div" style={{ flexGrow: 1 }}>
                Siftbox
            </Typography>
            <Typography variant="h4">Hello, {displayName}!</Typography>
            <IconButton onClick={toggleTheme} color="inherit">
                <Brightness4Icon />
            </IconButton>
            <IconButton onClick={handleLogout} color="inherit">
                <ExitToAppIcon />
            </IconButton>
        </StyledDiv>
    );
}

export default Header;