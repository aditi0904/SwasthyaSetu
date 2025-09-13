import React, { useState } from 'react';
import { motion } from 'motion/react';
import { 
  Download, 
  FileText, 
  Activity, 
  Pill, 
  Calendar, 
  Heart,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Eye,
  Search,
  Filter
} from 'lucide-react';
import { Button } from '../../ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Badge } from '../../ui/badge';
import { Input } from '../../ui/input';
import { Label } from '../../ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../ui/tabs';
import { ScrollArea } from '../../ui/scroll-area';
import { Progress } from '../../ui/progress';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../../ui/dialog';
import { ImageWithFallback } from '../../figma/ImageWithFallback';
import type { User } from '../../../App';

interface PatientHealthRecordsProps {
  user: User;
}

const PatientHealthRecords: React.FC<PatientHealthRecordsProps> = ({ user }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState('all');

  // Mock health data
  const vitals = {
    bloodPressure: { value: '120/80', status: 'normal', trend: 'stable' },
    heartRate: { value: '72 bpm', status: 'normal', trend: 'stable' },
    temperature: { value: '98.6°F', status: 'normal', trend: 'stable' },
    weight: { value: '65 kg', status: 'normal', trend: 'decreasing' },
    bmi: { value: '22.1', status: 'normal', trend: 'stable' },
    bloodSugar: { value: '95 mg/dL', status: 'normal', trend: 'stable' }
  };

  const medications = [
    {
      id: '1',
      name: 'Metformin',
      dosage: '500mg',
      frequency: 'Twice daily',
      prescribedBy: 'Dr. Sharma',
      startDate: '2024-01-01',
      status: 'active'
    },
    {
      id: '2',
      name: 'Vitamin D3',
      dosage: '1000 IU',
      frequency: 'Once daily',
      prescribedBy: 'Dr. Patel',
      startDate: '2023-12-15',
      status: 'active'
    },
    {
      id: '3',
      name: 'Amoxicillin',
      dosage: '250mg',
      frequency: 'Three times daily',
      prescribedBy: 'Dr. Kumar',
      startDate: '2023-11-20',
      status: 'completed'
    }
  ];

  const medicalHistory = [
    {
      id: '1',
      date: '2024-01-15',
      type: 'Consultation',
      doctor: 'Dr. Sharma',
      diagnosis: 'Type 2 Diabetes - Well Controlled',
      status: 'ongoing',
      notes: 'Blood sugar levels are well controlled. Continue current medication.',
      prescriptions: ['Metformin 500mg twice daily', 'Regular blood sugar monitoring']
    },
    {
      id: '2',
      date: '2024-01-10',
      type: 'Lab Test',
      doctor: 'Dr. Patel',
      diagnosis: 'Vitamin D Deficiency',
      status: 'improving',
      notes: 'Vitamin D levels low. Started supplementation.',
      prescriptions: ['Vitamin D3 1000 IU daily']
    },
    {
      id: '3',
      date: '2023-12-20',
      type: 'Follow-up',
      doctor: 'Dr. Kumar',
      diagnosis: 'Upper Respiratory Infection',
      status: 'resolved',
      notes: 'Infection cleared completely. No further treatment needed.',
      prescriptions: []
    }
  ];

  const labResults = [
    {
      id: '1',
      date: '2024-01-12',
      test: 'HbA1c',
      result: '6.8%',
      range: '< 7.0%',
      status: 'normal'
    },
    {
      id: '2',
      date: '2024-01-12',
      test: 'Fasting Glucose',
      result: '95 mg/dL',
      range: '70-100 mg/dL',
      status: 'normal'
    },
    {
      id: '3',
      date: '2024-01-10',
      test: 'Vitamin D',
      result: '25 ng/mL',
      range: '30-50 ng/mL',
      status: 'low'
    },
    {
      id: '4',
      date: '2024-01-08',
      test: 'Total Cholesterol',
      result: '180 mg/dL',
      range: '< 200 mg/dL',
      status: 'normal'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'normal': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      case 'low': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400';
      case 'high': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      case 'active': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400';
      case 'completed': return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
      case 'ongoing': return 'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-400';
      case 'improving': return 'bg-cyan-100 text-cyan-800 dark:bg-cyan-900/20 dark:text-cyan-400';
      case 'resolved': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'increasing': return <TrendingUp className="w-3 h-3 text-red-500" />;
      case 'decreasing': return <TrendingUp className="w-3 h-3 text-green-500 rotate-180" />;
      case 'stable': return <Activity className="w-3 h-3 text-gray-500" />;
      default: return <Activity className="w-3 h-3 text-gray-500" />;
    }
  };

  const exportToFormat = (format: 'pdf' | 'fhir' | 'json') => {
    // Mock export functionality
    const exportData = {
      patient: user,
      vitals,
      medications,
      medicalHistory,
      labResults,
      exportDate: new Date().toISOString(),
      format
    };
    
    console.log(`Exporting to ${format.toUpperCase()}:`, exportData);
    
    // In a real app, this would trigger a download
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `health-records-${user.name}-${new Date().toISOString().split('T')[0]}.${format}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-7xl mx-auto space-y-6"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl">My Health Records</h1>
          <p className="text-gray-600 dark:text-gray-400">Complete overview of your health information</p>
        </div>
        <div className="flex space-x-2">
          <Button onClick={() => exportToFormat('pdf')} variant="outline">
            <Download className="w-4 h-4 mr-2" />
            PDF
          </Button>
          <Button onClick={() => exportToFormat('fhir')} variant="outline">
            <Download className="w-4 h-4 mr-2" />
            FHIR
          </Button>
          <Button onClick={() => exportToFormat('json')} className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white">
            <Download className="w-4 h-4 mr-2" />
            JSON
          </Button>
        </div>
      </div>

      {/* Health Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Heart className="w-5 h-5 text-red-500" />
            <span>Health Overview</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {Object.entries(vitals).map(([key, vital]) => (
              <div key={key} className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs text-gray-600 dark:text-gray-400 capitalize">
                    {key.replace(/([A-Z])/g, ' $1').toLowerCase()}
                  </span>
                  {getTrendIcon(vital.trend)}
                </div>
                <p className="text-lg">{vital.value}</p>
                <Badge className={getStatusColor(vital.status)} variant="secondary">
                  {vital.status}
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Main Content Tabs */}
      <Tabs defaultValue="history" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="history">Medical History</TabsTrigger>
          <TabsTrigger value="medications">Medications</TabsTrigger>
          <TabsTrigger value="labs">Lab Results</TabsTrigger>
          <TabsTrigger value="reports">Reports</TabsTrigger>
        </TabsList>

        <TabsContent value="history" className="space-y-4">
          <div className="flex space-x-4 mb-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
              <Input
                placeholder="Search medical history..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={filterType} onValueChange={setFilterType}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Filter by type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Records</SelectItem>
                <SelectItem value="consultation">Consultations</SelectItem>
                <SelectItem value="lab-test">Lab Tests</SelectItem>
                <SelectItem value="follow-up">Follow-ups</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-4">
            {medicalHistory.map((record) => (
              <Card key={record.id}>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <Badge variant="outline">{record.type}</Badge>
                        <Badge className={getStatusColor(record.status)} variant="secondary">
                          {record.status}
                        </Badge>
                        <span className="text-sm text-gray-500">{record.date}</span>
                      </div>
                      <h3 className="text-lg mb-2">{record.diagnosis}</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        Attended by {record.doctor}
                      </p>
                      <p className="text-sm">{record.notes}</p>
                      
                      {record.prescriptions.length > 0 && (
                        <div className="mt-3">
                          <p className="text-sm mb-1">Prescriptions:</p>
                          <div className="space-y-1">
                            {record.prescriptions.map((prescription, index) => (
                              <p key={index} className="text-xs bg-blue-50 dark:bg-blue-900/20 p-2 rounded">
                                {prescription}
                              </p>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                    
                    <Dialog>
                      <DialogTrigger asChild>
                        <Button variant="ghost" size="sm">
                          <Eye className="w-4 h-4" />
                        </Button>
                      </DialogTrigger>
                      <DialogContent className="max-w-2xl">
                        <DialogHeader>
                          <DialogTitle>Medical Record Details</DialogTitle>
                        </DialogHeader>
                        <div className="space-y-4">
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <Label className="text-sm">Date</Label>
                              <p>{record.date}</p>
                            </div>
                            <div>
                              <Label className="text-sm">Type</Label>
                              <p>{record.type}</p>
                            </div>
                            <div>
                              <Label className="text-sm">Doctor</Label>
                              <p>{record.doctor}</p>
                            </div>
                            <div>
                              <Label className="text-sm">Status</Label>
                              <Badge className={getStatusColor(record.status)} variant="secondary">
                                {record.status}
                              </Badge>
                            </div>
                          </div>
                          <div>
                            <Label className="text-sm">Diagnosis</Label>
                            <p>{record.diagnosis}</p>
                          </div>
                          <div>
                            <Label className="text-sm">Clinical Notes</Label>
                            <p>{record.notes}</p>
                          </div>
                          {record.prescriptions.length > 0 && (
                            <div>
                              <Label className="text-sm">Prescriptions</Label>
                              <div className="space-y-1">
                                {record.prescriptions.map((prescription, index) => (
                                  <p key={index} className="text-sm bg-gray-50 dark:bg-gray-800 p-2 rounded">
                                    {prescription}
                                  </p>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </DialogContent>
                    </Dialog>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="medications" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {medications.map((medication) => (
              <Card key={medication.id}>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-lg">{medication.name}</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {medication.dosage} • {medication.frequency}
                      </p>
                    </div>
                    <Badge className={getStatusColor(medication.status)} variant="secondary">
                      {medication.status}
                    </Badge>
                  </div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Prescribed by:</span>
                      <span>{medication.prescribedBy}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Start date:</span>
                      <span>{medication.startDate}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="labs" className="space-y-4">
          <div className="space-y-4">
            {labResults.map((lab) => (
              <Card key={lab.id}>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-lg">{lab.test}</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">{lab.date}</p>
                    </div>
                    <div className="text-right">
                      <div className="flex items-center space-x-2">
                        <span className="text-xl">{lab.result}</span>
                        <Badge className={getStatusColor(lab.status)} variant="secondary">
                          {lab.status}
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-500">Range: {lab.range}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="reports" className="space-y-4">
          <div className="text-center py-12">
            <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg mb-2">No Reports Available</h3>
            <p className="text-sm text-gray-500 mb-4">
              Medical reports and imaging studies will appear here
            </p>
            <Button variant="outline" onClick={() => exportToFormat('pdf')}>
              <Download className="w-4 h-4 mr-2" />
              Generate Summary Report
            </Button>
          </div>
        </TabsContent>
      </Tabs>
    </motion.div>
  );
};

export default PatientHealthRecords;