import React, { useState } from 'react';
import { motion } from 'motion/react';
import { 
  Search, 
  Filter, 
  Calendar, 
  User, 
  FileText, 
  Download,
  Eye,
  Clock,
  Activity,
  AlertTriangle,
  CheckCircle,
  Heart
} from 'lucide-react';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Badge } from '../../ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '../../ui/avatar';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../ui/tabs';
import { ScrollArea } from '../../ui/scroll-area';
import { Separator } from '../../ui/separator';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../../ui/dialog';

const ProblemListHistory: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedPatient, setSelectedPatient] = useState<any>(null);
  const [filterStatus, setFilterStatus] = useState('all');
  const [selectedRecord, setSelectedRecord] = useState<any>(null);

  // Mock patient data with medical history
  const patients = [
    {
      id: '1',
      name: 'Rajesh Kumar',
      age: 45,
      gender: 'Male',
      phone: '+91 98765 43210',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=rajesh',
      status: 'active',
      lastVisit: '2024-01-15',
      vitals: {
        bloodPressure: '140/90',
        heartRate: '78 bpm',
        temperature: '98.6°F',
        weight: '75 kg',
        height: '170 cm'
      },
      allergies: ['Penicillin', 'Peanuts'],
      currentMedications: ['Amlodipine 5mg', 'Metformin 500mg'],
      totalVisits: 12,
      diagnoses: [
        {
          id: '1',
          date: '2024-01-15',
          diagnosis: 'I10 - Essential (primary) hypertension',
          status: 'ongoing',
          notes: 'Blood pressure remains elevated. Continue current medication.',
          prescriptions: ['Amlodipine 5mg once daily', 'Regular BP monitoring'],
          doctor: 'Dr. Smith'
        },
        {
          id: '2',
          date: '2024-01-10',
          diagnosis: 'E11.9 - Type 2 diabetes mellitus without complications',
          status: 'stable',
          notes: 'HbA1c levels improved. Continue current management.',
          prescriptions: ['Metformin 500mg twice daily', 'Dietary modifications'],
          doctor: 'Dr. Smith'
        }
      ]
    },
    {
      id: '2',
      name: 'Priya Sharma',
      age: 32,
      gender: 'Female',
      phone: '+91 87654 32109',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=priya',
      status: 'monitoring',
      lastVisit: '2024-01-12',
      vitals: {
        bloodPressure: '120/80',
        heartRate: '72 bpm',
        temperature: '98.2°F',
        weight: '58 kg',
        height: '162 cm'
      },
      allergies: ['Lactose'],
      currentMedications: ['Iron supplements', 'Prenatal vitamins'],
      totalVisits: 8,
      diagnoses: [
        {
          id: '1',
          date: '2024-01-12',
          diagnosis: 'O99.0 - Anemia complicating pregnancy',
          status: 'improving',
          notes: 'Iron levels improving with supplementation.',
          prescriptions: ['Iron sulfate 325mg twice daily', 'Prenatal vitamins'],
          doctor: 'Dr. Patel'
        }
      ]
    },
    {
      id: '3',
      name: 'Amit Patel',
      age: 28,
      gender: 'Male',
      phone: '+91 76543 21098',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=amit',
      status: 'recovered',
      lastVisit: '2024-01-08',
      vitals: {
        bloodPressure: '118/75',
        heartRate: '68 bpm',
        temperature: '98.4°F',
        weight: '70 kg',
        height: '175 cm'
      },
      allergies: [],
      currentMedications: [],
      totalVisits: 3,
      diagnoses: [
        {
          id: '1',
          date: '2024-01-08',
          diagnosis: 'J45.9 - Asthma, unspecified',
          status: 'resolved',
          notes: 'Asthma symptoms well controlled with inhaler.',
          prescriptions: ['Salbutamol inhaler as needed'],
          doctor: 'Dr. Johnson'
        }
      ]
    }
  ];

  const filteredPatients = patients.filter(patient => {
    const matchesSearch = patient.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         patient.phone.includes(searchQuery);
    const matchesStatus = filterStatus === 'all' || patient.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400';
      case 'monitoring': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400';
      case 'recovered': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      case 'stable': return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/20 dark:text-emerald-400';
      case 'ongoing': return 'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-400';
      case 'improving': return 'bg-cyan-100 text-cyan-800 dark:bg-cyan-900/20 dark:text-cyan-400';
      case 'resolved': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
      case 'ongoing': return <Activity className="w-3 h-3" />;
      case 'monitoring': return <Eye className="w-3 h-3" />;
      case 'recovered':
      case 'resolved': return <CheckCircle className="w-3 h-3" />;
      case 'stable':
      case 'improving': return <Heart className="w-3 h-3" />;
      default: return <Clock className="w-3 h-3" />;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-7xl mx-auto space-y-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl">Problem List History</h1>
          <p className="text-gray-600 dark:text-gray-400">View patient medical history and current status</p>
        </div>
        <Button className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white">
          <Download className="w-4 h-4 mr-2" />
          Export Report
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Patient List */}
        <Card>
          <CardHeader>
            <CardTitle>Patient Search</CardTitle>
            <div className="space-y-4">
              <div className="relative">
                <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
                <Input
                  placeholder="Search by name or phone..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger>
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Patients</SelectItem>
                  <SelectItem value="active">Active</SelectItem>
                  <SelectItem value="monitoring">Monitoring</SelectItem>
                  <SelectItem value="recovered">Recovered</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardHeader>
          <CardContent>
            <ScrollArea className="h-96">
              <div className="space-y-3">
                {filteredPatients.map((patient) => (
                  <div
                    key={patient.id}
                    onClick={() => setSelectedPatient(patient)}
                    className={`p-4 rounded-lg cursor-pointer transition-colors ${
                      selectedPatient?.id === patient.id
                        ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white'
                        : 'bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700'
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <Avatar className="w-10 h-10">
                        <AvatarImage src={patient.avatar} alt={patient.name} />
                        <AvatarFallback>{patient.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <p className="text-sm">{patient.name}</p>
                        <p className={`text-xs ${selectedPatient?.id === patient.id ? 'text-indigo-100' : 'text-gray-500'}`}>
                          {patient.age}yr • {patient.totalVisits} visits
                        </p>
                      </div>
                      <Badge className={getStatusColor(patient.status)} variant="secondary">
                        {patient.status}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>

        {/* Patient Details */}
        <div className="lg:col-span-2">
          {selectedPatient ? (
            <div className="space-y-6">
              {/* Patient Overview */}
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <Avatar className="w-16 h-16">
                        <AvatarImage src={selectedPatient.avatar} alt={selectedPatient.name} />
                        <AvatarFallback>{selectedPatient.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                      </Avatar>
                      <div>
                        <h2 className="text-xl">{selectedPatient.name}</h2>
                        <p className="text-gray-600 dark:text-gray-400">
                          {selectedPatient.age} years • {selectedPatient.gender}
                        </p>
                        <p className="text-sm text-gray-500">{selectedPatient.phone}</p>
                      </div>
                    </div>
                    <Badge className={getStatusColor(selectedPatient.status)} variant="secondary">
                      {getStatusIcon(selectedPatient.status)}
                      <span className="ml-1 capitalize">{selectedPatient.status}</span>
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <Tabs defaultValue="vitals" className="w-full">
                    <TabsList className="grid w-full grid-cols-4">
                      <TabsTrigger value="vitals">Vitals</TabsTrigger>
                      <TabsTrigger value="allergies">Allergies</TabsTrigger>
                      <TabsTrigger value="medications">Medications</TabsTrigger>
                      <TabsTrigger value="history">History</TabsTrigger>
                    </TabsList>
                    
                    <TabsContent value="vitals" className="mt-4">
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                          <p className="text-xs text-gray-600 dark:text-gray-400">Blood Pressure</p>
                          <p className="text-lg text-blue-600 dark:text-blue-400">{selectedPatient.vitals.bloodPressure}</p>
                        </div>
                        <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                          <p className="text-xs text-gray-600 dark:text-gray-400">Heart Rate</p>
                          <p className="text-lg text-green-600 dark:text-green-400">{selectedPatient.vitals.heartRate}</p>
                        </div>
                        <div className="p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                          <p className="text-xs text-gray-600 dark:text-gray-400">Temperature</p>
                          <p className="text-lg text-orange-600 dark:text-orange-400">{selectedPatient.vitals.temperature}</p>
                        </div>
                        <div className="p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                          <p className="text-xs text-gray-600 dark:text-gray-400">Weight</p>
                          <p className="text-lg text-purple-600 dark:text-purple-400">{selectedPatient.vitals.weight}</p>
                        </div>
                        <div className="p-3 bg-indigo-50 dark:bg-indigo-900/20 rounded-lg">
                          <p className="text-xs text-gray-600 dark:text-gray-400">Height</p>
                          <p className="text-lg text-indigo-600 dark:text-indigo-400">{selectedPatient.vitals.height}</p>
                        </div>
                        <div className="p-3 bg-cyan-50 dark:bg-cyan-900/20 rounded-lg">
                          <p className="text-xs text-gray-600 dark:text-gray-400">Last Visit</p>
                          <p className="text-lg text-cyan-600 dark:text-cyan-400">
                            {new Date(selectedPatient.lastVisit).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                    </TabsContent>
                    
                    <TabsContent value="allergies" className="mt-4">
                      {selectedPatient.allergies.length > 0 ? (
                        <div className="space-y-2">
                          {selectedPatient.allergies.map((allergy, index) => (
                            <div key={index} className="flex items-center space-x-2 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                              <AlertTriangle className="w-4 h-4 text-red-500" />
                              <span className="text-red-700 dark:text-red-300">{allergy}</span>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p className="text-gray-500 text-center py-4">No known allergies</p>
                      )}
                    </TabsContent>
                    
                    <TabsContent value="medications" className="mt-4">
                      {selectedPatient.currentMedications.length > 0 ? (
                        <div className="space-y-2">
                          {selectedPatient.currentMedications.map((medication, index) => (
                            <div key={index} className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                              <span className="text-blue-700 dark:text-blue-300">{medication}</span>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p className="text-gray-500 text-center py-4">No current medications</p>
                      )}
                    </TabsContent>
                    
                    <TabsContent value="history" className="mt-4">
                      <div className="space-y-4">
                        {selectedPatient.diagnoses.map((diagnosis, index) => (
                          <div key={diagnosis.id} className="p-4 border rounded-lg">
                            <div className="flex items-center justify-between mb-2">
                              <Badge className={getStatusColor(diagnosis.status)} variant="secondary">
                                {getStatusIcon(diagnosis.status)}
                                <span className="ml-1 capitalize">{diagnosis.status}</span>
                              </Badge>
                              <span className="text-xs text-gray-500">{diagnosis.date}</span>
                            </div>
                            <h4 className="text-sm mb-2">{diagnosis.diagnosis}</h4>
                            <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">{diagnosis.notes}</p>
                            <p className="text-xs text-gray-500">by {diagnosis.doctor}</p>
                            
                            <Dialog>
                              <DialogTrigger asChild>
                                <Button variant="ghost" size="sm" className="mt-2">
                                  <Eye className="w-3 h-3 mr-1" />
                                  View Details
                                </Button>
                              </DialogTrigger>
                              <DialogContent className="max-w-2xl">
                                <DialogHeader>
                                  <DialogTitle>Diagnosis Details</DialogTitle>
                                </DialogHeader>
                                <div className="space-y-4">
                                  <div>
                                    <Label className="text-sm">Diagnosis</Label>
                                    <p className="text-sm">{diagnosis.diagnosis}</p>
                                  </div>
                                  <div>
                                    <Label className="text-sm">Date</Label>
                                    <p className="text-sm">{diagnosis.date}</p>
                                  </div>
                                  <div>
                                    <Label className="text-sm">Status</Label>
                                    <Badge className={getStatusColor(diagnosis.status)} variant="secondary">
                                      {diagnosis.status}
                                    </Badge>
                                  </div>
                                  <div>
                                    <Label className="text-sm">Clinical Notes</Label>
                                    <p className="text-sm">{diagnosis.notes}</p>
                                  </div>
                                  <div>
                                    <Label className="text-sm">Prescriptions</Label>
                                    <div className="space-y-1">
                                      {diagnosis.prescriptions.map((prescription, idx) => (
                                        <p key={idx} className="text-sm bg-gray-50 dark:bg-gray-800 p-2 rounded">
                                          {prescription}
                                        </p>
                                      ))}
                                    </div>
                                  </div>
                                  <div>
                                    <Label className="text-sm">Attending Doctor</Label>
                                    <p className="text-sm">{diagnosis.doctor}</p>
                                  </div>
                                </div>
                              </DialogContent>
                            </Dialog>
                          </div>
                        ))}
                      </div>
                    </TabsContent>
                  </Tabs>
                </CardContent>
              </Card>
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12 text-center">
                <User className="w-12 h-12 text-gray-400 mb-4" />
                <h3 className="text-lg mb-2">Select a Patient</h3>
                <p className="text-sm text-gray-500">
                  Choose a patient from the list to view their medical history and current status
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default ProblemListHistory;