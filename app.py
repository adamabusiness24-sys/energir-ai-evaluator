
import streamlit as st
from ai_engine import analyze_project

# ==========================================
# CONFIGURATION STREAMLIT
# ==========================================

st.set_page_config(
    page_title="Énergir - AI Project Evaluator",
    page_icon="⚡",
    layout="wide"
)

# Tarifs fournis dans l'exercice Énergir
PRICES = {
    "Copilot M365 / Agent Builder": 0.00,
    "Copilot Studio": 0.02,
    "Azure AI Foundry": 0.08
}


# ==========================================
# CALCUL DES COÛTS ET BÉNÉFICES
# ==========================================

def evaluate_project(
    technology,
    interactions,
    projects,
    minutes_saved,
    hourly_rate,
    setup_cost
):
    # Coût d'utilisation de la technologie
    monthly_cost = interactions * PRICES[technology]

    # Coût estimé de la première année
    annual_cost = monthly_cost * 12 + setup_cost

    # Temps économisé mensuellement
    monthly_hours = projects * minutes_saved / 60

    # Bénéfices financiers estimés
    monthly_benefits = monthly_hours * hourly_rate
    annual_benefits = monthly_benefits * 12

    # Bénéfice net
    net_benefit = annual_benefits - annual_cost

    # Retour sur investissement
    roi = (
        net_benefit / annual_cost * 100
        if annual_cost > 0
        else None
    )

    return {
        "monthly_cost": monthly_cost,
        "annual_cost": annual_cost,
        "monthly_hours": monthly_hours,
        "annual_benefits": annual_benefits,
        "net_benefit": net_benefit,
        "roi": roi
    }


# ==========================================
# INTERFACE UTILISATEUR
# ==========================================

st.title("⚡ Énergir | AI Project Evaluator")

st.write(
    "Solution intelligente d'évaluation de projets "
    "basée sur OpenAI GPT et LangChain."
)

st.divider()

st.subheader("Description du projet")

description = st.text_area(
    "Décrivez votre projet",
    height=180,
    placeholder=(
        "Exemple : Nous souhaitons automatiser "
        "la validation des factures et des "
        "pièces justificatives..."
    )
)

st.subheader("Paramètres financiers")

col1, col2 = st.columns(2)

with col1:

    technology = st.selectbox(
        "Technologie Microsoft",
        list(PRICES.keys()),
        index=2
    )

    interactions = st.number_input(
        "Interactions IA par mois",
        min_value=0,
        value=1000,
        step=100
    )

    projects = st.number_input(
        "Dossiers / projets par mois",
        min_value=0,
        value=100,
        step=10
    )

with col2:

    minutes_saved = st.number_input(
        "Minutes économisées par dossier",
        min_value=0.0,
        value=10.0,
        step=1.0
    )

    hourly_rate = st.number_input(
        "Coût horaire ($)",
        min_value=0.0,
        value=40.0,
        step=1.0
    )

    setup_cost = st.number_input(
        "Coût initial d'implantation ($)",
        min_value=0.0,
        value=0.0,
        step=100.0
    )

st.divider()


# ==========================================
# BOUTON D'ÉVALUATION
# ==========================================

