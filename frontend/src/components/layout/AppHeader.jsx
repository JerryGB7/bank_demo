import {AppBar, Toolbar, Typography, Box, Button} from '@mui/material'
import PrecisionManufacturingIcon from '@mui/icons-material/PrecisionManufacturing'



function AppHeader({username, role, onLogout}) {
    return(
        <AppBar position='static'>
            <Toolbar sx={{justifyContent: 'space-between', width: '100%'}}>
                <Box sx={{display: 'flex', alignItems: 'center'}}>
                    <PrecisionManufacturingIcon sx={{mr : 2}}/>
                    <Typography variant='h4' component='h1' color='secondary'>
                        Meridian Bank Demo 
                    </Typography>
                </Box>
                {username && (
                    <Box sx={{display: 'flex', alignItems: 'center', gap: 5, ml: 'auto'}}>
                        <Typography variant='body2'>Welcome, {username} ({role})!</Typography>
                        <Button color='secondary' onClick={onLogout}>Log Out</Button>
                    </Box>
                )}
            </Toolbar>
        </AppBar>
    )
};

export default AppHeader;