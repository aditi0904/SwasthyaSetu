import React from 'react';
import { motion } from 'motion/react';
import { 
  Users, 
  Activity, 
  Database, 
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  Server,
  Shield,
  Heart,
  FileText,
  RefreshCw
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Progress } from '../../ui/progress';
import { Badge } from '../../ui/badge';
import { Button } from '../../ui/button';
import { ImageWithFallback } from '../../figma/ImageWithFallback';
import type { User } from '../../../App';

interface AdminDashboardHomeProps {
  user: User;
}

const AdminDashboardHome: React.FC<AdminDashboardHomeProps> = ({ user }) => {
  // Mock system stats
  const systemStats = [
    { 
      title: 'Total Users', 
      value: '12,847', 
      change: '+5.2%', 
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
      breakdown: { doctors: 2847, patients: 9234, admins: 766 }
    },
    { 
      title: 'System Health', 
      value: '98.7%', 
      change: '+0.3%', 
      icon: Activity,
      color: 'text-green-600',
      bgColor: 'bg-green-50 dark:bg-green-900/20',
      breakdown: { uptime: 98.7, performance: 96.2, errors: 0.8 }
    },
    { 
      title: 'Data Sync Status', 
      value: '99.2%', 
      change: '+1.1%', 
      icon: Database,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50 dark:bg-purple-900/20',
      breakdown: { synced: 99.2, pending: 0.5, failed: 0.3 }
    },
    { 
      title: 'Daily Transactions', 
      value: '8,342', 
      change: '+12.4%', 
      icon: TrendingUp,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50 dark:bg-orange-900/20',
      breakdown: { diagnoses: 3421, records: 2987, claims: 1934 }
    },
  ];

  // Mock recent activities
  const recentActivities = [
    {
      id: '1',
      type: 'user_registration',
      message: 'New doctor registered: Dr. Rajesh Sharma',
      timestamp: '2 minutes ago',
      severity: 'info'
    },
    {
      id: '2',
      type: 'system_alert',
      message: 'High server load detected on DB-02',
      timestamp: '15 minutes ago',
      severity: 'warning'
    },
    {
      id: '3',
      type: 'sync_success',
      message: 'NAMASTE-ICD mapping sync completed successfully',
      timestamp: '1 hour ago',
      severity: 'success'
    },
    {
      id: '4',
      type: 'security',
      message: 'Failed login attempt detected from unknown IP',
      timestamp: '2 hours ago',
      severity: 'error'
    },
    {
      id: '5',
      type: 'maintenance',
      message: 'Scheduled backup completed for patient database',
      timestamp: '3 hours ago',
      severity: 'success'
    }
  ];

  // Mock system services
  const systemServices = [
    { name: 'Authentication Service', status: 'online', uptime: 99.8, lastCheck: '1 min ago' },
    { name: 'Patient Data API', status: 'online', uptime: 98.9, lastCheck: '2 min ago' },
    { name: 'NAMASTE Mapping Service', status: 'warning', uptime: 95.2, lastCheck: '5 min ago' },
    { name: 'Insurance Integration', status: 'online', uptime: 97.6, lastCheck: '3 min ago' },
    { name: 'Notification Service', status: 'maintenance', uptime: 0, lastCheck: '30 min ago' },
    { name: 'Backup Service', status: 'online', uptime: 99.9, lastCheck: '1 min ago' }
  ];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'success': return 'text-green-600 bg-green-50 dark:bg-green-900/20';
      case 'warning': return 'text-yellow-600 bg-yellow-50 dark:bg-yellow-900/20';
      case 'error': return 'text-red-600 bg-red-50 dark:bg-red-900/20';
      default: return 'text-blue-600 bg-blue-50 dark:bg-blue-900/20';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'success': return <CheckCircle className="w-4 h-4" />;
      case 'warning': return <AlertTriangle className="w-4 h-4" />;
      case 'error': return <AlertTriangle className="w-4 h-4" />;
      default: return <Clock className="w-4 h-4" />;
    }
  };

  const getServiceStatusColor = (status: string) => {
    switch (status) {
      case 'online': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      case 'warning': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400';
      case 'maintenance': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400';
      case 'offline': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
    }
  };

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-indigo-600 via-purple-600 to-cyan-500 p-8 text-white"
      >
        <div className="relative z-10">
          <h1 className="text-3xl mb-2">Good morning, {user.name}!</h1>
          <p className="text-indigo-100 text-lg mb-6">
            System is running smoothly. Here's your administrative overview.
          </p>
          <div className="flex items-center space-x-4">
            <Button variant="secondary" className="bg-white/20 text-white hover:bg-white/30">
              <Shield className="w-4 h-4 mr-2" />
              System Status
            </Button>
            <Button variant="ghost" className="text-white hover:bg-white/10">
              <FileText className="w-4 h-4 mr-2" />
              Generate Report
            </Button>
          </div>
        </div>
        
        {/* Background decoration */}
        <div className="absolute right-0 top-0 opacity-20">
          <ImageWithFallback
            src="https://images.unsplash.com/photo-1698306642516-9841228dcff3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHxtZWRpY2FsJTIwZGFzaGJvYXJkJTIwYW5hbHl0aWNzfGVufDF8fHx8MTc1Nzc1MjgzMXww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
            alt="Medical dashboard analytics"
            className="h-48 w-64 object-cover"
          />
        </div>
      </motion.div>

      {/* System Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {systemStats.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm">{stat.title}</CardTitle>
                <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                  <stat.icon className={`w-4 h-4 ${stat.color}`} />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl mb-2">{stat.value}</div>
                <p className="text-xs text-muted-foreground mb-3">
                  <span className={stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}>
                    {stat.change}
                  </span>
                  {' '}from last month
                </p>
                <div className="space-y-1">
                  {Object.entries(stat.breakdown).map(([key, value]) => (
                    <div key={key} className="flex justify-between text-xs">
                      <span className="capitalize text-gray-600 dark:text-gray-400">{key}:</span>
                      <span>{typeof value === 'number' ? `${value}%` : value}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* System Services */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="lg:col-span-2"
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span className="flex items-center space-x-2">
                  <Server className="w-5 h-5" />
                  <span>System Services</span>
                </span>
                <Button variant="outline" size="sm">
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Refresh
                </Button>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {systemServices.map((service) => (
                  <div key={service.name} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="text-sm">{service.name}</h4>
                        <Badge className={getServiceStatusColor(service.status)} variant="secondary">
                          {service.status}
                        </Badge>
                      </div>
                      <div className="flex items-center justify-between text-xs text-gray-500">
                        <span>Uptime: {service.uptime}%</span>
                        <span>Last check: {service.lastCheck}</span>
                      </div>
                      <Progress value={service.uptime} className="h-1 mt-2" />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Recent Activities */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Activity className="w-5 h-5" />
                <span>Recent Activities</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentActivities.map((activity) => (
                  <div key={activity.id} className="flex items-start space-x-3">
                    <div className={`p-1 rounded-full ${getSeverityColor(activity.severity)}`}>
                      {getSeverityIcon(activity.severity)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm">{activity.message}</p>
                      <p className="text-xs text-gray-500 mt-1">{activity.timestamp}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Button variant="outline" className="h-20 flex flex-col items-center justify-center space-y-2">
                <Users className="w-6 h-6" />
                <span className="text-xs">Manage Users</span>
              </Button>
              <Button variant="outline" className="h-20 flex flex-col items-center justify-center space-y-2">
                <Database className="w-6 h-6" />
                <span className="text-xs">Sync Data</span>
              </Button>
              <Button variant="outline" className="h-20 flex flex-col items-center justify-center space-y-2">
                <FileText className="w-6 h-6" />
                <span className="text-xs">View Logs</span>
              </Button>
              <Button variant="outline" className="h-20 flex flex-col items-center justify-center space-y-2">
                <Shield className="w-6 h-6" />
                <span className="text-xs">Security</span>
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* System Health Overview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Heart className="w-5 h-5 text-red-500" />
              <span>System Health Overview</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="space-y-3">
                <h4 className="text-sm text-gray-600 dark:text-gray-400">Performance Metrics</h4>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>CPU Usage</span>
                    <span>45%</span>
                  </div>
                  <Progress value={45} className="h-2" />
                  <div className="flex justify-between text-sm">
                    <span>Memory Usage</span>
                    <span>67%</span>
                  </div>
                  <Progress value={67} className="h-2" />
                  <div className="flex justify-between text-sm">
                    <span>Disk Usage</span>
                    <span>34%</span>
                  </div>
                  <Progress value={34} className="h-2" />
                </div>
              </div>

              <div className="space-y-3">
                <h4 className="text-sm text-gray-600 dark:text-gray-400">Network Status</h4>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>API Response Time</span>
                    <span>125ms</span>
                  </div>
                  <Progress value={85} className="h-2" />
                  <div className="flex justify-between text-sm">
                    <span>Database Queries</span>
                    <span>2,341/min</span>
                  </div>
                  <Progress value={72} className="h-2" />
                  <div className="flex justify-between text-sm">
                    <span>Active Connections</span>
                    <span>847</span>
                  </div>
                  <Progress value={58} className="h-2" />
                </div>
              </div>

              <div className="space-y-3">
                <h4 className="text-sm text-gray-600 dark:text-gray-400">Security Status</h4>
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span className="text-sm">SSL Certificates Valid</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span className="text-sm">Firewall Active</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <AlertTriangle className="w-4 h-4 text-orange-500" />
                    <span className="text-sm">2 Security Warnings</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-500" />
                    <span className="text-sm">Backup Status: OK</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default AdminDashboardHome;