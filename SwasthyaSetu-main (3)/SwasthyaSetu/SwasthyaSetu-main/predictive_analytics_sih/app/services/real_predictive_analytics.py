"""Real Predictive Analytics Engine with Google Healthcare AI"""

import asyncio
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json
from datetime import datetime, timedelta
import structlog
from google.cloud import healthcare_v1
from google.cloud import aiplatform
import google.generativeai as genai

from app.core.config import get_settings
from app.services.google_healthcare_service import GoogleHealthcareService

logger = structlog.get_logger(__name__)

class RealPredictiveAnalyticsEngine:
    """Real-time predictive analytics using Google Healthcare AI and trained models"""
    
    def __init__(self, google_healthcare_service: GoogleHealthcareService):
        self.settings = get_settings()
        self.google_healthcare = google_healthcare_service
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.feature_columns = []
        self.initialized = False
        self.training_data = None
        
    async def initialize(self):
        """Initialize the predictive analytics engine"""
        try:
            # Initialize Google Healthcare service
            if not await self.google_healthcare.initialize():
                logger.warning("Google Healthcare service not available, using fallback models")
            
            # Load or train models
            await self._initialize_models()
            
            # Load training data from Google Healthcare API
            await self._load_training_data()
            
            self.initialized = True
            logger.info("Real predictive analytics engine initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize predictive analytics engine", error=str(e))
            # Initialize with basic models as fallback
            await self._initialize_fallback_models()
            self.initialized = True
    
    async def _load_training_data(self):
        """Load training data from Google Healthcare API and other sources"""
        try:
            # Generate synthetic training data based on medical knowledge
            # In production, this would load real anonymized data
            training_data = await self._generate_training_data()
            
            if training_data is not None and not training_data.empty:
                self.training_data = training_data
                logger.info(f"Loaded {len(training_data)} training samples")
                
                # Train models with loaded data
                await self._train_models()
            else:
                logger.warning("No training data available, using pre-trained models")
                
        except Exception as e:
            logger.error("Failed to load training data", error=str(e))
            await self._initialize_fallback_models()
    
    async def _generate_training_data(self) -> pd.DataFrame:
        """Generate synthetic training data based on medical knowledge"""
        try:
            # Create synthetic medical data for training
            np.random.seed(42)  # For reproducibility
            
            n_samples = 5000
            
            # Generate patient features
            data = {
                'age': np.random.normal(45, 15, n_samples).clip(18, 90),
                'gender': np.random.choice(['male', 'female'], n_samples),
                'bmi': np.random.normal(25, 5, n_samples).clip(15, 45),
                'systolic_bp': np.random.normal(130, 20, n_samples).clip(90, 200),
                'diastolic_bp': np.random.normal(80, 15, n_samples).clip(60, 120),
                'heart_rate': np.random.normal(72, 12, n_samples).clip(50, 120),
                'temperature': np.random.normal(98.6, 1.5, n_samples).clip(96, 104),
                'respiratory_rate': np.random.normal(16, 4, n_samples).clip(12, 30),
                'glucose': np.random.normal(100, 25, n_samples).clip(70, 300),
                'cholesterol': np.random.normal(200, 40, n_samples).clip(120, 400),
                
                # Symptoms (binary)
                'has_chest_pain': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
                'has_shortness_breath': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
                'has_fatigue': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
                'has_dizziness': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
                'has_nausea': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
                'has_fever': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
                'has_headache': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
                
                # Lifestyle factors
                'smoking': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
                'alcohol_use': np.random.choice([0, 1, 2], n_samples, p=[0.4, 0.5, 0.1]),  # 0=none, 1=moderate, 2=heavy
                'exercise_level': np.random.choice([0, 1, 2], n_samples, p=[0.3, 0.5, 0.2]),  # 0=low, 1=moderate, 2=high
                'stress_level': np.random.choice([0, 1, 2], n_samples, p=[0.2, 0.6, 0.2]),  # 0=low, 1=moderate, 2=high
            }
            
            df = pd.DataFrame(data)
            
            # Generate target conditions based on risk factors
            conditions = []
            risk_scores = []
            
            for idx, row in df.iterrows():
                # Calculate risk factors for different conditions
                hypertension_risk = self._calculate_hypertension_risk(row)
                diabetes_risk = self._calculate_diabetes_risk(row)
                cardiac_risk = self._calculate_cardiac_risk(row)
                respiratory_risk = self._calculate_respiratory_risk(row)
                
                # Determine primary condition based on highest risk
                risks = {
                    'hypertension': hypertension_risk,
                    'diabetes': diabetes_risk,
                    'cardiac_condition': cardiac_risk,
                    'respiratory_condition': respiratory_risk,
                    'healthy': 0.3  # Baseline healthy probability
                }
                
                primary_condition = max(risks, key=risks.get)
                max_risk = risks[primary_condition]
                
                conditions.append(primary_condition)
                risk_scores.append(max_risk)
            
            df['primary_condition'] = conditions
            df['risk_score'] = risk_scores
            
            # Add outcome predictions
            df['hospitalization_risk'] = self._calculate_hospitalization_risk(df)
            df['treatment_complexity'] = self._calculate_treatment_complexity(df)
            
            logger.info("Generated synthetic training data successfully")
            return df
            
        except Exception as e:
            logger.error("Failed to generate training data", error=str(e))
            return pd.DataFrame()
    
    def _calculate_hypertension_risk(self, row: pd.Series) -> float:
        """Calculate hypertension risk based on patient data"""
        risk = 0.0
        
        # Age factor
        if row['age'] > 65:
            risk += 0.3
        elif row['age'] > 45:
            risk += 0.2
        
        # Blood pressure
        if row['systolic_bp'] > 140 or row['diastolic_bp'] > 90:
            risk += 0.4
        elif row['systolic_bp'] > 130 or row['diastolic_bp'] > 80:
            risk += 0.2
        
        # BMI
        if row['bmi'] > 30:
            risk += 0.2
        elif row['bmi'] > 25:
            risk += 0.1
        
        # Lifestyle factors
        if row['smoking']:
            risk += 0.15
        if row['stress_level'] == 2:
            risk += 0.1
        if row['exercise_level'] == 0:
            risk += 0.1
        
        return min(risk, 1.0)
    
    def _calculate_diabetes_risk(self, row: pd.Series) -> float:
        """Calculate diabetes risk based on patient data"""
        risk = 0.0
        
        # Glucose level
        if row['glucose'] > 200:
            risk += 0.5
        elif row['glucose'] > 126:
            risk += 0.3
        elif row['glucose'] > 100:
            risk += 0.1
        
        # Age and BMI
        if row['age'] > 45:
            risk += 0.2
        if row['bmi'] > 30:
            risk += 0.25
        
        # Symptoms
        if row['has_fatigue']:
            risk += 0.1
        if row['has_dizziness']:
            risk += 0.05
        
        return min(risk, 1.0)
    
    def _calculate_cardiac_risk(self, row: pd.Series) -> float:
        """Calculate cardiac condition risk"""
        risk = 0.0
        
        # Symptoms
        if row['has_chest_pain']:
            risk += 0.4
        if row['has_shortness_breath']:
            risk += 0.3
        
        # Vital signs
        if row['heart_rate'] > 100 or row['heart_rate'] < 60:
            risk += 0.2
        
        # Risk factors
        if row['cholesterol'] > 240:
            risk += 0.2
        if row['smoking']:
            risk += 0.2
        
        return min(risk, 1.0)
    
    def _calculate_respiratory_risk(self, row: pd.Series) -> float:
        """Calculate respiratory condition risk"""
        risk = 0.0
        
        # Symptoms
        if row['has_shortness_breath']:
            risk += 0.3
        if row['has_fever']:
            risk += 0.2
        
        # Vital signs
        if row['respiratory_rate'] > 20:
            risk += 0.2
        if row['temperature'] > 100.4:
            risk += 0.2
        
        # Lifestyle
        if row['smoking']:
            risk += 0.3
        
        return min(risk, 1.0)
    
    def _calculate_hospitalization_risk(self, df: pd.DataFrame) -> np.ndarray:
        """Calculate hospitalization risk"""
        risk = np.zeros(len(df))
        
        # Age factor
        risk += (df['age'] > 70).astype(int) * 0.3
        risk += (df['age'] > 80).astype(int) * 0.2
        
        # Multiple symptoms
        symptom_count = (df['has_chest_pain'] + df['has_shortness_breath'] + 
                        df['has_fever'] + df['has_nausea'])
        risk += (symptom_count >= 2) * 0.2
        risk += (symptom_count >= 3) * 0.3
        
        # Severe vital signs
        risk += (df['systolic_bp'] > 180).astype(int) * 0.4
        risk += (df['temperature'] > 102).astype(int) * 0.3
        risk += (df['heart_rate'] > 110).astype(int) * 0.2
        
        return np.clip(risk, 0, 1)
    
    def _calculate_treatment_complexity(self, df: pd.DataFrame) -> np.ndarray:
        """Calculate treatment complexity score"""
        complexity = np.zeros(len(df))
        
        # Age increases complexity
        complexity += (df['age'] > 65).astype(int) * 0.2
        
        # Multiple conditions
        complexity += (df['primary_condition'] != 'healthy').astype(int) * 0.3
        
        # Comorbidities (multiple risk factors)
        complexity += (df['smoking'] + (df['bmi'] > 30).astype(int) + 
                      (df['stress_level'] == 2).astype(int)) * 0.1
        
        return np.clip(complexity, 0, 1)
    
    async def _train_models(self):
        """Train ML models with the loaded data"""
        try:
            if self.training_data is None or self.training_data.empty:
                raise ValueError("No training data available")
            
            # Prepare features
            feature_columns = [
                'age', 'bmi', 'systolic_bp', 'diastolic_bp', 'heart_rate',
                'temperature', 'respiratory_rate', 'glucose', 'cholesterol',
                'has_chest_pain', 'has_shortness_breath', 'has_fatigue',
                'has_dizziness', 'has_nausea', 'has_fever', 'has_headache',
                'smoking', 'alcohol_use', 'exercise_level', 'stress_level'
            ]
            
            # Encode categorical variables
            df_encoded = self.training_data.copy()
            
            # Encode gender
            gender_encoder = LabelEncoder()
            df_encoded['gender_encoded'] = gender_encoder.fit_transform(df_encoded['gender'])
            feature_columns.append('gender_encoded')
            self.encoders['gender'] = gender_encoder
            
            X = df_encoded[feature_columns]
            self.feature_columns = feature_columns
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            self.scalers['main'] = scaler
            
            # Train condition prediction model
            y_condition = df_encoded['primary_condition']
            condition_encoder = LabelEncoder()
            y_condition_encoded = condition_encoder.fit_transform(y_condition)
            self.encoders['condition'] = condition_encoder
            
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y_condition_encoded, test_size=0.2, random_state=42
            )
            
            # Train Random Forest for condition prediction
            rf_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            rf_model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = rf_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            logger.info(f"Condition prediction model accuracy: {accuracy:.3f}")
            
            self.models['condition_predictor'] = rf_model
            
            # Train risk score regression model
            risk_regressor = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
            risk_regressor.fit(X_train, df_encoded.loc[df_encoded.index.isin(
                pd.Index(range(len(X_train)))), 'risk_score'].iloc[:len(X_train)]
            )
            self.models['risk_predictor'] = risk_regressor
            
            # Train hospitalization risk model
            hosp_regressor = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
            hosp_regressor.fit(X_train, df_encoded.loc[df_encoded.index.isin(
                pd.Index(range(len(X_train)))), 'hospitalization_risk'].iloc[:len(X_train)]
            )
            self.models['hospitalization_predictor'] = hosp_regressor
            
            # Save models
            await self._save_models()
            
            logger.info("Models trained successfully")
            
        except Exception as e:
            logger.error("Failed to train models", error=str(e))
            raise
    
    async def _initialize_models(self):
        """Initialize or load pre-trained models"""
        try:
            # Try to load existing models
            models_loaded = await self._load_models()
            
            if not models_loaded:
                logger.info("No pre-trained models found, will train new models")
                
        except Exception as e:
            logger.error("Failed to initialize models", error=str(e))
            await self._initialize_fallback_models()
    
    async def _initialize_fallback_models(self):
        """Initialize basic fallback models"""
        try:
            # Create basic models for fallback
            self.models['condition_predictor'] = RandomForestClassifier(
                n_estimators=50, random_state=42
            )
            self.models['risk_predictor'] = GradientBoostingRegressor(
                n_estimators=50, random_state=42
            )
            self.scalers['main'] = StandardScaler()
            
            logger.info("Initialized fallback models")
            
        except Exception as e:
            logger.error("Failed to initialize fallback models", error=str(e))
    
    async def predict_condition(
        self,
        patient_data: Dict[str, Any],
        symptoms: List[str],
        vital_signs: Dict[str, float],
        lab_results: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Predict medical conditions using trained models and Google AI"""
        try:
            # Get AI-powered insights first
            ai_insights = await self.google_healthcare.get_predictive_insights(
                patient_data, symptoms, vital_signs
            )
            
            # Prepare features for ML model
            features = await self._prepare_prediction_features(
                patient_data, symptoms, vital_signs, lab_results or {}
            )
            
            # Get ML predictions
            ml_predictions = await self._get_ml_predictions(features)
            
            # Combine AI and ML insights
            combined_predictions = await self._combine_predictions(
                ai_insights, ml_predictions, patient_data
            )
            
            return combined_predictions
            
        except Exception as e:
            logger.error("Failed to predict condition", error=str(e))
            return self._get_fallback_predictions(symptoms, patient_data)
    
    async def _prepare_prediction_features(
        self,
        patient_data: Dict[str, Any],
        symptoms: List[str],
        vital_signs: Dict[str, float],
        lab_results: Dict[str, Any]
    ) -> np.ndarray:
        """Prepare features for ML model prediction"""
        try:
            # Create feature vector
            features = {}
            
            # Basic demographics
            features['age'] = patient_data.get('age', 45)
            features['bmi'] = patient_data.get('bmi', 25)
            
            # Gender encoding
            gender = patient_data.get('gender', 'unknown').lower()
            if 'gender' in self.encoders:
                try:
                    features['gender_encoded'] = self.encoders['gender'].transform([gender])[0]
                except:
                    features['gender_encoded'] = 0
            else:
                features['gender_encoded'] = 1 if gender == 'female' else 0
            
            # Vital signs
            features['systolic_bp'] = vital_signs.get('systolic_bp', 120)
            features['diastolic_bp'] = vital_signs.get('diastolic_bp', 80)
            features['heart_rate'] = vital_signs.get('heart_rate', 72)
            features['temperature'] = vital_signs.get('temperature', 98.6)
            features['respiratory_rate'] = vital_signs.get('respiratory_rate', 16)
            
            # Lab results
            features['glucose'] = lab_results.get('glucose', 100)
            features['cholesterol'] = lab_results.get('cholesterol', 200)
            
            # Symptom encoding
            symptom_mapping = {
                'chest_pain': 'has_chest_pain',
                'shortness_of_breath': 'has_shortness_breath',
                'fatigue': 'has_fatigue',
                'dizziness': 'has_dizziness',
                'nausea': 'has_nausea',
                'fever': 'has_fever',
                'headache': 'has_headache'
            }
            
            symptoms_lower = [s.lower().replace(' ', '_') for s in symptoms]
            
            for symptom_key, feature_key in symptom_mapping.items():
                features[feature_key] = 1 if any(symptom_key in s for s in symptoms_lower) else 0
            
            # Lifestyle factors (with defaults)
            features['smoking'] = 1 if patient_data.get('smoking', False) else 0
            features['alcohol_use'] = patient_data.get('alcohol_use', 0)
            features['exercise_level'] = patient_data.get('exercise_level', 1)
            features['stress_level'] = patient_data.get('stress_level', 1)
            
            # Convert to array in correct order
            if self.feature_columns:
                feature_array = np.array([
                    features.get(col, 0) for col in self.feature_columns
                ]).reshape(1, -1)
            else:
                # Fallback feature order
                feature_array = np.array([
                    features['age'], features['bmi'], features['systolic_bp'],
                    features['diastolic_bp'], features['heart_rate'], features['temperature'],
                    features['respiratory_rate'], features['glucose'], features['cholesterol'],
                    features['has_chest_pain'], features['has_shortness_breath'],
                    features['has_fatigue'], features['has_dizziness'], features['has_nausea'],
                    features['has_fever'], features['has_headache'], features['smoking'],
                    features['alcohol_use'], features['exercise_level'], features['stress_level'],
                    features['gender_encoded']
                ]).reshape(1, -1)
            
            # Scale features
            if 'main' in self.scalers:
                feature_array = self.scalers['main'].transform(feature_array)
            
            return feature_array
            
        except Exception as e:
            logger.error("Failed to prepare features", error=str(e))
            # Return zero array as fallback
            return np.zeros((1, 21))
    
    async def _get_ml_predictions(self, features: np.ndarray) -> Dict[str, Any]:
        """Get predictions from trained ML models"""
        try:
            predictions = {}
            
            # Condition prediction
            if 'condition_predictor' in self.models:
                condition_probs = self.models['condition_predictor'].predict_proba(features)[0]
                condition_classes = self.models['condition_predictor'].classes_
                
                # Decode condition classes
                if 'condition' in self.encoders:
                    condition_names = self.encoders['condition'].inverse_transform(condition_classes)
                else:
                    condition_names = [f"condition_{i}" for i in condition_classes]
                
                # Create condition predictions
                condition_predictions = []
                for name, prob in zip(condition_names, condition_probs):
                    if prob > 0.1:  # Only include predictions with >10% probability
                        condition_predictions.append({
                            'condition': name,
                            'probability': float(prob),
                            'confidence': float(prob)
                        })
                
                # Sort by probability
                condition_predictions.sort(key=lambda x: x['probability'], reverse=True)
                predictions['conditions'] = condition_predictions
            
            # Risk score prediction
            if 'risk_predictor' in self.models:
                risk_score = self.models['risk_predictor'].predict(features)[0]
                predictions['overall_risk_score'] = float(max(0, min(1, risk_score)))
            
            # Hospitalization risk
            if 'hospitalization_predictor' in self.models:
                hosp_risk = self.models['hospitalization_predictor'].predict(features)[0]
                predictions['hospitalization_risk'] = float(max(0, min(1, hosp_risk)))
            
            return predictions
            
        except Exception as e:
            logger.error("Failed to get ML predictions", error=str(e))
            return {}
    
    async def _combine_predictions(
        self,
        ai_insights: Dict[str, Any],
        ml_predictions: Dict[str, Any],
        patient_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Combine AI and ML predictions into final result"""
        try:
            combined_results = []
            
            # Get ML condition predictions
            ml_conditions = ml_predictions.get('conditions', [])
            
            # Get AI differential diagnosis
            ai_conditions = ai_insights.get('differential_diagnosis', [])
            
            # Create comprehensive prediction list
            all_conditions = {}
            
            # Add ML predictions
            for ml_cond in ml_conditions:
                condition_name = ml_cond['condition']
                all_conditions[condition_name] = {
                    'condition': condition_name,
                    'ml_confidence': ml_cond['confidence'],
                    'ai_confidence': 0.0,
                    'combined_confidence': ml_cond['confidence'] * 0.7,  # Weight ML at 70%
                    'source': 'ml_model',
                    'supporting_evidence': [],
                    'risk_factors': [],
                    'recommended_tests': []
                }
            
            # Add AI predictions
            for ai_cond in ai_conditions:
                condition_name = ai_cond.get('condition', 'unknown')
                ai_confidence = ai_cond.get('confidence', 0.0)
                
                if condition_name in all_conditions:
                    # Update existing
                    all_conditions[condition_name]['ai_confidence'] = ai_confidence
                    all_conditions[condition_name]['combined_confidence'] = (
                        all_conditions[condition_name]['ml_confidence'] * 0.7 +
                        ai_confidence * 0.3
                    )
                    all_conditions[condition_name]['source'] = 'ml_and_ai'
                else:
                    # Add new AI prediction
                    all_conditions[condition_name] = {
                        'condition': condition_name,
                        'ml_confidence': 0.0,
                        'ai_confidence': ai_confidence,
                        'combined_confidence': ai_confidence * 0.3,  # Weight AI at 30% if no ML
                        'source': 'ai_model',
                        'supporting_evidence': ai_cond.get('supporting_symptoms', []),
                        'risk_factors': [],
                        'recommended_tests': ai_cond.get('recommended_tests', [])
                    }
            
            # Convert to list and add additional information
            for condition_name, pred in all_conditions.items():
                # Add risk assessment
                pred['risk_level'] = self._classify_risk_level(pred['combined_confidence'])
                
                # Add patient-specific considerations
                pred['patient_considerations'] = self._get_patient_considerations(
                    condition_name, patient_data
                )
                
                # Add monitoring recommendations
                pred['monitoring_recommendations'] = self._get_monitoring_recommendations(
                    condition_name, pred['combined_confidence']
                )
                
                # Add urgency level
                pred['urgency'] = self._assess_urgency(condition_name, pred['combined_confidence'])
                
                combined_results.append(pred)
            
            # Sort by combined confidence
            combined_results.sort(key=lambda x: x['combined_confidence'], reverse=True)
            
            # Add overall assessment
            if combined_results:
                overall_assessment = {
                    'total_predictions': len(combined_results),
                    'highest_confidence': combined_results[0]['combined_confidence'],
                    'primary_concern': combined_results[0]['condition'],
                    'overall_risk_score': ml_predictions.get('overall_risk_score', 0.5),
                    'hospitalization_risk': ml_predictions.get('hospitalization_risk', 0.3),
                    'requires_immediate_attention': any(
                        pred['urgency'] == 'high' for pred in combined_results[:3]
                    ),
                    'ai_insights': ai_insights,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Add overall assessment to first result
                combined_results.insert(0, {
                    'type': 'overall_assessment',
                    **overall_assessment
                })
            
            return combined_results
            
        except Exception as e:
            logger.error("Failed to combine predictions", error=str(e))
            return self._get_fallback_predictions([], {})
    
    def _classify_risk_level(self, confidence: float) -> str:
        """Classify risk level based on confidence score"""
        if confidence >= 0.8:
            return "high"
        elif confidence >= 0.6:
            return "moderate"
        elif confidence >= 0.4:
            return "low"
        else:
            return "minimal"
    
    def _get_patient_considerations(self, condition: str, patient_data: Dict[str, Any]) -> List[str]:
        """Get patient-specific considerations for a condition"""
        considerations = []
        age = patient_data.get('age', 0)
        gender = patient_data.get('gender', '').lower()
        
        # Age-based considerations
        if age > 65:
            considerations.append("Consider age-related complications")
            considerations.append("Monitor for polypharmacy interactions")
        elif age < 18:
            considerations.append("Pediatric dosing and protocols required")
        
        # Gender-specific considerations
        if gender == 'female' and age >= 18 and age <= 50:
            considerations.append("Consider reproductive health implications")
        
        # Condition-specific considerations
        condition_specific = {
            'hypertension': ["Monitor kidney function", "Assess cardiovascular risk"],
            'diabetes': ["Monitor blood glucose closely", "Assess for complications"],
            'cardiac_condition': ["ECG monitoring recommended", "Assess exercise tolerance"],
            'respiratory_condition': ["Monitor oxygen saturation", "Assess breathing patterns"]
        }
        
        if condition in condition_specific:
            considerations.extend(condition_specific[condition])
        
        return considerations
    
    def _get_monitoring_recommendations(self, condition: str, confidence: float) -> List[str]:
        """Get monitoring recommendations based on condition and confidence"""
        recommendations = []
        
        # Base monitoring based on confidence
        if confidence > 0.8:
            recommendations.append("Close monitoring required")
            recommendations.append("Follow-up within 24-48 hours")
        elif confidence > 0.6:
            recommendations.append("Regular monitoring recommended")
            recommendations.append("Follow-up within 1 week")
        else:
            recommendations.append("Routine monitoring sufficient")
            recommendations.append("Follow-up as scheduled")
        
        # Condition-specific monitoring
        monitoring_map = {
            'hypertension': ["Daily blood pressure checks", "Weekly weight monitoring"],
            'diabetes': ["Blood glucose monitoring", "HbA1c every 3 months"],
            'cardiac_condition': ["Heart rate monitoring", "Activity tolerance assessment"],
            'respiratory_condition': ["Respiratory rate monitoring", "Oxygen saturation checks"]
        }
        
        if condition in monitoring_map:
            recommendations.extend(monitoring_map[condition])
        
        return recommendations
    
    def _assess_urgency(self, condition: str, confidence: float) -> str:
        """Assess urgency level for a condition"""
        high_urgency_conditions = ['cardiac_condition', 'severe_respiratory', 'stroke']
        moderate_urgency_conditions = ['hypertension', 'diabetes_complications']
        
        if condition in high_urgency_conditions and confidence > 0.7:
            return "high"
        elif condition in moderate_urgency_conditions and confidence > 0.6:
            return "moderate"
        elif confidence > 0.8:
            return "moderate"
        else:
            return "low"
    
    def _get_fallback_predictions(self, symptoms: List[str], patient_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get fallback predictions when models fail"""
        return [
            {
                "type": "fallback_assessment",
                "condition": "general_health_assessment_needed",
                "combined_confidence": 0.5,
                "source": "fallback",
                "message": "Unable to generate specific predictions. Recommend comprehensive health assessment.",
                "recommended_actions": [
                    "Schedule appointment with healthcare provider",
                    "Complete comprehensive medical history",
                    "Consider basic diagnostic tests"
                ],
                "urgency": "low"
            }
        ]
    
    async def _save_models(self):
        """Save trained models to disk"""
        try:
            import os
            models_dir = "models"
            os.makedirs(models_dir, exist_ok=True)
            
            # Save models
            for name, model in self.models.items():
                joblib.dump(model, f"{models_dir}/{name}.pkl")
            
            # Save scalers and encoders
            for name, scaler in self.scalers.items():
                joblib.dump(scaler, f"{models_dir}/scaler_{name}.pkl")
            
            for name, encoder in self.encoders.items():
                joblib.dump(encoder, f"{models_dir}/encoder_{name}.pkl")
            
            # Save feature columns
            with open(f"{models_dir}/feature_columns.json", 'w') as f:
                json.dump(self.feature_columns, f)
            
            logger.info("Models saved successfully")
            
        except Exception as e:
            logger.error("Failed to save models", error=str(e))
    
    async def _load_models(self) -> bool:
        """Load pre-trained models from disk"""
        try:
            import os
            models_dir = "models"
            
            if not os.path.exists(models_dir):
                return False
            
            # Load models
            model_files = {
                'condition_predictor': f"{models_dir}/condition_predictor.pkl",
                'risk_predictor': f"{models_dir}/risk_predictor.pkl",
                'hospitalization_predictor': f"{models_dir}/hospitalization_predictor.pkl"
            }
            
            for name, filepath in model_files.items():
                if os.path.exists(filepath):
                    self.models[name] = joblib.load(filepath)
            
            # Load scalers
            scaler_files = {
                'main': f"{models_dir}/scaler_main.pkl"
            }
            
            for name, filepath in scaler_files.items():
                if os.path.exists(filepath):
                    self.scalers[name] = joblib.load(filepath)
            
            # Load encoders
            encoder_files = {
                'gender': f"{models_dir}/encoder_gender.pkl",
                'condition': f"{models_dir}/encoder_condition.pkl"
            }
            
            for name, filepath in encoder_files.items():
                if os.path.exists(filepath):
                    self.encoders[name] = joblib.load(filepath)
            
            # Load feature columns
            features_file = f"{models_dir}/feature_columns.json"
            if os.path.exists(features_file):
                with open(features_file, 'r') as f:
                    self.feature_columns = json.load(f)
            
            logger.info("Pre-trained models loaded successfully")
            return True
            
        except Exception as e:
            logger.error("Failed to load models", error=str(e))
            return False
    
    async def get_treatment_recommendations(
        self,
        patient_data: Dict[str, Any],
        predictions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Get integrative treatment recommendations based on predictions"""
        try:
            if not predictions or predictions[0].get('type') == 'overall_assessment':
                primary_condition = predictions[0].get('primary_concern', 'unknown') if predictions else 'unknown'
                confidence = predictions[0].get('highest_confidence', 0.5) if predictions else 0.5
            else:
                primary_condition = predictions[0].get('condition', 'unknown')
                confidence = predictions[0].get('combined_confidence', 0.5)
            
            # Get integrative treatment plan from Google Healthcare AI
            treatment_plan = await self.google_healthcare.get_integrative_treatment_plan(
                patient_data, primary_condition, {'risk_level': self._classify_risk_level(confidence)}
            )
            
            # Enhance with evidence-based recommendations
            enhanced_plan = await self._enhance_treatment_plan(
                treatment_plan, patient_data, primary_condition, confidence
            )
            
            return enhanced_plan
            
        except Exception as e:
            logger.error("Failed to get treatment recommendations", error=str(e))
            return {"error": str(e), "fallback_recommendations": self._get_basic_recommendations()}
    
    async def _enhance_treatment_plan(
        self,
        plan: Dict[str, Any],
        patient_data: Dict[str, Any],
        condition: str,
        confidence: float
    ) -> Dict[str, Any]:
        """Enhance treatment plan with additional analysis"""
        try:
            enhanced = plan.copy()
            
            # Add risk stratification
            enhanced['risk_stratification'] = {
                'overall_risk': self._classify_risk_level(confidence),
                'factors': self._identify_risk_factors(patient_data, condition),
                'mitigation_strategies': self._get_mitigation_strategies(patient_data, condition)
            }
            
            # Add monitoring protocol
            enhanced['monitoring_protocol'] = {
                'frequency': self._determine_monitoring_frequency(confidence),
                'parameters': self._get_monitoring_parameters(condition),
                'alert_thresholds': self._get_alert_thresholds(condition, patient_data)
            }
            
            # Add patient education components
            enhanced['patient_education'] = {
                'condition_info': f"Educational materials about {condition}",
                'self_management': self._get_self_management_tips(condition),
                'warning_signs': self._get_warning_signs(condition),
                'lifestyle_modifications': self._get_lifestyle_recommendations(condition, patient_data)
            }
            
            # Add integration considerations
            enhanced['integration_considerations'] = {
                'contraindications': await self._check_contraindications(plan, patient_data),
                'synergies': self._identify_synergies(plan),
                'sequencing': self._recommend_treatment_sequence(plan),
                'cost_considerations': self._estimate_treatment_costs(plan)
            }
            
            return enhanced
            
        except Exception as e:
            logger.error("Failed to enhance treatment plan", error=str(e))
            return plan
    
    def _identify_risk_factors(self, patient_data: Dict[str, Any], condition: str) -> List[str]:
        """Identify patient-specific risk factors"""
        risk_factors = []
        age = patient_data.get('age', 0)
        
        # Age-related risks
        if age > 65:
            risk_factors.append("Advanced age")
        if age < 18:
            risk_factors.append("Pediatric considerations")
        
        # Lifestyle risks
        if patient_data.get('smoking'):
            risk_factors.append("Tobacco use")
        if patient_data.get('alcohol_use', 0) > 1:
            risk_factors.append("Excessive alcohol consumption")
        if patient_data.get('exercise_level', 1) == 0:
            risk_factors.append("Sedentary lifestyle")
        
        # Medical history risks
        medical_history = patient_data.get('medical_history', [])
        for condition_hist in medical_history:
            if any(term in condition_hist.lower() for term in ['diabetes', 'hypertension', 'heart']):
                risk_factors.append(f"History of {condition_hist}")
        
        return risk_factors
    
    def _get_mitigation_strategies(self, patient_data: Dict[str, Any], condition: str) -> List[str]:
        """Get risk mitigation strategies"""
        strategies = []
        
        # Universal strategies
        strategies.extend([
            "Regular medical follow-up",
            "Medication adherence monitoring",
            "Lifestyle modification support"
        ])
        
        # Condition-specific strategies
        condition_strategies = {
            'hypertension': ["Blood pressure self-monitoring", "Sodium restriction"],
            'diabetes': ["Blood glucose monitoring", "Carbohydrate counting education"],
            'cardiac_condition': ["Cardiac rehabilitation referral", "Activity monitoring"]
        }
        
        if condition in condition_strategies:
            strategies.extend(condition_strategies[condition])
        
        return strategies
    
    def _determine_monitoring_frequency(self, confidence: float) -> str:
        """Determine monitoring frequency based on confidence/risk"""
        if confidence > 0.8:
            return "Daily to weekly"
        elif confidence > 0.6:
            return "Weekly to bi-weekly"
        else:
            return "Monthly"
    
    def _get_monitoring_parameters(self, condition: str) -> List[str]:
        """Get condition-specific monitoring parameters"""
        parameters_map = {
            'hypertension': ["Blood pressure", "Heart rate", "Weight", "Symptoms"],
            'diabetes': ["Blood glucose", "HbA1c", "Weight", "Ketones"],
            'cardiac_condition': ["Heart rate", "Blood pressure", "Exercise tolerance", "Symptoms"],
            'respiratory_condition': ["Respiratory rate", "Oxygen saturation", "Peak flow", "Symptoms"]
        }
        
        return parameters_map.get(condition, ["Vital signs", "Symptoms", "General wellness"])
    
    def _get_alert_thresholds(self, condition: str, patient_data: Dict[str, Any]) -> Dict[str, str]:
        """Get alert thresholds for monitoring parameters"""
        age = patient_data.get('age', 45)
        
        # Age-adjusted thresholds
        if age > 65:
            bp_threshold = "Blood pressure >150/90 or <90/60"
        else:
            bp_threshold = "Blood pressure >140/90 or <90/60"
        
        thresholds = {
            'blood_pressure': bp_threshold,
            'heart_rate': "Heart rate >100 or <60 bpm",
            'temperature': "Temperature >101°F or <96°F",
            'respiratory_rate': "Respiratory rate >24 or <12/min"
        }
        
        # Condition-specific thresholds
        if condition == 'diabetes':
            thresholds.update({
                'glucose': "Blood glucose >300 or <70 mg/dL",
                'ketones': "Ketones >1.5 mmol/L"
            })
        
        return thresholds
    
    def _get_self_management_tips(self, condition: str) -> List[str]:
        """Get self-management tips for condition"""
        general_tips = [
            "Take medications as prescribed",
            "Keep regular appointments",
            "Monitor symptoms daily",
            "Maintain healthy lifestyle"
        ]
        
        condition_tips = {
            'hypertension': [
                "Monitor blood pressure regularly",
                "Limit sodium intake",
                "Exercise regularly",
                "Manage stress"
            ],
            'diabetes': [
                "Monitor blood sugar levels",
                "Follow meal plan",
                "Take medications on time",
                "Stay hydrated"
            ]
        }
        
        if condition in condition_tips:
            return general_tips + condition_tips[condition]
        return general_tips
    
    def _get_warning_signs(self, condition: str) -> List[str]:
        """Get warning signs that require immediate attention"""
        general_warnings = [
            "Severe or worsening symptoms",
            "Difficulty breathing",
            "Chest pain",
            "Loss of consciousness"
        ]
        
        condition_warnings = {
            'hypertension': [
                "Severe headache",
                "Vision changes",
                "Severe chest pain",
                "Difficulty breathing"
            ],
            'diabetes': [
                "Very high or low blood sugar",
                "Ketones in urine",
                "Severe dehydration",
                "Persistent vomiting"
            ]
        }
        
        if condition in condition_warnings:
            return general_warnings + condition_warnings[condition]
        return general_warnings
    
    def _get_lifestyle_recommendations(self, condition: str, patient_data: Dict[str, Any]) -> List[str]:
        """Get lifestyle recommendations based on condition and patient data"""
        recommendations = []
        
        # Universal recommendations
        recommendations.extend([
            "Maintain regular sleep schedule",
            "Stay physically active as tolerated",
            "Eat balanced, nutritious meals",
            "Avoid tobacco and limit alcohol"
        ])
        
        # Condition-specific recommendations
        if condition == 'hypertension':
            recommendations.extend([
                "Follow DASH diet principles",
                "Limit sodium to <2300mg daily",
                "Maintain healthy weight"
            ])
        elif condition == 'diabetes':
            recommendations.extend([
                "Count carbohydrates",
                "Eat at regular intervals",
                "Monitor portion sizes"
            ])
        
        # Age-specific modifications
        age = patient_data.get('age', 0)
        if age > 65:
            recommendations.append("Consider gentle, low-impact exercises")
            recommendations.append("Ensure adequate calcium and vitamin D intake")
        
        return recommendations
    
    async def _check_contraindications(self, plan: Dict[str, Any], patient_data: Dict[str, Any]) -> List[str]:
        """Check for contraindications in treatment plan"""
        contraindications = []
        
        # Check allergies
        allergies = patient_data.get('allergies', [])
        for allergy in allergies:
            # Simple check - in production, would need comprehensive drug/herb database
            if any(allergy.lower() in str(treatment).lower() for treatment in plan.values()):
                contraindications.append(f"Patient allergic to {allergy}")
        
        # Age-based contraindications
        age = patient_data.get('age', 0)
        if age < 18:
            contraindications.append("Some adult medications not suitable for pediatric use")
        if age > 75:
            contraindications.append("Consider dose adjustments for advanced age")
        
        return contraindications
    
    def _identify_synergies(self, plan: Dict[str, Any]) -> List[str]:
        """Identify potential synergies in treatment plan"""
        synergies = []
        
        # Check for complementary approaches
        if 'allopathic' in plan and 'ayurvedic' in plan:
            synergies.append("Allopathic and Ayurvedic approaches may complement each other")
        
        if 'yoga' in plan and any(key in plan for key in ['ayurvedic', 'lifestyle']):
            synergies.append("Yoga therapy enhances overall wellness approach")
        
        return synergies
    
    def _recommend_treatment_sequence(self, plan: Dict[str, Any]) -> List[str]:
        """Recommend sequence for implementing treatments"""
        sequence = []
        
        # General sequencing principles
        if 'allopathic' in plan:
            sequence.append("1. Initiate allopathic treatment for immediate symptom control")
        
        if 'lifestyle' in plan:
            sequence.append("2. Implement lifestyle modifications gradually")
        
        if 'ayurvedic' in plan:
            sequence.append("3. Add Ayurvedic therapies after stabilization")
        
        if 'complementary' in plan:
            sequence.append("4. Introduce complementary therapies as adjunct")
        
        return sequence
    
    def _estimate_treatment_costs(self, plan: Dict[str, Any]) -> Dict[str, str]:
        """Provide rough cost estimates for treatment modalities"""
        return {
            'allopathic': "Moderate to high (insurance may cover)",
            'ayurvedic': "Low to moderate (typically out-of-pocket)",
            'yoga_therapy': "Low (group classes) to moderate (private sessions)",
            'acupuncture': "Moderate (some insurance coverage)",
            'lifestyle_modifications': "Low (mainly lifestyle changes)"
        }
    
    def _get_basic_recommendations(self) -> List[str]:
        """Get basic fallback recommendations"""
        return [
            "Consult with healthcare provider for proper diagnosis",
            "Maintain healthy lifestyle with regular exercise",
            "Follow balanced diet appropriate for your condition",
            "Monitor symptoms and seek care if they worsen",
            "Consider integrative approaches under professional guidance"
        ]