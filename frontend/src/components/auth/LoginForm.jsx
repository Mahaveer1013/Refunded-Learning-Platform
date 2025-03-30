import React, { useState, useContext } from 'react';
import api from '../api/api';
import { storeToken } from '../../utils/auth';
import { AppContext } from '../../utils/Context';


export const EmailPasswordFields = ({ formData, handleChange, errors }) => {
    return (
        <>
            <div>
                <label htmlFor="email" className="block text-sm font-medium text-[var(--color-text)]">
                    Email address
                </label>
                <div className="mt-1">
                    <input
                        id="email"
                        name="email"
                        type="email"
                        autoComplete="email"
                        value={formData.email}
                        onChange={handleChange}
                        className={`block p-2 w-full rounded-md border-[var(--color-border)]_2px shadow-sm focus:border-[var(--color-primary)] focus:ring-[var(--color-primary)] sm:text-sm ${errors.email ? 'border-[var(--color-error)]' : 'border-gray-300'
                            }`}
                    />
                    {errors.email && (
                        <p className="mt-2 text-sm text-[var(--color-error)]">{errors.email}</p>
                    )}
                </div>
            </div>

            <div>
                <label htmlFor="password" className="block text-sm font-medium text-[var(--color-text)]">
                    Password
                </label>
                <div className="mt-1">
                    <input
                        id="password"
                        name="password"
                        type="password"
                        autoComplete='new-password'
                        value={formData.password}
                        onChange={handleChange}
                        className={`block p-2 w-full rounded-md border-[var(--color-border)]_2px shadow-sm focus:border-[var(--color-primary)] focus:ring-[var(--color-primary)] sm:text-sm ${errors.password ? 'border-[var(--color-error)]' : 'border-gray-300'
                            }`}
                    />
                    {errors.password && (
                        <p className="mt-2 text-sm text-[var(--color-error)]">{errors.password}</p>
                    )}
                </div>
            </div>
        </>
)};

const LoginForm = ({ setAuthError }) => {
    const AppContextValue = useContext(AppContext);
    const { setIsAuthenticated } = AppContextValue;
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    const [errors, setErrors] = useState({});
    const [loading, setLoading] = useState(false);

    const validate = () => {
        const newErrors = {};

        if (!formData.email) {
            newErrors.email = 'Email is required';
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            newErrors.email = 'Email is invalid';
        }

        if (!formData.password) {
            newErrors.password = 'Password is required';
        } else if (formData.password.length < 6) {
            newErrors.password = 'Password must be at least 6 characters';
        }
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setAuthError('');

        if (!validate()) return;

        setLoading(true);

        try {
            const response = await api.post('/auth/login', {
                email: formData.email,
                password: formData.password,
            });

            console.log('Auth success:', response.data);
            storeToken(response.data.token);
            // Handle successful auth (store token, redirect, etc.)
            setIsAuthenticated(true);
            setFormData({
                email: '',
                password: '',
            })
            alert('Login successful!');
        } catch (error) {
            console.error('Auth error:', error.response?.data || error.message);
            setAuthError(error.response?.data?.message || 'Authentication failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    return (
        <form className="space-y-6" onSubmit={handleSubmit}>
            <EmailPasswordFields formData={formData} handleChange={handleChange} errors={errors} />

                    <div className="flex items-center justify-between">
                        <div className="flex items-center">
                            <input
                                id="remember-me"
                                name="remember-me"
                                type="checkbox"
                                className="h-4 w-4 text-[var(--color-primary)] focus:ring-[var(--color-primary)] border-[var(--color-border)] rounded"
                            />
                            <label htmlFor="remember-me" className="ml-2 block text-sm text-[var(--color-text)]">
                                Remember me
                            </label>
                        </div>

                        <div className="text-sm">
                            <a href="#" className="font-medium text-[var(--color-primary)] hover:text-[var(--color-primary-dark)]">
                                Forgot your password?
                            </a>
                        </div>
                    </div>

                <div>
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-[var(--color-primary)] hover:bg-[var(--color-primary-dark)] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--color-primary-light)] disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading ? (
                            <span className="flex items-center">
                                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Signing in...
                            </span>
                        ) : (
                            'Sign in'
                        )}
                    </button>
                </div>
            </form>
    );
};

export default LoginForm;
