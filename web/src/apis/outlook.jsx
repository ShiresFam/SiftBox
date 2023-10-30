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