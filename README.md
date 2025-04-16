# Bangladesh Energy System Dynamics Simulation (2025-2050)

## Overview

This project implements a comprehensive Python-based simulation modeling Bangladesh's energy ecosystem, currently configured to run from 2025 to 2040 (adjustable in `main_simulation.py`). It captures the complex interplay of various factors using interconnected component models:

*   **Generation Portfolio (`models/generation_portfolio.py`):** Models capacity evolution (expansion/retirement) and simulates simplified dispatch.
*   **Fuel Supply (`models/fuel_supply.py`):** Models availability and pricing for domestic gas, LNG, coal, liquid fuels, and assesses renewable resource potential.
*   **Grid Infrastructure (`models/grid_infrastructure.py`):** Simulates high-voltage transmission, distribution networks, system losses, smart grid development, and cross-border interconnections.
*   **Demand (`models/demand.py`):** Projects electricity demand across residential, industrial, commercial, agricultural, and transport sectors based on configurable drivers.
*   **Market (`models/market.py`):** Simulates wholesale market outcomes, retail tariff structures, PPA dynamics, and renewable energy support mechanisms.
*   **Governance (`models/governance.py`):** Models sector unbundling progress, regulatory framework effectiveness, planning processes, and private sector participation environment using qualitative scores.
*   **Renewable Transition (`models/renewable_transition.py`):** Models expansion of solar, wind, bioenergy, hydro based on costs, policy, and assesses grid integration challenges (curtailment).
*   **Energy Access (`models/energy_access.py`):** Tracks rural/urban/national access rates, affordability metrics, and qualitative scores for gender and just transition aspects.
*   **Climate Resilience (`models/climate_resilience.py`):** Models impacts of cyclones, flooding, temperature rise, and sea-level rise, considering adaptation investments and calculating a resilience score.
*   **Environmental Impact (`models/environmental_impact.py`):** Calculates GHG emissions (CO2eq), air pollutants (SOx, NOx, PM2.5), water withdrawal/consumption, land use, and waste based on generation mix and emission factors.
*   **Innovation Ecosystem (`models/innovation_ecosystem.py`):** Models technology adaptation capacity, local manufacturing share, business model innovation, and digitalization level.
*   **Energy Finance (`models/energy_finance.py`):** Estimates annual investment needs and simulates mobilized funds from public, private, development, commercial, and household sources, calculating the financing gap.

The simulation integrates these components to project energy security, accessibility, affordability, and sustainability under various scenarios (though currently only a 'baseline' scenario is configured with synthetic data).

## Project Structure

```
.bangladesh_energy_simulation/
├── models/               # Core simulation component models
│   ├── __init__.py
│   ├── generation_portfolio.py
│   ├── fuel_supply.py
│   ├── grid_infrastructure.py
│   ├── demand.py
│   ├── market.py
│   ├── governance.py
│   ├── renewable_transition.py
│   ├── energy_access.py
│   ├── climate_resilience.py
│   ├── environmental_impact.py
│   ├── innovation_ecosystem.py
│   └── energy_finance.py
├── data/                 # Placeholder for input data files
├── results/              # Simulation output files (e.g., HTML reports)
├── visualizations/       # Placeholder for custom visualization scripts
├── utils/                # Placeholder for utility functions
├── tests/                # Placeholder for unit and integration tests
├── main_simulation.py    # Main simulation runner script with configuration
├── data_handler.py       # Placeholder data handler class
├── results_analyzer.py   # Analyzes results and generates reports/plots
├── requirements.txt      # Project dependencies
└── README.md             # This file
```

## Current Status

*   All 12 core model classes are implemented with placeholder logic for their sub-components.
*   The main simulation loop in `main_simulation.py` orchestrates the models, passing outputs as inputs where appropriate.
*   A plausible (but synthetic) configuration for a 'baseline' scenario (2025-2040) is included in `main_simulation.py`.
*   The `results_analyzer.py` processes the simulation output using Pandas, generates key plots using Plotly (Capacity, Generation Mix, Emissions, Access Rates, Investment), and saves an interactive HTML report.

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/deluair/BD_energy_simulation.git
    cd BD_energy_simulation
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the simulation:**
    ```bash
    python main_simulation.py
    ```
    This will execute the baseline scenario simulation (currently 2025-2040) and print logs to the console.

5.  **View the results:**
    *   An HTML report will be generated in the `results/` directory (e.g., `results/simulation_report_baseline.html`).
    *   Open this file in a web browser to view summary plots of key indicators over the simulation period.

## Next Steps & Potential Enhancements

*   **Refine Model Logic:** Replace placeholder calculations in model methods with more sophisticated, data-driven logic.
*   **Data Integration:** Implement `data_handler.py` to load real-world data for configuration and validation.
*   **Calibration & Validation:** Calibrate model parameters against historical data and validate simulation outputs.
*   **Scenario Development:** Define multiple scenarios (e.g., high renewables, delayed nuclear, carbon tax) by modifying the configuration in `main_simulation.py` or through a dedicated scenario management system.
*   **Dispatch Model:** Implement a more realistic unit commitment / economic dispatch model within `GenerationPortfolioModel.simulate_dispatch`.
*   **Capacity Expansion:** Add an endogenous capacity expansion planning module instead of relying solely on the predefined `expansion_pipeline`.
*   **Agent-Based Modeling:** Incorporate agent-based approaches for decisions like household DER adoption or investor behavior.
*   **System Dynamics:** Explicitly model feedback loops (e.g., between tariffs, demand, and collection efficiency).
*   **Visualization:** Enhance the HTML report or create dedicated dashboards (e.g., using Dash) for deeper result exploration.
*   **Testing:** Develop unit tests for individual model components and integration tests for the overall simulation flow. 