import { useState, useEffect } from 'react';
import { styled } from '@mui/material/styles';
import { Typography } from '@mui/material';
import { getUser } from '../apis/auth';
import { getEmails } from '../apis/outlook';

const WrapperDiv = styled('div')(() => ({
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    height: '100%',
}));

const Home = () => {
    const [loading, setLoading] = useState(true);
    const [displayName, setDisplayName] = useState('');
    const [emails, setEmails] = useState([]);
    const [unread, setUnread] = useState(0);

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
            const fetchedEmails = await getEmails();
            setEmails(fetchedEmails['emails']);
            setUnread(fetchedEmails['unread_count']);
        }
        fetchEmails();
    }, [displayName])

    if (loading) {
        return <p>Loading</p>
    }
    return (
        <WrapperDiv>
            <Typography variant='h2'>Hello, {displayName}</Typography>
            <Typography variant='h4'>You have {unread} unread emails</Typography>
        </WrapperDiv>
    )

};

export default Home;