import { baseUrl } from "./utils";

export const createImportantEmails = async () => {
    try {
        const response = await fetch(baseUrl + '/mail/create-important');
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
        return null;
    }
}

export const createSummaries = async () => {
    try {
        const response = await fetch(baseUrl + '/mail/create-summaries');
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
        return null;
    }
}

export const createSummary = async (emailId) => {
    try {
        const response = await fetch(baseUrl + `/mail/create-summary/${emailId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
        return null;
    }
}

export const createResponse = async (emailId) => {
    try {
        const response = await fetch(baseUrl + `/mail/response/${emailId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
        return null;
    }
}

export const createTodoList = async () => {
    try {
        const response = await fetch(baseUrl + '/mail/create-todolist');
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
        return null;
    }
}

export const getTodoList = async () => {
    try {
        const response = await fetch(baseUrl + '/mail/todolist');
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
        return null;

    }
}

export const completeTodo = async (id) => {
    try {
        const response = await fetch(baseUrl + '/mail/todo-complete/' + id, {
            method: 'PUT',
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
        return null;
    }
}

export const deleteTodo = async (id) => {
    try {
        const response = await fetch(baseUrl + '/mail/todo-complete/' + id, {
            method: 'PUT',
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
        return null;
    }
}

export const getImportantEmails = async () => {
    try {
        const response = await fetch(baseUrl + '/mail/get-important/emails');
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
        return null;
    }
}