import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout";

export default function Login() {
    const [credentials, setCredentials] = useState({username: "", password: ""});
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async(e) => {
        e.preventDefault();
        setError('');
        const response = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers:{ 'Content-Type': 'application/json'},
            body: JSON.stringify(credentials)
        });

        const data = await response.json();
        if (response.ok){
            localStorage.setItem('token', data.token);
            navigate('/home');
        } else {
            setError(data.error);
        }
    };
        return(
<AuthLayout>
    <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-[#a8e6cf] mb-2">Genesis</h2>
        <p className="text-gray-400 text-sm">Sign in to your dashboard</p>
    </div>

    {error && <p className="text-red-400 text-sm text-center mb-4">{error}</p>}

    <form onSubmit={handleLogin} className="space-y-6">
        <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Username</label>
            <input type="text" required className="w-full px-4 py-2 bg-[#1a1d1c] border border-gray-700 rounded-lg text-gray-200 focus:outline-none focus:border-[#a8e6cf] focus:ring-1 focus:ring-[#a8e6cf] transition-colors" placeholder="Enter custom username" onChange={(e) => setCredentials({...credentials, username: e.target.value})} />
        </div>

        <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Password</label>
            <input type="password" required className="w-full px-4 py-2 bg-[#1a1d1c] border border-gray-700 rounded-lg text-gray-200 focus:outline-none focus:border-[#a8e6cf] focus:ring-1 focus:ring-[#a8e6cf] transition-colors" placeholder="••••••••"
            onChange={(e) => setCredentials({...credentials, password: e.target.value})} />
        </div>

        <div className="flex justify-end">
            <Link to="/forgot-password" className="text-xs text-[#a8e6cf] hover:text-green-300 transition-colors">
            Forgot Password?
            </Link>
        </div>

        <button type="submit" className="w-full py-2.5 bg-[#a8e6cf] text-[#1a1d1c] font-bold rounded-lg hover:bg-green-300 transition-colors">
            Sign In
        </button>
    </form>

        <p className="mt-6 text-center text-sm text-gray-400">
        Don't have an account?{' '}
        <Link to="/register" className="text-[#a8e6cf] hover:text-green-300 transition-colors font-medium">
            Register here
        </Link>
        </p>
</AuthLayout>
    );
}