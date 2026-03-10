import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(page_title="Cancer Wellness Platform", page_icon="🎗️", layout="wide")

# Enhanced color scheme with cancer-specific colors
COLOR_SCHEME = {
    'primary': '#4A90E2',
    'secondary': '#87CEEB',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'light': '#f8f9fa',
    'dark': '#343a40',
    'cancer_colors': {
        'Respiratory': '#FF6B6B',
        'Gastrointestinal': '#4ECDC4',
        'Reproductive': '#FFD166',
        'Genitourinary': '#06D6A0',
        'Endocrine': '#118AB2',
        'Dermatologic': '#073B4C',
        'Hematologic': '#EF476F',
        'Neurological': '#7209B7'
    }
}

# Session state
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'symptom_log' not in st.session_state:
    st.session_state.symptom_log = []
if 'activity_completed' not in st.session_state:
    st.session_state.activity_completed = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = "tracker"

# Cancer types database with categories - 20 cancer types
CANCER_TYPES = {
    # Respiratory/Thoracic
    "Lung Cancer": {
        "category": "Respiratory",
        "gender_prevalence": "Both",
        "specific_challenges": ["Breathing difficulties", "Chest pain", "Fatigue", "Shortness of breath"],
        "priority_activities": ["Breathing exercises", "Gentle mobility", "Respiratory rehabilitation"]
    },
    "Mesothelioma": {
        "category": "Respiratory",
        "gender_prevalence": "Both",
        "specific_challenges": ["Chest pain", "Breathing difficulties", "Fluid buildup", "Fatigue"],
        "priority_activities": ["Breathing exercises", "Gentle movement", "Pain management"]
    },
    
    # Gastrointestinal
    "Colorectal Cancer": {
        "category": "Gastrointestinal",
        "gender_prevalence": "Both",
        "specific_challenges": ["Digestive issues", "Abdominal pain", "Changes in bowel habits", "Fatigue"],
        "priority_activities": ["Nutrition focus", "Gentle movement", "Stress management"]
    },
    "Liver Cancer": {
        "category": "Gastrointestinal",
        "gender_prevalence": "Both",
        "specific_challenges": ["Abdominal swelling", "Fatigue", "Loss of appetite", "Nausea"],
        "priority_activities": ["Nutrition management", "Gentle activities", "Energy conservation"]
    },
    "Stomach Cancer": {
        "category": "Gastrointestinal", 
        "gender_prevalence": "Both",
        "specific_challenges": ["Nausea", "Loss of appetite", "Abdominal pain", "Early satiety"],
        "priority_activities": ["Small frequent meals", "Gentle movement", "Nausea management"]
    },
    "Esophageal Cancer": {
        "category": "Gastrointestinal",
        "gender_prevalence": "Both",
        "specific_challenges": ["Swallowing difficulties", "Chest pain", "Weight loss", "Reflux"],
        "priority_activities": ["Swallowing exercises", "Nutrition support", "Gentle mobility"]
    },
    "Pancreatic Cancer": {
        "category": "Gastrointestinal",
        "gender_prevalence": "Both",
        "specific_challenges": ["Abdominal pain", "Diabetes management", "Weight loss", "Fatigue"],
        "priority_activities": ["Pain management", "Nutrition support", "Gentle exercise"]
    },
    "Gallbladder Cancer": {
        "category": "Gastrointestinal",
        "gender_prevalence": "Females",
        "specific_challenges": ["Abdominal pain", "Jaundice", "Nausea", "Weight loss"],
        "priority_activities": ["Nutrition support", "Pain management", "Gentle activities"]
    },
    
    # Reproductive - Female
    "Breast Cancer": {
        "category": "Reproductive",
        "gender_prevalence": "Both",
        "specific_challenges": ["Arm mobility issues", "Lymphedema risk", "Body image concerns", "Surgical recovery"],
        "priority_activities": ["Arm mobility exercises", "Lymphatic drainage", "Body image support"]
    },
    "Cervical Cancer": {
        "category": "Reproductive",
        "gender_prevalence": "Females",
        "specific_challenges": ["Pelvic pain", "Urinary issues", "Sexual health concerns", "Fatigue"],
        "priority_activities": ["Pelvic floor exercises", "Gentle movement", "Emotional support"]
    },
    "Ovarian Cancer": {
        "category": "Reproductive",
        "gender_prevalence": "Females", 
        "specific_challenges": ["Abdominal bloating", "Pelvic pain", "Digestive issues", "Fatigue"],
        "priority_activities": ["Gentle abdominal exercises", "Nutrition support", "Stress management"]
    },
    "Uterine Cancer": {
        "category": "Reproductive",
        "gender_prevalence": "Females",
        "specific_challenges": ["Pelvic pain", "Urinary issues", "Hormonal changes", "Recovery from surgery"],
        "priority_activities": ["Pelvic rehabilitation", "Hormonal balance support", "Gentle exercise"]
    },
    
    # Reproductive - Male  
    "Prostate Cancer": {
        "category": "Reproductive",
        "gender_prevalence": "Males",
        "specific_challenges": ["Urinary incontinence", "Sexual dysfunction", "Fatigue", "Hormone therapy effects"],
        "priority_activities": ["Pelvic floor exercises", "Gentle strength training", "Emotional support"]
    },
    "Testicular Cancer": {
        "category": "Reproductive", 
        "gender_prevalence": "Males",
        "specific_challenges": ["Hormonal changes", "Fertility concerns", "Body image", "Recovery from surgery"],
        "priority_activities": ["Gentle exercise", "Emotional support", "Body image counseling"]
    },
    
    # Genitourinary
    "Kidney Cancer": {
        "category": "Genitourinary",
        "gender_prevalence": "Both",
        "specific_challenges": ["Flank pain", "Blood in urine", "Fatigue", "High blood pressure"],
        "priority_activities": ["Gentle movement", "Blood pressure management", "Fatigue management"]
    },
    "Bladder Cancer": {
        "category": "Genitourinary",
        "gender_prevalence": "Both",
        "specific_challenges": ["Urinary frequency", "Pelvic pain", "Fatigue", "Incontinence"],
        "priority_activities": ["Pelvic floor exercises", "Bladder training", "Gentle exercise"]
    },
    
    # Endocrine
    "Thyroid Cancer": {
        "category": "Endocrine",
        "gender_prevalence": "Both",
        "specific_challenges": ["Hormone imbalances", "Voice changes", "Neck stiffness", "Fatigue"],
        "priority_activities": ["Voice exercises", "Neck mobility", "Energy management"]
    },
    
    # Dermatologic
    "Melanoma": {
        "category": "Dermatologic",
        "gender_prevalence": "Both",
        "specific_challenges": ["Sun sensitivity", "Scarring", "Anxiety about recurrence", "Fatigue"],
        "priority_activities": ["Sun protection education", "Scar management", "Stress reduction"]
    },
    
    # Hematologic
    "Leukemia": {
        "category": "Hematologic",
        "gender_prevalence": "Both",
        "specific_challenges": ["Fatigue", "Increased infection risk", "Bleeding tendency", "Bone pain"],
        "priority_activities": ["Infection prevention", "Gentle movement", "Energy conservation"]
    },
    "Lymphoma": {
        "category": "Hematologic",
        "gender_prevalence": "Both",
        "specific_challenges": ["Swollen lymph nodes", "Fatigue", "Night sweats", "Infection risk"],
        "priority_activities": ["Gentle exercise", "Temperature regulation", "Immune support"]
    },
    
    # Neurological
    "Brain Cancer": {
        "category": "Neurological",
        "gender_prevalence": "Equal",
        "specific_challenges": ["Cognitive changes", "Balance issues", "Seizures", "Headaches"],
        "priority_activities": ["Cognitive rehabilitation", "Balance training", "Seizure safety"]
    }
}

