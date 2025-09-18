import React from 'react';
<<<<<<< HEAD
=======

>>>>>>> 63416a3 (added icons and public folder)
import { motion } from 'motion/react';
import { 
  Users, 
  Calendar, 
  TrendingUp, 
  Clock,
  Activity,
  AlertTriangle,
  CheckCircle,
  Heart
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Progress } from '../../ui/progress';
import { Badge } from '../../ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '../../ui/avatar';
import { Button } from '../../ui/button';
import { ImageWithFallback } from '../../figma/ImageWithFallback';
import type { User } from '../../../App';

interface DoctorDashboardHomeProps {
  user: User;
}

const DoctorDashboardHome: React.FC<DoctorDashboardHomeProps> = ({ user }) => {
  const stats = [
    { 
      title: 'Total Patients', 
      value: '248', 
      change: '+12%', 
      icon: Users, 
      color: 'text-blue-600', 
      bgColor: 'bg-blue-50 dark:bg-blue-900/20' 
    },
    { 
      title: 'Today\'s Appointments', 
      value: '18', 
      change: '+3', 
      icon: Calendar, 
      color: 'text-green-600', 
      bgColor: 'bg-green-50 dark:bg-green-900/20' 
    },
    { 
      title: 'Pending Diagnoses', 
      value: '7', 
      change: '-2', 
      icon: Activity, 
      color: 'text-orange-600', 
      bgColor: 'bg-orange-50 dark:bg-orange-900/20' 
    },
    { 
      title: 'Success Rate', 
      value: '96.2%', 
      change: '+1.2%', 
      icon: TrendingUp, 
      color: 'text-purple-600', 
      bgColor: 'bg-purple-50 dark:bg-purple-900/20' 
    },
  ];

  const recentPatients = [
    { 
      id: '1', 
      name: 'Rajesh Kumar', 
      age: 45, 
      condition: 'Hypertension', 
      status: 'Stable', 
      lastVisit: '2 hours ago',
      avatar:"./man.png"
    },
    { 
      id: '2', 
      name: 'Priya Sharma', 
      age: 32, 
      condition: 'Diabetes Type 2', 
      status: 'Monitoring', 
      lastVisit: '1 day ago',
      avatar: './woman.png'
    },
    { 
      id: '3', 
      name: 'Amit Patel', 
      age: 28, 
      condition: 'Allergic Rhinitis', 
      status: 'Recovered', 
      lastVisit: '3 days ago',
<<<<<<< HEAD
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=amit'
=======
      avatar: './man.png'
>>>>>>> 63416a3 (added icons and public folder)
    },
    { 
      id: '4', 
      name: 'Sunita Verma', 
      age: 52, 
      condition: 'Arthritis', 
      status: 'Treatment', 
      lastVisit: '1 week ago',
<<<<<<< HEAD
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=sunita'
=======
      avatar: './woman.png'
>>>>>>> 63416a3 (added icons and public folder)
    },
  ];

  const todaySchedule = [
    { time: '09:00 AM', patient: 'Vikram Singh', type: 'Consultation' },
    { time: '10:30 AM', patient: 'Meera Joshi', type: 'Follow-up' },
    { time: '11:45 AM', patient: 'Ravi Gupta', type: 'Check-up' },
    { time: '02:00 PM', patient: 'Kavita Nair', type: 'Consultation' },
    { time: '03:30 PM', patient: 'Manoj Yadav', type: 'Treatment' },
  ];

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'stable': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      case 'monitoring': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400';
      case 'treatment': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400';
      case 'recovered': return 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/20 dark:text-emerald-400';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400';
    }
  };

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-indigo-600 via-purple-600 to-cyan-500 p-8 text-white"
      >
        <div className="relative z-10">
          <h1 className="text-3xl mb-2">Good morning, Dr. {user.name}!</h1>
          <p className="text-indigo-100 text-lg">
            You have 18 appointments today. Stay focused and make a difference!
          </p>
          <div className="mt-6 flex items-center space-x-4">
            <Button variant="secondary" className="bg-white/20 text-white hover:bg-white/30">
              View Today's Schedule
            </Button>
            <Button variant="ghost" className="text-white hover:bg-white/10">
              Quick Actions
            </Button>
          </div>
        </div>
        
        {/* Background decoration */}
        <div className="absolute right-0 top-0 opacity-20">
          <ImageWithFallback
            src="https://images.unsplash.com/photo-1690784261287-f32b7b79b29f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkb2N0b3IlMjBzdGV0aG9zY29wZSUyMG1vZGVybnxlbnwxfHx8fDE3NTc3NTI4Mjh8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
            alt="Doctor with stethoscope"
            className="h-48 w-64 object-cover"
          />
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm">{stat.title}</CardTitle>
                <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                  <stat.icon className={`w-4 h-4 ${stat.color}`} />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl">{stat.value}</div>
                <p className="text-xs text-muted-foreground">
                  <span className={stat.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}>
                    {stat.change}
                  </span>
                  {' '}from last month
                </p>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Patients */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="lg:col-span-2"
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                Recent Patients
                <Button variant="outline" size="sm">View All</Button>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentPatients.map((patient) => (
                  <div key={patient.id} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div className="flex items-center space-x-4">
                      <Avatar className="w-12 h-12">
                        <AvatarImage src={patient.avatar} alt={patient.name} />
                        <AvatarFallback>{patient.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                      </Avatar>
                      <div>
                        <h4 className="text-sm">{patient.name}</h4>
                        <p className="text-xs text-gray-500">Age {patient.age} • {patient.condition}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <Badge className={getStatusColor(patient.status)} variant="secondary">
                        {patient.status}
                      </Badge>
                      <p className="text-xs text-gray-500 mt-1">{patient.lastVisit}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Today's Schedule */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Clock className="w-5 h-5" />
                <span>Today's Schedule</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {todaySchedule.map((appointment, index) => (
                  <div key={index} className="flex items-center space-x-3 p-2">
                    <div className="text-xs text-gray-500 w-16">{appointment.time}</div>
                    <div className="flex-1">
                      <p className="text-sm">{appointment.patient}</p>
                      <p className="text-xs text-gray-500">{appointment.type}</p>
                    </div>
                    {index < 2 && (
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Quick Actions & Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4">
                <Button variant="outline" className="h-20 flex flex-col items-center justify-center space-y-2">
                  <Users className="w-6 h-6" />
                  <span className="text-xs">Add Patient</span>
                </Button>
                <Button variant="outline" className="h-20 flex flex-col items-center justify-center space-y-2">
                  <Activity className="w-6 h-6" />
                  <span className="text-xs">New Diagnosis</span>
                </Button>
                <Button variant="outline" className="h-20 flex flex-col items-center justify-center space-y-2">
                  <Calendar className="w-6 h-6" />
                  <span className="text-xs">Schedule</span>
                </Button>
                <Button variant="outline" className="h-20 flex flex-col items-center justify-center space-y-2">
                  <Heart className="w-6 h-6" />
                  <span className="text-xs">Health Records</span>
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* System Alerts */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <AlertTriangle className="w-5 h-5 text-orange-500" />
                <span>System Alerts</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-start space-x-3 p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                  <AlertTriangle className="w-4 h-4 text-orange-500 mt-0.5" />
                  <div>
                    <p className="text-sm">Medication reminder for Rajesh Kumar</p>
                    <p className="text-xs text-gray-500">Due in 30 minutes</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <CheckCircle className="w-4 h-4 text-blue-500 mt-0.5" />
                  <div>
                    <p className="text-sm">Lab results available for Priya Sharma</p>
                    <p className="text-xs text-gray-500">2 hours ago</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <CheckCircle className="w-4 h-4 text-green-500 mt-0.5" />
                  <div>
                    <p className="text-sm">System backup completed successfully</p>
                    <p className="text-xs text-gray-500">12:00 AM</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
};

export default DoctorDashboardHome;