if st.button(
    "🚀 Évaluer le projet avec l'IA",
    type="primary",
    use_container_width=True
):

    if not description.strip():

        st.warning(
            "Veuillez saisir une description du projet."
        )

    else:

        try:

            # ==================================
            # 1. ANALYSE AVEC OPENAI + LANGCHAIN
            # ==================================

            with st.spinner(
                "GPT analyse votre projet..."
            ):

                ai_result = analyze_project(description)

            # ==================================
            # 2. CALCULS FINANCIERS PYTHON
            # ==================================

            financial = evaluate_project(
                technology,
                interactions,
                projects,
                minutes_saved,
                hourly_rate,
                setup_cost
            )

            st.success(
                "Analyse du projet terminée avec succès !"
            )

            st.divider()

            # ==================================
            # 3. BESOIN RAFFINÉ
            # ==================================

            st.header("1. Besoin raffiné")

            st.subheader(ai_result.titre)

            st.write(
                "**Catégorie :**",
                ai_result.categorie
            )

            st.markdown("### Problématique")

            st.write(
                ai_result.problematique
            )

            st.markdown("### Objectif métier")

            st.write(
                ai_result.objectif
            )

            # ==================================
            # 4. MATRICE REQUIS / HYPOTHÈSES
            # ==================================

            st.header(
                "2. Matrice requis / hypothèses"
            )

            rows = []

            for req in ai_result.exigences:

                rows.append({
                    "Type": "Exigence",
                    "Élément": req.exigence,
                    "Priorité / Justification": req.priorite
                })

            for hyp in ai_result.hypotheses:

                rows.append({
                    "Type": "Hypothèse",
                    "Élément": hyp.hypothese,
                    "Priorité / Justification": (
                        hyp.justification
                    )
                })

            # Hypothèses financières saisies
            rows.extend([
                {
                    "Type": "Hypothèse financière",
                    "Élément": "Volume mensuel",
                    "Priorité / Justification": (
                        f"{projects} dossiers"
                    )
                },
                {
                    "Type": "Hypothèse financière",
                    "Élément": "Gain de temps",
                    "Priorité / Justification": (
                        f"{minutes_saved} minutes / dossier"
                    )
                }
            ])

            st.dataframe(
                rows,
                use_container_width=True,
                hide_index=True
            )

            # ==================================
            # 5. ÉVALUATION DES COÛTS
            # ==================================

            st.header("3. Évaluation des coûts")

            st.write(
                "**Technologie sélectionnée :**",
                technology
            )

            st.write(
                "**Coût par interaction :**",
                f"{PRICES[technology]:.2f} $"
            )

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "Coût mensuel d'interactions",
                    f"{financial['monthly_cost']:,.2f} $"
                )

            with c2:

                st.metric(
                    "Coût première année",
                    f"{financial['annual_cost']:,.2f} $"
                )

            st.caption(
                "Les coûts sont calculés selon les "
                "hypothèses de l'exercice Énergir. "
                "Les frais supplémentaires de services, "
                "d'intégration et de maintenance ne "
                "sont pas inclus."
            )

            # ==================================
            # 6. ÉVALUATION DES BÉNÉFICES
            # ==================================

            st.header(
                "4. Évaluation des bénéfices"
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Heures économisées / mois",
                    f"{financial['monthly_hours']:.1f} h"
                )

            with c2:

                st.metric(
                    "Bénéfices annuels estimés",
                    f"{financial['annual_benefits']:,.2f} $"
                )

            with c3:

                st.metric(
                    "Bénéfice net première année",
                    f"{financial['net_benefit']:,.2f} $"
                )

            if financial["roi"] is not None:

                st.metric(
                    "ROI estimé",
                    f"{financial['roi']:.1f}%"
                )

            else:

                st.info(
                    "ROI non calculable : "
                    "coût estimé nul."
                )

            st.caption(
                "Les bénéfices représentent une "
                "valorisation du temps économisé, "
                "pas nécessairement une économie "
                "budgétaire réalisée."
            )

            st.subheader(
                "Bénéfices qualitatifs"
            )

            for benefit in ai_result.benefices_qualitatifs:

                st.write(f"• {benefit}")

            st.subheader(
                "Indicateurs de succès"
            )

            for indicator in ai_result.indicateurs_succes:

                st.write(f"• {indicator}")

            # ==================================
            # 7. ARCHITECTURE DE SOLUTION
            # ==================================

            st.header(
                "5. Architecture recommandée"
            )

            st.write(
                "Architecture proposée par "
                "le modèle d'intelligence artificielle :"
            )

            for index, step in enumerate(
                ai_result.architecture,
                start=1
            ):

                st.write(
                    f"**{index}.** {step}"
                )

            st.info(
                "L'architecture doit être validée "
                "selon les services, connecteurs "
                "et droits disponibles chez Énergir."
            )

            # ==================================
            # 8. RISQUES
            # ==================================

            st.header("6. Risques identifiés")

            for risk in ai_result.risques:

                st.write(f"• {risk}")

            # ==================================
            # 9. QUESTIONS OUVERTES
            # ==================================

            st.header(
                "7. Questions à clarifier"
            )

            for question in ai_result.questions:

                st.write(f"• {question}")

            st.divider()

            st.success(
                "Évaluation complète du projet."
            )

        except Exception as error:

            st.error(
                "Une erreur est survenue "
                "pendant l'analyse IA."
            )

            st.exception(error)
