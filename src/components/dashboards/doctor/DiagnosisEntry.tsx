import React, { useState } from 'react';
import { motion } from 'motion/react';
import { 
  Search, 
  User, 
  Calendar, 
  Stethoscope, 
  AlertTriangle, 
  Plus, 
  X, 
  Languages,
  Save,
  FileText,
  Pill,
  Activity
} from 'lucide-react';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { Label } from '../../ui/label';
import { Textarea } from '../../ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../ui/select';
import { Badge } from '../../ui/badge';
import { Separator } from '../../ui/separator';
import { Avatar, AvatarFallback, AvatarImage } from '../../ui/avatar';
import { ScrollArea } from '../../ui/scroll-area';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../ui/tabs';
import { toast } from 'sonner@2.0.3';

const DiagnosisEntry: React.FC = () => {
  const [selectedPatient, setSelectedPatient] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [diagnosisSearch, setDiagnosisSearch] = useState('');
  const [selectedDiagnoses, setSelectedDiagnoses] = useState<string[]>([]);
  const [notes, setNotes] = useState('');
  const [prescriptions, setPrescriptions] = useState<string[]>([]);
  const [prescriptionInput, setPrescriptionInput] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Mock patient data
  const patients = [
    {
      id: '1',
      name: 'Rajesh Kumar',
      age: 45,
      gender: 'Male',
      phone: '+91 98765 43210',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=rajesh',
      allergies: ['Penicillin', 'Peanuts'],
      lastVisit: '2024-01-10'
    },
    {
      id: '2',
      name: 'Priya Sharma',
      age: 32,
      gender: 'Female',
      phone: '+91 87654 32109',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=priya',
      allergies: ['Lactose'],
      lastVisit: '2024-01-08'
    },
    {
      id: '3',
      name: 'Amit Patel',
      age: 28,
      gender: 'Male',
      phone: '+91 76543 21098',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=amit',
      allergies: [],
      lastVisit: '2024-01-12'
    }
  ];

  // Mock NAMASTE/ICD-11 diagnosis suggestions
  const diagnosisSuggestions = [
    { code: 'J00', name: 'Acute nasopharyngitis (common cold)', category: 'Respiratory' },
    { code: 'K59.0', name: 'Constipation', category: 'Digestive' },
    { code: 'M79.3', name: 'Panniculitis, unspecified', category: 'Musculoskeletal' },
    { code: 'R50.9', name: 'Fever, unspecified', category: 'General' },
    { code: 'I10', name: 'Essential (primary) hypertension', category: 'Cardiovascular' },
    { code: 'E11.9', name: 'Type 2 diabetes mellitus without complications', category: 'Endocrine' },
    { code: 'J45.9', name: 'Asthma, unspecified', category: 'Respiratory' },
    { code: 'M25.50', name: 'Pain in joint, unspecified', category: 'Musculoskeletal' }
  ];

  // Mock treatment recommendations
  const treatmentRecommendations = {
    ayush: [
      'Tulsi (Holy Basil) - 2 tablets twice daily for respiratory health',
      'Ashwagandha - 500mg daily for stress management',
      'Triphala - 1 tablet before bed for digestive health',
      'Turmeric (Curcumin) - 500mg twice daily for inflammation'
    ],
    modern: [
      'Paracetamol 500mg - Every 6 hours for fever/pain',
      'Amoxicillin 500mg - Three times daily for bacterial infections',
      'Omeprazole 20mg - Once daily for acid reflux',
      'Metformin 500mg - Twice daily for diabetes management'
    ]
  };

  const filteredPatients = patients.filter(patient =>
    patient.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    patient.phone.includes(searchQuery)
  );

  const filteredDiagnoses = diagnosisSuggestions.filter(diagnosis =>
    diagnosis.name.toLowerCase().includes(diagnosisSearch.toLowerCase()) ||
    diagnosis.code.toLowerCase().includes(diagnosisSearch.toLowerCase())
  );

  const addDiagnosis = (diagnosis: string) => {
    if (!selectedDiagnoses.includes(diagnosis)) {
      setSelectedDiagnoses(prev => [...prev, diagnosis]);
      setDiagnosisSearch('');
    }
  };

  const removeDiagnosis = (diagnosis: string) => {
    setSelectedDiagnoses(prev => prev.filter(d => d !== diagnosis));
  };

  const addPrescription = () => {
    if (prescriptionInput.trim() && !prescriptions.includes(prescriptionInput.trim())) {
      setPrescriptions(prev => [...prev, prescriptionInput.trim()]);
      setPrescriptionInput('');
    }
  };

  const removePrescription = (prescription: string) => {
    setPrescriptions(prev => prev.filter(p => p !== prescription));
  };

  const handleSubmit = async () => {
    if (!selectedPatient || selectedDiagnoses.length === 0) {
      toast.error('Please select a patient and at least one diagnosis');
      return;
    }

    setIsSubmitting(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));

    const diagnosisRecord = {
      patientId: selectedPatient.id,
      diagnoses: selectedDiagnoses,
      notes,
      prescriptions,
      createdAt: new Date().toISOString(),
      doctorId: 'current-doctor-id'
    };

    console.log('Diagnosis record:', diagnosisRecord);
    toast.success('Diagnosis saved successfully!');
    
    // Reset form
    setSelectedDiagnoses([]);
    setNotes('');
    setPrescriptions([]);
    setIsSubmitting(false);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-6xl mx-auto space-y-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl">Diagnosis Entry</h1>
          <p className="text-gray-600 dark:text-gray-400">Enter diagnosis and treatment information</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Patient Selection */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Search className="w-5 h-5" />
              <span>Select Patient</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="relative">
              <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
              <Input
                placeholder="Search by name or phone..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>

            <ScrollArea className="h-64">
              <div className="space-y-2">
                {filteredPatients.map((patient) => (
                  <div
                    key={patient.id}
                    onClick={() => setSelectedPatient(patient)}
                    className={`p-3 rounded-lg cursor-pointer transition-colors ${
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
                          {patient.age}yr, {patient.gender}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>

            {selectedPatient && (
              <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                <div className="flex items-center space-x-3 mb-3">
                  <Avatar className="w-12 h-12">
                    <AvatarImage src={selectedPatient.avatar} alt={selectedPatient.name} />
                    <AvatarFallback>{selectedPatient.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                  </Avatar>
                  <div>
                    <h4 className="text-sm">{selectedPatient.name}</h4>
                    <p className="text-xs text-gray-600 dark:text-gray-400">
                      Age {selectedPatient.age} • {selectedPatient.gender}
                    </p>
                    <p className="text-xs text-gray-600 dark:text-gray-400">{selectedPatient.phone}</p>
                  </div>
                </div>
                
                {selectedPatient.allergies.length > 0 && (
                  <div>
                    <p className="text-xs text-red-600 dark:text-red-400 mb-1 flex items-center">
                      <AlertTriangle className="w-3 h-3 mr-1" />
                      Allergies:
                    </p>
                    <div className="flex flex-wrap gap-1">
                      {selectedPatient.allergies.map((allergy) => (
                        <Badge key={allergy} variant="destructive" className="text-xs">
                          {allergy}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Diagnosis Entry */}
        <div className="lg:col-span-2 space-y-6">
          {selectedPatient ? (
            <>
              {/* Diagnosis Search */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Stethoscope className="w-5 h-5" />
                    <span>Diagnosis (NAMASTE/ICD-11)</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="relative">
                    <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
                    <Input
                      placeholder="Search diagnosis codes or conditions..."
                      value={diagnosisSearch}
                      onChange={(e) => setDiagnosisSearch(e.target.value)}
                      className="pl-10"
                    />
                  </div>

                  {diagnosisSearch && (
                    <div className="max-h-32 overflow-y-auto border rounded-lg">
                      {filteredDiagnoses.map((diagnosis) => (
                        <div
                          key={diagnosis.code}
                          onClick={() => addDiagnosis(`${diagnosis.code} - ${diagnosis.name}`)}
                          className="p-2 hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer border-b last:border-0"
                        >
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="text-sm">{diagnosis.name}</p>
                              <p className="text-xs text-gray-500">{diagnosis.code} • {diagnosis.category}</p>
                            </div>
                            <Plus className="w-4 h-4 text-gray-400" />
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {selectedDiagnoses.length > 0 && (
                    <div>
                      <Label>Selected Diagnoses</Label>
                      <div className="flex flex-wrap gap-2 mt-2">
                        {selectedDiagnoses.map((diagnosis) => (
                          <Badge key={diagnosis} variant="secondary" className="flex items-center space-x-1">
                            <span className="text-xs">{diagnosis}</span>
                            <X
                              className="w-3 h-3 cursor-pointer hover:text-red-500"
                              onClick={() => removeDiagnosis(diagnosis)}
                            />
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Translation & Treatment Recommendations */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Languages className="w-5 h-5 text-cyan-500" />
                    <span>Treatment Recommendations</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Tabs defaultValue="ayush" className="w-full">
                    <TabsList className="grid w-full grid-cols-2">
                      <TabsTrigger value="ayush">AYUSH Treatments</TabsTrigger>
                      <TabsTrigger value="modern">Modern Medicine</TabsTrigger>
                    </TabsList>
                    
                    <TabsContent value="ayush" className="mt-4">
                      <ScrollArea className="h-48">
                        <div className="space-y-2">
                          {treatmentRecommendations.ayush.map((treatment, index) => (
                            <div
                              key={index}
                              className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg cursor-pointer hover:bg-green-100 dark:hover:bg-green-900/30 transition-colors"
                              onClick={() => {
                                if (!prescriptions.includes(treatment)) {
                                  setPrescriptions(prev => [...prev, treatment]);
                                }
                              }}
                            >
                              <p className="text-sm text-green-800 dark:text-green-200">{treatment}</p>
                            </div>
                          ))}
                        </div>
                      </ScrollArea>
                    </TabsContent>
                    
                    <TabsContent value="modern" className="mt-4">
                      <ScrollArea className="h-48">
                        <div className="space-y-2">
                          {treatmentRecommendations.modern.map((treatment, index) => (
                            <div
                              key={index}
                              className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg cursor-pointer hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors"
                              onClick={() => {
                                if (!prescriptions.includes(treatment)) {
                                  setPrescriptions(prev => [...prev, treatment]);
                                }
                              }}
                            >
                              <p className="text-sm text-blue-800 dark:text-blue-200">{treatment}</p>
                            </div>
                          ))}
                        </div>
                      </ScrollArea>
                    </TabsContent>
                  </Tabs>
                </CardContent>
              </Card>

              {/* Prescriptions */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Pill className="w-5 h-5" />
                    <span>Prescriptions</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex space-x-2">
                    <Input
                      placeholder="Enter prescription or medication..."
                      value={prescriptionInput}
                      onChange={(e) => setPrescriptionInput(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addPrescription())}
                    />
                    <Button type="button" onClick={addPrescription} variant="outline">
                      Add
                    </Button>
                  </div>

                  {prescriptions.length > 0 && (
                    <div className="space-y-2">
                      {prescriptions.map((prescription, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                          <span className="text-sm">{prescription}</span>
                          <X
                            className="w-4 h-4 cursor-pointer hover:text-red-500"
                            onClick={() => removePrescription(prescription)}
                          />
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Clinical Notes */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <FileText className="w-5 h-5" />
                    <span>Clinical Notes</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Textarea
                    placeholder="Enter clinical observations, patient symptoms, treatment plan, etc..."
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    rows={6}
                  />
                </CardContent>
              </Card>

              {/* Save Button */}
              <div className="flex justify-end space-x-4 pt-4">
                <Button variant="outline" disabled={isSubmitting}>
                  Cancel
                </Button>
                <Button 
                  onClick={handleSubmit}
                  disabled={!selectedPatient || selectedDiagnoses.length === 0 || isSubmitting}
                  className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white px-8"
                >
                  {isSubmitting ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                      Saving...
                    </>
                  ) : (
                    <>
                      <Save className="w-4 h-4 mr-2" />
                      Save Diagnosis
                    </>
                  )}
                </Button>
              </div>
            </>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12 text-center">
                <User className="w-12 h-12 text-gray-400 mb-4" />
                <h3 className="text-lg mb-2">Select a Patient</h3>
                <p className="text-sm text-gray-500">
                  Choose a patient from the list to start entering diagnosis information
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default DiagnosisEntry;