# Enhanced activity instructions with cancer-specific recommendations
activity_instructions = {
    "Respiratory Rehabilitation": {
        "duration": "15-20 minutes", 
        "difficulty": "Easy to Moderate",
        "benefits": "Improves lung capacity, reduces shortness of breath, enhances oxygen flow",
        "cancer_specific": ["Lung Cancer", "Mesothelioma"],
        "steps": [
            "Sit upright in a comfortable chair with back support",
            "Practice diaphragmatic breathing: hand on chest, hand on belly",
            "Inhale slowly through nose, expanding belly not chest",
            "Exhale slowly through pursed lips like blowing out a candle",
            "Repeat for 5-10 breaths, rest, then repeat",
            "Practice coughing technique: take deep breath, cough twice sharply",
            "End with gentle shoulder and neck stretches"
        ],
        "tips": [
            "Stop if you feel dizzy or lightheaded",
            "Use pillows for support if needed",
            "Practice when you're most energetic"
        ],
        "ideal_conditions": {
            "energy": (4, 10),
            "fatigue": (1, 7)
        }
    },
    
    "Lymphatic Drainage Exercises": {
        "duration": "10-15 minutes",
        "difficulty": "Easy", 
        "benefits": "Reduces lymphedema risk, improves circulation, reduces swelling",
        "cancer_specific": ["Breast Cancer", "Melanoma"],
        "steps": [
            "Start with deep breathing to activate lymphatic system",
            "Gentle neck stretches: turn head side to side slowly",
            "Shoulder pumps: lift shoulders up and back, release slowly",
            "Arm circles: small circles progressing to larger ones",
            "Gentle self-massage: stroke from fingers toward heart",
            "Elevate affected arm on pillows for 10 minutes",
            "End with gentle whole-body stretching"
        ],
        "tips": [
            "Never massage directly over tumor sites", 
            "Use light pressure only",
            "Watch for signs of swelling"
        ],
        "ideal_conditions": {
            "pain": (1, 5),
            "energy": (3, 10)
        }
    },
    
    "Pelvic Floor Rehabilitation": {
        "duration": "15-20 minutes",
        "difficulty": "Easy",
        "benefits": "Improves incontinence, supports pelvic health, reduces pain",
        "cancer_specific": ["Prostate Cancer", "Cervical Cancer", "Uterine Cancer", "Bladder Cancer"],
        "steps": [
            "Find comfortable position: lying down or sitting",
            "Locate pelvic floor muscles (stop urine flow muscles)",
            "Contract muscles gently, hold for 3 seconds",
            "Relax completely for 3 seconds", 
            "Repeat 10 times, rest, do 2 more sets",
            "Practice quick contractions: squeeze and release rapidly",
            "Coordinate with breathing: contract on exhale"
        ],
        "tips": [
            "Don't hold your breath",
            "Avoid tightening buttocks or thighs",
            "Be patient - improvement takes weeks"
        ],
        "ideal_conditions": {
            "energy": (3, 10),
            "pain": (1, 6)
        }
    },
    
    "Cognitive Rehabilitation Exercises": {
        "duration": "15-25 minutes", 
        "difficulty": "Easy to Moderate",
        "benefits": "Improves memory, focus, and mental clarity, addresses chemo brain",
        "cancer_specific": ["Brain Cancer", "Leukemia", "Lymphoma"],
        "steps": [
            "Set up quiet environment with minimal distractions",
            "Memory games: remember and recite grocery lists",
            "Word puzzles: crosswords, word searches, anagrams", 
            "Number sequences: count backwards from 100 by 7s",
            "Visual attention: find differences in pictures",
            "Dual tasking: walk while naming animals alphabetically",
            "Journal writing: describe your day in detail"
        ],
        "tips": [
            "Start with easier tasks and progress gradually",
            "Use memory aids and reminders",
            "Practice daily for best results"
        ],
        "ideal_conditions": {
            "mental_clarity": (4, 10),
            "energy": (4, 10),
            "fatigue": (1, 6)
        }
    },
    
    "Gentle Digestive Support": {
        "duration": "Throughout day",
        "difficulty": "Easy",
        "benefits": "Improves digestion, reduces nausea, supports nutrition absorption",
        "cancer_specific": ["Colorectal Cancer", "Stomach Cancer", "Pancreatic Cancer", "Liver Cancer", "Gallbladder Cancer"],
        "steps": [
            "Eat small, frequent meals (6 small vs 3 large)",
            "Choose bland foods when nauseous: rice, toast, bananas",
            "Stay hydrated: sip fluids between (not during) meals",
            "Practice mindful eating: chew slowly, focus on food",
            "Gentle abdominal massage: circular motions clockwise",
            "Light walking after meals to aid digestion", 
            "Track food tolerance and symptoms"
        ],
        "tips": [
            "Avoid spicy, greasy, or very hot foods",
            "Keep crackers nearby for nausea",
            "Consider ginger tea for stomach upset"
        ],
        "ideal_conditions": {
            "nausea": (1, 6),
            "appetite": (3, 10)
        }
    },
    
    "Hormone Balance Support": {
        "duration": "20-30 minutes",
        "difficulty": "Easy", 
        "benefits": "Supports hormonal health, reduces hot flashes, improves mood",
        "cancer_specific": ["Breast Cancer", "Prostate Cancer", "Thyroid Cancer"],
        "steps": [
            "Practice stress-reduction techniques: deep breathing",
            "Gentle yoga poses: child's pose, legs up wall",
            "Temperature regulation: layered clothing, cool compresses",
            "Regular sleep schedule: same bedtime/wake time daily",
            "Moderate exercise: 20 minutes walking or swimming",
            "Mindfulness meditation: 10 minutes daily",
            "Track symptoms and triggers in journal"
        ],
        "tips": [
            "Avoid alcohol and caffeine if they trigger symptoms",
            "Use fans or cooling products for hot flashes", 
            "Consider relaxation apps for guided meditation"
        ],
        "ideal_conditions": {
            "mood": (1, 7),
            "sleep_quality": (1, 7),
            "energy": (3, 10)
        }
    },
    
    "Voice and Swallowing Therapy": {
        "duration": "10-15 minutes",
        "difficulty": "Easy",
        "benefits": "Improves voice quality, supports safe swallowing, reduces throat discomfort",
        "cancer_specific": ["Thyroid Cancer", "Esophageal Cancer"],
        "steps": [
            "Warm up with gentle humming and lip trills",
            "Voice exercises: say 'ahh' at comfortable pitch",
            "Swallowing practice: dry swallows, then small sips water",
            "Throat clearing: gentle 'ahem' sounds",
            "Reading aloud: start with short passages",
            "Neck and jaw stretches: gentle circular motions",
            "Cool down with quiet humming"
        ],
        "tips": [
            "Stay well hydrated throughout the day",
            "Avoid whispering - use normal voice or rest",
            "Take frequent voice breaks"
        ],
        "ideal_conditions": {
            "pain": (1, 5),
            "energy": (3, 10)
        }
    },
    
    # Universal activities work for all cancer types
    "Gentle Yoga and Stretching": {
        "duration": "20-30 minutes",
        "difficulty": "Easy", 
        "benefits": "Reduces fatigue, improves flexibility, boosts mood, reduces stress",
        "cancer_specific": "All",
        "steps": [
            "Start with 5 minutes of gentle breathing",
            "Neck rolls and shoulder shrugs",
            "Seated spinal twists if comfortable",
            "Gentle forward fold from chair",
            "Arms overhead reach and side bends",
            "Legs up the wall pose or on chair",
            "End with 5 minutes of relaxation"
        ],
        "tips": [
            "Listen to your body - modify as needed",
            "Use props like pillows and blankets",
            "Never force any position"
        ],
        "ideal_conditions": {
            "energy": (3, 8),
            "pain": (1, 6),
            "fatigue": (1, 7)
        }
    },
    
    "Mindful Breathing and Meditation": {
        "duration": "10-20 minutes",
        "difficulty": "Easy",
        "benefits": "Reduces anxiety, improves sleep, manages pain, promotes healing",
        "cancer_specific": "All",
        "steps": [
            "Find comfortable position, close eyes softly",
            "Focus on natural breath without changing it",
            "Count breaths: inhale 1, exhale 2, up to 10",
            "When mind wanders, gently return to counting",
            "Body scan: notice sensations without judgment",
            "Loving-kindness: send good wishes to yourself",
            "End with three deep, intentional breaths"
        ],
        "tips": [
            "No need to stop thoughts - just observe them",
            "Start with shorter sessions and build up",
            "Use guided meditation apps if helpful"
        ],
        "ideal_conditions": {
            "mood": (1, 8),
            "mental_clarity": (1, 10),
            "fatigue": (1, 10)
        }
    },
    
    "Gentle Strength and Balance": {
        "duration": "15-25 minutes", 
        "difficulty": "Easy to Moderate",
        "benefits": "Maintains muscle mass, improves bone health, prevents falls",
        "cancer_specific": "All",
        "steps": [
            "Warm up: marching in place for 2 minutes",
            "Chair-based exercises: sit to stand 5-10 reps",
            "Wall push-ups: arms length from wall 5-10 reps",
            "Balance practice: stand on one foot hold chair",
            "Light weights or water bottles: bicep curls",
            "Heel-to-toe walking along straight line",
            "Cool down with gentle stretching"
        ],
        "tips": [
            "Progress slowly and safely",
            "Use chair or wall for balance support",
            "Stop if feeling dizzy or overly tired"
        ],
        "ideal_conditions": {
            "energy": (5, 10),
            "fatigue": (1, 5),
            "pain": (1, 4)
        }
    },
    
    "Social Connection and Support": {
        "duration": "30-60 minutes",
        "difficulty": "Easy",
        "benefits": "Reduces isolation, improves mood, provides emotional support",
        "cancer_specific": "All", 
        "steps": [
            "Schedule regular calls with family/friends",
            "Join cancer support groups online or in-person",
            "Participate in community activities within energy level",
            "Share feelings honestly with trusted people",
            "Ask for specific help when needed",
            "Write in gratitude journal or letters",
            "Consider peer mentoring or volunteering"
        ],
        "tips": [
            "Quality connections matter more than quantity",
            "Set boundaries about your energy and time",
            "Use technology when travel is difficult"
        ],
        "ideal_conditions": {
            "mood": (1, 8),
            "energy": (3, 10),
            "mental_clarity": (3, 10)
        }
    },
    
    # Additional specialized activities
    "Aquatic Therapy": {
        "duration": "20-30 minutes",
        "difficulty": "Easy to Moderate",
        "benefits": "Low impact exercise, improves circulation, reduces joint stress",
        "cancer_specific": ["Bone Cancer", "Joint-related cancers"],
        "steps": [
            "Enter pool gradually to adjust to temperature",
            "Start with gentle walking in shallow end",
            "Water marching: lift knees alternately",
            "Arm circles and shoulder rolls in water",
            "Gentle leg swings forward and back",
            "Float on back with pool noodle if comfortable",
            "Cool down with gentle stretching in water"
        ],
        "tips": [
            "Water temperature should be comfortable (82-86°F)",
            "Never swim alone - have supervision",
            "Exit pool if feeling tired or dizzy"
        ],
        "ideal_conditions": {
            "pain": (1, 7),
            "energy": (4, 10)
        }
    },
    
    "Art and Music Therapy": {
        "duration": "30-45 minutes",
        "difficulty": "Easy",
        "benefits": "Emotional expression, stress relief, cognitive stimulation",
        "cancer_specific": "All",
        "steps": [
            "Gather simple art supplies or music device",
            "Choose activity: drawing, painting, listening, singing",
            "Focus on process rather than outcome",
            "Express emotions through chosen medium",
            "Try different colors, rhythms, or techniques",
            "Share creation with others if desired",
            "Reflect on experience in journal"
        ],
        "tips": [
            "No artistic skill required - focus on enjoyment",
            "Use music to match or change your mood",
            "Consider group sessions for social benefits"
        ],
        "ideal_conditions": {
            "mood": (1, 8),
            "mental_clarity": (3, 10)
        }
    },
    
    "Sleep Hygiene Practices": {
        "duration": "Evening routine",
        "difficulty": "Easy",
        "benefits": "Improves sleep quality, supports healing, reduces fatigue",
        "cancer_specific": "All",
        "steps": [
            "Establish consistent bedtime routine",
            "Dim lights 1 hour before bedtime",
            "Avoid screens 30 minutes before sleep",
            "Create comfortable sleep environment",
            "Practice relaxation techniques in bed",
            "Use comfortable pillows and positioning",
            "Keep room cool and dark"
        ],
        "tips": [
            "Avoid caffeine 6 hours before bedtime",
            "Try chamomile tea or warm milk",
            "Use blackout curtains or eye mask"
        ],
        "ideal_conditions": {
            "sleep_quality": (1, 6),
            "fatigue": (1, 8)
        }
    }
}

