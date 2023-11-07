import { useState, useEffect, Fragment } from 'react';
import { styled } from '@mui/material/styles';
import { Typography, List, ListItem, Checkbox, IconButton, Button, TextField } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import RefreshIcon from '@mui/icons-material/Refresh';
import { getEmails, replyToEmail, markAsRead } from '../apis/outlook';
import EmailList from './EmailList';
import { createImportantEmails, createSummaries, createTodoList, completeTodo, deleteTodo, getImportantEmails, getTodoList, createSummary, createResponse } from '../apis/emails';
import Loading from './Loading';


const WrapperDiv = styled('div')({
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    height: '100%',
    padding: '2rem',
    overflow: 'hidden', // Prevents scroll on the whole page
});


const FlexContainer = styled('div')({
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    height: '100%',
});

const CenteredDiv = styled('div')({
    display: 'flex',
    justifyContent: 'center',
});

const StyledCard = styled('div')(({ theme }) => ({
    width: '30%',
    flex: '1 1 auto',
    margin: theme.spacing(2),
    overflowY: 'auto',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: theme.palette.background.paper,
    borderRadius: theme.shape.borderRadius,
    boxShadow: theme.shadows[1],
}));

const CardContent = styled('div')(({ theme }) => ({
    padding: theme.spacing(2), // Gives the div some padding
    flex: '1 1 auto', // Allows the div to grow and shrink
}));

const RowDiv = styled('div')({ display: 'flex', flexDirection: 'row', alignItems: 'center' });

