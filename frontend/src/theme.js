/*

*/

import {createTheme} from '@mui/material/styles'

const theme = createTheme({
    palette: {
        mode: 'light', 
        primary:{
            main: '#0d47a1'
        },
        secondary: {
            main: '#ffffff'
        },
    },
    shape: {
        borderRadius: 8,
    },
});

export default theme;