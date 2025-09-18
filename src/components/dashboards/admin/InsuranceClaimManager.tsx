import React, { useState } from 'react';
import { motion } from 'motion/react';
import {
  Shield,
  FileText,
  Search,
  Filter,
  Plus,
  Eye,
  CheckCircle,
  XCircle,
  AlertTriangle,
  TrendingUp,
  Users,
  DollarSign,
  Calendar,
  Edit,
  Trash2,
  BarChart3,
  PieChart,
  Activity
} from 'lucide-react';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { Label } from '../../ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../ui/table';
import { Badge } from '../../ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../ui/tabs';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../../ui/dialog';
import { Textarea } from '../../ui/textarea';
import { ScrollArea } from '../../ui/scroll-area';
import { Progress } from '../../ui/progress';
import { Separator } from '../../ui/separator';
import { Avatar, AvatarFallback, AvatarImage } from '../../ui/avatar';
import { toast } from 'sonner@2.0.3';

interface ClaimRecord {
  id: string;
  patientName: string;
  patientAvatar: string;
  diagnosis: string;
  diagnosisCode: string;
  insuranceProvider: string;
  claimAmount: number;
  status: 'pending' | 'approved' | 'rejected' | 'flagged';
  submittedDate: string;
  reviewedDate?: string;
  reviewerNotes?: string;
  flaggedReason?: string;
  doctorName: string;
}

interface CoverageRule {
  id: string;
  diagnosisCode: string;
  diagnosisName: string;
  insuranceProvider: string;
  coverage: string;
  maxAmount: number;
  copayment: number;
  isActive: boolean;
  createdDate: string;
}

