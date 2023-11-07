import { createTheme } from '@mui/material/styles';

const lightThemeOptions = {
    "palette": {
        "mode": "light",
        "primary": {
            "main": "rgb(75, 131, 151)"
        },
        "secondary": {
            "main": "rgb(230, 127, 104)"
        },
        "error": {
            "main": "#f44336"
        },
        "warning": {
            "main": "#ff9800"
        },
        "info": {
            "main": "#2196f3"
        },
        "success": {
            "main": "#4caf50"
        },
        "background": {
            "default": "#ffffff",
            "paper": "#f7f7f7"
        },
        "text": {
            "primary": "rgba(0, 0, 0, 0.87)",
            "secondary": "rgba(0, 0, 0, 0.54)",
            "disabled": "rgba(0, 0, 0, 0.38)",
            "hint": "rgba(0, 0, 0, 0.38)"
        }
    }
}

const darkThemeOptions = {
    "palette": {
        "mode": "dark",
        "primary": {
            "main": "rgb(75, 131, 151)"
        },
        "secondary": {
            "main": "rgb(230, 127, 104)"
        },
        "error": {
            "main": "#cf6679"
        },
        "warning": {
            "main": "#ffb74d"
        },
        "info": {
            "main": "#64b5f6"
        },
        "success": {
            "main": "#81c784"
        },
        "background": {
            "default": "rgb(34, 37, 47)",
            "paper": "rgb(47, 74, 88)"
        },
        "text": {
            "primary": "#ffffff",
            "secondary": "rgba(255, 255, 255, 0.7)",
            "disabled": "rgba(255, 255, 255, 0.5)",
            "hint": "rgba(255, 255, 255, 0.5)"
        }
    }
}

// Create the theme instances using createTheme
const lightTheme = createTheme(lightThemeOptions);
const darkTheme = createTheme(darkThemeOptions);

export { lightTheme, darkTheme };