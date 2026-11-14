import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout";

export default function Register(){
    const [formData, setFormData] = useState({username: "", email: "", password: ""});
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleRegister = async(e) => {
        e.preventDefault();
        setError('');
        const response = await fetch('http://localhost:5000/api/register', {
            method: 'POST',
            headers:{ 'Content-Type': 'application/json'},
            body: JSON.stringify(formData)
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
            <h2 className="test-3xl font-bold text-[#a8e6cf] mb-2">Create Account</h2>
            <p className="text-gray-400 text-sm">Join Genesis and start learning!</p>
        </div>

        {error && <p className="text-red-400 text-sm text-center mb-4">{error}</p>}

        <form onSubmit={handleRegister} className="space-y-6">
            <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Username</label>
                <input type="text" name="username" required className="w-full px-4 py-2 bg-[#1a1d1c] border border-gray-700 rounded-lg text-gray-200 focus:outline-none focus:border-[#a8e6cf] focus:ring-1 focus:ring-[#a8e6cf] transition-colors" onChange={(e) => setFormData({...formData, username: e.target.value})} />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Email</label>
                <input type="email" name="email" required className="w-full px-4 py-2 bg-[#1a1d1c] border border-gray-700 rounded-lg text-gray-200 focus:outline-none focus:border-[#a8e6cf] focus:ring-1 focus:ring-[#a8e6cf] transition-colors" onChange={(e) => setFormData({...formData, email: e.target.value})} />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Password</label>
                <input type="password" name="password" required className="w-full px-4 py-2 bg-[#1a1d1c] border border-gray-700 rounded-lg text-gray-200 focus:outline-none focus:border-[#a8e6cf] focus:ring-1 focus:ring-[#a8e6cf] transition-colors" onChange={(e) => setFormData({...formData, password: e.target.value})} />
            </div>

            <button type="submit" className="w-full py-2.5 mt-2 bg-[#a8e6cf] text-[#1a1d1c] font-bold rounded-lg hover:bg-green-300 transition-colors">
                Register
            </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-400">
            Already have an account?{' '}
            <a href="/login" className="text-[#a8e6cf] hover:text-green-300 transition-colors font-medium">
                Sign in here
            </a>
        </p>
    </AuthLayout>
    );
}

