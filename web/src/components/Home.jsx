import { useState, useEffect } from 'react';
import { styled } from '@mui/material/styles';
import { Typography } from '@mui/material';
import { getUser, fe } from '../apis/auth';

const WrapperDiv = styled('div')(() => ({
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    height: '100%',
}));

const Home = () => {
    const [loading, setLoading] = useState(true);
    const [displayName, setDisplayName] = useState('');

    useEffect(() => {
        console.log('use effect called')
        const handleAuth = async () => {
            console.log('hi')
            const name = await getUser();
            setDisplayName(name);
            setLoading(false);
        }

        handleAuth();
    }, []);

    useEffect(() => {
        const fetchEmails = async () => {

         }
    })

    if (loading) {
        return <p>Loading</p>
    }
    return (
        <WrapperDiv>
            <Typography variant='h2'>Hello, {displayName}</Typography>
            <Typography variant='h4'>You have </Typography>
        </WrapperDiv>
    )

};

export default Home;