# Enhanced scoring algorithm
def calculate_wellness_trends(symptom_log, days=7):
    if len(symptom_log) < 1:
        return {}
    
    df = pd.DataFrame(symptom_log)
    recent_data = df.tail(min(days, len(df)))
    
    trends = {}
    metrics = ['fatigue', 'pain', 'mood', 'appetite', 'sleep_quality', 'nausea', 'energy', 'mental_clarity']
    
    for metric in metrics:
        trends[f"{metric}_avg"] = recent_data[metric].mean()
        trends[f"{metric}_current"] = recent_data[metric].iloc[-1]
        
        if len(recent_data) >= 2:
            trends[f"{metric}_trend"] = recent_data[metric].diff().mean()
            trends[f"{metric}_volatility"] = recent_data[metric].std()
        else:
            trends[f"{metric}_trend"] = 0
            trends[f"{metric}_volatility"] = 0
    
    return trends

def get_cancer_specific_recommendations(cancer_type, symptom_log, user_profile, num_recommendations=3):
    """Get recommendations tailored to specific cancer type"""
    # Filter activities by cancer type
    relevant_activities = {}
    
    for activity_name, activity_info in activity_instructions.items():
        cancer_specific = activity_info.get("cancer_specific", "All")
        if cancer_specific == "All" or cancer_type in cancer_specific:
            relevant_activities[activity_name] = activity_info
    
    if not symptom_log:
        # Return default recommendations based on cancer type
        cancer_info = CANCER_TYPES.get(cancer_type, {})
        priority_activities = cancer_info.get("priority_activities", [])
        
        recommended = []
        for activity_name in relevant_activities.keys():
            if any(priority in activity_name for priority in priority_activities):
                recommended.append((activity_name, 85))
            elif len(recommended) < num_recommendations:
                recommended.append((activity_name, 70))
        
        return recommended[:num_recommendations]
    
    # Calculate scores for relevant activities
    trends = calculate_wellness_trends(symptom_log)
    recent_entries = symptom_log[-3:] if len(symptom_log) >= 3 else symptom_log[-1:]
    
    recent_metrics = {}
    metrics = ['fatigue', 'pain', 'mood', 'appetite', 'sleep_quality', 'nausea', 'energy', 'mental_clarity']
    
    for metric in metrics:
        values = [entry[metric] for entry in recent_entries if metric in entry]
        if values:
            recent_metrics[metric] = np.mean(values)
    
    # Score activities
    activity_scores = {}
    for activity_name, activity_info in relevant_activities.items():
        base_score = 50
        
        # Check ideal conditions
        ideal_conditions = activity_info.get("ideal_conditions", {})
        condition_score = 0
        matches = 0
        
        for metric, (min_val, max_val) in ideal_conditions.items():
            if metric in recent_metrics:
                current_value = recent_metrics[metric]
                if min_val <= current_value <= max_val:
                    condition_score += 100
                else:
                    distance = min(abs(current_value - min_val), abs(current_value - max_val))
                    condition_score += max(0, 100 - (distance * 15))
                matches += 1
        
        if matches > 0:
            base_score = condition_score / matches
        
        # Cancer-specific bonuses
        cancer_info = CANCER_TYPES.get(cancer_type, {})
        specific_challenges = cancer_info.get("specific_challenges", [])
        
        # Boost score if activity addresses specific challenges
        if any(challenge.lower() in activity_name.lower() for challenge in specific_challenges):
            base_score += 25
        
        # Treatment phase considerations
        treatment_phase = user_profile.get("treatment_phase", "")
        if "Chemotherapy" in treatment_phase and "Gentle" in activity_name:
            base_score += 15
        
        activity_scores[activity_name] = min(100, base_score)
    
    # Sort and return top recommendations
    sorted_activities = sorted(activity_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_activities[:num_recommendations]

def calculate_advanced_metrics(symptom_log):
    """Calculate advanced wellness metrics with single-day support"""
    if len(symptom_log) < 1:
        return {}, pd.DataFrame()
    
    df = pd.DataFrame(symptom_log)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Calculate wellness score
    positive_metrics = ['mood', 'appetite', 'sleep_quality', 'energy', 'mental_clarity']
    negative_metrics = ['fatigue', 'pain', 'nausea']
    
    wellness_scores = []
    for _, row in df.iterrows():
        positive_avg = np.mean([row[metric] for metric in positive_metrics if metric in row])
        negative_avg = np.mean([11 - row[metric] for metric in negative_metrics if metric in row])
        wellness_score = (positive_avg + negative_avg) / 2
        wellness_scores.append(wellness_score)
    
    df['wellness_score'] = wellness_scores
    
    metrics = {}
    
    # Basic metrics
    metrics['current_wellness'] = wellness_scores[-1]
    metrics['best_wellness'] = max(wellness_scores)
    metrics['worst_wellness'] = min(wellness_scores)
    
    # Trend analysis
    if len(df) >= 2:
        dates_numeric = np.arange(len(df))
        trend_coeffs = np.polyfit(dates_numeric, wellness_scores, 1)
        metrics['wellness_trend'] = trend_coeffs[0]
        metrics['wellness_volatility'] = df['wellness_score'].std()
        
        # Weekly improvement if enough data
        if len(df) >= 7:
            last_week_avg = df['wellness_score'].tail(7).mean()
            previous_week_avg = df['wellness_score'].iloc[-14:-7].mean() if len(df) >= 14 else last_week_avg
            metrics['weekly_improvement'] = last_week_avg - previous_week_avg
    else:
        metrics['wellness_trend'] = 0
        metrics['wellness_volatility'] = 0
        metrics['weekly_improvement'] = 0
    
    return metrics, df

# Enhanced CSS with cancer-specific colors
st.markdown(f"""
<style>
/* Enhanced color scheme */
.primary-bg {{ background-color: {COLOR_SCHEME['primary']}; }}
.secondary-bg {{ background-color: {COLOR_SCHEME['secondary']}; }}

/* Enhanced slider styling */
.stSlider > div > div > div {{
    background: linear-gradient(to right, {COLOR_SCHEME['secondary']} 0%, {COLOR_SCHEME['primary']} 100%);
}}

.stSlider > div > div > div > div {{
    background-color: {COLOR_SCHEME['primary']};
}}

.stSlider > div > div > div > div:hover {{
    background-color: #357ABD;
}}

/* Cancer category badges with specific colors */
.category-badge-respiratory {{ background: {COLOR_SCHEME['cancer_colors']['Respiratory']}; color: white; }}
.category-badge-gastrointestinal {{ background: {COLOR_SCHEME['cancer_colors']['Gastrointestinal']}; color: white; }}
.category-badge-reproductive {{ background: {COLOR_SCHEME['cancer_colors']['Reproductive']}; color: white; }}
.category-badge-genitourinary {{ background: {COLOR_SCHEME['cancer_colors']['Genitourinary']}; color: white; }}
.category-badge-endocrine {{ background: {COLOR_SCHEME['cancer_colors']['Endocrine']}; color: white; }}
.category-badge-dermatologic {{ background: {COLOR_SCHEME['cancer_colors']['Dermatologic']}; color: white; }}
.category-badge-hematologic {{ background: {COLOR_SCHEME['cancer_colors']['Hematologic']}; color: white; }}
.category-badge-neurological {{ background: {COLOR_SCHEME['cancer_colors']['Neurological']}; color: white; }}

.cancer-selection-box {{
    background: linear-gradient(135deg, #f0f8ff 0%, #e3f2fd 100%);
    border: 2px solid {COLOR_SCHEME['primary']};
    border-radius: 15px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(74, 144, 226, 0.1);
}}

.cancer-info-box {{
    background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
    border: 2px solid {COLOR_SCHEME['primary']};
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(74, 144, 226, 0.15);
}}

.activity-card {{
    border: 2px solid #e1f5fe;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    background: linear-gradient(135deg, #f8f9ff 0%, #e3f2fd 100%);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.activity-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(74, 144, 226, 0.15);
}}

.challenge-tag {{
    background: {COLOR_SCHEME['secondary']};
    color: #333;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.85rem;
    margin: 0.2rem;
    display: inline-block;
    font-weight: 500;
}}

.category-badge {{
    background: linear-gradient(135deg, {COLOR_SCHEME['primary']} 0%, #357ABD 100%);
    color: white;
    padding: 0.4rem 1rem;
    border-radius: 25px;
    font-size: 0.9rem;
    font-weight: bold;
    box-shadow: 0 2px 8px rgba(74, 144, 226, 0.3);
}}

.metric-box {{
    background: linear-gradient(135deg, #f0f8ff 0%, #e3f2fd 100%);
    border: 1px solid {COLOR_SCHEME['primary']};
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
    text-align: center;
}}

.info-highlight {{
    background: linear-gradient(135deg, {COLOR_SCHEME['secondary']} 0%, {COLOR_SCHEME['primary']} 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    font-weight: 500;
}}

.progress-card {{
    background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
    border: 2px solid {COLOR_SCHEME['primary']};
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(74, 144, 226, 0.1);
}}

.insight-box {{
    background: linear-gradient(135deg, #e8f4f8 0%, #d4edda 100%);
    border-left: 4px solid {COLOR_SCHEME['primary']};
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 5px;
}}

.alert-box {{
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    border-left: 4px solid {COLOR_SCHEME['warning']};
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 5px;
}}

.success-box {{
    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    border-left: 4px solid {COLOR_SCHEME['success']};
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 5px;
}}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {{
    gap: 2px;
}}

.stTabs [data-baseweb="tab"] {{
    height: 50px;
    white-space: pre-wrap;
    background-color: #f0f2f6;
    border-radius: 10px 10px 0px 0px;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
}}

.stTabs [aria-selected="true"] {{
    background-color: {COLOR_SCHEME['primary']};
    color: white;
}}

/* Button enhancements */
.stButton > button {{
    border-radius: 10px;
    border: 2px solid {COLOR_SCHEME['primary']};
    background: white;
    color: {COLOR_SCHEME['primary']};
    font-weight: bold;
    transition: all 0.3s ease;
}}

.stButton > button:hover {{
    background: {COLOR_SCHEME['primary']};
    color: white;
    transform: translateY(-1px);
}}

/* Progress bars */
.stProgress > div > div > div > div {{
    background-color: {COLOR_SCHEME['primary']};
}}
</style>
""", unsafe_allow_html=True)

# Main navigation in main area
st.title("Cancer Wellness Platform")

# Navigation tabs in main area
tab1, tab2, tab3, tab4 = st.tabs([
    "Cancer-Specific Wellness", 
    "Today's Activities", 
    "Progress Analysis", 
    "Detailed Insights & Patterns"
])

# Page 1: Cancer-Specific Wellness
with tab1:
    # User Profile Section
    st.header("👤 Patient Profile Setup")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name", value=st.session_state.user_profile.get("name", ""))
            age = st.number_input("Age", min_value=18, max_value=100, 
                                value=st.session_state.user_profile.get("age", 50))
            
        with col2:
            treatment_phase = st.selectbox("Treatment Phase", [
                "Pre-Treatment", "During Chemotherapy", "During Radiation", 
                "Post-Treatment", "Maintenance Therapy", "Survivorship"
            ], index=0 if not st.session_state.user_profile else 
                    ["Pre-Treatment", "During Chemotherapy", "During Radiation", 
                     "Post-Treatment", "Maintenance Therapy", "Survivorship"].index(
                         st.session_state.user_profile.get("treatment_phase", "Pre-Treatment")))
            
            energy_level = st.slider("Current Energy Level (1-10)", 1, 10, 
                                    st.session_state.user_profile.get("energy_level", 5))
        
        if st.form_submit_button("Save Profile", type="primary"):
            st.session_state.user_profile.update({
                "name": name, "age": age, "treatment_phase": treatment_phase,
                "energy_level": energy_level
            })
            st.success("Profile saved successfully! Now select your cancer type below.")
    
    # Cancer Type Selection Box
    st.markdown('<div class="cancer-selection-box">', unsafe_allow_html=True)
    st.header("Select Your Cancer Type")
    
    # Create a list of all cancer types for the selectbox
    cancer_options = ["Select a cancer type..."] + list(CANCER_TYPES.keys())
    
    selected_cancer = st.selectbox(
        "Choose your specific cancer type:",
        options=cancer_options,
        index=0 if not st.session_state.user_profile.get("cancer_type") 
        else cancer_options.index(st.session_state.user_profile.get("cancer_type"))
    )
    
    if selected_cancer != "Select a cancer type...":
        # Update session state
        st.session_state.user_profile["cancer_type"] = selected_cancer
        
        # Show specific information
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="cancer-info-box">', unsafe_allow_html=True)
        
        cancer_info = CANCER_TYPES[selected_cancer]
        category = cancer_info["category"].lower().replace(" ", "-")
        
        # Display key information in organized layout
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="category-badge-{category}">Category: {cancer_info["category"]} System</div>', 
                       unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="info-highlight">Higher Prevalence: {cancer_info["gender_prevalence"]}</div>', 
                       unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="info-highlight">Tracked Challenges: {len(cancer_info["specific_challenges"])}</div>', 
                       unsafe_allow_html=True)
        
        # Common challenges section
        st.subheader("Common Challenges for Your Cancer Type")
        st.write("These are the most frequently reported challenges for patients with your cancer type:")
        challenge_cols = st.columns(2)
        for i, challenge in enumerate(cancer_info["specific_challenges"]):
            with challenge_cols[i % 2]:
                st.markdown(f'<div class="challenge-tag">{i+1}. {challenge}</div>', 
                           unsafe_allow_html=True)
        
        # Priority activities section
        st.subheader("Recommended Activity Focus Areas")
        st.write("Based on your cancer type, these activities are most beneficial:")
        for i, activity in enumerate(cancer_info["priority_activities"], 1):
            st.markdown(f"**{i}. {activity}**")
        
        # Personalized recommendations if available
        if st.session_state.symptom_log:
            recommendations = get_cancer_specific_recommendations(
                selected_cancer, 
                st.session_state.symptom_log, 
                st.session_state.user_profile
            )
            
            st.subheader("Personalized Activity Recommendations")
            st.write("Based on your recent symptom logs:")
            for activity, score in recommendations:
                color = "green" if score > 80 else "orange" if score > 60 else "red"
                st.markdown(f"• **{activity}** <span style='color:{color}'>(Compatibility: {score:.0f}%)</span>", 
                           unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('</div>', unsafe_allow_html=True)

# Page 2: Today's Activities
with tab2:
    st.header("Today's Wellness Activities")
    
    if not st.session_state.user_profile.get("cancer_type"):
        st.warning("Please select your cancer type on the Cancer-Specific Wellness tab first.")
    else:
        cancer_type = st.session_state.user_profile["cancer_type"]
        
        # Symptom logging
        st.subheader("Log Today's Symptoms")
        with st.form("symptom_form"):
            st.write("Rate your symptoms today (1 = Worst, 10 = Best)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fatigue = st.slider("Fatigue Level", 1, 10, 5, 
                                  help="1 = Extremely fatigued, 10 = Full of energy")
                pain = st.slider("Pain Level", 1, 10, 8, 
                               help="1 = Severe pain, 10 = No pain")
                nausea = st.slider("Nausea Level", 1, 10, 8, 
                                 help="1 = Severe nausea, 10 = No nausea")
                appetite = st.slider("Appetite Level", 1, 10, 6, 
                                   help="1 = No appetite, 10 = Excellent appetite")
            
            with col2:
                mood = st.slider("Mood Level", 1, 10, 7, 
                               help="1 = Very low mood, 10 = Excellent mood")
                sleep_quality = st.slider("Sleep Quality", 1, 10, 6, 
                                        help="1 = Very poor sleep, 10 = Excellent sleep")
                energy = st.slider("Energy Level", 1, 10, 5, 
                                 help="1 = No energy, 10 = High energy")
                mental_clarity = st.slider("Mental Clarity", 1, 10, 7, 
                                         help="1 = Brain fog, 10 = Very clear")
            
            notes = st.text_area("Additional Notes", placeholder="Any other symptoms or observations...")
            
            if st.form_submit_button("Save Today's Log", type="primary"):
                today_entry = {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "fatigue": fatigue,
                    "pain": pain,
                    "nausea": nausea,
                    "appetite": appetite,
                    "mood": mood,
                    "sleep_quality": sleep_quality,
                    "energy": energy,
                    "mental_clarity": mental_clarity,
                    "notes": notes
                }
                st.session_state.symptom_log.append(today_entry)
                st.success("Today's symptoms logged successfully!")
        
        # Activity recommendations
        if st.session_state.symptom_log:
            st.subheader("Recommended Activities for Today")
            recommendations = get_cancer_specific_recommendations(
                cancer_type, 
                st.session_state.symptom_log, 
                st.session_state.user_profile,
                num_recommendations=4
            )
            
            for i, (activity, score) in enumerate(recommendations):
                with st.expander(f"{activity} (Recommended: {score:.0f}%)", expanded=i==0):
                    activity_info = activity_instructions[activity]
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**Duration:** {activity_info['duration']}")
                        st.write(f"**Difficulty:** {activity_info['difficulty']}")
                        st.write(f"**Benefits:** {activity_info['benefits']}")
                    
                    with col2:
                        if st.button(f"Mark as Completed", key=f"complete_{i}"):
                            completion_entry = {
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "activity": activity,
                                "score": score
                            }
                            st.session_state.activity_completed.append(completion_entry)
                            st.success(f"Great job completing {activity}!")
                    
                    st.write("**Steps:**")
                    for j, step in enumerate(activity_info['steps'], 1):
                        st.write(f"{j}. {step}")
                    
                    st.write("**Tips:**")
                    for tip in activity_info['tips']:
                        st.write(f"• {tip}")

# Page 3: Enhanced Progress Analysis
with tab3:
    st.header("Comprehensive Progress Analysis")
    
    if not st.session_state.symptom_log:
        st.info("Log some symptoms first to see your progress analysis.")
    else:
        # Calculate advanced metrics with single-day support
        advanced_metrics, df = calculate_advanced_metrics(st.session_state.symptom_log)
        
        # Overall wellness dashboard
        st.markdown('<div class="progress-card">', unsafe_allow_html=True)
        st.subheader("Wellness Dashboard")
        
        if len(st.session_state.symptom_log) == 1:
            # Single day view
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Today's Wellness",
                    f"{advanced_metrics['current_wellness']:.1f}/10",
                    "First day tracked!"
                )
            
            with col2:
                st.metric(
                    "Consistency",
                    "Starting",
                    "Keep logging daily"
                )
            
            with col3:
                st.metric(
                    "Next Steps",
                    "Log 3+ days",
                    "For trend analysis"
                )
            
            st.info("Continue logging symptoms daily to unlock trend analysis and advanced insights!")
            
        else:
            # Multi-day view
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                current_wellness = advanced_metrics['current_wellness']
                trend = advanced_metrics['wellness_trend']
                st.metric(
                    "Current Wellness",
                    f"{current_wellness:.1f}/10",
                    f"{trend:+.2f}/day" if abs(trend) > 0.01 else "Stable"
                )
            
            with col2:
                best_wellness = advanced_metrics['best_wellness']
                st.metric(
                    "Best Day",
                    f"{best_wellness:.1f}/10",
                    f"Peak performance"
                )
            
            with col3:
                volatility = advanced_metrics['wellness_volatility']
                stability_score = max(0, 10 - volatility * 2)
                st.metric(
                    "Stability Score",
                    f"{stability_score:.1f}/10",
                    "Higher is better"
                )
            
            with col4:
                if 'weekly_improvement' in advanced_metrics and len(st.session_state.symptom_log) >= 7:
                    weekly_imp = advanced_metrics['weekly_improvement']
                    st.metric(
                        "Weekly Progress",
                        f"{weekly_imp:+.1f}",
                        "vs previous week"
                    )
                else:
                    st.metric("Weekly Progress", "N/A", "Need 7+ days data")
            
            with col5:
                total_days = len(st.session_state.symptom_log)
                st.metric(
                    "Days Tracked",
                    f"{total_days}",
                    "Consistency matters"
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced visualizations (only show if we have enough data)
        if len(st.session_state.symptom_log) >= 2:
            st.subheader("Advanced Trend Analysis")
            
            # Create simplified visualization for limited data
            if len(st.session_state.symptom_log) < 3:
                # Simple line chart for 2 days
                fig = px.line(df, x='date', y='wellness_score', 
                             title="Wellness Progress - Early Tracking",
                             markers=True)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                st.info("Log one more day to unlock comprehensive trend analysis!")
                
            else:
                # Full analysis for 3+ days
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('Overall Wellness Trend', 'Symptom Categories', 
                                  'Energy vs Fatigue Balance', 'Sleep Impact Analysis'),
                    specs=[[{"secondary_y": False}, {"secondary_y": False}],
                           [{"secondary_y": True}, {"secondary_y": False}]]
                )
                
                # Overall wellness trend with moving average
                wellness_ma = df['wellness_score'].rolling(window=min(3, len(df)), center=True).mean()
                fig.add_trace(
                    go.Scatter(x=df['date'], y=df['wellness_score'], 
                              name='Daily Wellness', line=dict(color=COLOR_SCHEME['secondary'], width=1)),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Scatter(x=df['date'], y=wellness_ma, 
                              name=f'{min(3, len(df))}-Day Average', line=dict(color=COLOR_SCHEME['primary'], width=3)),
                    row=1, col=1
                )
                
                # Symptom categories comparison
                categories = {
                    'Physical Symptoms': ['fatigue', 'pain', 'nausea'],
                    'Mental Wellness': ['mood', 'mental_clarity'],
                    'Basic Functions': ['sleep_quality', 'appetite', 'energy']
                }
                
                category_scores = {}
                for category, metrics in categories.items():
                    recent_avg = df[metrics].tail(min(7, len(df))).mean().mean()
                    category_scores[category] = recent_avg
                
                fig.add_trace(
                    go.Bar(x=list(category_scores.keys()), y=list(category_scores.values()),
                           name='Recent Average', marker_color=[
                               COLOR_SCHEME['cancer_colors']['Respiratory'],
                               COLOR_SCHEME['cancer_colors']['Endocrine'],
                               COLOR_SCHEME['cancer_colors']['Gastrointestinal']
                           ]),
                    row=1, col=2
                )
                
                # Energy vs Fatigue balance
                fig.add_trace(
                    go.Scatter(x=df['date'], y=df['energy'], name='Energy Level',
                              line=dict(color=COLOR_SCHEME['success']), yaxis='y'),
                    row=2, col=1
                )
                fig.add_trace(
                    go.Scatter(x=df['date'], y=11-df['fatigue'], name='Anti-Fatigue (inverted)',
                              line=dict(color=COLOR_SCHEME['danger'], dash='dash'), yaxis='y'),
                    row=2, col=1
                )
                
                # Sleep quality impact
                if len(df) >= 3:
                    sleep_impact = df.groupby('sleep_quality')['wellness_score'].mean().reset_index()
                    if len(sleep_impact) > 1:
                        fig.add_trace(
                            go.Scatter(x=sleep_impact['sleep_quality'], y=sleep_impact['wellness_score'],
                                      mode='markers+lines', name='Sleep Quality Impact',
                                      marker=dict(size=10, color=COLOR_SCHEME['warning'])),
                            row=2, col=2
                        )
                
                fig.update_layout(height=600, showlegend=True, 
                                 title_text="Comprehensive Wellness Analytics")
                fig.update_yaxes(range=[1, 10])
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Activity effectiveness analysis
        if st.session_state.activity_completed and len(st.session_state.activity_completed) >= 1:
            st.subheader("Activity Effectiveness Analysis")
            
            activity_df = pd.DataFrame(st.session_state.activity_completed)
            activity_df['date'] = pd.to_datetime(activity_df['date'])
            
            if len(st.session_state.symptom_log) >= 2:
                # Merge with symptom data
                merged_df = pd.merge(df, activity_df, on='date', how='left')
                merged_df['has_activity'] = ~merged_df['activity'].isna()
                
                activity_days = merged_df[merged_df['has_activity']]
                no_activity_days = merged_df[~merged_df['has_activity']]
                
                if len(activity_days) > 0 and len(no_activity_days) > 0:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        activity_wellness = activity_days['wellness_score'].mean()
                        no_activity_wellness = no_activity_days['wellness_score'].mean()
                        improvement = activity_wellness - no_activity_wellness
                        
                        st.metric(
                            "Activity Impact",
                            f"{improvement:+.1f}",
                            "vs non-activity days"
                        )
                    
                    with col2:
                        completion_rate = len(activity_days) / len(merged_df) * 100
                        st.metric(
                            "Activity Frequency",
                            f"{completion_rate:.0f}%",
                            "of tracked days"
                        )
                    
                    with col3:
                        if len(activity_days) >= 2:
                            activity_trend = np.polyfit(range(len(activity_days)), 
                                                      activity_days['wellness_score'].values, 1)[0]
                            st.metric(
                                "Activity Trend",
                                f"{activity_trend:+.2f}",
                                "improvement/session"
                            )
                        else:
                            st.metric(
                                "Activity Trend",
                                "Track more",
                                "Need 2+ activities"
                            )

