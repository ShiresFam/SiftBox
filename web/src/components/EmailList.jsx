import { useState } from 'react';
import { Tooltip, IconButton, useMediaQuery } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { DataGrid } from '@mui/x-data-grid';
import { styled } from '@mui/system';
import MarkAsReadIcon from '@mui/icons-material/Drafts';
import SummaryIcon from '@mui/icons-material/Description';

const WrapperDiv = styled('div')({
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    height: 'auto',
});

const GridWrapperDiv = styled('div')({
    height: '100%',
    flex: '1 1 auto', // Allows the div to grow and shrink
    overflow: 'auto', // Makes the content within the div scrollable
});

const EmailList = ({ emails, summaryHandler, readHandler }) => {
    const theme = useTheme();
    const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));
    const [selectedEmail, setSelectedEmail] = useState(null);

    const handleEmailClick = (email) => {
        setSelectedEmail(email);
    }

    const markAsRead = (email) => {
        // Call your API to mark the email as read
        // Then remove the email from the selected state
        readHandler(email);
    }

    const requestSummary = (email) => {
        console.log('Making a summary');
        summaryHandler(email);
    }

    const columns = [
        {
            field: 'priorityRating',
            hide: true,
            hideable: true,
        },
        {
            field: 'sender',
            headerName: 'From',
            flex: 1,
            renderCell: (params) => (
                <Tooltip title={params.value}>
                    <span>{params.value}</span>
                </Tooltip>
            ),
        },
        {
            field: 'subject',
            headerName: 'Subject',
            flex: 2,
            renderCell: (params) => (
                <Tooltip title={params.value}>
                    <span>{params.value}</span>
                </Tooltip>
            ),
        },
        {
            field: 'actions',
            headerName: 'Actions',
            width: isSmallScreen ? 100 : 100,
            renderCell: (params) => (
                <div>
                    <IconButton onClick={() => markAsRead(params.row)} color="primary">
                        <MarkAsReadIcon />
                    </IconButton>
                    <IconButton onClick={() => requestSummary(params.row)} color="primary">
                        <SummaryIcon />
                    </IconButton>
                </div>
            ),
        },

    ];

    return (
        <WrapperDiv>
            <GridWrapperDiv>
                <DataGrid rows={emails} columns={columns} initialState={{ pagination: { paginationModel: { pageSize: 10 } } }} autoHeight pageSizeOptions={[5, 10, 25]}
                    columnVisibilityModel={{
                        priorityRating: false,
                    }}
                    sortModel={[
                        {
                            field: 'priorityRating',
                            sort: 'asc', // or 'desc' for descending
                        },
                    ]}
                />
            </GridWrapperDiv>
        </WrapperDiv>
    );
}

export default EmailList;