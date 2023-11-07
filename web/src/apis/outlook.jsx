import { baseUrl } from "./utils";

export const getEmails = async () => {
    try {
        const response = await fetch(baseUrl + '/mail/unread');
        console.log(response);
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
        return null;
    }
}

export const replyToEmail = async (emailId, reply) => {
    try {
        const response = await fetch(baseUrl + `/mail/reply/${emailId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ reply }),
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
        return null;
    }
}

export const markAsRead = async (emailId) => {
    try {
        const response = await fetch(baseUrl + `/mail/mark-as-read/${emailId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
        return null;
    }
}