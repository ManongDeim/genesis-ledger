import { useState } from "react";
import { Link } from "react-router-dom";
import AuthLayout from "../layouts/AuthLayout";

export default function Login() {
    const [credentials, setCredentials] = useState({username: "", password: ""});
    const [error, setError] = useState('');
    const [navigate] = useNavigate();
        return(
        <AuthLayout>
            <div className="text-center mb-8">
                <h1 className="text-xl font-bold text-[#a8e6cf] mb-2">Genesis</h1>
                <h3 className="text-gray-400 text-sm">Sign in to your dashboard</h3>
            </div>

            <form className="space-y-6">
                <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1" for="username">Username</label>
                    <input type="text" className="w-full px-4 py-2 bg-[#1a1d1c] border border-gray-700 rounded-lg text-gray-200 focus:outline-none focus:border-[#a8e6cf] focus:ring-1 focus:ring-[#a8e6cf] transition-colors" placeholder="Enter custom username" name="username"/>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1" for="password">Password</label>
                    <input type="password" className="w-full px-4 py-2 bg-[#1a1d1c] border border-gray-700 rounded-lg text-gray-200 focus:outline-none focus:border-[#a8e6cf] focus:ring-1 focus:ring-[#a8e6cf] transition-colors" placeholder="••••••••" name="password"/>
                </div>

                <div className="flex justify-end">
                    <Link to="/forgot-password" className="text-xs text-[#a8e6cf] hover:text-green-300 transition-colors">
                        Forgot password?
                    </Link>
                </div>

                <button type="submit" className="w-full py-2.5 bg-[#a8e6cf] text-[#1a1d1c] font-bold rounded-lg hover:bg-green-300 transition-colors">
                    Sign in
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