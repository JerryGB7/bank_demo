// Global auth state using react's context api

import {createContext, useContext, useMemo, useState} from "react"
import apiClient from "../api/client"

//create a global react context which acts as a central store to hold authentication state
// so any component can access it without passing props down manually

const AuthContext = createContext(null);

// extracts and decodes the user payload from JWT so that react can read it
function decodeToken(token){
    const payloadSegment = token.split('.')[1]
    return JSON.parse(atob(payloadSegment))
};

//Auth provider manages authentication state 
export function AuthProvider({children}){
    //initializing our token state from the browser's local storage to ensure a user 
    // stays logged in even if they refresh the page
    const [token, setToken] = useState(() => localStorage.getItem('bankToken'))

    //decode the JWT into a user object and cache the results and prevent re-coding
    // the token string on every re-render. 
    const user = useMemo(() => (token ? decodeToken(token) : null), [token])

    //authenticates the user credentials against the backend API by sending credentials,
    // saving the returned token to localstorage, and updates the react state
    const login = async (username, password) => {
        const formData = new URLSearchParams()
        formData.append('username', username)
        formData.append('password', password)

        const response = await apiClient.post('/auth/token', formData, {
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        });

        localStorage.setItem('bankToken', response.data.access_token)
        setToken(response.data.access_token)
    }

    //logout function clears the authentication session and reset the state to null
    const logout = () => {
        localStorage.removeItem('bankToken')
        setToken(null)
    }

    // bundles all auth state variables and action functions into a single object to define
    // the exact interface exposed to components that are consuming this context
    const value = {token, user, isAuthenticated: Boolean(token), login, logout}

    //renders the context provider and passes down the value object to make the auth state
    // and functions available to all nested child components
    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// a custom react hook that exposes the auth context to any component 
// this simplifies context usage in child react components
export function useAuth(){
    const context = useContext(AuthContext)
    if (context === null){
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
}




