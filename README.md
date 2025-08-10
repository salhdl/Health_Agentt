🏋️‍♂️ AI Health & Fitness Planner
Une application Streamlit permettant de générer des plans alimentaires et fitness personnalisés grâce à l'intelligence artificielle Google Gemini.
L'application analyse votre profil (âge, poids, taille, sexe, niveau d'activité, préférences alimentaires, objectifs fitness) et génère :

Un plan alimentaire détaillé avec macronutriments et conseils nutritionnels

Un programme d'entraînement structuré avec exercices, séries, répétitions et temps de repos

🚀 Fonctionnalités
Calcul IMC avec catégorisation visuelle

Génération automatique d’un plan alimentaire adapté à vos objectifs

Création d’un programme fitness personnalisé

Conseils nutritionnels et fitness intégrés

Section Q&A pour poser des questions sur vos plans

Interface moderne et animée avec CSS personnalisé

🛠️ Technologies utilisées
Python 3.10+

Streamlit pour l’interface web

Agno pour la gestion des agents IA

Google Gemini API pour la génération de contenu

HTML/CSS pour le design et les animations

📦 Installation
Cloner le projet

bash
Copier
Modifier
git clone https://github.com/ton-utilisateur/ai-health-fitness-planner.git
cd ai-health-fitness-planner
Créer un environnement virtuel (optionnel mais recommandé)

bash
Copier
Modifier
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
Installer les dépendances

bash
Copier
Modifier
pip install -r requirements.txt
🔑 Configuration
Obtenez une clé API Google Gemini sur AI Studio

Lancez l’application et entrez la clé dans la sidebar ou créez un fichier .env avec :

env
Copier
Modifier
GOOGLE_API_KEY=ta_cle_api
▶️ Utilisation
Lancer l'application Streamlit :

bash
Copier
Modifier
streamlit run app.py
Puis ouvrir l’URL affichée dans votre terminal (par défaut : http://localhost:8501).
