import decode from 'jwt-decode'
import axios from 'axios'

const AUTH_TOKEN_KEY = 'authToken'

export function loginUser(username, password) {
    return new Promise(async (resolve, reject) => {
        try {
            let res = await axios({
                url: '/login',
                method: 'POST',
                data: {
                    login: username,
                    password: password,
                }
            })
            setAuthToken(res.data)
            resolve()
        }
        catch (error) {
            console.error(`Caught an error during login: ${error}`)
            reject(error)
        }
    })
}

export function registerUser(register_data) {
    return new Promise(async (resolve, reject) => {
        try {
            let res = await axios({
                url: '/register',
                method: 'PUT',
                data: register_data
            })

            setAuthToken(res.data)
            resolve()
        }
        catch (error) {
            console.error(`Caught an error during login: ${error}`)
            reject(error)
        }
    })
}

export function logoutUser() {
    clearAuthToken()
}

export function setAuthToken(token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    localStorage.setItem(AUTH_TOKEN_KEY, token)
}

export function getAuthToken() {
    return localStorage.getItem(AUTH_TOKEN_KEY)
}

export function clearAuthToken() {
    axios.defaults.headers.common['Authorization'] = ''
    localStorage.removeItem(AUTH_TOKEN_KEY)
}

export function isLoggedIn() {
    let authToken = getAuthToken()
    return !!authToken && !isTokenExpired(authToken)
}

export function getUserInfo() {
    if (isLoggedIn()) {
        return decode(getAuthToken())
    }
}

function getTokenExpirationDate(encodedToken) {
    let token = decode(encodedToken)
    if (!token.exp) {
        return null
    }

    let date = new Date(0)
    date.setUTCSeconds(token.exp)

    return date
}

function isTokenExpired(token) {
    let expirationDate = getTokenExpirationDate(token)
    return expirationDate < new Date()
}