const InsuranceClaimManager: React.FC = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [dateFilter, setDateFilter] = useState('all');
  const [selectedClaim, setSelectedClaim] = useState<ClaimRecord | null>(null);
  const [showRuleDialog, setShowRuleDialog] = useState(false);
  const [newRule, setNewRule] = useState<Partial<CoverageRule>>({});

  // Mock Claims Data
  const claimsData: ClaimRecord[] = [
    {
      id: 'CLM-001',
      patientName: 'Rajesh Kumar',
      patientAvatar: 'https://images.unsplash.com/photo-1676552055618-22ec8cde399a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxoYXBweSUyMHBhdGllbnQlMjBoZWFsdGhjYXJlJTIwcG9ydHJhaXR8ZW58MXx8fHwxNzU4MjAzODE0fDA&ixlib=rb-4.1.0&q=80&w=1080',
      diagnosis: 'Essential (primary) hypertension',
      diagnosisCode: 'I10',
      insuranceProvider: 'Star Health',
      claimAmount: 15000,
      status: 'pending',
      submittedDate: '2024-01-15',
      doctorName: 'Dr. Priya Sharma'
    },
    {
      id: 'CLM-002',
      patientName: 'Priya Patel',
      patientAvatar: 'https://images.unsplash.com/photo-1676552055618-22ec8cde399a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxoYXBweSUyMHBhdGllbnQlMjBoZWFsdGhjYXJlJTIwcG9ydHJhaXR8ZW58MXx8fHwxNzU4MjAzODE0fDA&ixlib=rb-4.1.0&q=80&w=1080',
      diagnosis: 'Type 2 diabetes mellitus without complications',
      diagnosisCode: 'E11.9',
      insuranceProvider: 'HDFC ERGO',
      claimAmount: 25000,
      status: 'approved',
      submittedDate: '2024-01-12',
      reviewedDate: '2024-01-14',
      reviewerNotes: 'All documentation verified. Claim approved.',
      doctorName: 'Dr. Amit Singh'
    },
    {
      id: 'CLM-003',
      patientName: 'Amit Verma',
      patientAvatar: 'https://images.unsplash.com/photo-1676552055618-22ec8cde399a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxoYXBweSUyMHBhdGllbnQlMjBoZWFsdGhjYXJlJTIwcG9ydHJhaXR8ZW58MXx8fHwxNzU4MjAzODE0fDA&ixlib=rb-4.1.0&q=80&w=1080',
      diagnosis: 'Acute nasopharyngitis (common cold)',
      diagnosisCode: 'J00',
      insuranceProvider: 'ICICI Lombard',
      claimAmount: 5000,
      status: 'flagged',
      submittedDate: '2024-01-10',
      flaggedReason: 'Diagnosis code mismatch with symptoms',
      doctorName: 'Dr. Neha Gupta'
    },
    {
      id: 'CLM-004',
      patientName: 'Sunita Devi',
      patientAvatar: 'https://images.unsplash.com/photo-1676552055618-22ec8cde399a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxoYXBweSUyMHBhdGllbnQlMjBoZWFsdGhjYXJlJTIwcG9ydHJhaXR8ZW58MXx8fHwxNzU4MjAzODE0fDA&ixlib=rb-4.1.0&q=80&w=1080',
      diagnosis: 'Asthma, unspecified',
      diagnosisCode: 'J45.9',
      insuranceProvider: 'New India Assurance',
      claimAmount: 12000,
      status: 'rejected',
      submittedDate: '2024-01-08',
      reviewedDate: '2024-01-11',
      reviewerNotes: 'Pre-existing condition not disclosed during policy purchase.',
      doctorName: 'Dr. Rakesh Kumar'
    }
  ];

  // Mock Coverage Rules
  const coverageRules: CoverageRule[] = [
    {
      id: 'RULE-001',
      diagnosisCode: 'I10',
      diagnosisName: 'Essential (primary) hypertension',
      insuranceProvider: 'Star Health',
      coverage: '80%',
      maxAmount: 50000,
      copayment: 20,
      isActive: true,
      createdDate: '2024-01-01'
    },
    {
      id: 'RULE-002',
      diagnosisCode: 'E11.9',
      diagnosisName: 'Type 2 diabetes mellitus without complications',
      insuranceProvider: 'HDFC ERGO',
      coverage: '100%',
      maxAmount: 100000,
      copayment: 0,
      isActive: true,
      createdDate: '2024-01-01'
    },
    {
      id: 'RULE-003',
      diagnosisCode: 'J45.9',
      diagnosisName: 'Asthma, unspecified',
      insuranceProvider: 'New India Assurance',
      coverage: '70%',
      maxAmount: 30000,
      copayment: 30,
      isActive: true,
      createdDate: '2024-01-01'
    }
  ];

  const filteredClaims = claimsData.filter(claim => {
    const matchesSearch = claim.patientName.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         claim.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         claim.diagnosisCode.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'all' || claim.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'pending':
        return <Badge variant="secondary" className="bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400">Pending</Badge>;
      case 'approved':
        return <Badge variant="secondary" className="bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400">Approved</Badge>;
      case 'rejected':
        return <Badge variant="secondary" className="bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400">Rejected</Badge>;
      case 'flagged':
        return <Badge variant="secondary" className="bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-400">Flagged</Badge>;
      default:
        return <Badge variant="secondary">{status}</Badge>;
    }
  };

  const handleApprove = (claimId: string) => {
    toast.success(`Claim ${claimId} approved successfully`);
  };

  const handleReject = (claimId: string) => {
    toast.success(`Claim ${claimId} rejected`);
  };

  const addCoverageRule = () => {
    if (!newRule.diagnosisCode || !newRule.diagnosisName || !newRule.insuranceProvider) {
      toast.error('Please fill in all required fields');
      return;
    }
    
    toast.success('Coverage rule added successfully');
    setShowRuleDialog(false);
    setNewRule({});
  };

  // Analytics calculations
  const totalClaims = claimsData.length;
  const approvedClaims = claimsData.filter(c => c.status === 'approved').length;
  const rejectedClaims = claimsData.filter(c => c.status === 'rejected').length;
  const pendingClaims = claimsData.filter(c => c.status === 'pending').length;
  const flaggedClaims = claimsData.filter(c => c.status === 'flagged').length;
  const approvalRate = totalClaims > 0 ? Math.round((approvedClaims / totalClaims) * 100) : 0;
  const totalClaimAmount = claimsData.reduce((sum, claim) => sum + claim.claimAmount, 0);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl flex items-center space-x-3">
            <Shield className="w-8 h-8 text-blue-500" />
            <span>Insurance Claim Manager</span>
          </h1>
          <p className="text-gray-600 dark:text-gray-400">Manage and validate insurance claims</p>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">📋 Claims Overview</TabsTrigger>
          <TabsTrigger value="rules">✅ Rule Management</TabsTrigger>
          <TabsTrigger value="audit">🔍 Audit & Verification</TabsTrigger>
          <TabsTrigger value="analytics">📊 Analytics</TabsTrigger>
        </TabsList>

        {/* Claims Overview */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center space-x-2">
                  <FileText className="w-5 h-5 text-blue-500" />
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Total Claims</p>
                    <p className="text-2xl">{totalClaims}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Approved</p>
                    <p className="text-2xl text-green-600">{approvedClaims}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center space-x-2">
                  <XCircle className="w-5 h-5 text-red-500" />
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Rejected</p>
                    <p className="text-2xl text-red-600">{rejectedClaims}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center space-x-2">
                  <AlertTriangle className="w-5 h-5 text-orange-500" />
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Flagged</p>
                    <p className="text-2xl text-orange-600">{flaggedClaims}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Claims Management</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-col sm:flex-row gap-4">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
                  <Input
                    placeholder="Search by patient name, claim ID, or diagnosis code..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-full sm:w-48">
                    <SelectValue placeholder="Filter by status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="pending">Pending</SelectItem>
                    <SelectItem value="approved">Approved</SelectItem>
                    <SelectItem value="rejected">Rejected</SelectItem>
                    <SelectItem value="flagged">Flagged</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Claim ID</TableHead>
                      <TableHead>Patient</TableHead>
                      <TableHead>Diagnosis</TableHead>
                      <TableHead>Provider</TableHead>
                      <TableHead>Amount</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredClaims.map((claim) => (
                      <TableRow key={claim.id}>
                        <TableCell className="text-blue-600 hover:underline cursor-pointer">
                          {claim.id}
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center space-x-2">
                            <Avatar className="w-8 h-8">
                              <AvatarImage src={claim.patientAvatar} alt={claim.patientName} />
                              <AvatarFallback>{claim.patientName.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                            </Avatar>
                            <span>{claim.patientName}</span>
                          </div>
                        </TableCell>
                        <TableCell>
                          <div>
                            <p className="text-sm">{claim.diagnosis}</p>
                            <p className="text-xs text-gray-500">{claim.diagnosisCode}</p>
                          </div>
                        </TableCell>
                        <TableCell>{claim.insuranceProvider}</TableCell>
                        <TableCell>₹{claim.claimAmount.toLocaleString()}</TableCell>
                        <TableCell>{getStatusBadge(claim.status)}</TableCell>
                        <TableCell>
                          <div className="flex items-center space-x-2">
                            <Dialog>
                              <DialogTrigger asChild>
                                <Button variant="ghost" size="sm" onClick={() => setSelectedClaim(claim)}>
                                  <Eye className="w-4 h-4" />
                                </Button>
                              </DialogTrigger>
                              <DialogContent className="max-w-2xl">
                                <DialogHeader>
                                  <DialogTitle>Claim Details - {claim.id}</DialogTitle>
                                </DialogHeader>
                                <div className="space-y-4">
                                  <div className="grid grid-cols-2 gap-4">
                                    <div>
                                      <Label>Patient</Label>
                                      <p>{claim.patientName}</p>
                                    </div>
                                    <div>
                                      <Label>Doctor</Label>
                                      <p>{claim.doctorName}</p>
                                    </div>
                                    <div>
                                      <Label>Diagnosis</Label>
                                      <p>{claim.diagnosis}</p>
                                    </div>
                                    <div>
                                      <Label>Code</Label>
                                      <p>{claim.diagnosisCode}</p>
                                    </div>
                                    <div>
                                      <Label>Insurance Provider</Label>
                                      <p>{claim.insuranceProvider}</p>
                                    </div>
                                    <div>
                                      <Label>Claim Amount</Label>
                                      <p>₹{claim.claimAmount.toLocaleString()}</p>
                                    </div>
                                  </div>
                                  {claim.flaggedReason && (
                                    <div>
                                      <Label>Flag Reason</Label>
                                      <p className="text-orange-600">{claim.flaggedReason}</p>
                                    </div>
                                  )}
                                  {claim.reviewerNotes && (
                                    <div>
                                      <Label>Reviewer Notes</Label>
                                      <p>{claim.reviewerNotes}</p>
                                    </div>
                                  )}
                                  {claim.status === 'pending' || claim.status === 'flagged' ? (
                                    <div className="flex space-x-2 pt-4">
                                      <Button
                                        onClick={() => handleApprove(claim.id)}
                                        className="bg-green-600 hover:bg-green-700"
                                      >
                                        <CheckCircle className="w-4 h-4 mr-2" />
                                        Approve
                                      </Button>
                                      <Button
                                        variant="destructive"
                                        onClick={() => handleReject(claim.id)}
                                      >
                                        <XCircle className="w-4 h-4 mr-2" />
                                        Reject
                                      </Button>
                                    </div>
                                  ) : null}
                                </div>
                              </DialogContent>
                            </Dialog>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Rule Management */}
        <TabsContent value="rules" className="space-y-6">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Coverage Rules</CardTitle>
                <Dialog open={showRuleDialog} onOpenChange={setShowRuleDialog}>
                  <DialogTrigger asChild>
                    <Button>
                      <Plus className="w-4 h-4 mr-2" />
                      Add Rule
                    </Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Add Coverage Rule</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                      <div>
                        <Label>Diagnosis Code</Label>
                        <Input
                          placeholder="e.g., I10"
                          value={newRule.diagnosisCode || ''}
                          onChange={(e) => setNewRule({ ...newRule, diagnosisCode: e.target.value })}
                        />
                      </div>
                      <div>
                        <Label>Diagnosis Name</Label>
                        <Input
                          placeholder="e.g., Essential (primary) hypertension"
                          value={newRule.diagnosisName || ''}
                          onChange={(e) => setNewRule({ ...newRule, diagnosisName: e.target.value })}
                        />
                      </div>
                      <div>
                        <Label>Insurance Provider</Label>
                        <Select
                          value={newRule.insuranceProvider || ''}
                          onValueChange={(value) => setNewRule({ ...newRule, insuranceProvider: value })}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select provider" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="Star Health">Star Health</SelectItem>
                            <SelectItem value="HDFC ERGO">HDFC ERGO</SelectItem>
                            <SelectItem value="ICICI Lombard">ICICI Lombard</SelectItem>
                            <SelectItem value="New India Assurance">New India Assurance</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <Label>Coverage %</Label>
                          <Input
                            type="number"
                            placeholder="80"
                            value={newRule.coverage || ''}
                            onChange={(e) => setNewRule({ ...newRule, coverage: e.target.value + '%' })}
                          />
                        </div>
                        <div>
                          <Label>Max Amount</Label>
                          <Input
                            type="number"
                            placeholder="50000"
                            value={newRule.maxAmount || ''}
                            onChange={(e) => setNewRule({ ...newRule, maxAmount: parseInt(e.target.value) })}
                          />
                        </div>
                      </div>
                      <Button onClick={addCoverageRule} className="w-full">
                        Add Rule
                      </Button>
                    </div>
                  </DialogContent>
                </Dialog>
              </div>
            </CardHeader>
            <CardContent>
              <div className="rounded-md border">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Diagnosis Code</TableHead>
                      <TableHead>Diagnosis Name</TableHead>
                      <TableHead>Provider</TableHead>
                      <TableHead>Coverage</TableHead>
                      <TableHead>Max Amount</TableHead>
                      <TableHead>Copayment</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {coverageRules.map((rule) => (
                      <TableRow key={rule.id}>
                        <TableCell className="text-blue-600">{rule.diagnosisCode}</TableCell>
                        <TableCell>{rule.diagnosisName}</TableCell>
                        <TableCell>{rule.insuranceProvider}</TableCell>
                        <TableCell>
                          <Badge variant="secondary" className="bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400">
                            {rule.coverage}
                          </Badge>
                        </TableCell>
                        <TableCell>₹{rule.maxAmount.toLocaleString()}</TableCell>
                        <TableCell>{rule.copayment}%</TableCell>
                        <TableCell>
                          <Badge variant={rule.isActive ? "secondary" : "destructive"}>
                            {rule.isActive ? 'Active' : 'Inactive'}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center space-x-2">
                            <Button variant="ghost" size="sm">
                              <Edit className="w-4 h-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Audit & Verification */}
        <TabsContent value="audit" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <AlertTriangle className="w-5 h-5 text-orange-500" />
                <span>Flagged Claims</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {claimsData.filter(claim => claim.status === 'flagged').map((claim) => (
                  <div key={claim.id} className="border rounded-lg p-4 bg-orange-50 dark:bg-orange-900/20">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <Avatar>
                          <AvatarImage src={claim.patientAvatar} alt={claim.patientName} />
                          <AvatarFallback>{claim.patientName.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                        </Avatar>
                        <div>
                          <p>{claim.patientName} - {claim.id}</p>
                          <p className="text-sm text-gray-600">{claim.diagnosis} ({claim.diagnosisCode})</p>
                          <p className="text-sm text-orange-600">{claim.flaggedReason}</p>
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        <Button
                          size="sm"
                          onClick={() => handleApprove(claim.id)}
                          className="bg-green-600 hover:bg-green-700"
                        >
                          <CheckCircle className="w-4 h-4 mr-2" />
                          Approve
                        </Button>
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() => handleReject(claim.id)}
                        >
                          <XCircle className="w-4 h-4 mr-2" />
                          Reject
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Analytics */}
        <TabsContent value="analytics" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center space-x-2">
                  <TrendingUp className="w-5 h-5 text-green-500" />
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Approval Rate</p>
                    <p className="text-2xl text-green-600">{approvalRate}%</p>
                  </div>
                </div>
                <Progress value={approvalRate} className="mt-2" />
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center space-x-2">
                  <DollarSign className="w-5 h-5 text-blue-500" />
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Total Claim Value</p>
                    <p className="text-2xl">₹{totalClaimAmount.toLocaleString()}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center space-x-2">
                  <Activity className="w-5 h-5 text-purple-500" />
                  <div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Processing Time</p>
                    <p className="text-2xl">2.3 days</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Top Rejection Reasons</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span>Pre-existing condition not disclosed</span>
                  <div className="flex items-center space-x-2">
                    <Progress value={45} className="w-32" />
                    <span className="text-sm text-gray-600">45%</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span>Diagnosis code mismatch</span>
                  <div className="flex items-center space-x-2">
                    <Progress value={30} className="w-32" />
                    <span className="text-sm text-gray-600">30%</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span>Insufficient documentation</span>
                  <div className="flex items-center space-x-2">
                    <Progress value={15} className="w-32" />
                    <span className="text-sm text-gray-600">15%</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span>Policy exclusion</span>
                  <div className="flex items-center space-x-2">
                    <Progress value={10} className="w-32" />
                    <span className="text-sm text-gray-600">10%</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </motion.div>
  );
};

export default InsuranceClaimManager;