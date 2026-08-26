import {Grid} from '@mui/material'
import ATMCard from './ATMCard'

function ATMList({atms}){
    return (
        <Grid container spacing={2}>
            {atms.map((atm)=>
                <Grid item key={atm.id}>
                    <ATMCard atm={atm}/>
                </Grid>)}
        </Grid>
    )
};

export default ATMList;