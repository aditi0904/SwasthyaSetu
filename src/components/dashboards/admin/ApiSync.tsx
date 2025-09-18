import React, { useState } from 'react';
import { motion } from 'motion/react';
import { 
  Database, 
  RefreshCw, 
  CheckCircle, 
  XCircle, 
  Clock,
  AlertTriangle,
  Play,
  Pause,
  Settings,
  Activity,
  TrendingUp,
  Download
} from 'lucide-react';
import { Button } from '../../ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Badge } from '../../ui/badge';
import { Progress } from '../../ui/progress';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../ui/table';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../../ui/dialog';
import { Label } from '../../ui/label';
import { Input } from '../../ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../ui/select';
import { Switch } from '../../ui/switch';
import { toast } from 'sonner';

const ApiSync: React.FC = () => {
  const [isRunningSync, setIsRunningSync] = useState(false);
  const [selectedService, setSelectedService] = useState<any>(null);

  // Mock API sync services
  const syncServices = [
    {
      id: 'namaste-icd',
      name: 'NAMASTE ↔ ICD-11 Mapping',
      description: 'Synchronize medical terminology mappings',
      status: 'online',
      lastSync: '2024-01-15 10:30 AM',
      nextSync: '2024-01-15 11:00 AM',
      frequency: 'Every 30 minutes',
      recordsProcessed: 2847,
      successRate: 98.2,
      errors: 3,
      endpoint: 'https://api.namaste.gov.in/mappings',
      autoSync: true
    },
    {
      id: 'insurance-provider',
      name: 'Insurance Provider Integration',
      description: 'Sync with insurance company APIs for claims',
      status: 'warning',
      lastSync: '2024-01-15 9:45 AM',
      nextSync: '2024-01-15 12:00 PM',
      frequency: 'Every 2 hours',
      recordsProcessed: 1234,
      successRate: 95.7,
      errors: 12,
      endpoint: 'https://api.starhealth.com/claims',
      autoSync: true
    },
    {
      id: 'patient-registry',
      name: 'National Patient Registry',
      description: 'Sync patient data with national health registry',
      status: 'offline',
      lastSync: '2024-01-14 6:00 PM',
      nextSync: 'Manual sync required',
      frequency: 'Daily at 6:00 PM',
      recordsProcessed: 0,
      successRate: 0,
      errors: 1,
      endpoint: 'https://api.nhr.gov.in/patients',
      autoSync: false
    },
    {
      id: 'lab-results',
      name: 'Laboratory Results API',
      description: 'Fetch lab results from partner laboratories',
      status: 'online',
      lastSync: '2024-01-15 10:15 AM',
      nextSync: '2024-01-15 10:45 AM',
      frequency: 'Every 15 minutes',
      recordsProcessed: 456,
      successRate: 99.1,
      errors: 0,
      endpoint: 'https://api.pathlab.com/results',
      autoSync: true
    },
    {
      id: 'pharmacy-inventory',
      name: 'Pharmacy Inventory Sync',
      description: 'Update medicine availability and pricing',
      status: 'online',
      lastSync: '2024-01-15 10:00 AM',
      nextSync: '2024-01-15 11:00 AM',
      frequency: 'Every hour',
      recordsProcessed: 3421,
      successRate: 97.8,
      errors: 5,
      endpoint: 'https://api.medplus.com/inventory',
      autoSync: true
    }
  ];

  // Mock sync logs
  const syncLogs = [
    {
      id: '1',
      service: 'NAMASTE ↔ ICD-11 Mapping',
      timestamp: '2024-01-15 10:30:15',
      status: 'success',
      duration: '2.3s',
      recordsProcessed: 234,
      message: 'Successfully processed 234 mapping records'
    },
    {
      id: '2',
      service: 'Insurance Provider Integration',
      timestamp: '2024-01-15 10:25:42',
      status: 'warning',
      duration: '15.7s',
      recordsProcessed: 89,
      message: '3 records failed validation - rate limiting detected'
    },
    {
      id: '3',
      service: 'Laboratory Results API',
      timestamp: '2024-01-15 10:15:08',
      status: 'success',
      duration: '1.1s',
      recordsProcessed: 12,
      message: 'Lab results updated successfully'
    },
    {
      id: '4',
      service: 'National Patient Registry',
      timestamp: '2024-01-14 18:00:00',
      status: 'error',
      duration: '45.2s',
      recordsProcessed: 0,
      message: 'Connection timeout - service unavailable'
    },
    {
      id: '5',
      service: 'Pharmacy Inventory Sync',
      timestamp: '2024-01-15 10:00:23',
      status: 'success',
      duration: '5.8s',
      recordsProcessed: 567,
      message: 'Inventory updated - 567 items processed'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'online': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      case 'warning': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400';
      case 'offline': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      case 'error': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      case 'success': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'online': return <CheckCircle className="w-4 h-4" />;
      case 'warning': return <AlertTriangle className="w-4 h-4" />;
      case 'offline': return <XCircle className="w-4 h-4" />;
      case 'error': return <XCircle className="w-4 h-4" />;
      case 'success': return <CheckCircle className="w-4 h-4" />;
      default: return <Clock className="w-4 h-4" />;
    }
  };

  const handleManualSync = async (serviceId: string) => {
    setIsRunningSync(true);
    toast.info('Starting manual sync...');
    
    // Simulate sync process
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    toast.success('Manual sync completed successfully!');
    setIsRunningSync(false);
  };

  const handleToggleAutoSync = (serviceId: string, enabled: boolean) => {
    const action = enabled ? 'enabled' : 'disabled';
    toast.success(`Auto-sync ${action} for ${serviceId}`);
  };

  const stats = {
    totalServices: syncServices.length,
    onlineServices: syncServices.filter(s => s.status === 'online').length,
    warningServices: syncServices.filter(s => s.status === 'warning').length,
    offlineServices: syncServices.filter(s => s.status === 'offline').length,
    totalRecords: syncServices.reduce((sum, s) => sum + s.recordsProcessed, 0),
    avgSuccessRate: syncServices.reduce((sum, s) => sum + s.successRate, 0) / syncServices.length
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
          <h1 className="text-3xl">API Sync Management</h1>
          <p className="text-gray-600 dark:text-gray-400">Monitor and manage external API synchronization</p>
        </div>
        <div className="flex space-x-2">
          <Button 
            variant="outline"
            onClick={() => handleManualSync('all')}
            disabled={isRunningSync}
          >
            {isRunningSync ? (
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <RefreshCw className="w-4 h-4 mr-2" />
            )}
            Sync All
          </Button>
          <Button className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white">
            <Download className="w-4 h-4 mr-2" />
            Export Logs
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <Database className="w-5 h-5 text-blue-500" />
              <div>
                <p className="text-2xl">{stats.totalServices}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Services</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <div>
                <p className="text-2xl">{stats.onlineServices}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Online</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-5 h-5 text-purple-500" />
              <div>
                <p className="text-2xl">{stats.totalRecords.toLocaleString()}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Records Synced</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <Activity className="w-5 h-5 text-orange-500" />
              <div>
                <p className="text-2xl">{stats.avgSuccessRate.toFixed(1)}%</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Avg Success Rate</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Sync Services */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Database className="w-5 h-5" />
            <span>Sync Services</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {syncServices.map((service) => (
              <div key={service.id} className="p-4 border rounded-lg">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-lg">{service.name}</h3>
                      <Badge className={getStatusColor(service.status)} variant="secondary">
                        {getStatusIcon(service.status)}
                        <span className="ml-1 capitalize">{service.status}</span>
                      </Badge>
                      <div className="flex items-center space-x-2">
                        <Label htmlFor={`auto-sync-${service.id}`} className="text-sm">Auto-sync</Label>
                        <Switch
                          id={`auto-sync-${service.id}`}
                          checked={service.autoSync}
                          onCheckedChange={(checked) => handleToggleAutoSync(service.name, checked)}
                        />
                      </div>
                    </div>
                    
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                      {service.description}
                    </p>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Last Sync</p>
                        <p>{service.lastSync}</p>
                      </div>
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Next Sync</p>
                        <p>{service.nextSync}</p>
                      </div>
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Frequency</p>
                        <p>{service.frequency}</p>
                      </div>
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Records Processed</p>
                        <p>{service.recordsProcessed.toLocaleString()}</p>
                      </div>
                    </div>
                    
                    <div className="mt-3 space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Success Rate</span>
                        <span className="text-green-600">{service.successRate}%</span>
                      </div>
                      <Progress value={service.successRate} className="h-2" />
                      
                      {service.errors > 0 && (
                        <p className="text-sm text-red-600 dark:text-red-400">
                          {service.errors} error{service.errors > 1 ? 's' : ''} in last sync
                        </p>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex space-x-2 ml-4">
                    <Dialog>
                      <DialogTrigger asChild>
                        <Button 
                          variant="ghost" 
                          size="sm"
                          onClick={() => setSelectedService(service)}
                        >
                          <Settings className="w-4 h-4" />
                        </Button>
                      </DialogTrigger>
                    </Dialog>
                    
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleManualSync(service.id)}
                      disabled={isRunningSync}
                      className="text-blue-600 hover:bg-blue-50"
                    >
                      {isRunningSync ? (
                        <RefreshCw className="w-4 h-4 animate-spin" />
                      ) : (
                        <Play className="w-4 h-4" />
                      )}
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Recent Sync Logs */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Activity className="w-5 h-5" />
            <span>Recent Sync Logs</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Service</TableHead>
                  <TableHead>Timestamp</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Duration</TableHead>
                  <TableHead>Records</TableHead>
                  <TableHead>Message</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {syncLogs.map((log) => (
                  <TableRow key={log.id}>
                    <TableCell className="text-sm">{log.service}</TableCell>
                    <TableCell className="text-sm">{log.timestamp}</TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(log.status)} variant="secondary">
                        {getStatusIcon(log.status)}
                        <span className="ml-1 capitalize">{log.status}</span>
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm">{log.duration}</TableCell>
                    <TableCell className="text-sm">{log.recordsProcessed}</TableCell>
                    <TableCell className="text-sm max-w-xs truncate" title={log.message}>
                      {log.message}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {/* Service Configuration Dialog */}
      <Dialog open={!!selectedService} onOpenChange={() => setSelectedService(null)}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Service Configuration - {selectedService?.name}</DialogTitle>
          </DialogHeader>
          {selectedService && (
            <div className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Service Name</Label>
                  <Input value={selectedService.name} disabled />
                </div>
                <div className="space-y-2">
                  <Label>Status</Label>
                  <Badge className={getStatusColor(selectedService.status)} variant="secondary">
                    {selectedService.status}
                  </Badge>
                </div>
              </div>
              
              <div className="space-y-2">
                <Label>API Endpoint</Label>
                <Input value={selectedService.endpoint} />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Sync Frequency</Label>
                  <Select defaultValue="30min">
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="5min">Every 5 minutes</SelectItem>
                      <SelectItem value="15min">Every 15 minutes</SelectItem>
                      <SelectItem value="30min">Every 30 minutes</SelectItem>
                      <SelectItem value="1hour">Every hour</SelectItem>
                      <SelectItem value="2hour">Every 2 hours</SelectItem>
                      <SelectItem value="daily">Daily</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label>Timeout (seconds)</Label>
                  <Input type="number" defaultValue="30" />
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Retry Attempts</Label>
                  <Input type="number" defaultValue="3" />
                </div>
                <div className="space-y-2">
                  <Label>Batch Size</Label>
                  <Input type="number" defaultValue="100" />
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <Switch 
                  id="auto-sync"
                  checked={selectedService.autoSync}
                />
                <Label htmlFor="auto-sync">Enable automatic synchronization</Label>
              </div>
              
              <div className="flex justify-end space-x-2">
                <Button variant="outline" onClick={() => setSelectedService(null)}>
                  Cancel
                </Button>
                <Button>Save Configuration</Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </motion.div>
  );
};

export default ApiSync;