import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
    LayoutDashboard,
    PieChart,
    Zap,
    Settings,
    Cloud,
    Menu,
    X,
    LogOut
} from 'lucide-react';

interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    const [isSidebarOpen, setIsSidebarOpen] = React.useState(false);
    const location = useLocation();

    const isActive = (path: string) => location.pathname === path;

    const navItems = [
        { path: '/', label: 'Dashboard', icon: LayoutDashboard },
        { path: '/optimization', label: 'Optimization Hub', icon: Zap },
        { path: '/analyze', label: 'Cost Analyzer', icon: PieChart },
        { path: '/settings', label: 'Settings', icon: Settings },
    ];

    return (
        <div className="min-h-screen bg-gray-50 flex">
            {/* Sidebar */}
            <aside
                className={`
          fixed inset-y-0 left-0 z-50 w-64 bg-slate-900 text-white transform transition-transform duration-200 ease-in-out
          ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}
          md:relative md:translate-x-0
        `}
            >
                <div className="flex items-center justify-between h-16 px-4 bg-slate-950">
                    <div className="flex items-center space-x-2">
                        <Cloud className="h-8 w-8 text-blue-400" />
                        <span className="text-xl font-bold">CloudSathi</span>
                    </div>
                    <button
                        onClick={() => setIsSidebarOpen(false)}
                        className="md:hidden text-gray-400 hover:text-white"
                    >
                        <X className="h-6 w-6" />
                    </button>
                </div>

                <nav className="mt-8 px-2 space-y-1">
                    {navItems.map((item) => {
                        const Icon = item.icon;
                        return (
                            <Link
                                key={item.path}
                                to={item.path}
                                className={`
                  flex items-center px-4 py-3 text-sm font-medium rounded-md transition-colors
                  ${isActive(item.path)
                                        ? 'bg-blue-600 text-white'
                                        : 'text-gray-300 hover:bg-slate-800 hover:text-white'}
                `}
                            >
                                <Icon className="mr-3 h-5 w-5" />
                                {item.label}
                            </Link>
                        );
                    })}
                </nav>

                <div className="absolute bottom-0 w-full p-4 border-t border-slate-800">
                    <button className="flex items-center w-full px-4 py-2 text-sm font-medium text-gray-400 hover:text-white transition-colors">
                        <LogOut className="mr-3 h-5 w-5" />
                        Sign Out
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
                {/* Top Header (Mobile only) */}
                <header className="md:hidden bg-white border-b border-gray-200 flex items-center justify-between px-4 h-16">
                    <div className="flex items-center">
                        <Cloud className="h-8 w-8 text-blue-600" />
                        <span className="ml-2 text-xl font-bold text-gray-900">CloudSathi</span>
                    </div>
                    <button
                        onClick={() => setIsSidebarOpen(true)}
                        className="text-gray-500 hover:text-gray-700"
                    >
                        <Menu className="h-6 w-6" />
                    </button>
                </header>

                <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
                    {children}
                </main>
            </div>
        </div>
    );
};

export default Layout;
