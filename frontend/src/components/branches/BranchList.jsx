import {Grid} from '@mui/material'
import BranchCard from './BranchCard'

function BranchList({branches}){
    return (
        <Grid container spacing={2}>
            {branches.map((branch)=>
                <Grid item key={branch.id}>
                    <BranchCard branch={branch}/>
                </Grid>)}
        </Grid>
    )
};

export default BranchList;