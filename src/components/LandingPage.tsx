import React, { useState } from 'react';
import { motion } from 'motion/react';
import { Heart, Stethoscope, Shield, Moon, Sun, User, Lock, Mail, Phone, IdCard } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { useTheme } from './ThemeProvider';
import { ImageWithFallback } from './figma/ImageWithFallback';
import type { User, UserType } from '../App';

interface LandingPageProps {
  onLogin: (user: User) => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onLogin }) => {
  const { theme, toggleTheme } = useTheme();
  const [authMode, setAuthMode] = useState<'signin' | 'signup'>('signin');
  const [userType, setUserType] = useState<UserType>('patient');

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const email = formData.get('email') as string;
    const name = formData.get('name') as string || email.split('@')[0];
    
    // Mock user creation
    const user: User = {
      id: Math.random().toString(36).substr(2, 9),
      name,
      email,
      type: userType,
      avatar: `./man.png?seed=${email}`
    };
    
    onLogin(user);
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-600 via-purple-600 to-cyan-500 dark:from-indigo-900 dark:via-purple-900 dark:to-cyan-900" />
      <div className="absolute inset-0 bg-black/20 dark:bg-black/40" />
      
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(6)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-64 h-64 rounded-full bg-white/10 dark:bg-white/5 blur-xl"
            animate={{
              x: [0, 100, 0],
              y: [0, -100, 0],
              scale: [1, 1.2, 1],
            }}
            transition={{
              duration: 10 + i * 2,
              repeat: Infinity,
              ease: "easeInOut",
            }}
            style={{
              left: `${20 + i * 15}%`,
              top: `${10 + i * 10}%`,
            }}
          />
        ))}
      </div>

      {/* Header */}
      <header className="relative z-10 flex items-center justify-between p-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center space-x-2"
        >
          <div className="w-10 h-10 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
            <Heart className="w-6 h-6 text-white" />
          </div>
          <span className="text-2xl text-white">SwasthyaSetu</span>
        </motion.div>
        
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleTheme}
          className="text-white hover:bg-white/10"
        >
          {theme === 'light' ? <Moon className="w-5 h-5" /> : <Sun className="w-5 h-5" />}
        </Button>
      </header>

      {/* Main content */}
      <div className="relative z-10 container mx-auto px-6 py-12">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left side - Hero content */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-white space-y-8"
          >
            <div className="space-y-4">
              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="text-5xl lg:text-6xl leading-tight"
              >
                Your Health,
                <br />
                <span className="bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
                  Digitally Connected
                </span>
              </motion.h1>
              
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="text-xl text-white/90 max-w-lg"
              >
                Empowering healthcare with modern technology. Connect doctors, patients, and administrators in one unified platform.
              </motion.p>
            </div>

            {/* Features */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="grid grid-cols-1 sm:grid-cols-3 gap-6"
            >
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-cyan-500/20 rounded-lg flex items-center justify-center">
                  <Stethoscope className="w-6 h-6 text-cyan-400" />
                </div>
                <div>
                  <h3 className="text-lg">Doctor Portal</h3>
                  <p className="text-white/70 text-sm">Manage patients & diagnoses</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center">
                  <User className="w-6 h-6 text-purple-400" />
                </div>
                <div>
                  <h3 className="text-lg">Patient Records</h3>
                  <p className="text-white/70 text-sm">Digital health passport</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-indigo-500/20 rounded-lg flex items-center justify-center">
                  <Shield className="w-6 h-6 text-indigo-400" />
                </div>
                <div>
                  <h3 className="text-lg">Admin Console</h3>
                  <p className="text-white/70 text-sm">System management</p>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="pt-4"
            >
              <ImageWithFallback
                src="https://images.unsplash.com/photo-1747224317356-6dd1a4a078fd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxoZWFsdGhjYXJlJTIwbWVkaWNhbCUyMHRlY2hub2xvZ3l8ZW58MXx8fHwxNzU3NjkwOTUzfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
                alt="Healthcare Technology"
                className="w-full h-64 object-cover rounded-2xl shadow-2xl opacity-80"
              />
            </motion.div>
          </motion.div>

          {/* Right side - Auth form */}
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card className="backdrop-blur-md bg-white/10 dark:bg-white/5 border-white/20 shadow-2xl">
              <CardHeader>
                <CardTitle className="text-white text-2xl text-center">
                  Welcome to SwasthyaSetu
                </CardTitle>
                <CardDescription className="text-white/70 text-center">
                  {authMode === 'signin' ? 'Sign in to your account' : 'Create your account'}
                </CardDescription>
              </CardHeader>
              
              <CardContent className="space-y-6">
                <Tabs value={authMode} onValueChange={(value) => setAuthMode(value as 'signin' | 'signup')}>
                  <TabsList className="grid w-full grid-cols-2 bg-white/10">
                    <TabsTrigger value="signin" className="text-white data-[state=active]:bg-white/20">
                      Sign In
                    </TabsTrigger>
                    <TabsTrigger value="signup" className="text-white data-[state=active]:bg-white/20">
                      Sign Up
                    </TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="signin" className="space-y-4">
                    <form onSubmit={handleSubmit} className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="signin-type" className="text-white">I am a</Label>
                        <Select value={userType || 'patient'} onValueChange={(value) => setUserType(value as UserType)}>
                          <SelectTrigger className="bg-white/10 border-white/20 text-white">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="patient">Patient</SelectItem>
                            <SelectItem value="doctor">Doctor</SelectItem>
                            <SelectItem value="admin">Administrator</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="signin-email" className="text-white">Email</Label>
                        <div className="relative">
                          <Mail className="absolute left-3 top-3 w-4 h-4 text-white/50" />
                          <Input
                            id="signin-email"
                            name="email"
                            type="email"
                            placeholder="Enter your email"
                            className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-white/50"
                            required
                          />
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="signin-password" className="text-white">Password</Label>
                        <div className="relative">
                          <Lock className="absolute left-3 top-3 w-4 h-4 text-white/50" />
                          <Input
                            id="signin-password"
                            name="password"
                            type="password"
                            placeholder="Enter your password"
                            className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-white/50"
                            required
                          />
                        </div>
                      </div>
                      
                      <Button type="submit" className="w-full bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white border-0">
                        Sign In
                      </Button>
                    </form>
                  </TabsContent>
                  
                  <TabsContent value="signup" className="space-y-4">
                    <form onSubmit={handleSubmit} className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="signup-type" className="text-white">I am a</Label>
                        <Select value={userType || 'patient'} onValueChange={(value) => setUserType(value as UserType)}>
                          <SelectTrigger className="bg-white/10 border-white/20 text-white">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="patient">Patient</SelectItem>
                            <SelectItem value="doctor">Doctor</SelectItem>
                            <SelectItem value="admin">Administrator</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label htmlFor="signup-fname" className="text-white">First Name</Label>
                          <Input
                            id="signup-fname"
                            name="firstName"
                            placeholder="First name"
                            className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
                            required
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="signup-lname" className="text-white">Last Name</Label>
                          <Input
                            id="signup-lname"
                            name="lastName"
                            placeholder="Last name"
                            className="bg-white/10 border-white/20 text-white placeholder:text-white/50"
                            required
                          />
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="signup-email" className="text-white">Email</Label>
                        <div className="relative">
                          <Mail className="absolute left-3 top-3 w-4 h-4 text-white/50" />
                          <Input
                            id="signup-email"
                            name="email"
                            type="email"
                            placeholder="Enter your email"
                            className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-white/50"
                            required
                          />
                        </div>
                      </div>
                      
                      {userType === 'doctor' && (
                        <div className="space-y-2">
                          <Label htmlFor="signup-license" className="text-white">Medical License</Label>
                          <div className="relative">
                            <IdCard className="absolute left-3 top-3 w-4 h-4 text-white/50" />
                            <Input
                              id="signup-license"
                              name="license"
                              placeholder="License number"
                              className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-white/50"
                              required
                            />
                          </div>
                        </div>
                      )}
                      
                      <div className="space-y-2">
                        <Label htmlFor="signup-phone" className="text-white">Phone</Label>
                        <div className="relative">
                          <Phone className="absolute left-3 top-3 w-4 h-4 text-white/50" />
                          <Input
                            id="signup-phone"
                            name="phone"
                            type="tel"
                            placeholder="Phone number"
                            className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-white/50"
                            required
                          />
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="signup-password" className="text-white">Password</Label>
                        <div className="relative">
                          <Lock className="absolute left-3 top-3 w-4 h-4 text-white/50" />
                          <Input
                            id="signup-password"
                            name="password"
                            type="password"
                            placeholder="Create password"
                            className="pl-10 bg-white/10 border-white/20 text-white placeholder:text-white/50"
                            required
                          />
                        </div>
                      </div>
                      
                      <Button type="submit" className="w-full bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white border-0">
                        Create Account
                      </Button>
                    </form>
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;