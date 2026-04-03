Progiciel de Gestion des Risques : Value-at-
Risk (VaR)


Objectif du Projet
Développement d'un progiciel financier complet en Python permettant d'estimer, de comparer
et de valider la Value-at-Risk (VaR) d'un portefeuille d'actifs. Ce projet démontre une
expertise allant de la modélisation stochastique à la mise en production d'une interface
décisionnelle.

Méthodologies Implémentées

Le moteur de calcul intègre 7 modèles de gestion des risques, couvrant les approches
standards et avancées :
VaR Historique : Basée sur la distribution empirique des rendements passés.
VaR Paramétrique : Approche Variance-Covariance (Loi Normale).
Cornish-Fisher : Ajustement de la VaR paramétrique prenant en compte l'asymétrie
(Skewness) et le Kurtosis.
RiskMetrics (EWMA) : Modélisation de la volatilité par lissage exponentiel.
GARCH(1,1) : Capture des clusters de volatilité via modèles hétéroscédastiques.
TVE (Extreme Value Theory) : Utilisation de la loi de Pareto Généralisée
(GPD) pour modéliser les queues de distribution (Risques de queue).
TVE-GARCH : Modèle hybride filtrant les rendements par GARCH avant
d'appliquer la TVE sur les résidus standardisés.


Backtesting & Validation

Pour garantir la fiabilité des modèles, le progiciel exécute automatiquement :
• Test de Kupiec (POF) : Vérification de la proportion de dépassements.
• Test de Christoffersen : Vérification de l'indépendance des exceptions (absence de
clusters de pertes).


Fonctionnalités du Progiciel
• Interface Web Interactive : Développée avec Streamlit pour une manipulation facile
des portefeuilles.


• Reporting Automatisé :
o Génération d'un Tableau Excel détaillé avec les statistiques de backtesting.
o Édition d'un Rapport PDF de synthèse destiné à une Direction des Risques.
• Data Pipeline : Connexion temps réel à l'API Yahoo Finance.


Installation
1. Cloner le projet :
Bash
git clone https://github.com/Ecclesiastee/VaR_Project.git
2. Installer les dépendances :
Bash
pip install -r requirements.txt
3. Lancer l'interface graphique :
Bash
streamlit run app.py
Structure du Dépôt
• app.py : Point d'entrée de l'interface Web Streamlit.
• engine_var.py : Bibliothèque mathématique des modèles de risque.
• backtesting.py : Moteur de validation statistique.
• data_loader.py : Pipeline d'acquisition et de traitement des données.
• reporting.py : Modules de génération PDF et Excel.
Auteur : Écclésiaste GNARGO Élève Ingénieur en Mathématiques Appliquées et Finance
(IFIM) - Institut Galilée
