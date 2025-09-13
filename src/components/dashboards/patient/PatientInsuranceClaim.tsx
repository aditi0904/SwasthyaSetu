import React, { useState } from 'react';
import { motion } from 'motion/react';
import { 
  CreditCard, 
  FileText, 
  Upload, 
  CheckCircle, 
  AlertCircle, 
  Clock,
  Download,
  Eye,
  Search,
  Filter,
  Plus,
  X
} from 'lucide-react';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { Label } from '../../ui/label';
import { Textarea } from '../../ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../ui/select';
import { Badge } from '../../ui/badge';
import { Progress } from '../../ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../ui/tabs';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../../ui/dialog';
import { toast } from 'sonner@2.0.3';
import type { User } from '../../../App';

interface PatientInsuranceClaimProps {
  user: User;
}

const PatientInsuranceClaim: React.FC<PatientInsuranceClaimProps> = ({ user }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  // Mock claim form data
  const [claimForm, setClaimForm] = useState({
    claimType: '',
    treatmentDate: '',
    hospitalName: '',
    doctorName: '',
    diagnosisCode: '',
    treatmentDescription: '',
    claimAmount: '',
    policyNumber: 'SH123456789',
    memberName: user.name,
    memberId: 'MB001122',
    relationToMember: 'self'
  });

  // Mock existing claims
  const existingClaims = [
    {
      id: 'CLM001',
      date: '2024-01-15',
      type: 'Hospitalization',
      amount: '₹25,000',
      status: 'approved',
      hospital: 'Apollo Hospital',
      approvedAmount: '₹23,500',
      processedDate: '2024-01-20'
    },
    {
      id: 'CLM002',
      date: '2024-01-10',
      type: 'Outpatient',
      amount: '₹5,500',
      status: 'processing',
      hospital: 'Max Healthcare',
      approvedAmount: '',
      processedDate: ''
    },
    {
      id: 'CLM003',
      date: '2023-12-20',
      type: 'Pharmacy',
      amount: '₹1,200',
      status: 'rejected',
      hospital: 'MedPlus Pharmacy',
      approvedAmount: '₹0',
      processedDate: '2023-12-25',
      rejectionReason: 'Medicine not covered under policy'
    }
  ];

  // Live validation
  const validateField = (fieldName: string, value: string) => {
    const errors: Record<string, string> = {};

    switch (fieldName) {
      case 'claimAmount':
        if (value && (isNaN(Number(value)) || Number(value) <= 0)) {
          errors[fieldName] = 'Please enter a valid amount';
        } else if (Number(value) > 500000) {
          errors[fieldName] = 'Claim amount cannot exceed ₹5,00,000';
        }
        break;
      case 'treatmentDate':
        if (value && new Date(value) > new Date()) {
          errors[fieldName] = 'Treatment date cannot be in the future';
        }
        break;
      case 'hospitalName':
        if (value && value.length < 3) {
          errors[fieldName] = 'Hospital name must be at least 3 characters';
        }
        break;
      case 'doctorName':
        if (value && value.length < 3) {
          errors[fieldName] = 'Doctor name must be at least 3 characters';
        }
        break;
    }

    setValidationErrors(prev => ({ ...prev, ...errors }));
    return Object.keys(errors).length === 0;
  };

  const handleInputChange = (field: string, value: string) => {
    setClaimForm(prev => ({ ...prev, [field]: value }));
    validateField(field, value);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    const validFiles = files.filter(file => {
      const validTypes = ['image/jpeg', 'image/png', 'application/pdf'];
      const maxSize = 5 * 1024 * 1024; // 5MB
      return validTypes.includes(file.type) && file.size <= maxSize;
    });

    if (validFiles.length !== files.length) {
      toast.error('Some files were rejected. Please upload only JPEG, PNG, or PDF files under 5MB.');
    }

    setUploadedFiles(prev => [...prev, ...validFiles]);
  };

  const removeFile = (index: number) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate all fields
    const requiredFields = ['claimType', 'treatmentDate', 'hospitalName', 'doctorName', 'claimAmount'];
    const missingFields = requiredFields.filter(field => !claimForm[field as keyof typeof claimForm]);
    
    if (missingFields.length > 0) {
      toast.error('Please fill in all required fields');
      return;
    }

    if (uploadedFiles.length === 0) {
      toast.error('Please upload at least one supporting document');
      return;
    }

    setIsSubmitting(true);

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 3000));

    const newClaim = {
      id: `CLM${String(existingClaims.length + 1).padStart(3, '0')}`,
      date: new Date().toISOString().split('T')[0],
      type: claimForm.claimType,
      amount: `₹${claimForm.claimAmount}`,
      status: 'processing',
      hospital: claimForm.hospitalName,
      approvedAmount: '',
      processedDate: ''
    };

    console.log('New claim submitted:', newClaim);
    toast.success('Claim submitted successfully! You will receive updates via email and SMS.');

    // Reset form
    setClaimForm({
      claimType: '',
      treatmentDate: '',
      hospitalName: '',
      doctorName: '',
      diagnosisCode: '',
      treatmentDescription: '',
      claimAmount: '',
      policyNumber: 'SH123456789',
      memberName: user.name,
      memberId: 'MB001122',
      relationToMember: 'self'
    });
    setUploadedFiles([]);
    setIsSubmitting(false);
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'approved': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      case 'processing': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400';
      case 'rejected': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'approved': return <CheckCircle className="w-4 h-4" />;
      case 'processing': return <Clock className="w-4 h-4" />;
      case 'rejected': return <AlertCircle className="w-4 h-4" />;
      default: return <Clock className="w-4 h-4" />;
    }
  };

  const filteredClaims = existingClaims.filter(claim => {
    const matchesSearch = claim.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         claim.hospital.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'all' || claim.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-6xl mx-auto space-y-6"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl">Insurance Claims</h1>
          <p className="text-gray-600 dark:text-gray-400">Submit new claims and track existing ones</p>
        </div>
        <Card className="p-4">
          <div className="text-center">
            <p className="text-sm text-gray-600 dark:text-gray-400">Policy Number</p>
            <p className="text-lg">SH123456789</p>
            <Badge variant="secondary" className="bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400 mt-1">
              Active
            </Badge>
          </div>
        </Card>
      </div>

      <Tabs defaultValue="new-claim" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="new-claim">New Claim</TabsTrigger>
          <TabsTrigger value="claim-history">Claim History</TabsTrigger>
        </TabsList>

        <TabsContent value="new-claim" className="space-y-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Claim Information */}
              <div className="lg:col-span-2 space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <FileText className="w-5 h-5" />
                      <span>Claim Information</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="claimType">Claim Type *</Label>
                        <Select value={claimForm.claimType} onValueChange={(value) => handleInputChange('claimType', value)}>
                          <SelectTrigger>
                            <SelectValue placeholder="Select claim type" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="hospitalization">Hospitalization</SelectItem>
                            <SelectItem value="outpatient">Outpatient Treatment</SelectItem>
                            <SelectItem value="pharmacy">Pharmacy</SelectItem>
                            <SelectItem value="diagnostic">Diagnostic Tests</SelectItem>
                            <SelectItem value="emergency">Emergency</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="treatmentDate">Treatment Date *</Label>
                        <Input
                          id="treatmentDate"
                          type="date"
                          value={claimForm.treatmentDate}
                          onChange={(e) => handleInputChange('treatmentDate', e.target.value)}
                          className={validationErrors.treatmentDate ? 'border-red-500' : ''}
                        />
                        {validationErrors.treatmentDate && (
                          <p className="text-sm text-red-500">{validationErrors.treatmentDate}</p>
                        )}
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="hospitalName">Hospital/Clinic Name *</Label>
                        <Input
                          id="hospitalName"
                          value={claimForm.hospitalName}
                          onChange={(e) => handleInputChange('hospitalName', e.target.value)}
                          placeholder="Enter hospital or clinic name"
                          className={validationErrors.hospitalName ? 'border-red-500' : ''}
                        />
                        {validationErrors.hospitalName && (
                          <p className="text-sm text-red-500">{validationErrors.hospitalName}</p>
                        )}
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="doctorName">Doctor Name *</Label>
                        <Input
                          id="doctorName"
                          value={claimForm.doctorName}
                          onChange={(e) => handleInputChange('doctorName', e.target.value)}
                          placeholder="Enter doctor's name"
                          className={validationErrors.doctorName ? 'border-red-500' : ''}
                        />
                        {validationErrors.doctorName && (
                          <p className="text-sm text-red-500">{validationErrors.doctorName}</p>
                        )}
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="diagnosisCode">Diagnosis Code (ICD-10)</Label>
                        <Input
                          id="diagnosisCode"
                          value={claimForm.diagnosisCode}
                          onChange={(e) => handleInputChange('diagnosisCode', e.target.value)}
                          placeholder="e.g., E11.9"
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="claimAmount">Claim Amount (₹) *</Label>
                        <Input
                          id="claimAmount"
                          type="number"
                          value={claimForm.claimAmount}
                          onChange={(e) => handleInputChange('claimAmount', e.target.value)}
                          placeholder="Enter amount"
                          className={validationErrors.claimAmount ? 'border-red-500' : ''}
                        />
                        {validationErrors.claimAmount && (
                          <p className="text-sm text-red-500">{validationErrors.claimAmount}</p>
                        )}
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="treatmentDescription">Treatment Description</Label>
                      <Textarea
                        id="treatmentDescription"
                        value={claimForm.treatmentDescription}
                        onChange={(e) => handleInputChange('treatmentDescription', e.target.value)}
                        placeholder="Describe the treatment received..."
                        rows={4}
                      />
                    </div>
                  </CardContent>
                </Card>

                {/* Document Upload */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Upload className="w-5 h-5" />
                      <span>Supporting Documents</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center">
                      <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        Upload medical bills, prescriptions, and discharge summaries
                      </p>
                      <p className="text-xs text-gray-500 mb-4">
                        Supported formats: JPEG, PNG, PDF (Max 5MB each)
                      </p>
                      <Label htmlFor="file-upload" className="cursor-pointer">
                        <Button type="button" variant="outline" className="pointer-events-none">
                          Choose Files
                        </Button>
                        <Input
                          id="file-upload"
                          type="file"
                          multiple
                          accept="image/jpeg,image/png,application/pdf"
                          onChange={handleFileUpload}
                          className="hidden"
                        />
                      </Label>
                    </div>

                    {uploadedFiles.length > 0 && (
                      <div className="space-y-2">
                        <Label>Uploaded Files ({uploadedFiles.length})</Label>
                        {uploadedFiles.map((file, index) => (
                          <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <div className="flex items-center space-x-2">
                              <FileText className="w-4 h-4 text-gray-400" />
                              <span className="text-sm">{file.name}</span>
                              <span className="text-xs text-gray-500">
                                ({(file.size / 1024 / 1024).toFixed(2)} MB)
                              </span>
                            </div>
                            <Button
                              type="button"
                              variant="ghost"
                              size="sm"
                              onClick={() => removeFile(index)}
                            >
                              <X className="w-4 h-4" />
                            </Button>
                          </div>
                        ))}
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>

              {/* Member Information & Progress */}
              <div className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <CreditCard className="w-5 h-5" />
                      <span>Member Information</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label>Policy Number</Label>
                      <Input value={claimForm.policyNumber} disabled />
                    </div>

                    <div className="space-y-2">
                      <Label>Member Name</Label>
                      <Input value={claimForm.memberName} disabled />
                    </div>

                    <div className="space-y-2">
                      <Label>Member ID</Label>
                      <Input value={claimForm.memberId} disabled />
                    </div>

                    <div className="space-y-2">
                      <Label>Relation to Member</Label>
                      <Select value={claimForm.relationToMember} onValueChange={(value) => handleInputChange('relationToMember', value)}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="self">Self</SelectItem>
                          <SelectItem value="spouse">Spouse</SelectItem>
                          <SelectItem value="child">Child</SelectItem>
                          <SelectItem value="parent">Parent</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </CardContent>
                </Card>

                {/* Claim Progress */}
                <Card>
                  <CardHeader>
                    <CardTitle>Claim Submission Progress</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Form Completion</span>
                        <span>75%</span>
                      </div>
                      <Progress value={75} className="h-2" />
                    </div>

                    <div className="space-y-3 text-sm">
                      <div className="flex items-center space-x-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span>Member information verified</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span>Basic claim details provided</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        {uploadedFiles.length > 0 ? (
                          <CheckCircle className="w-4 h-4 text-green-500" />
                        ) : (
                          <AlertCircle className="w-4 h-4 text-orange-500" />
                        )}
                        <span>Supporting documents</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Quick Tips */}
                <Card>
                  <CardHeader>
                    <CardTitle>Tips for Faster Processing</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="text-sm space-y-2">
                      <li className="flex items-start space-x-2">
                        <CheckCircle className="w-4 h-4 text-green-500 mt-0.5" />
                        <span>Upload clear, readable documents</span>
                      </li>
                      <li className="flex items-start space-x-2">
                        <CheckCircle className="w-4 h-4 text-green-500 mt-0.5" />
                        <span>Include all relevant medical bills</span>
                      </li>
                      <li className="flex items-start space-x-2">
                        <CheckCircle className="w-4 h-4 text-green-500 mt-0.5" />
                        <span>Submit within 30 days of treatment</span>
                      </li>
                    </ul>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* Submit Button */}
            <div className="flex justify-end space-x-4">
              <Button type="button" variant="outline" disabled={isSubmitting}>
                Save as Draft
              </Button>
              <Button 
                type="submit" 
                disabled={isSubmitting}
                className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white px-8"
              >
                {isSubmitting ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                    Submitting...
                  </>
                ) : (
                  <>
                    <FileText className="w-4 h-4 mr-2" />
                    Submit Claim
                  </>
                )}
              </Button>
            </div>
          </form>
        </TabsContent>

        <TabsContent value="claim-history" className="space-y-4">
          {/* Filters */}
          <div className="flex space-x-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
              <Input
                placeholder="Search claims..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Claims</SelectItem>
                <SelectItem value="approved">Approved</SelectItem>
                <SelectItem value="processing">Processing</SelectItem>
                <SelectItem value="rejected">Rejected</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Claims List */}
          <div className="space-y-4">
            {filteredClaims.map((claim) => (
              <Card key={claim.id}>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-lg">Claim #{claim.id}</h3>
                        <Badge className={getStatusColor(claim.status)} variant="secondary">
                          {getStatusIcon(claim.status)}
                          <span className="ml-1 capitalize">{claim.status}</span>
                        </Badge>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                        <div>
                          <p className="text-gray-600 dark:text-gray-400">Date</p>
                          <p>{claim.date}</p>
                        </div>
                        <div>
                          <p className="text-gray-600 dark:text-gray-400">Type</p>
                          <p>{claim.type}</p>
                        </div>
                        <div>
                          <p className="text-gray-600 dark:text-gray-400">Hospital</p>
                          <p>{claim.hospital}</p>
                        </div>
                        <div>
                          <p className="text-gray-600 dark:text-gray-400">Claim Amount</p>
                          <p className="text-lg">{claim.amount}</p>
                        </div>
                        {claim.approvedAmount && (
                          <div>
                            <p className="text-gray-600 dark:text-gray-400">Approved Amount</p>
                            <p className="text-lg text-green-600">{claim.approvedAmount}</p>
                          </div>
                        )}
                        {claim.processedDate && (
                          <div>
                            <p className="text-gray-600 dark:text-gray-400">Processed Date</p>
                            <p>{claim.processedDate}</p>
                          </div>
                        )}
                      </div>

                      {claim.status === 'rejected' && claim.rejectionReason && (
                        <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                          <p className="text-sm text-red-800 dark:text-red-200">
                            <strong>Rejection Reason:</strong> {claim.rejectionReason}
                          </p>
                        </div>
                      )}
                    </div>
                    
                    <div className="flex space-x-2">
                      <Dialog>
                        <DialogTrigger asChild>
                          <Button variant="ghost" size="sm">
                            <Eye className="w-4 h-4" />
                          </Button>
                        </DialogTrigger>
                        <DialogContent className="max-w-2xl">
                          <DialogHeader>
                            <DialogTitle>Claim Details - #{claim.id}</DialogTitle>
                          </DialogHeader>
                          <div className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                              <div>
                                <Label>Claim ID</Label>
                                <p>{claim.id}</p>
                              </div>
                              <div>
                                <Label>Status</Label>
                                <Badge className={getStatusColor(claim.status)} variant="secondary">
                                  {claim.status}
                                </Badge>
                              </div>
                              <div>
                                <Label>Date</Label>
                                <p>{claim.date}</p>
                              </div>
                              <div>
                                <Label>Type</Label>
                                <p>{claim.type}</p>
                              </div>
                              <div>
                                <Label>Hospital</Label>
                                <p>{claim.hospital}</p>
                              </div>
                              <div>
                                <Label>Claim Amount</Label>
                                <p>{claim.amount}</p>
                              </div>
                            </div>
                            {claim.status === 'rejected' && claim.rejectionReason && (
                              <div className="p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                                <Label>Rejection Reason</Label>
                                <p className="text-red-800 dark:text-red-200">{claim.rejectionReason}</p>
                              </div>
                            )}
                          </div>
                        </DialogContent>
                      </Dialog>
                      
                      <Button variant="ghost" size="sm">
                        <Download className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </motion.div>
  );
};

export default PatientInsuranceClaim;