const Home = () => {
    const [loading, setLoading] = useState(true);

    const [emails, setEmails] = useState([]);
    const [unread, setUnread] = useState(0);
    const [summary, setSummary] = useState('');
    const [suggestedResponse, setSuggestedResponse] = useState('');
    const [isSummaryLoading, setSummaryLoading] = useState(false);
    const [importantEmails, setImportantEmails] = useState([]);
    const [importantRefreshing, setImportantRefreshing] = useState(false);
    const [todoList, setTodoList] = useState([]);
    const [todoListLoading, setTodoListLoading] = useState(true);
    const [isUnreadEmailsExpanded, setUnreadEmailsExpanded] = useState(false);
    const [isImportantEmailsExpanded, setImportantEmailsExpanded] = useState(false);
    const [responseRequested, setResponseRequested] = useState(false);

    const handleSummary = async (email) => {
        if (email.summary !== null) {
            setSummary(email);
        } else {

            setSummaryLoading(true);
            const newSummary = await createSummary(email.id);
            setSummary(newSummary);
            setSummaryLoading(false);
        }

    }

    const handleRead = async (email) => {
        const resp = await markAsRead(email.id);
        if (resp.message) {
            const fetchedEmails = await getEmails();
            console.log(fetchedEmails)
            if (fetchedEmails !== null) {
                setEmails(fetchedEmails['emails']);
                setUnread(fetchedEmails['unread_count']);
            }
        }

    }

    const handleSuggestedResponse = async (email) => {
        setResponseRequested(true);
        setSuggestedResponse('');
        const resp = await createResponse(email.id);
        console.log(resp.response)
        setSuggestedResponse(resp.response);

    }

    const handleSendResponse = async (email) => {
        const resp = await replyToEmail(email.id, suggestedResponse);
        console.log(resp);
        setResponseRequested(false);
        setSuggestedResponse('');
    }

    const handleTodoRefresh = async () => {
        setTodoListLoading(true);
        const newTodoList = await createTodoList();
        setTodoList(newTodoList.todo);
        setTodoListLoading(false);
    }

    const handleImportantRefresh = async () => {
        setImportantRefreshing(true);
        const importantStatus = await createImportantEmails();
        const newImportantEmails = await getImportantEmails();
        setImportantEmails(newImportantEmails);
        setImportantRefreshing(false);
    }

    const cancelResponse = () => {
        setResponseRequested(false);
        setSuggestedResponse('');
    }

    useEffect(() => {
        const fetchEmails = async () => {
            const fetchedEmails = await getEmails();
            if (fetchedEmails !== null) {
                setEmails(fetchedEmails['emails']);
                setUnread(fetchedEmails['unread_count']);
            }
            setLoading(false);

        }

        fetchEmails();
    }, []);

    useEffect(() => {
        const fetchImportantEmails = async () => {
            const fetchedImportantEmails = await getImportantEmails();
            console.log(fetchedImportantEmails)
            if (fetchedImportantEmails !== null) {
                setImportantEmails(fetchedImportantEmails);
            }
        }
        if (emails.length > 0)
            fetchImportantEmails();
    }, [emails]);

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
            <FlexContainer>
                <StyledCard>
                    <CardContent>
                        <RowDiv style={{ justifyContent: 'space-between' }}>
                            <Typography variant="h5">Emails</Typography>
                            <IconButton onClick={handleImportantRefresh}>
                                <RefreshIcon />
                            </IconButton>
                        </RowDiv>
                        <RowDiv>
                            <Typography>Unread Emails: {unread}</Typography>
                            <IconButton onClick={() => setUnreadEmailsExpanded(!isUnreadEmailsExpanded)}>
                                {isUnreadEmailsExpanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                            </IconButton>
                        </RowDiv>
                        {isUnreadEmailsExpanded && <EmailList emails={emails} summaryHandler={handleSummary} readHandler={handleRead} />}
                        <RowDiv>
                            {importantRefreshing ? (
                                <Fragment>
                                    <Typography>Important Emails: </Typography>
                                    <Loading size={20} />
                                </Fragment>

                            ) : (
                                <Fragment>
                                    <Typography>Important Emails: {importantEmails.length}</Typography>
                                    <IconButton onClick={() => setImportantEmailsExpanded(!isImportantEmailsExpanded)}>
                                        {isImportantEmailsExpanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                                    </IconButton>
                                </Fragment>
                            )}


                        </RowDiv>
                        {isImportantEmailsExpanded && <EmailList emails={importantEmails} summaryHandler={handleSummary} readHandler={handleRead} />}
                    </CardContent>
                </StyledCard>
                <StyledCard>
                    <CardContent>
                        <RowDiv style={{ justifyContent: 'space-between' }}>
                            <Typography variant="h5">Todo List</Typography>
                            <IconButton onClick={handleTodoRefresh}>
                                <RefreshIcon />
                            </IconButton>
                        </RowDiv>
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
                        <RowDiv style={{ justifyContent: 'space-between', marginBottom: '1rem' }}>
                            <Typography variant="h5">Email Summaries</Typography>
                            {summary.summary && (
                                <Button
                                    size='small'
                                    variant="contained"
                                    color="primary"
                                    onClick={() => handleSuggestedResponse(summary)} // This function should send the request to get the suggested response
                                >
                                    Get Suggested Response
                                </Button>
                            )}
                        </RowDiv>
                        {isSummaryLoading ? (
                            <CenteredDiv>
                                <Loading />
                            </CenteredDiv>
                        ) : (
                            <div>

                                <Typography>{summary.summary}</Typography>

                                {responseRequested && suggestedResponse === '' ? (
                                    <CenteredDiv>
                                        <Loading />
                                    </CenteredDiv>
                                ) : suggestedResponse && (
                                    <Fragment>
                                        <TextField
                                            multiline
                                            rows={20} // Increase this value as needed
                                            defaultValue={suggestedResponse}
                                            variant="outlined"
                                            style={{ width: '100%', marginTop: '0.5rem', marginBottom: '0.5rem' }} // This will make the TextField take up the full width of its parent
                                        />
                                        <RowDiv>
                                            <Button
                                                style={{ marginRight: '1rem' }}
                                                variant="contained"
                                                color="primary"
                                                onClick={handleSendResponse} // This function should send the response
                                            >
                                                Send Response
                                            </Button>
                                            <Button
                                                variant="contained"
                                                color="primary"
                                                onClick={cancelResponse} // This function should send the response
                                            >
                                                Cancel
                                            </Button>
                                        </RowDiv>
                                    </Fragment>
                                )}
                            </div>
                        )}
                    </CardContent>
                </StyledCard>
            </FlexContainer>

        </WrapperDiv>
    );
};

export default Home;