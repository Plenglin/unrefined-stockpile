import React, {createContext, useContext, useState} from "react";
import axios from "axios";
import {useCookies} from "react-cookie";


const LoginContext = createContext(null);

export function useLoginContext() {
    return useContext(LoginContext);
}

export function setupCSRFToken() {
    return axios.get('/auth/csrf')
        .then(res => {
            axios.defaults.headers = {
                'X-CSRFToken': res.data.csrfToken
            };
            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios.defaults.csrfCookieName = res.data.csrfToken;
        })
}

export function LoginProvider(props) {
    const [cookies, setCookie, removeCookie] = useCookies(['loginToken']);
    const [token, setToken] = useState(cookies.loginToken);
    const [userData, setUserData] = useState(null);

    if (token && !userData) {
        axios.get('/api/users/current/')
            .then(res => {
                setUserData(res.data);
            });
    }

    const login = (username, password) => {
        return axios.get("/auth/csrf")
            .then(res => axios({
                method: 'post',
                url: "/auth/rest-auth/login/",
                data: {
                    username: username,
                    password: password,
                },
                headers: {
                    'X-CSRFToken': res.data.csrfToken
                },
                xsrfHeaderName: "X-CSRFToken",
                csrfCookieName: res.data.csrfToken
            }))
            .then(res => {
                const token = res.data.key;
                setToken(token);
                setCookie('loginToken', token);

                axios.defaults.headers['Authorization'] = `Token ${token}`;
                return axios.get('/api/users/current/')
                    .then(res => {
                        setUserData(res.data);
                    });
            });
    };

    const logout = () => {
        return axios.get('/auth/csrf')
            .then(res => axios({
                method: 'post',
                url: "/auth/rest-auth/logout/",
                headers: {
                    'X-CSRFToken': res.data.csrfToken
                },
                xsrfHeaderName: "X-CSRFToken",
                csrfCookieName: res.data.csrfToken
            }))
            .then(_ => {
                removeCookie('loginToken');
                setToken(null);
                setUserData(null);
            });
    };

    return <LoginContext.Provider value={{token, userData, login, logout}}>
        {props.children}
    </LoginContext.Provider>
}