import React, { useState } from 'react';
import { motion } from 'motion/react';
import { 
  QrCode, 
  Download, 
  Share2, 
  Eye, 
  EyeOff, 
  Shield,
  User,
  Phone,
  Mail,
  Calendar,
  MapPin,
  AlertTriangle,
  Heart,
  Activity
} from 'lucide-react';
import { Button } from '../../ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Badge } from '../../ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '../../ui/avatar';
import { Switch } from '../../ui/switch';
import { Label } from '../../ui/label';
import { Separator } from '../../ui/separator';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../../ui/dialog';
import QRCode from 'qrcode';
import type { User } from '../../../App';

interface PatientHealthPassportProps {
  user: User;
}

const PatientHealthPassport: React.FC<PatientHealthPassportProps> = ({ user }) => {
  const [qrCodeDataURL, setQrCodeDataURL] = useState<string>('');
  const [showSensitiveInfo, setShowSensitiveInfo] = useState(false);
  const [isGeneratingQR, setIsGeneratingQR] = useState(false);

  // Mock patient health passport data
  const passportData = {
    id: 'HP-2024-001',
    patientId: user.id,
    name: user.name,
    email: user.email,
    phone: '+91 98765 43210',
    dateOfBirth: '1988-05-15',
    gender: 'Male',
    bloodGroup: 'O+',
    address: '123 Health Street, Mumbai, Maharashtra 400001',
    emergencyContact: {
      name: 'Sunita Kumar',
      phone: '+91 87654 32109',
      relation: 'Spouse'
    },
    medicalInfo: {
      allergies: ['Penicillin', 'Peanuts'],
      chronicConditions: ['Type 2 Diabetes', 'Hypertension'],
      currentMedications: ['Metformin 500mg', 'Amlodipine 5mg'],
      lastCheckup: '2024-01-15',
      vaccinations: ['COVID-19 (Booster)', 'Influenza 2023'],
      insuranceProvider: 'Star Health Insurance',
      policyNumber: 'SH123456789'
    },
    securityLevel: 'Medium',
    lastUpdated: '2024-01-15',
    version: '1.2'
  };

  const generateQRCode = async () => {
    setIsGeneratingQR(true);
    try {
      // Create a secure, minimal data set for QR code
      const qrData = {
        id: passportData.id,
        name: passportData.name,
        dob: passportData.dateOfBirth,
        bloodGroup: passportData.bloodGroup,
        emergencyContact: passportData.emergencyContact.phone,
        allergies: passportData.medicalInfo.allergies,
        url: `https://swasthyasetu.health/passport/${passportData.id}`,
        timestamp: new Date().toISOString()
      };

      const qrString = await QRCode.toDataURL(JSON.stringify(qrData), {
        width: 300,
        margin: 2,
        color: {
          dark: '#1f2937',
          light: '#ffffff'
        }
      });
      
      setQrCodeDataURL(qrString);
    } catch (error) {
      console.error('Error generating QR code:', error);
    } finally {
      setIsGeneratingQR(false);
    }
  };

  const downloadPassport = () => {
    // Mock download functionality
    const passportHTML = `
      <html>
        <head><title>Health Passport - ${passportData.name}</title></head>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
          <h1>SwasthyaSetu Health Passport</h1>
          <h2>${passportData.name}</h2>
          <p><strong>ID:</strong> ${passportData.id}</p>
          <p><strong>Date of Birth:</strong> ${passportData.dateOfBirth}</p>
          <p><strong>Blood Group:</strong> ${passportData.bloodGroup}</p>
          <p><strong>Emergency Contact:</strong> ${passportData.emergencyContact.name} - ${passportData.emergencyContact.phone}</p>
          <h3>Medical Information</h3>
          <p><strong>Allergies:</strong> ${passportData.medicalInfo.allergies.join(', ')}</p>
          <p><strong>Current Medications:</strong> ${passportData.medicalInfo.currentMedications.join(', ')}</p>
          <p><strong>Chronic Conditions:</strong> ${passportData.medicalInfo.chronicConditions.join(', ')}</p>
          ${qrCodeDataURL ? `<img src="${qrCodeDataURL}" alt="QR Code" style="margin-top: 20px;">` : ''}
        </body>
      </html>
    `;

    const blob = new Blob([passportHTML], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `health-passport-${passportData.name.replace(/\s+/g, '-').toLowerCase()}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const sharePassport = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'My Health Passport',
          text: `Health Passport for ${passportData.name}`,
          url: `https://swasthyasetu.health/passport/${passportData.id}`
        });
      } catch (error) {
        console.error('Error sharing:', error);
      }
    } else {
      // Fallback for browsers that don't support native sharing
      navigator.clipboard.writeText(`https://swasthyasetu.health/passport/${passportData.id}`);
      // toast.success('Link copied to clipboard!');
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto space-y-6"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl">Health Passport</h1>
          <p className="text-gray-600 dark:text-gray-400">Your digital health identity and emergency information</p>
        </div>
        <div className="flex space-x-2">
          <Button onClick={sharePassport} variant="outline">
            <Share2 className="w-4 h-4 mr-2" />
            Share
          </Button>
          <Button onClick={downloadPassport} className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white">
            <Download className="w-4 h-4 mr-2" />
            Download
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* QR Code Section */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <QrCode className="w-5 h-5" />
              <span>QR Code</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-col items-center space-y-4">
              {qrCodeDataURL ? (
                <div className="p-4 bg-white rounded-lg shadow-inner">
                  <img src={qrCodeDataURL} alt="Health Passport QR Code" className="w-full max-w-xs" />
                </div>
              ) : (
                <div className="w-64 h-64 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
                  <QrCode className="w-16 h-16 text-gray-400" />
                </div>
              )}
              
              <Button 
                onClick={generateQRCode} 
                disabled={isGeneratingQR}
                className="w-full bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white"
              >
                {isGeneratingQR ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                    Generating...
                  </>
                ) : (
                  <>
                    <QrCode className="w-4 h-4 mr-2" />
                    Generate QR Code
                  </>
                )}
              </Button>
            </div>

            <div className="text-center text-sm text-gray-600 dark:text-gray-400">
              <p>Scan this code for emergency access to your basic health information</p>
            </div>

            {/* Security Settings */}
            <div className="space-y-3">
              <Separator />
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Shield className="w-4 h-4 text-gray-600" />
                  <Label htmlFor="sensitive-info" className="text-sm">Show sensitive information</Label>
                </div>
                <Switch
                  id="sensitive-info"
                  checked={showSensitiveInfo}
                  onCheckedChange={setShowSensitiveInfo}
                />
              </div>
              <p className="text-xs text-gray-500">
                When enabled, includes medical history and contact details in QR code
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Passport Information */}
        <div className="lg:col-span-2 space-y-6">
          {/* Personal Information */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <User className="w-5 h-5" />
                <span>Personal Information</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-start space-x-4 mb-6">
                <Avatar className="w-20 h-20">
                  <AvatarImage src={user.avatar} alt={passportData.name} />
                  <AvatarFallback className="text-xl">{passportData.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <h2 className="text-2xl mb-2">{passportData.name}</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div className="flex items-center space-x-2">
                      <Calendar className="w-4 h-4 text-gray-400" />
                      <span>Born {passportData.dateOfBirth}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Activity className="w-4 h-4 text-gray-400" />
                      <span>{passportData.gender}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Heart className="w-4 h-4 text-red-500" />
                      <span>Blood Group: {passportData.bloodGroup}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Shield className="w-4 h-4 text-gray-400" />
                      <span>ID: {passportData.id}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-3">
                  <h4 className="text-sm text-gray-600 dark:text-gray-400">Contact Information</h4>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2 text-sm">
                      <Phone className="w-4 h-4 text-gray-400" />
                      <span>{showSensitiveInfo ? passportData.phone : '••••••••••'}</span>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setShowSensitiveInfo(!showSensitiveInfo)}
                      >
                        {showSensitiveInfo ? <EyeOff className="w-3 h-3" /> : <Eye className="w-3 h-3" />}
                      </Button>
                    </div>
                    <div className="flex items-center space-x-2 text-sm">
                      <Mail className="w-4 h-4 text-gray-400" />
                      <span>{showSensitiveInfo ? passportData.email : '••••••@••••.com'}</span>
                    </div>
                    <div className="flex items-start space-x-2 text-sm">
                      <MapPin className="w-4 h-4 text-gray-400 mt-0.5" />
                      <span className="flex-1">
                        {showSensitiveInfo ? passportData.address : '•••••••••••••••••••••••••'}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  <h4 className="text-sm text-gray-600 dark:text-gray-400">Emergency Contact</h4>
                  <div className="p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                    <div className="flex items-center space-x-2 mb-1">
                      <AlertTriangle className="w-4 h-4 text-red-500" />
                      <span className="text-sm">{passportData.emergencyContact.name}</span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {passportData.emergencyContact.relation}
                    </p>
                    <p className="text-sm">
                      {showSensitiveInfo ? passportData.emergencyContact.phone : '••••••••••'}
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Medical Information */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Heart className="w-5 h-5 text-red-500" />
                <span>Medical Information</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Allergies */}
              <div>
                <h4 className="text-sm text-gray-600 dark:text-gray-400 mb-2">Allergies</h4>
                <div className="flex flex-wrap gap-2">
                  {passportData.medicalInfo.allergies.map((allergy) => (
                    <Badge key={allergy} variant="destructive" className="flex items-center space-x-1">
                      <AlertTriangle className="w-3 h-3" />
                      <span>{allergy}</span>
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Chronic Conditions */}
              <div>
                <h4 className="text-sm text-gray-600 dark:text-gray-400 mb-2">Chronic Conditions</h4>
                <div className="flex flex-wrap gap-2">
                  {passportData.medicalInfo.chronicConditions.map((condition) => (
                    <Badge key={condition} variant="secondary" className="bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-400">
                      {condition}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Current Medications */}
              <div>
                <h4 className="text-sm text-gray-600 dark:text-gray-400 mb-2">Current Medications</h4>
                <div className="space-y-2">
                  {passportData.medicalInfo.currentMedications.map((medication) => (
                    <div key={medication} className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded text-sm">
                      {medication}
                    </div>
                  ))}
                </div>
              </div>

              {/* Vaccinations */}
              <div>
                <h4 className="text-sm text-gray-600 dark:text-gray-400 mb-2">Recent Vaccinations</h4>
                <div className="flex flex-wrap gap-2">
                  {passportData.medicalInfo.vaccinations.map((vaccination) => (
                    <Badge key={vaccination} variant="secondary" className="bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400">
                      {vaccination}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Insurance Information */}
              {showSensitiveInfo && (
                <div>
                  <h4 className="text-sm text-gray-600 dark:text-gray-400 mb-2">Insurance Information</h4>
                  <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <p className="text-sm mb-1">
                      <strong>Provider:</strong> {passportData.medicalInfo.insuranceProvider}
                    </p>
                    <p className="text-sm">
                      <strong>Policy Number:</strong> {passportData.medicalInfo.policyNumber}
                    </p>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Passport Metadata */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Shield className="w-5 h-5" />
                <span>Passport Information</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <p className="text-gray-600 dark:text-gray-400">Security Level</p>
                  <Badge variant="outline">{passportData.securityLevel}</Badge>
                </div>
                <div>
                  <p className="text-gray-600 dark:text-gray-400">Last Updated</p>
                  <p>{passportData.lastUpdated}</p>
                </div>
                <div>
                  <p className="text-gray-600 dark:text-gray-400">Version</p>
                  <p>{passportData.version}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </motion.div>
  );
};

export default PatientHealthPassport;