# Page 4: Enhanced Detailed Insights & Patterns
with tab4:
    st.header("Advanced Pattern Recognition & Insights")
    
    if not st.session_state.symptom_log:
        st.info("Log at least 2 days of symptoms to unlock pattern analysis.")
    elif len(st.session_state.symptom_log) < 2:
        st.info("Log more symptoms to unlock comprehensive pattern analysis.")
    else:
        df = pd.DataFrame(st.session_state.symptom_log)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Ensure wellness_score exists
        if 'wellness_score' not in df.columns:
            positive_metrics = ['mood', 'appetite', 'sleep_quality', 'energy', 'mental_clarity']
            negative_metrics = ['fatigue', 'pain', 'nausea']
            
            wellness_scores = []
            for _, row in df.iterrows():
                positive_avg = np.mean([row[metric] for metric in positive_metrics if metric in row])
                negative_avg = np.mean([11 - row[metric] for metric in negative_metrics if metric in row])
                wellness_score = (positive_avg + negative_avg) / 2
                wellness_scores.append(wellness_score)
            
            df['wellness_score'] = wellness_scores
        
        # Basic correlation analysis for 2+ days
        if len(df) >= 2:
            st.subheader("Symptom Relationship Analysis")
            
            corr_metrics = ['fatigue', 'pain', 'nausea', 'mood', 'appetite', 'sleep_quality', 'energy', 'mental_clarity']
            available_metrics = [m for m in corr_metrics if m in df.columns]
            
            if len(available_metrics) >= 2:
                corr_matrix = df[available_metrics].corr()
                
                # Create enhanced correlation heatmap
                fig_corr = px.imshow(
                    corr_matrix, 
                    title="Symptom Correlation Matrix - Discover Hidden Connections",
                    color_continuous_scale='RdBu_r',
                    range_color=[-1, 1],
                    aspect="auto"
                )
                fig_corr.update_layout(height=500)
                st.plotly_chart(fig_corr, use_container_width=True)
                
                # Simple pattern detection
                st.subheader("Basic Pattern Detection")
                
                # Find strongest correlation
                max_corr = 0
                max_pair = None
                
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        corr_value = abs(corr_matrix.iloc[i, j])
                        if corr_value > max_corr and not np.isnan(corr_value):
                            max_corr = corr_value
                            max_pair = (corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j])
                
                if max_pair and max_corr > 0.5:
                    metric1, metric2, corr_value = max_pair
                    relationship = "improves with" if corr_value > 0 else "worsens with"
                    st.markdown(f'<div class="insight-box">**Key Insight:** {metric1.replace("_", " ").title()} {relationship} {metric2.replace("_", " ").title()} (r = {corr_value:.2f})</div>', 
                               unsafe_allow_html=True)
                else:
                    st.info("Continue tracking to discover stronger symptom relationships")
        
        # Time-based pattern analysis for 7+ days
        if len(df) >= 7:
            st.subheader(" Weekly Pattern Analysis")
            
            df['day_of_week'] = df['date'].dt.day_name()
            weekly_patterns = df.groupby('day_of_week')[['wellness_score', 'energy', 'mood', 'fatigue']].mean()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            weekly_patterns = weekly_patterns.reindex(day_order)
            
            fig_weekly = px.line(
                weekly_patterns.reset_index(), 
                x='day_of_week', 
                y=['wellness_score', 'energy', 'mood'],
                title="Weekly Patterns - How Your Week Affects Wellness",
                labels={'value': 'Score (1-10)', 'day_of_week': 'Day of Week'},
                color_discrete_map={
                    'wellness_score': COLOR_SCHEME['primary'],
                    'energy': COLOR_SCHEME['success'],
                    'mood': COLOR_SCHEME['warning']
                }
            )
            st.plotly_chart(fig_weekly, use_container_width=True)
        
        # Predictive insights for 5+ days
        if len(df) >= 5:
            st.subheader(" Predictive Health Insights")
            
            # Simple trend prediction
            dates_numeric = np.arange(len(df))
            wellness_scores = df['wellness_score'].values
            
            # Fit trend line
            trend_coeffs = np.polyfit(dates_numeric, wellness_scores, 1)
            trend_line = np.poly1d(trend_coeffs)
            
            # Simple prediction
            next_day_prediction = trend_line(len(df))
            current_wellness = wellness_scores[-1]
            change = next_day_prediction - current_wellness
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    "Tomorrow's Forecast",
                    f"{next_day_prediction:.1f}/10",
                    f"{change:+.1f} change"
                )
            
            with col2:
                trend_direction = "Improving" if trend_coeffs[0] > 0 else "Declining" if trend_coeffs[0] < 0 else "Stable"
                st.metric(
                    "Trend Direction",
                    trend_direction,
                    "Based on recent data"
                )
            
            # Recommendations based on trend
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.write("** Forecast-Based Recommendations:**")
            
            if change > 0.3:
                st.write("• Your positive trend suggests continuing current activities")
                st.write("• Consider maintaining your current routine")
            elif change < -0.3:
                st.write("• Consider more rest and gentle activities")
                st.write("• Focus on activities that address your main symptoms")
            else:
                st.write("• Your wellness is expected to remain stable")
                st.write("• Consider trying new activities for variety")
            
            st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    <p> Cancer Wellness Platform - Designed to support your journey with personalized, data-driven insights</p>
    <p> Always consult with your healthcare team before making changes to your wellness routine</p>
    </div>
    """, 
    unsafe_allow_html=True
)