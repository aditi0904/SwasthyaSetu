import React, { useState } from 'react';
import { motion } from 'motion/react';
import { 
  Heart, 
  Users, 
  Settings, 
  Database, 
  FileText, 
  Activity,
  HelpCircle,
  LogOut,
  Bell,
  ChevronDown,
  Menu,
  Shield
} from 'lucide-react';
import { Button } from '../ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar';
import { Badge } from '../ui/badge';
import { Separator } from '../ui/separator';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '../ui/dropdown-menu';
import { Sheet, SheetContent, SheetTrigger } from '../ui/sheet';
import { useTheme } from '../ThemeProvider';
import AdminDashboardHome from './admin/AdminDashboardHome';
import UserManagement from './admin/UserManagement';
import MappingReviewer from './admin/MappingReviewer';
import ApiSync from './admin/ApiSync';
import AuditLogs from './admin/AuditLogs';
import type { User } from '../../App';

interface AdminDashboardProps {
  user: User;
  onLogout: () => void;
}

type AdminView = 'dashboard' | 'users' | 'mapping' | 'sync' | 'logs';

const AdminDashboard: React.FC<AdminDashboardProps> = ({ user, onLogout }) => {
  const { theme, toggleTheme } = useTheme();
  const [currentView, setCurrentView] = useState<AdminView>('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Activity, active: currentView === 'dashboard' },
    { id: 'users', label: 'User Management', icon: Users, active: currentView === 'users' },
    { id: 'mapping', label: 'Mapping Reviewer', icon: Settings, active: currentView === 'mapping' },
    { id: 'sync', label: 'API Sync', icon: Database, active: currentView === 'sync' },
    { id: 'logs', label: 'Audit Logs', icon: FileText, active: currentView === 'logs' },
  ];

  const renderContent = () => {
    switch (currentView) {
      case 'dashboard':
        return <AdminDashboardHome user={user} />;
      case 'users':
        return <UserManagement />;
      case 'mapping':
        return <MappingReviewer />;
      case 'sync':
        return <ApiSync />;
      case 'logs':
        return <AuditLogs />;
      default:
        return <AdminDashboardHome user={user} />;
    }
  };

  const Sidebar = ({ mobile = false }) => (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
            <Heart className="w-6 h-6 text-white" />
          </div>
          <div>
            <span className="text-xl text-gray-900 dark:text-white">SwasthyaSetu</span>
            <Badge variant="secondary" className="ml-2 bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400">
              Admin
            </Badge>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => {
              setCurrentView(item.id as AdminView);
              if (mobile) setSidebarOpen(false);
            }}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-colors ${
              item.active
                ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
            }`}
          >
            <item.icon className="w-5 h-5" />
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      {/* Help & Support */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700">
        <Button variant="ghost" className="w-full justify-start text-gray-600 dark:text-gray-300">
          <HelpCircle className="w-5 h-5 mr-3" />
          Help & Support
        </Button>
      </div>
    </div>
  );

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Desktop Sidebar */}
      <div className="hidden lg:flex lg:w-64 bg-white dark:bg-gray-800 shadow-sm">
        <Sidebar />
      </div>

      {/* Mobile Sidebar */}
      <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
        <SheetContent side="left" className="w-64 p-0">
          <Sidebar mobile />
        </SheetContent>
      </Sheet>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Navigation */}
        <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
          <div className="px-6 py-4 flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Sheet>
                <SheetTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="lg:hidden"
                    onClick={() => setSidebarOpen(true)}
                  >
                    <Menu className="w-5 h-5" />
                  </Button>
                </SheetTrigger>
              </Sheet>
              
              <div>
                <div className="flex items-center space-x-2">
                  <h1 className="text-xl text-gray-900 dark:text-white">
                    {menuItems.find(item => item.id === currentView)?.label || 'Dashboard'}
                  </h1>
                  <Shield className="w-5 h-5 text-red-500" />
                </div>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Admin Panel - {user.name}
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* System Status */}
              <div className="hidden md:flex items-center space-x-2 px-3 py-1 bg-green-100 dark:bg-green-900/20 rounded-full">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-green-700 dark:text-green-400">System Online</span>
              </div>

              {/* Notifications */}
              <Button variant="ghost" size="icon" className="relative">
                <Bell className="w-5 h-5" />
                <Badge className="absolute -top-2 -right-2 w-5 h-5 p-0 flex items-center justify-center bg-red-500 text-white text-xs">
                  5
                </Badge>
              </Button>

              {/* Profile Dropdown */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="flex items-center space-x-2 p-2">
                    <Avatar className="w-8 h-8">
                      <AvatarImage src={user.avatar} alt={user.name} />
                      <AvatarFallback>{user.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                    </Avatar>
                    <ChevronDown className="w-4 h-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-56">
                  <div className="p-2">
                    <div className="text-sm">{user.name}</div>
                    <div className="text-xs text-gray-500">{user.email}</div>
                    <Badge variant="secondary" className="mt-1 bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400">
                      Administrator
                    </Badge>
                  </div>
                  <Separator />
                  <DropdownMenuItem>
                    Admin Settings
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={toggleTheme}>
                    {theme === 'light' ? 'Dark Mode' : 'Light Mode'}
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    System Preferences
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    Help & Support
                  </DropdownMenuItem>
                  <Separator />
                  <DropdownMenuItem onClick={onLogout} className="text-red-600 dark:text-red-400">
                    <LogOut className="w-4 h-4 mr-2" />
                    Logout
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 overflow-auto">
          <motion.div
            key={currentView}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="p-6"
          >
            {renderContent()}
          </motion.div>
        </main>
      </div>
    </div>
  );
};

export default AdminDashboard;