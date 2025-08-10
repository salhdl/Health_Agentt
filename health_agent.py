import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
import json
from datetime import datetime

st.set_page_config(
    page_title="AI Health & Fitness Planner",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS amélioré avec animations et design moderne
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
        padding: 1rem 2rem;
    }
    
    /* Header principal avec gradient */
    .hero-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        animation: fadeInUp 0.8s ease-out;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Cards avec glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Profil utilisateur stylisé */
    .profile-section {
        background: linear-gradient(145deg, #f8fafc, #e2e8f0);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .profile-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .profile-icon {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: white;
        margin-bottom: 1rem;
    }
    
    /* Boutons améliorés */
    .stButton > button {
        width: 100%;
        height: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 15px;
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    /* Plans avec design de cartes premium */
    .plan-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .plan-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #667eea, #764ba2);
    }
    
    .plan-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .plan-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Métriques utilisateur */
    .metrics-container {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
        flex: 1;
        min-width: 150px;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #64748b;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    /* Q&A Section */
    .qa-section {
        background: #f8fafc;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .question-input {
        margin-bottom: 1rem;
    }
    
    .qa-item {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #667eea;
    }
    
    .question {
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
    }
    
    .answer {
        color: #4a5568;
        line-height: 1.6;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Progress bar */
    .progress-container {
        background: #e2e8f0;
        border-radius: 10px;
        height: 8px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Sidebar améliorée */
    .sidebar-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(135deg, #48bb78, #38a169);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #ed8936, #dd6b20);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

def calculate_bmi(weight, height):
    """Calculate BMI"""
    height_m = height / 100
    return round(weight / (height_m ** 2), 1)

def get_bmi_category(bmi):
    """Get BMI category"""
    if bmi < 18.5:
        return "Sous-poids", "#3182ce"
    elif bmi < 25:
        return "Normal", "#38a169"
    elif bmi < 30:
        return "Surpoids", "#d69e2e"
    else:
        return "Obésité", "#e53e3e"

def display_user_metrics(age, weight, height, sex, activity_level):
    """Display user metrics with visual cards"""
    bmi = calculate_bmi(weight, height)
    bmi_category, bmi_color = get_bmi_category(bmi)
    
    st.markdown("""
        <div class="metrics-container">
            <div class="metric-card">
                <div class="metric-value">""" + str(bmi) + """</div>
                <div class="metric-label">IMC</div>
                <div style="color: """ + bmi_color + """; font-weight: 600;">""" + bmi_category + """</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">""" + str(age) + """</div>
                <div class="metric-label">Âge</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">""" + str(weight) + """</div>
                <div class="metric-label">Poids (kg)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">""" + str(height) + """</div>
                <div class="metric-label">Taille (cm)</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def display_dietary_plan(plan_content):
    """Display dietary plan with enhanced styling and better nutrition formatting"""
    st.markdown("""
        <div class="plan-card animate-in">
            <div class="plan-title">
                🍽️ Votre Plan Alimentaire Personnalisé
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📋 Détails du plan alimentaire", expanded=True):
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("### 🎯 Pourquoi ce plan fonctionne")
            st.info(plan_content.get("why_this_plan_works", "Information non disponible"))
            
            st.markdown("### 🍽️ Plan de repas détaillé")
            
            # Add CSS for better meal formatting
            st.markdown("""
            <style>
            .meal-plan {
                background: white;
                padding: 1.5rem;
                border-radius: 15px;
                border-left: 4px solid #667eea;
                margin: 1rem 0;
            }
            .meal-section {
                background: #f8fafc;
                padding: 1rem;
                margin: 1rem 0;
                border-radius: 10px;
                border-left: 3px solid #38a169;
            }
            .meal-title {
                color: #2d3748;
                font-weight: 600;
                font-size: 1.1rem;
                margin-bottom: 0.5rem;
            }
            .macros {
                background: #e6fffa;
                padding: 0.5rem;
                border-radius: 5px;
                font-size: 0.9rem;
                color: #234e52;
                margin-top: 0.5rem;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Display formatted meal plan
            meal_plan_content = plan_content.get("meal_plan", "Plan non disponible")
            st.markdown(f"""
                <div class="meal-plan">
                    {meal_plan_content.replace('**', '<strong>').replace('**', '</strong>').replace('\n', '<br>')}
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### ⚠️ Considérations importantes")
            considerations = plan_content.get("important_considerations", "").split('\n')
            for consideration in considerations:
                if consideration.strip():
                    st.warning(consideration)
            
            # Add nutritional guidelines
            st.markdown("### 🥗 Conseils Nutritionnels")
            st.markdown("""
            <div style="background: #f0f9ff; padding: 1rem; border-radius: 10px; border-left: 4px solid #0284c7;">
            <strong>Recommandations générales :</strong><br>
            🥬 6-8 portions de fruits et légumes/jour<br>
            🥩 Protéines de qualité à chaque repas<br>
            🍠 Glucides complexes prioritaires<br>
            🥑 Bonnes graisses quotidiennes<br>
            💧 2-3L d'eau par jour
            </div>
            """, unsafe_allow_html=True)

def display_fitness_plan(plan_content):
    """Display fitness plan with enhanced styling and better formatting"""
    st.markdown("""
        <div class="plan-card animate-in">
            <div class="plan-title">
                💪 Votre Programme Fitness Personnalisé
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🏋️‍♂️ Détails du programme fitness", expanded=True):
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("### 🎯 Objectifs")
            st.success(plan_content.get("goals", "Objectifs non spécifiés"))
            
            st.markdown("### 🏋️‍♂️ Programme d'exercices")
            
            # Parse and format the routine content better
            routine_content = plan_content.get("routine", "Programme non disponible")
            
            # Add some CSS for better table formatting
            st.markdown("""
            <style>
            .exercise-table {
                background: white;
                padding: 1.5rem;
                border-radius: 15px;
                border-left: 4px solid #764ba2;
                margin: 1rem 0;
            }
            .exercise-table h4 {
                color: #764ba2;
                margin-bottom: 1rem;
                font-weight: 600;
            }
            .exercise-item {
                background: #f8fafc;
                padding: 0.8rem;
                margin: 0.5rem 0;
                border-radius: 8px;
                border-left: 3px solid #667eea;
            }
            .exercise-details {
                display: grid;
                grid-template-columns: 2fr 1fr 1fr 1fr;
                gap: 1rem;
                align-items: center;
                font-size: 0.9rem;
            }
            .exercise-name { font-weight: 600; color: #2d3748; }
            .exercise-sets { color: #4a5568; }
            .exercise-reps { color: #4a5568; }
            .exercise-rest { color: #4a5568; }
            </style>
            """, unsafe_allow_html=True)
            
            # Display formatted routine
            st.markdown(f"""
                <div class="exercise-table">
                    {routine_content.replace('**', '<strong>').replace('**', '</strong>').replace('\n', '<br>')}
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 💡 Conseils Pro")
            tips = plan_content.get("tips", "").split('\n')
            for tip in tips:
                if tip.strip():
                    st.info(tip)
            
            # Add a sample workout structure
            st.markdown("### 📋 Structure Type")
            st.markdown("""
            <div style="background: #f0fff4; padding: 1rem; border-radius: 10px; border-left: 4px solid #38a169;">
            <strong>Séance Type :</strong><br>
            🟡 Échauffement : 10-15 min<br>
            🔴 Programme principal : 30-45 min<br>
            🟢 Récupération : 5-10 min<br>
            💧 Hydratation constante
            </div>
            """, unsafe_allow_html=True)

def validate_inputs(age, weight, height):
    """Validate user inputs"""
    errors = []
    if not 10 <= age <= 100:
        errors.append("L'âge doit être entre 10 et 100 ans")
    if not 30 <= weight <= 300:
        errors.append("Le poids doit être entre 30 et 300 kg")
    if not 100 <= height <= 250:
        errors.append("La taille doit être entre 100 et 250 cm")
    return errors

def main():
    # Initialize session state
    if 'dietary_plan' not in st.session_state:
        st.session_state.dietary_plan = {}
        st.session_state.fitness_plan = {}
        st.session_state.qa_pairs = []
        st.session_state.plans_generated = False
        st.session_state.user_profile = {}

    # Hero Header
    st.markdown("""
        <div class="hero-header">
            <div class="hero-title">🏋️‍♂️ AI Health & Fitness</div>
            <div class="hero-subtitle">
                Obtenez des plans alimentaires et fitness personnalisés grâce à l'intelligence artificielle. 
                Notre système prend en compte votre profil unique pour créer le plan parfait pour vous.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar Configuration
    with st.sidebar:
        st.markdown('<div class="sidebar-header"><h2>🔑 Configuration API</h2></div>', unsafe_allow_html=True)
        
        gemini_api_key = st.text_input(
            "Clé API Gemini",
            type="password",
            help="Entrez votre clé API Gemini pour accéder au service"
        )
        
        if not gemini_api_key:
            st.markdown('<div class="status-warning">⚠️ Veuillez entrer votre clé API Gemini</div>', unsafe_allow_html=True)
            st.markdown("[Obtenez votre clé API ici](https://aistudio.google.com/apikey)")
            return
        else:
            st.markdown('<div class="status-success">✅ Clé API acceptée!</div>', unsafe_allow_html=True)

    if gemini_api_key:
        try:
            gemini_model = Gemini(id="gemini-2.5-flash-preview-05-20", api_key=gemini_api_key)
        except Exception as e:
            st.error(f"❌ Erreur lors de l'initialisation du modèle Gemini: {e}")
            return

        # Profile Section
        st.markdown("""
            <div class="profile-section">
                <div class="profile-header">
                    <div class="profile-icon">👤</div>
                    <h2 style="margin: 0; color: #2d3748;">Votre Profil</h2>
                    <p style="color: #64748b; margin: 0.5rem 0;">Renseignez vos informations pour un plan personnalisé</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Âge", min_value=10, max_value=100, step=1, value=25, help="Entrez votre âge")
            height = st.number_input("Taille (cm)", min_value=100.0, max_value=250.0, step=0.1, value=170.0)
            activity_level = st.selectbox(
                "Niveau d'activité",
                options=["Sédentaire", "Légèrement actif", "Modérément actif", "Très actif", "Extrêmement actif"],
                help="Choisissez votre niveau d'activité typique"
            )
            dietary_preferences = st.selectbox(
                "Préférences alimentaires",
                options=["Végétarien", "Keto", "Sans gluten", "Faible en glucides", "Sans lactose"],
                help="Sélectionnez votre préférence alimentaire"
            )

        with col2:
            weight = st.number_input("Poids (kg)", min_value=20.0, max_value=300.0, step=0.1, value=70.0)
            sex = st.selectbox("Sexe", options=["Homme", "Femme", "Autre"])
            fitness_goals = st.selectbox(
                "Objectifs fitness",
                options=["Perdre du poids", "Gagner du muscle", "Endurance", "Rester en forme", "Musculation"],
                help="Que voulez-vous accomplir?"
            )

        # Display user metrics
        if age and weight and height:
            display_user_metrics(age, weight, height, sex, activity_level)

        # Validate inputs
        validation_errors = validate_inputs(age, weight, height)
        if validation_errors:
            for error in validation_errors:
                st.error(error)
            return

        # Generate Plan Button
        if st.button("🎯 Générer Mon Plan Personnalisé", use_container_width=True):
            with st.spinner("🔄 Création de votre routine santé et fitness parfaite..."):
                try:
                    # Create agents with enhanced instructions
                    dietary_agent = Agent(
                        name="Expert Nutritionnel",
                        role="Fournit des recommandations nutritionnelles personnalisées",
                        model=gemini_model,
                        instructions=[
                            "Analysez le profil utilisateur en tenant compte des restrictions et préférences alimentaires.",
                            "Structurez le plan avec des sections claires pour chaque repas :",
                            "**PETIT-DÉJEUNER** (exemple : 7h-8h)",
                            "• Plat principal avec quantités approximatives",
                            "• Macronutriments : Protéines Xg, Glucides Yg, Lipides Zg",
                            "",
                            "**COLLATION MATINALE** (optionnelle)",
                            "",
                            "**DÉJEUNER** (12h-13h)",
                            "• Plat complet avec légumes, protéines, glucides",
                            "• Macronutriments estimés",
                            "",
                            "**COLLATION APRÈS-MIDI**",
                            "",
                            "**DÎNER** (19h-20h)",
                            "• Repas équilibré plus léger",
                            "",
                            "**CONSEILS NUTRITIONNELS :**",
                            "• 6-8 portions de fruits et légumes par jour",
                            "• Sources de protéines de qualité à chaque repas",
                            "• Glucides complexes prioritaires",
                            "• Bonnes graisses (avocat, noix, huile d'olive)",
                            "• Hydratation : 2-3L d'eau par jour",
                            "",
                            "Calculez les macronutriments approximatifs totaux.",
                            "Expliquez pourquoi ce plan convient aux objectifs spécifiques.",
                            "Proposez des alternatives pour la variété."
                        ]
                    )

                    fitness_agent = Agent(
                        name="Expert Fitness",
                        role="Fournit des recommandations d'entraînement personnalisées",
                        model=gemini_model,
                        instructions=[
                            "Créez un programme d'exercices adapté aux objectifs et au niveau de l'utilisateur.",
                            "Formatez la réponse avec des sections claires : Échauffement, Programme Principal, Récupération.",
                            "Pour chaque exercice, précisez : Nom | Séries | Répétitions | Temps de repos | Bénéfices principaux",
                            "Exemple de format souhaité:",
                            "**ÉCHAUFFEMENT (10 minutes)**",
                            "• Jumping jacks - 3 séries - 30 sec - 15 sec repos - Active la circulation",
                            "",
                            "**PROGRAMME PRINCIPAL**",
                            "• Squat - 4 séries - 12-15 reps - 90 sec repos - Renforce quadriceps et fessiers",
                            "• Push-ups - 3 séries - 10-12 reps - 60 sec repos - Développe pectoraux et triceps",
                            "",
                            "**RÉCUPÉRATION (5-10 minutes)**",
                            "• Étirements statiques",
                            "",
                            "Incluez des conseils de progression et des alternatives pour différents niveaux.",
                            "Assurez-vous que le plan soit réalisable et bien structuré."
                        ]
                    )

                    # User profile
                    user_profile = f"""
                    Profil utilisateur:
                    - Âge: {age} ans
                    - Poids: {weight}kg
                    - Taille: {height}cm
                    - Sexe: {sex}
                    - Niveau d'activité: {activity_level}
                    - Préférences alimentaires: {dietary_preferences}
                    - Objectifs fitness: {fitness_goals}
                    - IMC: {calculate_bmi(weight, height)}
                    """

                    # Generate plans
                    dietary_plan_response = dietary_agent.run(user_profile)
                    fitness_plan_response = fitness_agent.run(user_profile)

                    # Store in session state
                    dietary_plan = {
                        "why_this_plan_works": f"Plan optimisé pour {fitness_goals.lower()} avec {dietary_preferences}",
                        "meal_plan": dietary_plan_response.content,
                        "important_considerations": """
                        - Hydratation: Buvez beaucoup d'eau tout au long de la journée
                        - Électrolytes: Surveillez les niveaux de sodium, potassium et magnésium
                        - Fibres: Assurez un apport adéquat via légumes et fruits
                        - Écoutez votre corps: Ajustez les portions selon vos besoins
                        """
                    }

                    fitness_plan = {
                        "goals": f"Optimisé pour {fitness_goals.lower()} selon votre niveau {activity_level.lower()}",
                        "routine": fitness_plan_response.content,
                        "tips": """
                        - Suivez vos progrès régulièrement
                        - Accordez un repos approprié entre les séances
                        - Concentrez-vous sur la forme correcte
                        - Restez cohérent avec votre routine
                        """
                    }

                    st.session_state.dietary_plan = dietary_plan
                    st.session_state.fitness_plan = fitness_plan
                    st.session_state.plans_generated = True
                    st.session_state.qa_pairs = []
                    st.session_state.user_profile = user_profile

                    # Progress bar animation
                    progress_bar = st.progress(0)
                    for i in range(101):
                        progress_bar.progress(i)
                        
                    st.success("✅ Vos plans personnalisés sont prêts!")
                    
                    # Display plans
                    display_dietary_plan(dietary_plan)
                    display_fitness_plan(fitness_plan)

                except Exception as e:
                    st.error(f"❌ Une erreur s'est produite: {str(e)}")

        # Q&A Section
        if st.session_state.plans_generated:
            st.markdown("""
                <div class="qa-section">
                    <h2 style="text-align: center; margin-bottom: 2rem; color: #2d3748;">
                        ❓ Questions sur votre plan?
                    </h2>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                question_input = st.text_input(
                    "",
                    placeholder="Posez votre question sur votre plan alimentaire ou fitness...",
                    help="Exemple: Puis-je remplacer un repas? Combien de fois par semaine?"
                )
            
            with col2:
                ask_button = st.button("Poser la question", use_container_width=True)

            if ask_button and question_input:
                with st.spinner("🔍 Recherche de la meilleure réponse..."):
                    try:
                        context = f"""
                        Profil utilisateur: {st.session_state.user_profile}
                        
                        Plan alimentaire: {st.session_state.dietary_plan.get('meal_plan', '')}
                        
                        Plan fitness: {st.session_state.fitness_plan.get('routine', '')}
                        
                        Question de l'utilisateur: {question_input}
                        
                        Répondez de manière précise et personnalisée en tenant compte du profil et des plans générés.
                        """

                        agent = Agent(
                            model=gemini_model,
                            instructions=[
                                "Répondez de manière précise et personnalisée",
                                "Basez vos réponses sur les plans générés",
                                "Soyez encourageant et constructif",
                                "Proposez des alternatives si nécessaire"
                            ]
                        )
                        run_response = agent.run(context)

                        answer = run_response.content if hasattr(run_response, 'content') else "Désolé, je n'ai pas pu générer une réponse."
                        
                        st.session_state.qa_pairs.append({
                            "question": question_input,
                            "answer": answer,
                            "timestamp": datetime.now().strftime("%H:%M")
                        })

                    except Exception as e:
                        st.error(f"❌ Erreur lors de la génération de la réponse: {str(e)}")

            # Display Q&A History
            if st.session_state.qa_pairs:
                st.markdown("### 💬 Historique des questions")
                for i, qa in enumerate(reversed(st.session_state.qa_pairs[-5:])):  # Show last 5
                    st.markdown(f"""
                        <div class="qa-item">
                            <div class="question">
                                <strong>Q:</strong> {qa['question']}
                                <span style="float: right; color: #64748b; font-size: 0.8rem;">{qa['timestamp']}</span>
                            </div>
                            <div class="answer">
                                <strong>R:</strong> {qa['answer']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()