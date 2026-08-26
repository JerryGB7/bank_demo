import {AppBar, Toolbar, Typography} from '@mui/material'
import PrecisionManufacturingIcon from '@mui/icons-material/PrecisionManufacturing'

function AppHeader() {
    return(
        <AppBar position='static'>
            <Toolbar>
                <PrecisionManufacturingIcon sx={{mr : 2}}/>
                <Typography variant='h4' component='h1' color='secondary'>
                    Meridian Bank Demo 
                </Typography>
            </Toolbar>
        </AppBar>
    )
};

export default AppHeader;