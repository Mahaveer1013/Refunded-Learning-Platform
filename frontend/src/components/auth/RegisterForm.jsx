import React, { useState } from 'react';
import api from '../api/api';
import { EmailPasswordFields } from './LoginForm';

const RegisterForm = ({setAuthError}) => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirmPassword: '',
        firstName: '',
        lastName: '',
        phone: '',
        agreeTerms: false
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

        if (!formData.confirmPassword) {
            newErrors.confirmPassword = 'Please confirm your password';
        } else if (formData.password !== formData.confirmPassword) {
            newErrors.confirmPassword = 'Passwords do not match';
        }

        if (!formData.firstName) {
            newErrors.firstName = 'First name is required';
        }

        if (!formData.phone) {
            newErrors.phone = 'Phone number is required';
        }

        if (!/^\d{10}$/.test(formData.phone)) {
            newErrors.phone = 'Phone number not valid';
        }

        if (!formData.firstName) {
            newErrors.firstName = 'First name is required';
        }

        if (!formData.agreeTerms) {
            newErrors.agreeTerms = 'You must agree to the terms';
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

            const response = await api.post('/auth/register', {
                first_name: formData.firstName,
                last_name: formData.lastName,
                email: formData.email,
                password: formData.password,
                phone: formData.phone,
                confirm_password: formData.confirmPassword,
            });

            console.log('Auth success:', response.data);
            setFormData({
                email: '',
                password: '',
                confirmPassword: '',
                firstName: '',
                lastName: '',
                phone: '',
                agreeTerms: false
            })
            alert('Registration successful!');

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
                <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
                    <div>
                        <label htmlFor="firstName" className="block text-sm font-medium text-[var(--color-text)]">
                            First name
                        </label>
                        <div className="mt-1">
                            <input
                                id="firstName"
                                name="firstName"
                                type="text"
                                value={formData.firstName}
                                onChange={handleChange}
                                className={`block p-2 w-full rounded-md border-[var(--color-border)]_2px shadow-sm focus:border-[var(--color-primary)] focus:ring-[var(--color-primary)] sm:text-sm ${errors.firstName ? 'border-[var(--color-error)]' : 'border-gray-300'
                                    }`}
                            />
                            {errors.firstName && (
                                <p className="mt-2 text-sm text-[var(--color-error)]">{errors.firstName}</p>
                            )}
                        </div>
                    </div>

                    <div>
                        <label htmlFor="lastName" className="block text-sm font-medium text-[var(--color-text)]">
                            Last name
                        </label>
                        <div className="mt-1">
                            <input
                                id="lastName"
                                name="lastName"
                                type="text"
                                value={formData.lastName}
                                onChange={handleChange}
                                className="block p-2 w-full rounded-md border-[var(--color-border)]_2px shadow-sm focus:border-[var(--color-primary)] focus:ring-[var(--color-primary)] sm:text-sm"
                            />
                        </div>
                    </div>
                </div>

                <EmailPasswordFields formData={formData} handleChange={handleChange} errors={errors} />

                <div>
                    <label htmlFor="confirmPassword" className="block text-sm font-medium text-[var(--color-text)]">
                        Confirm password
                    </label>
                    <div className="mt-1">
                        <input
                            id="confirmPassword"
                            name="confirmPassword"
                            type="password"
                            autoComplete="new-password"
                            value={formData.confirmPassword}
                            onChange={handleChange}
                            className={`block p-2 w-full rounded-md border-[var(--color-border)]_2px shadow-sm focus:border-[var(--color-primary)] focus:ring-[var(--color-primary)] sm:text-sm ${errors.confirmPassword ? 'border-[var(--color-error)]' : 'border-gray-300'
                                }`}
                        />
                        {errors.confirmPassword && (
                            <p className="mt-2 text-sm text-[var(--color-error)]">{errors.confirmPassword}</p>
                        )}
                    </div>
                </div>

                <div>
                    <label htmlFor="phone" className="block text-sm font-medium text-[var(--color-text)]">
                        Phone number
                    </label>
                    <div className="mt-1">
                        <input
                            id="phone"
                            name="phone"
                            type="password"
                            autoComplete="phone"
                            value={formData.phone}
                            onChange={handleChange}
                            className={`block p-2 w-full rounded-md border-[var(--color-border)]_2px shadow-sm focus:border-[var(--color-primary)] focus:ring-[var(--color-primary)] sm:text-sm ${errors.phone ? 'border-[var(--color-error)]' : 'border-gray-300'
                                }`}
                        />
                        {errors.phone && (
                            <p className="mt-2 text-sm text-[var(--color-error)]">{errors.phone}</p>
                        )}
                    </div>
                </div>

                <div className="flex items-start">
                    <div className="flex items-center h-5">
                        <input
                            id="agreeTerms"
                            name="agreeTerms"
                            type="checkbox"
                            checked={formData.agreeTerms}
                            onChange={handleChange}
                            className="focus:ring-[var(--color-primary)] h-4 w-4 text-[var(--color-primary)] rounded border-[var(--color-border)]_2px"
                        />
                    </div>
                    <div className="ml-3 text-sm">
                        <label htmlFor="agreeTerms" className="font-medium text-[var(--color-text)]">
                            I agree to the{' '}
                            <a href="#" className="text-[var(--color-primary)] hover:text-[var(--color-primary-dark)]">
                                Terms of Service
                            </a>{' '}
                            and{' '}
                            <a href="#" className="text-[var(--color-primary)] hover:text-[var(--color-primary-dark)]">
                                Privacy Policy
                            </a>
                        </label>
                        {errors.agreeTerms && (
                            <p className="mt-1 text-sm text-[var(--color-error)]">{errors.agreeTerms}</p>
                        )}
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
                                Registering...
                            </span>
                        ) : (
                            'Register'
                        )}
                    </button>
                </div>
            </form>
    );
};

export default RegisterForm;
