// Global authentication state using React's Context API.
// This file creates a centralized auth store so any component in the app can access the
// current user, login/logout actions, and authentication status without manually passing
// props through many levels of the component tree.

import {createContext, useContext, useMemo, useState} from "react"
import apiClient from "../api/client"

// Create a React context with a default value of null.
// The provider will later supply the real auth value, and consumers can read it via useAuth().
// This is important because it gives us a single source of truth for authentication state.
const AuthContext = createContext(null);

// Decode the payload portion of a JWT so we can read user data in the frontend.
// JWTs are Base64-encoded JSON, so we split the token into segments, take the middle payload,
// decode it, and parse it into a JavaScript object.
// This matters because the backend stores user identity in the token, and the frontend can
// use that data for UI decisions like displaying the logged-in user's name or role.
function decodeToken(token){
    const payloadSegment = token.split('.')[1]
    return JSON.parse(atob(payloadSegment))
};

// AuthProvider wraps the app (or part of the app) and exposes authentication state to all
// children through the context. This keeps auth logic in one place and prevents duplicate
// state handling across components.
export function AuthProvider({children}){
    // Initialize the token from browser localStorage so the user remains logged in across a
    // page refresh. Using a lazy state initializer makes this happen once when the component
    // mounts, instead of on every render.
    const [token, setToken] = useState(() => localStorage.getItem('bankToken'))

    // Derive the logged-in user object from the JWT whenever the token changes.
    // useMemo caches the decoded user so we do not re-decode the token on every render.
    // This is important for performance and keeps the user data stable unless the token changes.
    const user = useMemo(() => (token ? decodeToken(token) : null), [token])

    // Login sends the user's username and password to the backend's token endpoint.
    // The backend returns an access token that we persist in local storage and also store in
    // React state. This allows the frontend to know the user is authenticated immediately and
    // to keep that state after refreshes.
    const login = async (username, password) => {
        // Build a URL-encoded form payload because the FastAPI OAuth token endpoint expects
        // form data rather than JSON. This matches the backend contract exactly.
        const formData = new URLSearchParams()
        formData.append('username', username)
        formData.append('password', password)

        // Send the credentials to the backend token endpoint.
        // The response contains access_token, which is the JWT used for subsequent authenticated requests.
        const response = await apiClient.post('/auth/token', formData, {
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        });

        // Save the token in browser storage so the session persists after a refresh,
        // and keep it in React state so the UI re-renders and updates protected routes/components.
        localStorage.setItem('bankToken', response.data.access_token)
        setToken(response.data.access_token)
    }

    // Logout clears the stored token and resets the auth state to null.
    // This is critical for ending the user's session and ensuring protected pages hide
    // content that requires authentication.
    const logout = () => {
        localStorage.removeItem('bankToken')
        setToken(null)
    }

    // Package all auth data and actions into a single value object.
    // This is the contract exposed to any component using the context; it keeps consumption
    // simple and predictable across the app.
    const value = {token, user, isAuthenticated: Boolean(token), login, logout}

    // Render the context provider and pass the computed auth value to all children.
    // Every nested component can then access the current auth state without prop drilling.
    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// Custom hook that exposes the auth context to components that need it.
// This prevents consumers from directly importing the context and makes the API cleaner.
// It also throws a clear error if the hook is used outside the AuthProvider, which helps catch
// mistakes during development.
export function useAuth(){
    const context = useContext(AuthContext)
    if (context === null){
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
}




