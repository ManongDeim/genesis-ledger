import { useState } from 'react';
import AuthLayout from '../layouts/AuthLayout';

export default function ForgotPassword() {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    const handleReset = async (e) => {
        e.preventDefault();
        setError('');
        setMessage('');

        const response = await fetch('http://localhost:5000/api/forgot-password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });

        const data = await response.json();
        if (response.ok) {
            setMessage(data.message);
        } else {
            setError(data.error);
        }
    };

    return (
        <AuthLayout>
            <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-[#a8e6cf] mb-2">Forgot Password</h2>
                <p className="text-gray-400 text-sm">Enter your email and we'll send you a recovery PIN.</p>
            </div>

            {error && <p className="text-red-400 text-sm text-center mb-4">{error}</p>}
            {message && <p className="text-green-400 text-sm text-center mb-4">{message}</p>}

            <form onSubmit={handleReset} className="space-y-6">
                <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">Email Address</label>
                    <input type="email" name="email" required className="w-full px-4 py-2 bg-[#1a1d1c] border border-gray-700 rounded-lg text-gray-200 focus:outline-none focus:border-[#a8e6cf] focus:ring-1 focus:ring-[#a8e6cf] transition-colors"
            placeholder="example@email.com" onChange={(e) => setEmail(e.target.value)} />
                </div>

                <button type="submit" className="w-full py-2.5 bg-[#a8e6cf] text-[#1a1d1c] font-bold rounded-lg hover:bg-green-300 transition-colors"> 
                Send PIN
                </button>
            </form>

            <div className="mt-6 text-center">
                <a to="/login" className="text-sm text-gray-400 hover:text-[#a8e6cf] transition-colors">Back to Login</a>
            </div>
        </AuthLayout>
    );
}