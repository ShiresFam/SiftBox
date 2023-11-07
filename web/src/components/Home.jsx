import { useState, useEffect } from 'react';
import { styled } from '@mui/material/styles';
import { Typography, Card, CardContent, List, ListItem, Checkbox } from '@mui/material';
import { getUser } from '../apis/auth';
import { getEmails, getTodoList } from '../apis/outlook';
import Loading from './Loading';

const WrapperDiv = styled('div')(() => ({
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    height: '100%',
    padding: '2rem',
}));

const StyledDiv = styled('div')(({ theme }) => ({
    padding: theme.spacing(2),
}));

const FlexContainer = styled('div')({
    display: 'flex',
    justifyContent: 'space-between',
});

const CenteredDiv = styled('div')({
    display: 'flex',
    justifyContent: 'center',
});

const StyledCard = styled(Card)(({ theme }) => ({
    width: '30%',
    margin: theme.spacing(2),
}));

const Home = () => {
    const [loading, setLoading] = useState(true);
    const [displayName, setDisplayName] = useState('');
    const [emails, setEmails] = useState([]);
    const [unread, setUnread] = useState(0);
    const [todoList, setTodoList] = useState([]);
    const [todoListLoading, setTodoListLoading] = useState(true);

    useEffect(() => {
        const handleAuth = async () => {
            const name = await getUser();
            const dispName = name === " " ? 'User' : name;
            setDisplayName(dispName);
            setLoading(false);
        }

        handleAuth();
    }, []);

    useEffect(() => {
        const fetchEmails = async () => {
            const fetchedEmails = await getEmails();
            if (fetchedEmails !== null) {
                setEmails(fetchedEmails['emails']);
                setUnread(fetchedEmails['unread_count']);
            }
        }

        fetchEmails();
    }, []);

    useEffect(() => {
        const fetchTodoList = async () => {
            const fetchedTodoList = await getTodoList();
            console.log(fetchedTodoList);
            if (fetchedTodoList !== null && fetchedTodoList.todo) {
                setTodoList(fetchedTodoList.todo);
                setTodoListLoading(false);
            }
        }
        if (!loading) {
            fetchTodoList();

        }
    }, [loading]);

    if (loading) {
        return <Loading />;
    }

    return (
        <WrapperDiv>
            <Typography variant="h4">Welcome, {displayName}!</Typography>
            <FlexContainer>
                <StyledCard>
                    <CardContent>
                        <Typography variant="h5">Unread Emails</Typography>
                        <Typography>{unread}</Typography>
                    </CardContent>
                </StyledCard>
                <StyledCard>
                    <CardContent>
                        <Typography variant="h5">Todo List</Typography>
                        {todoListLoading ? (
                            <CenteredDiv>
                                <Loading />
                            </CenteredDiv>
                        ) : (
                            <List>
                                {todoList.map((todo, index) => (
                                    <ListItem key={index}>
                                        <Checkbox />
                                        <Typography>{todo.task}</Typography>
                                    </ListItem>
                                ))}
                            </List>
                        )}
                    </CardContent>
                </StyledCard>
                <StyledCard>
                    <CardContent>
                        <Typography variant="h5">Email Summaries</Typography>
                        {/* Display email summaries here */}
                    </CardContent>
                </StyledCard>
            </FlexContainer>
        </WrapperDiv>
    );
};

export default Home;