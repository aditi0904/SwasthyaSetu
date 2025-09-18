import React, { useState } from 'react';
import { motion } from 'motion/react';
import { 
  Users, 
  Search, 
  Filter, 
  Plus, 
  Edit,
  Trash2,
  Eye,
  MoreHorizontal,
  UserCheck,
  UserX,
  Shield
} from 'lucide-react';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Badge } from '../../ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '../../ui/avatar';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../ui/table';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '../../ui/dropdown-menu';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../../ui/dialog';
import { Label } from '../../ui/label';
import { toast } from 'sonner@2.0.3';

const UserManagement: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedUser, setSelectedUser] = useState<any>(null);
  const [isAddUserOpen, setIsAddUserOpen] = useState(false);

  // Mock user data
  const users = [
    {
      id: '1',
      name: 'Dr. Rajesh Sharma',
      email: 'rajesh.sharma@hospital.com',
      type: 'doctor',
      status: 'active',
      lastLogin: '2024-01-15 10:30 AM',
      createdAt: '2023-08-15',
      avatar: './man.png',
      department: 'Cardiology',
      licenseNumber: 'MED123456'
    },
    {
      id: '2',
      name: 'Priya Patel',
      email: 'priya.patel@gmail.com',
      type: 'patient',
      status: 'active',
      lastLogin: '2024-01-14 2:15 PM',
      createdAt: '2023-11-20',
      avatar: './woman.png',
      phone: '+91 98765 43210',
      age: 32
    },
    {
      id: '3',
      name: 'Admin Kumar',
      email: 'admin@swasthyasetu.com',
      type: 'admin',
      status: 'active',
      lastLogin: '2024-01-15 9:00 AM',
      createdAt: '2023-01-01',
      avatar: './man.png',
      role: 'Super Admin',
      permissions: ['all']
    },
    {
      id: '4',
      name: 'Dr. Meera Singh',
      email: 'meera.singh@clinic.com',
      type: 'doctor',
      status: 'inactive',
      lastLogin: '2024-01-10 4:45 PM',
      createdAt: '2023-05-10',
      avatar: './woman.png',
      department: 'Pediatrics',
      licenseNumber: 'MED789012'
    },
    {
      id: '5',
      name: 'Amit Verma',
      email: 'amit.verma@yahoo.com',
      type: 'patient',
      status: 'suspended',
      lastLogin: '2024-01-05 11:20 AM',
      createdAt: '2023-12-01',
      avatar: './man.png',
      phone: '+91 87654 32109',
      age: 28
    }
  ];

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = filterType === 'all' || user.type === filterType;
    const matchesStatus = filterStatus === 'all' || user.status === filterStatus;
    return matchesSearch && matchesType && matchesStatus;
  });

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      case 'inactive': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400';
      case 'suspended': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
    }
  };

  const getTypeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case 'doctor': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400';
      case 'patient': return 'bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-400';
      case 'admin': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
    }
  };

  const handleUserAction = (action: string, user: any) => {
    switch (action) {
      case 'activate':
        toast.success(`${user.name} has been activated`);
        break;
      case 'deactivate':
        toast.success(`${user.name} has been deactivated`);
        break;
      case 'suspend':
        toast.success(`${user.name} has been suspended`);
        break;
      case 'delete':
        toast.success(`${user.name} has been deleted`);
        break;
      default:
        break;
    }
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
          <h1 className="text-3xl">User Management</h1>
          <p className="text-gray-600 dark:text-gray-400">Manage doctors, patients, and administrators</p>
        </div>
        <Dialog open={isAddUserOpen} onOpenChange={setIsAddUserOpen}>
          <DialogTrigger asChild>
            <Button className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white">
              <Plus className="w-4 h-4 mr-2" />
              Add User
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>Add New User</DialogTitle>
            </DialogHeader>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label>User Type</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select user type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="doctor">Doctor</SelectItem>
                    <SelectItem value="patient">Patient</SelectItem>
                    <SelectItem value="admin">Administrator</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>Name</Label>
                <Input placeholder="Full name" />
              </div>
              <div className="space-y-2">
                <Label>Email</Label>
                <Input type="email" placeholder="Email address" />
              </div>
              <div className="flex justify-end space-x-2">
                <Button variant="outline" onClick={() => setIsAddUserOpen(false)}>
                  Cancel
                </Button>
                <Button>Create User</Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <Users className="w-5 h-5 text-blue-500" />
              <div>
                <p className="text-2xl">12,847</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Users</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <UserCheck className="w-5 h-5 text-green-500" />
              <div>
                <p className="text-2xl">2,847</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Doctors</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <Users className="w-5 h-5 text-purple-500" />
              <div>
                <p className="text-2xl">9,234</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Patients</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <Shield className="w-5 h-5 text-red-500" />
              <div>
                <p className="text-2xl">766</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Admins</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle>User Directory</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
              <Input
                placeholder="Search users..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={filterType} onValueChange={setFilterType}>
              <SelectTrigger className="w-full md:w-48">
                <SelectValue placeholder="Filter by type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                <SelectItem value="doctor">Doctors</SelectItem>
                <SelectItem value="patient">Patients</SelectItem>
                <SelectItem value="admin">Administrators</SelectItem>
              </SelectContent>
            </Select>
            <Select value={filterStatus} onValueChange={setFilterStatus}>
              <SelectTrigger className="w-full md:w-48">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="inactive">Inactive</SelectItem>
                <SelectItem value="suspended">Suspended</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Users Table */}
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>User</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Last Login</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead className="w-12">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredUsers.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell>
                      <div className="flex items-center space-x-3">
                        <Avatar className="w-10 h-10">
                          <AvatarImage src={user.avatar} alt={user.name} />
                          <AvatarFallback>{user.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="text-sm">{user.name}</p>
                          <p className="text-xs text-gray-500">{user.email}</p>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge className={getTypeColor(user.type)} variant="secondary">
                        {user.type}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(user.status)} variant="secondary">
                        {user.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm">{user.lastLogin}</TableCell>
                    <TableCell className="text-sm">{user.createdAt}</TableCell>
                    <TableCell>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="sm">
                            <MoreHorizontal className="w-4 h-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem onClick={() => setSelectedUser(user)}>
                            <Eye className="w-4 h-4 mr-2" />
                            View Details
                          </DropdownMenuItem>
                          <DropdownMenuItem>
                            <Edit className="w-4 h-4 mr-2" />
                            Edit User
                          </DropdownMenuItem>
                          {user.status === 'active' ? (
                            <DropdownMenuItem onClick={() => handleUserAction('deactivate', user)}>
                              <UserX className="w-4 h-4 mr-2" />
                              Deactivate
                            </DropdownMenuItem>
                          ) : (
                            <DropdownMenuItem onClick={() => handleUserAction('activate', user)}>
                              <UserCheck className="w-4 h-4 mr-2" />
                              Activate
                            </DropdownMenuItem>
                          )}
                          <DropdownMenuItem 
                            onClick={() => handleUserAction('suspend', user)}
                            className="text-orange-600"
                          >
                            <UserX className="w-4 h-4 mr-2" />
                            Suspend
                          </DropdownMenuItem>
                          <DropdownMenuItem 
                            onClick={() => handleUserAction('delete', user)}
                            className="text-red-600"
                          >
                            <Trash2 className="w-4 h-4 mr-2" />
                            Delete
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {/* User Details Dialog */}
      <Dialog open={!!selectedUser} onOpenChange={() => setSelectedUser(null)}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>User Details</DialogTitle>
          </DialogHeader>
          {selectedUser && (
            <div className="space-y-6">
              <div className="flex items-center space-x-4">
                <Avatar className="w-16 h-16">
                  <AvatarImage src={selectedUser.avatar} alt={selectedUser.name} />
                  <AvatarFallback>{selectedUser.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                </Avatar>
                <div>
                  <h3 className="text-xl">{selectedUser.name}</h3>
                  <p className="text-gray-600 dark:text-gray-400">{selectedUser.email}</p>
                  <div className="flex space-x-2 mt-2">
                    <Badge className={getTypeColor(selectedUser.type)} variant="secondary">
                      {selectedUser.type}
                    </Badge>
                    <Badge className={getStatusColor(selectedUser.status)} variant="secondary">
                      {selectedUser.status}
                    </Badge>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <Label>User ID</Label>
                  <p>{selectedUser.id}</p>
                </div>
                <div>
                  <Label>Account Created</Label>
                  <p>{selectedUser.createdAt}</p>
                </div>
                <div>
                  <Label>Last Login</Label>
                  <p>{selectedUser.lastLogin}</p>
                </div>
                {selectedUser.type === 'doctor' && (
                  <>
                    <div>
                      <Label>Department</Label>
                      <p>{selectedUser.department}</p>
                    </div>
                    <div>
                      <Label>License Number</Label>
                      <p>{selectedUser.licenseNumber}</p>
                    </div>
                  </>
                )}
                {selectedUser.type === 'patient' && (
                  <>
                    <div>
                      <Label>Phone</Label>
                      <p>{selectedUser.phone}</p>
                    </div>
                    <div>
                      <Label>Age</Label>
                      <p>{selectedUser.age}</p>
                    </div>
                  </>
                )}
                {selectedUser.type === 'admin' && (
                  <>
                    <div>
                      <Label>Role</Label>
                      <p>{selectedUser.role}</p>
                    </div>
                    <div>
                      <Label>Permissions</Label>
                      <p>{selectedUser.permissions.join(', ')}</p>
                    </div>
                  </>
                )}
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </motion.div>
  );
};

export default UserManagement;