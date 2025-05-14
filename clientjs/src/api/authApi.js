const baseUrl = 'http://localhost:8000/accounts';

export const useRegister = () => {
    const register = async (userData) => {
        try {
            const response = await fetch(`${baseUrl}/register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            const result = await response.json();

            return result;
        } catch (err) {
            console.log(err.message);
        }
    };

    return {
        register
    };
};

export const useLogin = () => {
    const login = async (userData) => {
        try {
            const response = await fetch(`${baseUrl}/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            const result = await response.json();

            return result;
        } catch (err) {
            console.log(err.message);
        }
    };

    return {
        login
    };
};

export const useLogout = () => {
    const logout = async (data) => {
        try {
            const response = await fetch(`${baseUrl}/logout/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${data.access}`
                },
                body: JSON.stringify({ refresh: data.refresh })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || 'Logout failed');
            }

            return result;
        } catch (err) {
            console.log(err.message);
            throw err;
        }
    };

    return {
        logout
    };
};
