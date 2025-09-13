import React, { useState } from 'react';
import { motion } from 'motion/react';
import { 
  FileText, 
  Search, 
  Filter, 
  Download, 
  Eye,
  Calendar,
  User,
  Shield,
  AlertTriangle,
  CheckCircle,
  Clock,
  Activity
} from 'lucide-react';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Badge } from '../../ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../ui/table';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../../ui/dialog';
import { Label } from '../../ui/label';
import { Avatar, AvatarFallback, AvatarImage } from '../../ui/avatar';

const AuditLogs: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterAction, setFilterAction] = useState('all');
  const [filterUser, setFilterUser] = useState('all');
  const [filterDate, setFilterDate] = useState('all');
  const [selectedLog, setSelectedLog] = useState<any>(null);

  // Mock audit log data
  const auditLogs = [
    {
      id: 'LOG001',
      timestamp: '2024-01-15 10:35:22',
      user: {
        id: 'USR001',
        name: 'Dr. Rajesh Sharma',
        email: 'rajesh.sharma@hospital.com',
        type: 'doctor',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=rajesh'
      },
      action: 'patient_data_access',
      resource: 'Patient Record - Priya Patel (ID: PAT123)',
      details: 'Accessed patient medical history for consultation',
      ipAddress: '192.168.1.45',
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      status: 'success',
      severity: 'info'
    },
    {
      id: 'LOG002',
      timestamp: '2024-01-15 10:32:15',
      user: {
        id: 'USR002',
        name: 'Admin Kumar',
        email: 'admin@swasthyasetu.com',
        type: 'admin',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=admin'
      },
      action: 'user_management',
      resource: 'User Account - Dr. Meera Singh',
      details: 'Deactivated user account due to license expiry',
      ipAddress: '10.0.0.5',
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
      status: 'success',
      severity: 'warning'
    },
    {
      id: 'LOG003',
      timestamp: '2024-01-15 10:28:43',
      user: {
        id: 'USR003',
        name: 'System',
        email: 'system@swasthyasetu.com',
        type: 'system',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=system'
      },
      action: 'data_backup',
      resource: 'Patient Database',
      details: 'Automated daily backup completed successfully',
      ipAddress: 'localhost',
      userAgent: 'System Process',
      status: 'success',
      severity: 'info'
    },
    {
      id: 'LOG004',
      timestamp: '2024-01-15 10:25:18',
      user: {
        id: 'USR004',
        name: 'Unauthorized User',
        email: 'unknown@example.com',
        type: 'unknown',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=unknown'
      },
      action: 'failed_login',
      resource: 'Admin Panel',
      details: 'Failed login attempt with invalid credentials',
      ipAddress: '203.198.45.12',
      userAgent: 'curl/7.68.0',
      status: 'failed',
      severity: 'critical'
    },
    {
      id: 'LOG005',
      timestamp: '2024-01-15 10:20:05',
      user: {
        id: 'USR005',
        name: 'Priya Patel',
        email: 'priya.patel@gmail.com',
        type: 'patient',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=priya'
      },
      action: 'insurance_claim',
      resource: 'Insurance Claim - CLM001',
      details: 'Submitted new insurance claim for hospitalization',
      ipAddress: '192.168.1.87',
      userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)',
      status: 'success',
      severity: 'info'
    },
    {
      id: 'LOG006',
      timestamp: '2024-01-15 10:15:33',
      user: {
        id: 'USR006',
        name: 'Dr. Amit Verma',
        email: 'amit.verma@clinic.com',
        type: 'doctor',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=amit'
      },
      action: 'diagnosis_entry',
      resource: 'Diagnosis Record - DGN456',
      details: 'Created new diagnosis entry for patient consultation',
      ipAddress: '192.168.1.23',
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      status: 'success',
      severity: 'info'
    },
    {
      id: 'LOG007',
      timestamp: '2024-01-15 10:10:12',
      user: {
        id: 'USR007',
        name: 'System',
        email: 'system@swasthyasetu.com',
        type: 'system',
        avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=system'
      },
      action: 'api_sync_error',
      resource: 'NAMASTE Mapping Service',
      details: 'API synchronization failed - connection timeout',
      ipAddress: 'localhost',
      userAgent: 'System Process',
      status: 'failed',
      severity: 'error'
    }
  ];

  const filteredLogs = auditLogs.filter(log => {
    const matchesSearch = log.user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         log.action.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         log.resource.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         log.details.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesAction = filterAction === 'all' || log.action.includes(filterAction);
    const matchesUser = filterUser === 'all' || log.user.type === filterUser;
    
    return matchesSearch && matchesAction && matchesUser;
  });

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      case 'error': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      case 'warning': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400';
      case 'info': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical': return <AlertTriangle className="w-4 h-4" />;
      case 'error': return <AlertTriangle className="w-4 h-4" />;
      case 'warning': return <AlertTriangle className="w-4 h-4" />;
      case 'info': return <CheckCircle className="w-4 h-4" />;
      default: return <Clock className="w-4 h-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'success': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      case 'failed': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
    }
  };

  const getUserTypeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case 'doctor': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400';
      case 'patient': return 'bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-400';
      case 'admin': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      case 'system': return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
    }
  };

  const exportLogs = () => {
    const csvContent = [
      ['Timestamp', 'User', 'Action', 'Resource', 'Status', 'Severity', 'IP Address'],
      ...filteredLogs.map(log => [
        log.timestamp,
        log.user.name,
        log.action,
        log.resource,
        log.status,
        log.severity,
        log.ipAddress
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `audit-logs-${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const stats = {
    totalLogs: auditLogs.length,
    criticalEvents: auditLogs.filter(log => log.severity === 'critical').length,
    failedActions: auditLogs.filter(log => log.status === 'failed').length,
    userActions: auditLogs.filter(log => log.user.type !== 'system').length
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl">Audit Logs</h1>
          <p className="text-gray-600 dark:text-gray-400">Monitor system activities and security events</p>
        </div>
        <Button onClick={exportLogs} className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white">
          <Download className="w-4 h-4 mr-2" />
          Export Logs
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <FileText className="w-5 h-5 text-blue-500" />
              <div>
                <p className="text-2xl">{stats.totalLogs}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Events</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-red-500" />
              <div>
                <p className="text-2xl">{stats.criticalEvents}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Critical Events</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <Shield className="w-5 h-5 text-orange-500" />
              <div>
                <p className="text-2xl">{stats.failedActions}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Failed Actions</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <User className="w-5 h-5 text-purple-500" />
              <div>
                <p className="text-2xl">{stats.userActions}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">User Actions</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters and Search */}
      <Card>
        <CardHeader>
          <CardTitle>Audit Log Viewer</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
              <Input
                placeholder="Search logs..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={filterAction} onValueChange={setFilterAction}>
              <SelectTrigger className="w-full md:w-48">
                <SelectValue placeholder="Filter by action" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Actions</SelectItem>
                <SelectItem value="login">Login/Logout</SelectItem>
                <SelectItem value="patient_data">Patient Data</SelectItem>
                <SelectItem value="user_management">User Management</SelectItem>
                <SelectItem value="system">System Events</SelectItem>
                <SelectItem value="api">API Actions</SelectItem>
              </SelectContent>
            </Select>
            <Select value={filterUser} onValueChange={setFilterUser}>
              <SelectTrigger className="w-full md:w-48">
                <SelectValue placeholder="Filter by user type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Users</SelectItem>
                <SelectItem value="doctor">Doctors</SelectItem>
                <SelectItem value="patient">Patients</SelectItem>
                <SelectItem value="admin">Administrators</SelectItem>
                <SelectItem value="system">System</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Audit Logs Table */}
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Timestamp</TableHead>
                  <TableHead>User</TableHead>
                  <TableHead>Action</TableHead>
                  <TableHead>Resource</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Severity</TableHead>
                  <TableHead className="w-12">Details</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredLogs.map((log) => (
                  <TableRow key={log.id}>
                    <TableCell className="text-sm">{log.timestamp}</TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <Avatar className="w-6 h-6">
                          <AvatarImage src={log.user.avatar} alt={log.user.name} />
                          <AvatarFallback className="text-xs">
                            {log.user.name.split(' ').map(n => n[0]).join('')}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="text-sm">{log.user.name}</p>
                          <Badge className={getUserTypeColor(log.user.type)} variant="secondary">
                            {log.user.type}
                          </Badge>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell className="text-sm">{log.action.replace(/_/g, ' ')}</TableCell>
                    <TableCell className="text-sm max-w-xs truncate" title={log.resource}>
                      {log.resource}
                    </TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(log.status)} variant="secondary">
                        {log.status}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Badge className={getSeverityColor(log.severity)} variant="secondary">
                        {getSeverityIcon(log.severity)}
                        <span className="ml-1 capitalize">{log.severity}</span>
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Dialog>
                        <DialogTrigger asChild>
                          <Button 
                            variant="ghost" 
                            size="sm"
                            onClick={() => setSelectedLog(log)}
                          >
                            <Eye className="w-4 h-4" />
                          </Button>
                        </DialogTrigger>
                      </Dialog>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {/* Log Details Dialog */}
      <Dialog open={!!selectedLog} onOpenChange={() => setSelectedLog(null)}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>Audit Log Details - {selectedLog?.id}</DialogTitle>
          </DialogHeader>
          {selectedLog && (
            <div className="space-y-6">
              {/* Log Summary */}
              <div className="flex items-start space-x-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <Avatar className="w-12 h-12">
                  <AvatarImage src={selectedLog.user.avatar} alt={selectedLog.user.name} />
                  <AvatarFallback>
                    {selectedLog.user.name.split(' ').map(n => n[0]).join('')}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-1">
                    <h3 className="text-lg">{selectedLog.user.name}</h3>
                    <Badge className={getUserTypeColor(selectedLog.user.type)} variant="secondary">
                      {selectedLog.user.type}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">{selectedLog.user.email}</p>
                  <p className="text-sm mt-2">{selectedLog.details}</p>
                </div>
                <div className="flex flex-col space-y-2">
                  <Badge className={getStatusColor(selectedLog.status)} variant="secondary">
                    {selectedLog.status}
                  </Badge>
                  <Badge className={getSeverityColor(selectedLog.severity)} variant="secondary">
                    {getSeverityIcon(selectedLog.severity)}
                    <span className="ml-1">{selectedLog.severity}</span>
                  </Badge>
                </div>
              </div>

              {/* Detailed Information */}
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <Label className="text-sm">Log ID</Label>
                    <p>{selectedLog.id}</p>
                  </div>
                  <div>
                    <Label className="text-sm">Timestamp</Label>
                    <p>{selectedLog.timestamp}</p>
                  </div>
                  <div>
                    <Label className="text-sm">Action</Label>
                    <p className="capitalize">{selectedLog.action.replace(/_/g, ' ')}</p>
                  </div>
                  <div>
                    <Label className="text-sm">Resource</Label>
                    <p>{selectedLog.resource}</p>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <Label className="text-sm">IP Address</Label>
                    <p>{selectedLog.ipAddress}</p>
                  </div>
                  <div>
                    <Label className="text-sm">User Agent</Label>
                    <p className="text-sm break-all">{selectedLog.userAgent}</p>
                  </div>
                  <div>
                    <Label className="text-sm">Status</Label>
                    <Badge className={getStatusColor(selectedLog.status)} variant="secondary">
                      {selectedLog.status}
                    </Badge>
                  </div>
                  <div>
                    <Label className="text-sm">Severity</Label>
                    <Badge className={getSeverityColor(selectedLog.severity)} variant="secondary">
                      {selectedLog.severity}
                    </Badge>
                  </div>
                </div>
              </div>

              {/* Full Details */}
              <div>
                <Label className="text-sm">Full Details</Label>
                <div className="mt-2 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <p className="text-sm">{selectedLog.details}</p>
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </motion.div>
  );
};

export default AuditLogs;