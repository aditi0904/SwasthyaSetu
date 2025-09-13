import React, { useState } from 'react';
import { motion } from 'motion/react';
import { 
  CheckCircle, 
  XCircle, 
  Clock, 
  Search, 
  Filter,
  ThumbsUp,
  ThumbsDown,
  Eye,
  FileText,
  AlertTriangle
} from 'lucide-react';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Badge } from '../../ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../ui/table';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../../ui/dialog';
import { Textarea } from '../../ui/textarea';
import { Label } from '../../ui/label';
import { toast } from 'sonner@2.0.3';

const MappingReviewer: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [selectedMapping, setSelectedMapping] = useState<any>(null);

  // Mock NAMASTE ↔ ICD-11 mapping data
  const mappings = [
    {
      id: 'MAP001',
      namaste: {
        code: 'NAM-12345',
        term: 'शर्करा रोग (Diabetes)',
        category: 'endocrine',
        description: 'Traditional Ayurvedic term for diabetes mellitus'
      },
      icd11: {
        code: '5A11',
        term: 'Type 2 diabetes mellitus',
        category: 'Endocrine, nutritional or metabolic diseases',
        description: 'Non-insulin-dependent diabetes mellitus'
      },
      confidence: 95,
      status: 'pending',
      submittedBy: 'Dr. Ramesh Gupta',
      submittedDate: '2024-01-15',
      reviewedBy: '',
      reviewDate: '',
      comments: ''
    },
    {
      id: 'MAP002',
      namaste: {
        code: 'NAM-23456',
        term: 'हृदय रोग (Heart Disease)',
        category: 'cardiovascular',
        description: 'General term for heart-related ailments'
      },
      icd11: {
        code: 'BA00',
        term: 'Essential hypertension',
        category: 'Diseases of the circulatory system',
        description: 'High blood pressure without known secondary cause'
      },
      confidence: 87,
      status: 'approved',
      submittedBy: 'Dr. Priya Sharma',
      submittedDate: '2024-01-12',
      reviewedBy: 'Admin Kumar',
      reviewDate: '2024-01-14',
      comments: 'Good mapping with cultural context preserved'
    },
    {
      id: 'MAP003',
      namaste: {
        code: 'NAM-34567',
        term: 'श्वास रोग (Respiratory Disease)',
        category: 'respiratory',
        description: 'Breathing-related disorders in Ayurveda'
      },
      icd11: {
        code: 'CA20',
        term: 'Asthma',
        category: 'Diseases of the respiratory system',
        description: 'Chronic inflammatory airway disease'
      },
      confidence: 78,
      status: 'rejected',
      submittedBy: 'Dr. Meera Singh',
      submittedDate: '2024-01-10',
      reviewedBy: 'Admin Kumar',
      reviewDate: '2024-01-13',
      comments: 'Too broad - NAMASTE term covers multiple respiratory conditions'
    },
    {
      id: 'MAP004',
      namaste: {
        code: 'NAM-45678',
        term: 'संधिशोथ (Joint Inflammation)',
        category: 'musculoskeletal',
        description: 'Inflammatory joint conditions'
      },
      icd11: {
        code: 'FA20',
        term: 'Rheumatoid arthritis',
        category: 'Diseases of the musculoskeletal system',
        description: 'Chronic inflammatory arthritis'
      },
      confidence: 92,
      status: 'pending',
      submittedBy: 'Dr. Amit Verma',
      submittedDate: '2024-01-14',
      reviewedBy: '',
      reviewDate: '',
      comments: ''
    }
  ];

  const filteredMappings = mappings.filter(mapping => {
    const matchesSearch = mapping.namaste.term.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         mapping.icd11.term.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         mapping.namaste.code.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         mapping.icd11.code.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'all' || mapping.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'approved': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      case 'rejected': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      case 'pending': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'approved': return <CheckCircle className="w-4 h-4" />;
      case 'rejected': return <XCircle className="w-4 h-4" />;
      case 'pending': return <Clock className="w-4 h-4" />;
      default: return <Clock className="w-4 h-4" />;
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 90) return 'text-green-600';
    if (confidence >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  const handleReview = (mappingId: string, action: 'approve' | 'reject', comments: string) => {
    const actionText = action === 'approve' ? 'approved' : 'rejected';
    toast.success(`Mapping ${mappingId} has been ${actionText}`);
    setSelectedMapping(null);
  };

  const stats = {
    total: mappings.length,
    pending: mappings.filter(m => m.status === 'pending').length,
    approved: mappings.filter(m => m.status === 'approved').length,
    rejected: mappings.filter(m => m.status === 'rejected').length
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
          <h1 className="text-3xl">NAMASTE ↔ ICD-11 Mapping Reviewer</h1>
          <p className="text-gray-600 dark:text-gray-400">Review and approve medical terminology mappings</p>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <FileText className="w-5 h-5 text-blue-500" />
              <div>
                <p className="text-2xl">{stats.total}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Mappings</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <Clock className="w-5 h-5 text-yellow-500" />
              <div>
                <p className="text-2xl">{stats.pending}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Pending Review</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <div>
                <p className="text-2xl">{stats.approved}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Approved</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center space-x-2">
              <XCircle className="w-5 h-5 text-red-500" />
              <div>
                <p className="text-2xl">{stats.rejected}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Rejected</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters and Search */}
      <Card>
        <CardHeader>
          <CardTitle>Mapping Directory</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
              <Input
                placeholder="Search mappings..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-full md:w-48">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="pending">Pending</SelectItem>
                <SelectItem value="approved">Approved</SelectItem>
                <SelectItem value="rejected">Rejected</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Mappings Table */}
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>NAMASTE Term</TableHead>
                  <TableHead>ICD-11 Code</TableHead>
                  <TableHead>Confidence</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Submitted By</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredMappings.map((mapping) => (
                  <TableRow key={mapping.id}>
                    <TableCell>
                      <div>
                        <p className="text-sm">{mapping.namaste.term}</p>
                        <p className="text-xs text-gray-500">{mapping.namaste.code}</p>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div>
                        <p className="text-sm">{mapping.icd11.term}</p>
                        <p className="text-xs text-gray-500">{mapping.icd11.code}</p>
                      </div>
                    </TableCell>
                    <TableCell>
                      <span className={`text-sm ${getConfidenceColor(mapping.confidence)}`}>
                        {mapping.confidence}%
                      </span>
                    </TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(mapping.status)} variant="secondary">
                        {getStatusIcon(mapping.status)}
                        <span className="ml-1 capitalize">{mapping.status}</span>
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div>
                        <p className="text-sm">{mapping.submittedBy}</p>
                        <p className="text-xs text-gray-500">{mapping.submittedDate}</p>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => setSelectedMapping(mapping)}
                            >
                              <Eye className="w-4 h-4" />
                            </Button>
                          </DialogTrigger>
                        </Dialog>
                        
                        {mapping.status === 'pending' && (
                          <>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleReview(mapping.id, 'approve', 'Approved via quick action')}
                              className="text-green-600 hover:bg-green-50"
                            >
                              <ThumbsUp className="w-4 h-4" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleReview(mapping.id, 'reject', 'Rejected via quick action')}
                              className="text-red-600 hover:bg-red-50"
                            >
                              <ThumbsDown className="w-4 h-4" />
                            </Button>
                          </>
                        )}
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {/* Mapping Details Dialog */}
      <Dialog open={!!selectedMapping} onOpenChange={() => setSelectedMapping(null)}>
        <DialogContent className="max-w-4xl">
          <DialogHeader>
            <DialogTitle>Mapping Review - {selectedMapping?.id}</DialogTitle>
          </DialogHeader>
          {selectedMapping && (
            <div className="space-y-6">
              {/* Mapping Overview */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">NAMASTE Term</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div>
                      <Label>Term</Label>
                      <p className="text-lg">{selectedMapping.namaste.term}</p>
                    </div>
                    <div>
                      <Label>Code</Label>
                      <p>{selectedMapping.namaste.code}</p>
                    </div>
                    <div>
                      <Label>Category</Label>
                      <p className="capitalize">{selectedMapping.namaste.category}</p>
                    </div>
                    <div>
                      <Label>Description</Label>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {selectedMapping.namaste.description}
                      </p>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">ICD-11 Term</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div>
                      <Label>Term</Label>
                      <p className="text-lg">{selectedMapping.icd11.term}</p>
                    </div>
                    <div>
                      <Label>Code</Label>
                      <p>{selectedMapping.icd11.code}</p>
                    </div>
                    <div>
                      <Label>Category</Label>
                      <p>{selectedMapping.icd11.category}</p>
                    </div>
                    <div>
                      <Label>Description</Label>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {selectedMapping.icd11.description}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Mapping Metadata */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Mapping Information</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div>
                      <Label>Confidence Score</Label>
                      <p className={`text-lg ${getConfidenceColor(selectedMapping.confidence)}`}>
                        {selectedMapping.confidence}%
                      </p>
                    </div>
                    <div>
                      <Label>Status</Label>
                      <Badge className={getStatusColor(selectedMapping.status)} variant="secondary">
                        {selectedMapping.status}
                      </Badge>
                    </div>
                    <div>
                      <Label>Submitted By</Label>
                      <p>{selectedMapping.submittedBy}</p>
                    </div>
                    <div>
                      <Label>Submitted Date</Label>
                      <p>{selectedMapping.submittedDate}</p>
                    </div>
                  </div>

                  {selectedMapping.reviewedBy && (
                    <div className="grid grid-cols-2 gap-4 mt-4 pt-4 border-t">
                      <div>
                        <Label>Reviewed By</Label>
                        <p>{selectedMapping.reviewedBy}</p>
                      </div>
                      <div>
                        <Label>Review Date</Label>
                        <p>{selectedMapping.reviewDate}</p>
                      </div>
                    </div>
                  )}

                  {selectedMapping.comments && (
                    <div className="mt-4 pt-4 border-t">
                      <Label>Review Comments</Label>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        {selectedMapping.comments}
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Review Actions */}
              {selectedMapping.status === 'pending' && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Review Decision</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label>Comments</Label>
                      <Textarea placeholder="Add review comments..." rows={3} />
                    </div>
                    
                    <div className="flex justify-end space-x-4">
                      <Button
                        variant="outline"
                        onClick={() => handleReview(selectedMapping.id, 'reject', 'Rejected after review')}
                        className="text-red-600 border-red-200 hover:bg-red-50"
                      >
                        <XCircle className="w-4 h-4 mr-2" />
                        Reject Mapping
                      </Button>
                      <Button
                        onClick={() => handleReview(selectedMapping.id, 'approve', 'Approved after review')}
                        className="bg-green-600 hover:bg-green-700 text-white"
                      >
                        <CheckCircle className="w-4 h-4 mr-2" />
                        Approve Mapping
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>
    </motion.div>
  );
};

export default MappingReviewer;