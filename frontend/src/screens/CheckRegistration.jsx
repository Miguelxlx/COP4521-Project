const checkRegistration = async (email, password) => {
    try {
        const response = await fetch('/check_registration', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Registration check failed.');
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Registration check error:', error.message);
        throw error;
    }
};

// Example usage
const email = 'user@example.com';
const password = 'mypassword';

checkRegistration(email, password)
    .then(result => {
        console.log('Registration check result:', result);
        // Handle result (valid or invalid registration)
    })
    .catch(error => {
        console.error('Registration check failed:', error.message);
        // Handle error
    });
