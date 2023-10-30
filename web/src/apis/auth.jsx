import { baseUrl } from "./utils";

export const getUser = async () => {
    try {
        const response = await fetch(baseUrl + '/auth/me');
        console.log(response)
        const data = await response.json();
        if (response.status === 307) {
            // return an object with the redirect URL and the 'redirected' field
            console.log('h223i', data)
            window.location.href = data.url;
        } else {
            return data;
        }

    } catch (error) {
        console.log(error);
        return null;
    }
}