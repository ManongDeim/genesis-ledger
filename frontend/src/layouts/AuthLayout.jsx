export default function AuthLayout({ children }) {
    return (
        <div className="min-h-screen relative flex items-center justify-center bg-[#1a1d1c] overflow-hidden font-sans">
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-[#a8e6cf] rounded-full mix-blend-overlay filter blur-[120px] opacity-20"></div>
            <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-[#a8e6cf] rounded-full mix-blend-overlay filter blur-[100px] opacity-10"></div>

            <div className="absolute inset-0 backdrop-blur-md"></div>

            {/* Main modal container */}
            <div className="relative z-10 w-full max-w-md p-8 bg-[#242927]/90 rounded-2xl shadow-2xl border border-[#a8e6cf]/20">
                {children}
            </div>
        </div>
    );
    }