# Énergir — AI Project Evaluator

## Présentation
Application d'intelligence artificielle générique permettant d'évaluer des projets à partir d'une description métier.

## Technologies
- Python
- Streamlit
- LangChain
- OpenAI GPT
- Pydantic

## Fonctionnalités
1. Raffinement automatique des besoins métier.
2. Génération d'une matrice exigences / hypothèses.
3. Estimation des coûts d'utilisation des technologies Microsoft.
4. Évaluation des bénéfices financiers et du ROI.
5. Proposition d'une architecture de solution.
6. Identification des risques et questions à clarifier.

## Installation locale

```bash
uv sync
```

Créer un fichier `.env` contenant :

```env
OPENAI_API_KEY=votre_cle_api
```

Démarrer l'application :

```bash
uv run streamlit run app.py
```

## Limites
Ce prototype est destiné à l'évaluation préliminaire de projets. Les coûts sont fondés sur les hypothèses de l'exercice. Les recommandations générées par l'IA nécessitent une validation humaine.

## Cas d'utilisation
- Validation des pièces justificatives de biénergie commerciale.
- Revue de presse quotidienne.
- Création de plans d'entretien SAP.
