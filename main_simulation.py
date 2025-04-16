import json
import pandas as pd # Added import

# Import models (assuming they are in the 'models' directory)
from models.generation_portfolio import GenerationPortfolioModel
from models.fuel_supply import FuelSupplyModel
from models.grid_infrastructure import GridInfrastructureModel
from models.demand import DemandModel
from models.market import MarketModel
from models.governance import GovernanceModel
from models.renewable_transition import RenewableTransitionModel
from models.energy_access import EnergyAccessModel
from models.climate_resilience import ClimateResilienceModel
from models.environmental_impact import EnvironmentalImpactModel
from models.innovation_ecosystem import InnovationEcosystemModel
from models.energy_finance import EnergyFinanceModel

# Import analyzer (assuming it's in the root directory)
from results_analyzer import EnergyResultsAnalyzer # Added import

class BangladeshEnergySimulation:
    """Main simulation environment integrating all components"""
    def __init__(self, config):
        """
        Initialize simulation with configuration parameters.

        Args:
            config (dict): A dictionary containing configuration parameters
                           for all sub-models. Expected keys might include:
                           'base_year_capacity', 'technology_parameters',
                           'expansion_pipeline', 'retirement_schedule',
                           'dispatch_merit_order', 'operational_constraints',
                           'fuel_supply_config', 'grid_config', 'demand_config',
                           'market_config', 'governance_config', 'renewable_config',
                           'access_config', 'climate_config', 'environment_config',
                           'innovation_config', 'finance_config', etc.
        """
        print("Initializing Bangladesh Energy Simulation...")
        self.config = config
        self.results = {} # Store results keyed by scenario name

        # --- Initialize models --- 
        # Generation Portfolio
        self.generation_portfolio = GenerationPortfolioModel(
            base_year_capacity=config.get('generation_params', {}).get('base_year_capacity', {}),
            technology_parameters=config.get('generation_params', {}).get('technology_parameters', {}),
            expansion_pipeline=config.get('generation_params', {}).get('expansion_pipeline', []),
            retirement_schedule=config.get('generation_params', {}).get('retirement_schedule', []),
            dispatch_merit_order=config.get('generation_params', {}).get('dispatch_merit_order', []),
            operational_constraints=config.get('generation_params', {}).get('operational_constraints', {})
        )
        # Fuel Supply
        self.fuel_supply = FuelSupplyModel(config.get('fuel_supply_params', {}))
        # Grid Infrastructure
        self.grid_infrastructure = GridInfrastructureModel(config.get('grid_params', {}))
        # Demand
        self.demand = DemandModel(config.get('demand_params', {}))
        # Market
        self.market = MarketModel(config.get('market_params', {}))
        # Governance
        self.governance = GovernanceModel(config.get('governance_params', {}))
        # Renewable Transition
        self.renewable_transition = RenewableTransitionModel(config.get('renewable_params', {}))
        # Energy Access
        self.energy_access = EnergyAccessModel(config.get('access_params', {}))
        # Climate Resilience
        self.climate_resilience = ClimateResilienceModel(config.get('climate_params', {}))
        # Environmental Impact
        self.environmental_impact = EnvironmentalImpactModel(config.get('environment_params', {}))
        # Innovation Ecosystem
        self.innovation = InnovationEcosystemModel(config.get('innovation_params', {}))
        # Energy Finance
        self.finance = EnergyFinanceModel(config.get('finance_params', {}))

        print("All models initialized.")

    def run_simulation(self, start_year=2025, end_year=2050, scenarios=None):
        """
        Execute multi-year simulation across scenarios.

        Args:
            start_year (int): The starting year for the simulation.
            end_year (int): The ending year for the simulation.
            scenarios (list, optional): A list of scenario configurations to run.
                                        If None, runs a default baseline scenario.
        """
        print(f"Starting simulation run from {start_year} to {end_year}...")

        if scenarios is None:
            scenarios = [{'name': 'baseline', 'config_overrides': {}}]

        simulation_results = {}

        for scenario in scenarios:
            scenario_name = scenario['name']
            print(f"\n--- Running Scenario: {scenario_name} ---")
            # --- Scenario Setup --- 
            # Create a deep copy of the config for this scenario run if needed
            # For now, assume parameters are updated within models or passed explicitly
            current_scenario_config = self.config.copy() # Shallow copy for top-level items
            current_scenario_config.update(scenario.get('config_overrides', {}))
            # TODO: Re-initialize models if necessary based on scenario overrides, or update their internal state.
            # For simplicity now, we pass scenario-specific params directly to methods where possible.

            scenario_yearly_results = []
            for year in range(start_year, end_year + 1):
                print(f"\nSimulating Year: {year}")
                year_results = {'year': year, 'scenario': scenario_name}

                # --- Exogenous Scenario Drivers for the year --- 
                # These would typically come from scenario definitions / external data handler
                economic_growth_factors = {
                    'gdp_growth': current_scenario_config.get('economic_growth_rate', 0.06),
                    'industrial_gdp_growth': current_scenario_config.get('economic_growth_rate', 0.06) * 1.1,
                    'service_sector_growth': current_scenario_config.get('economic_growth_rate', 0.06) * 1.2,
                }
                policy_inputs = {
                    'reform_agenda': current_scenario_config.get('reform_agenda', {}).get(year, {}),
                    'policy_support': current_scenario_config.get('policy_support', {}).get(year, {}),
                    'industrial_policy': current_scenario_config.get('industrial_policy', {}),
                    'subsidy_policies': {'level': 0.1}, # Example
                    'mitigation_measures': {'ccs_on_coal': False} # Example
                }
                climate_inputs = {
                     'hazard_scenarios': {'cyclone_frequency': 0.5}, # Example
                     'adaptation_investment': current_scenario_config.get('adaptation_investment_m_usd_per_year', 50)
                }
                financial_inputs = {
                    'fiscal_space': {'total_adp_budget': 15000 + 500 * (year-start_year)}, # Example increasing budget
                    'investment_climate': {}, # Will be filled by Governance model output
                    'climate_finance_access': {}, # Placeholder
                    'local_market_depth': {'score': 0.3 + 0.01*(year-start_year)}, # Example slow growth
                    'household_adoption': {'rooftop_solar': {'increase_mw': 50 + 10*(year-start_year)}} # Example growth
                }
                # Other external factors
                external_factors = {
                    'investor_confidence': 0.7 + 0.01 * (year-start_year), # Example
                    'data_availability_score': 0.6 + 0.01 * (year-start_year), # Example
                    'global_markets': {'global_gas_price_factor': 1.0, 'global_lng_spot_factor': 1.2}, # Example
                    'climate_conditions': {'solar_irradiance_factor': 1.0} # Example
                }

                # --- Simulation Step Logic (Order matters!) ---

                # 0. Update Generation Capacity based on pipeline/retirements for the CURRENT year
                self.generation_portfolio.update_capacity(year)
                year_results['start_of_year_capacity'] = self.generation_portfolio.current_capacity.copy()

                # 1. Project Demand
                demand_projections = self.demand.project_demand(
                    year=year,
                    economic_growth_factors=economic_growth_factors,
                    structural_changes={}, # Placeholder
                    efficiency_improvements={'efficiency_improvement_residential': 0.01}, # Example
                    electrification_rates={'ev_fleet_growth': 0.25} # Example
                )
                year_results['demand'] = demand_projections

                # 2. Simulate Fuel Supply
                fuel_conditions = self.fuel_supply.simulate_fuel_conditions(
                    year=year,
                    global_markets=external_factors['global_markets'],
                    domestic_production_status={}, # Placeholder
                    infrastructure_constraints={}, # Placeholder
                    climate_conditions=external_factors['climate_conditions']
                )
                year_results['fuel_supply'] = fuel_conditions

                # 3. Simulate Generation Dispatch (using updated capacity and current demand/fuel)
                # Needs a representation of demand profile (e.g. hourly load curve) - simplified here
                demand_profile_simple = {'total_demand': demand_projections['total_demand']} # Use total TWh for placeholder dispatch
                generation_dispatch_results = self.generation_portfolio.simulate_dispatch(
                    year=year,
                    demand_profile=demand_profile_simple, # Needs refinement
                    fuel_conditions=fuel_conditions,
                    grid_constraints={} # Placeholder, could come from grid model previous step?
                )
                year_results['generation_dispatch'] = generation_dispatch_results

                # 4. Simulate Grid Operations
                grid_op_results = self.grid_infrastructure.simulate_grid_operations(
                    year=year,
                    generation_dispatch=generation_dispatch_results,
                    demand_patterns=demand_projections, # Pass full demand breakdown
                    network_constraints={}, # Placeholder
                    weather_conditions={} # Placeholder
                )
                year_results['grid_operations'] = grid_op_results

                # 5. Simulate Market Outcomes
                market_outcomes = self.market.simulate_market_operations(
                    year=year,
                    supply_costs=generation_dispatch_results.get('variable_costs_mwh', {'default': 60}), # Pass costs if available
                    policy_interventions=policy_inputs,
                    institutional_arrangements={}, # Placeholder, could link to Governance
                    generation_dispatch=generation_dispatch_results # Pass full dispatch results
                )
                year_results['market_outcomes'] = market_outcomes

                # 6. Simulate Governance Impacts
                governance_results = self.governance.simulate_governance_impacts(
                    year=year,
                    reform_agenda=policy_inputs['reform_agenda'],
                    implementation_capacity={'regulator_capacity': 0.6}, # Example
                    political_economy_constraints={}, # Placeholder
                    external_factors=external_factors # Pass investor confidence etc.
                )
                year_results['governance'] = governance_results
                # Update financial input based on governance output
                financial_inputs['investment_climate'] = governance_results.get('private_sector_participation', {})

                # 7. Simulate Renewable Transition (influences *next* year's capacity update)
                renewable_transition_results = self.renewable_transition.simulate_transition(
                    year=year,
                    policy_support=policy_inputs['policy_support'],
                    cost_trajectories={}, # Placeholder
                    grid_integration_capabilities={
                        **grid_op_results, # Pass grid status
                         'total_generation_capacity_mw': sum(self.generation_portfolio.current_capacity.values()) # Pass current total capacity
                    },
                    market_conditions=market_outcomes['wholesale_market'], # Pass wholesale price signal
                    cross_border_agreements=grid_op_results.get('interconnections', {}) # Pass interconnection status
                )
                year_results['renewable_transition'] = renewable_transition_results
                # TODO: Feed the 'total_capacity_increase_mw' into the *next* year's GenerationPortfolioModel update logic.
                # This requires adjusting how update_capacity works or storing planned additions.
                # For now, the increases happen based on the expansion_pipeline config.

                # 8. Simulate Energy Access
                # Pass relevant outputs from other models
                access_results = self.energy_access.simulate_access_expansion(
                    year=year,
                    grid_extension_plans={}, # Placeholder
                    off_grid_developments={}, # Placeholder
                    affordability_measures=market_outcomes['retail_tariffs'],
                    equity_programs=current_scenario_config.get('equity_programs', {}),
                    market_outcomes=market_outcomes, # Pass full market outcomes if needed
                    grid_outcomes=grid_op_results, # Pass grid reliability metrics
                    transition_outcomes=renewable_transition_results # Pass RE transition info
                )
                year_results['energy_access'] = access_results

                # 9. Simulate Climate Resilience Impacts
                climate_results = self.climate_resilience.simulate_climate_impacts(
                    year=year,
                    hazard_scenarios=climate_inputs['hazard_scenarios'],
                    infrastructure_vulnerability={}, # Placeholder
                    adaptation_investment=climate_inputs['adaptation_investment'],
                    infrastructure_state={
                        **year_results['start_of_year_capacity'],
                        **grid_op_results # Pass grid state
                    }
                )
                year_results['climate_resilience'] = climate_results

                # 10. Calculate Environmental Impacts
                env_impacts = self.environmental_impact.calculate_impacts(
                    year=year,
                    generation_dispatch_results=generation_dispatch_results,
                    technology_parameters=self.generation_portfolio.technology_parameters,
                    mitigation_measures=policy_inputs['mitigation_measures']
                )
                year_results['environmental_impact'] = env_impacts

                # 11. Simulate Innovation Ecosystem
                innovation_results = self.innovation.simulate_innovation(
                    year=year,
                    r_and_d_investment={}, # Placeholder
                    market_pull_factors=market_outcomes, # Example link
                    institutional_capacity=governance_results, # Example link
                    industrial_policy=policy_inputs['industrial_policy'],
                    policy_support=policy_inputs['policy_support'],
                    investment_digital={}
                )
                year_results['innovation_ecosystem'] = innovation_results

                # 12. Simulate Financial Flows
                # Needs capacity expansion plans - using the main config pipeline for now
                # A more dynamic approach would take expansion decisions from RE model or a capacity expansion model
                finance_results = self.finance.simulate_financial_flows(
                    year=year,
                    project_pipeline=self.config.get('generation_params', {}).get('expansion_pipeline', []), # Using static pipeline
                    financing_sources={}, # Placeholder
                    risk_mitigation_tools={}, # Placeholder
                    grid_investment_needs={'annual_investment_m_usd': 1200 + 50*(year-start_year)}, # Example growing need
                    fiscal_space=financial_inputs['fiscal_space'],
                    investment_climate=financial_inputs['investment_climate'], # From Governance model
                    # Pass the relevant score/params for climate finance access
                    climate_finance_access={
                        'climate_finance_access_score': self.finance.dev_finance_params.get('climate_finance_access_score', 0.5) 
                    },
                    local_market_depth=financial_inputs['local_market_depth'],
                    household_adoption=financial_inputs['household_adoption']
                )
                year_results['finance'] = finance_results

                # --- End of Simulation Step --- 
                scenario_yearly_results.append(year_results)
                print(f"Year {year} simulation complete.")

            simulation_results[scenario_name] = scenario_yearly_results
            print(f"--- Scenario {scenario_name} complete ---")

        self.results = simulation_results # Store all results
        print("\nSimulation run finished.")
        return self.results

# --- Main Execution Block --- 
if __name__ == "__main__":
    # --- Plausible Synthetic Configuration Data (Baseline) --- 
    config = {
        'simulation_years': (2025, 2040), # Shorter duration for testing
        'economic_growth_rate': 0.065, # Average annual GDP growth
        'adaptation_investment_m_usd_per_year': 75,

        'generation_params': {
            'base_year_capacity': {'gas_cc': 8000, 'gas_oc': 3000, 'coal': 6000, 'liquid': 2000, 'hydro': 230, 'solar_util': 800, 'wind': 150, 'nuclear': 0},
            'technology_parameters': {
                # Costs in USD/MWh (Variable O&M + Fuel)
                'gas_cc': {'efficiency': 0.52, 'vom_cost': 3, 'fuel_cost_mmbtu': 6, 'heat_rate_btu_kwh': 6560, 'ramp_rate_mw_min': 15, 'min_load': 0.4, 'co2_factor_t_mwh': 0.38, 'sox_factor_t_mwh': 0.0001, 'nox_factor_t_mwh': 0.0002},
                'gas_oc': {'efficiency': 0.38, 'vom_cost': 5, 'fuel_cost_mmbtu': 6.5, 'heat_rate_btu_kwh': 8980, 'ramp_rate_mw_min': 25, 'min_load': 0.5, 'co2_factor_t_mwh': 0.42, 'sox_factor_t_mwh': 0.0001, 'nox_factor_t_mwh': 0.0003},
                'coal': {'efficiency': 0.39, 'vom_cost': 4, 'fuel_cost_tonne': 120, 'heat_rate_btu_kwh': 8750, 'ramp_rate_mw_min': 5, 'min_load': 0.5, 'co2_factor_t_mwh': 0.95, 'sox_factor_t_mwh': 0.0015, 'nox_factor_t_mwh': 0.0010, 'pm25_factor_t_mwh': 0.0005, 'coal_ash_t_per_mwh': 0.08},
                'liquid': {'efficiency': 0.35, 'vom_cost': 8, 'fuel_cost_bbl': 80, 'heat_rate_btu_kwh': 9750, 'ramp_rate_mw_min': 20, 'min_load': 0.3, 'co2_factor_t_mwh': 0.75, 'sox_factor_t_mwh': 0.0020, 'nox_factor_t_mwh': 0.0015},
                'hydro': {'vom_cost': 2, 'ramp_rate_mw_min': 50, 'min_load': 0.1, 'co2_factor_t_mwh': 0.01}, # Small reservoir emissions
                'solar_util': {'vom_cost': 5, 'co2_factor_t_mwh': 0.02}, # Lifecycle
                'wind': {'vom_cost': 8, 'co2_factor_t_mwh': 0.015}, # Lifecycle
                'nuclear': {'efficiency': 0.33, 'vom_cost': 10, 'fuel_cost_mwh': 8, 'heat_rate_btu_kwh': 10340, 'ramp_rate_mw_min': 2, 'min_load': 0.7, 'co2_factor_t_mwh': 0.01} # Lifecycle
            },
            'expansion_pipeline': [
                {'year': 2025, 'tech': 'nuclear', 'capacity': 1200, 'plant_id': 'Rooppur_1'},
                {'year': 2026, 'tech': 'nuclear', 'capacity': 1200, 'plant_id': 'Rooppur_2'},
                {'year': 2026, 'tech': 'solar_util', 'capacity': 600},
                {'year': 2027, 'tech': 'coal', 'capacity': 1320, 'plant_id': 'Matarbari_Ext'}, # Example extension
                {'year': 2028, 'tech': 'wind', 'capacity': 300},
                {'year': 2029, 'tech': 'solar_util', 'capacity': 800},
                {'year': 2030, 'tech': 'gas_cc', 'capacity': 700},
                 # Add more entries up to 2050 based on plans/scenarios
            ],
            'retirement_schedule': [
                {'year': 2028, 'tech': 'liquid', 'capacity': 500, 'plant_id': 'old_rental_1'},
                {'year': 2030, 'tech': 'gas_oc', 'capacity': 300, 'plant_id': 'old_gas_peak_1'},
                {'year': 2035, 'tech': 'coal', 'capacity': 200, 'plant_id': 'old_coal_small'},
                # Add more based on plant ages
            ],
            'dispatch_merit_order': ['nuclear', 'hydro', 'solar_util', 'wind', 'gas_cc', 'coal', 'gas_oc', 'liquid'],
            'operational_constraints': {'min_gas_take_pct': 0.6, 'max_coal_utilization_pct': 0.85}
        },

        'fuel_supply_params': {
            'domestic_gas_params': {'initial_prod_bcf_yr': 800, 'decline_rate': 0.04},
            'lng_params': {'terminal_capacity_mtpa': 12.5, 'contract_price_usd_mmbtu': 9, 'spot_share': 0.25},
            'coal_params': {'import_dependency': 0.98, 'logistics_cost_usd_tonne': 25},
            'liquid_fuel_params': {},
            'renewable_resource_params': {'avg_solar_cf': 0.17, 'avg_wind_cf_coastal': 0.30}
        },

        'grid_params': {
            'transmission_params': {'base_capacity_gw': 30, 'expansion_rate': 0.06},
            'distribution_params': {'feeder_overload_base_pct': 0.08, 'saidi_base_hours': 15},
            'loss_params': {'base_technical_loss': 0.06, 'base_non_technical_loss': 0.05, 'nt_loss_reduction_factor_per_ami_pct': 0.08},
            'smart_grid_params': {'target_penetration': 0.9, 'rollout_speed_pct_yr': 0.06},
            'interconnection_params': {'base_import_capacity_mw': 1160, 'planned_increase_mw_yr': 150}
        },

        'demand_params': {
             'base_demand_twh': {'residential': 80, 'industrial': 100, 'commercial': 40, 'agricultural': 15, 'transport': 2, 'total': 237}, # Approx 2024/25 baseline TWh
             'sector_params': {},
             'elasticity_params': {'income_elasticity_residential': 0.85, 'gdp_elasticity_industrial': 1.05, 'gdp_elasticity_commercial': 0.95}
        },

        'market_params': {
            'market_structure_params': {'type': 'single_buyer'}, # Could change in a scenario
            'tariff_params': {'avg_retail_markup': 1.25, 'subsidy_level': 0.15},
            'ppa_params': {'avg_ppa_price': 70}, # Average existing PPA price $/MWh
            're_support_params': {'fit_solar': 85, 'auction_target_solar_mw_yr': 400}
        },

        'governance_params': {
            'unbundling_status': {'level': 'functional'}, # Example state
            'regulatory_params': {'capacity_score': 0.55, 'independence_score': 0.4},
            'planning_params': {'irp_adopted': True, 'adherence_score': 0.6},
            'ppp_framework': {'clarity_score': 0.65}
        },

        'renewable_params': {
            'solar_params': {'base_cost_mwh': 65, 'potential_gw': 50},
            'wind_params': {'base_cost_mwh': 75, 'potential_gw': 10},
            'integration_params': {'max_vre_penetration': 0.4, 'curtailment_start_thresh': 0.35},
            'learning_curves': {'solar_lr': 0.18, 'wind_lr': 0.12},
            'base_solar_mw': 800, # Match base capacity
            'base_wind_mw': 150 # Match base capacity
        },

        'access_params': {
            'baseline_access_rates': {'national': 0.98, 'urban': 1.0, 'rural': 0.96},
            'access_params': {'rural_target_access': 1.0},
            'affordability_params': {'max_energy_burden_pct': 0.10},
            'equity_programs': {'gender': {'support_level': 150}, 'just_transition': {'reskilling_effectiveness': 0.4}}
        },

        'climate_params': {
             'hazard_scenarios': {'rcp': 'rcp60'}, # Example scenario
             'adaptation_params': {'investment_effectiveness': 0.08}, # Lower effectiveness
             'baseline_resilience': 0.35
        },

        'environment_params': {
            # Emission factors (tonnes/MWh), Water (m3/MWh), Land (sqkm/MW)
             'emission_factors': {
                'gas_cc': {'co2eq_t_per_mwh': 0.38, 'sox_t_per_mwh': 0.0001, 'nox_t_per_mwh': 0.0002, 'pm25_t_per_mwh': 0.00005},
                'gas_oc': {'co2eq_t_per_mwh': 0.42, 'sox_t_per_mwh': 0.0001, 'nox_t_per_mwh': 0.0003, 'pm25_t_per_mwh': 0.00006},
                'coal': {'co2eq_t_per_mwh': 0.95, 'sox_t_per_mwh': 0.0015, 'nox_t_per_mwh': 0.0010, 'pm25_t_per_mwh': 0.0005},
                'liquid': {'co2eq_t_per_mwh': 0.75, 'sox_t_per_mwh': 0.0020, 'nox_t_per_mwh': 0.0015, 'pm25_t_per_mwh': 0.0008},
                'hydro': {'co2eq_t_per_mwh': 0.01},
                'solar_util': {'co2eq_t_per_mwh': 0.02},
                'wind': {'co2eq_t_per_mwh': 0.015},
                'nuclear': {'co2eq_t_per_mwh': 0.01}
            },
            'water_factors': {
                 'gas_cc': {'withdrawal_m3_per_mwh': 0.8, 'consumption_m3_per_mwh': 0.2},
                 'coal': {'withdrawal_m3_per_mwh': 1.5, 'consumption_m3_per_mwh': 0.5},
                 'nuclear': {'withdrawal_m3_per_mwh': 1.8, 'consumption_m3_per_mwh': 0.6},
            },
            'land_use_factors': {
                'solar_util': {'sqkm_per_mw': 0.02},
                'wind': {'sqkm_per_mw': 0.08},
                'coal': {'sqkm_per_mw': 0.005}
            }, # sqkm/MW
            'waste_factors': {'coal': {'coal_ash_t_per_mwh': 0.08}},
            'mitigation_params': {'ccs_capture_rate': 0.9} # If CCS is enabled
        },

        'innovation_params': {
             'baseline_innovation_scores': {'adaptation': 0.45, 'local_mfg_share': 0.06, 'biz_model': 0.35, 'digital': 0.25}
        },

        'finance_params': {
             'investment_needs': {'cost_per_mw_new': 1.4}, # M USD / MW average
             'public_finance_params': {'adp_share_energy': 0.08},
             'private_finance_params': {'investor_risk_perception': 0.65}, # 0=low risk, 1=high risk
             'dev_finance_params': {'climate_finance_access_score': 0.55}
        }
    }

    # --- Define Scenarios --- 
    baseline_scenario = {
        'name': 'baseline',
        'config_overrides': {}
    }

    high_renewables_scenario = {
        'name': 'high_renewables',
        'config_overrides': {
            # Example overrides for a high renewables scenario
            'renewable_params': {
                 # Faster cost reduction or lower base cost
                 'solar_params': {'base_cost_mwh': 55}, # Lower than baseline 65
                 'wind_params': {'base_cost_mwh': 65}, # Lower than baseline 75
                 'learning_curves': {'solar_lr': 0.20, 'wind_lr': 0.15}, # Faster learning
                 # Higher integration tolerance
                 'integration_params': {'max_vre_penetration': 0.6, 'curtailment_start_thresh': 0.5},
                 'base_solar_mw': 800, # Ensure base matches baseline if not overridden
                 'base_wind_mw': 150 # Ensure base matches baseline if not overridden
             },
            'market_params': {
                 # Higher RE support
                 're_support_params': {'fit_solar': 90, 'auction_target_solar_mw_yr': 600, 'auction_target_wind_mw_yr': 200}
             },
            # Optional: Adjust fossil/nuclear pipeline if RE is prioritized
            'generation_params': {
                'expansion_pipeline': [
                    # Keep nuclear for this example, but delay or remove some fossil?
                    {'year': 2025, 'tech': 'nuclear', 'capacity': 1200, 'plant_id': 'Rooppur_1'},
                    {'year': 2026, 'tech': 'nuclear', 'capacity': 1200, 'plant_id': 'Rooppur_2'},
                    {'year': 2026, 'tech': 'solar_util', 'capacity': 800}, # Increased solar early
                    # {'year': 2027, 'tech': 'coal', 'capacity': 1320, 'plant_id': 'Matarbari_Ext'}, # Removed coal expansion
                    {'year': 2028, 'tech': 'wind', 'capacity': 500}, # Increased wind
                    {'year': 2029, 'tech': 'solar_util', 'capacity': 1000}, # Increased solar
                    # {'year': 2030, 'tech': 'gas_cc', 'capacity': 700}, # Removed gas expansion
                ]
                 # Inherit other generation_params from baseline config implicitly during run
            }
             # Note: Overrides are shallow. Deep merging might be needed for nested dicts
             # like technology_parameters if only one sub-key needs changing.
        }
    }

    scenarios_to_run = [baseline_scenario, high_renewables_scenario]

    # --- Initialize and Run Simulation --- 
    simulation = BangladeshEnergySimulation(config)
    start_sim_year, end_sim_year = config['simulation_years']
    # Pass the list of scenarios to run
    results = simulation.run_simulation(start_year=start_sim_year, end_year=end_sim_year, scenarios=scenarios_to_run)

    # --- Analyze and Report Results --- 
    if results:
        print("\n--- Analyzing Results and Generating Reports --- ")
        analyzer = EnergyResultsAnalyzer(results)
        # Generate a report for each scenario that produced results
        generated_reports = []
        for scenario_name in results.keys():
             print(f"Generating report for scenario: {scenario_name}...")
             report_path = analyzer.generate_html_report(scenario=scenario_name)
             if report_path:
                 print(f"  Report generated: {report_path}")
                 generated_reports.append(report_path)
             else:
                 print(f"  Failed to generate report for {scenario_name}.")
        
        if not generated_reports:
             print("No reports were generated.")

    else:
        print("Simulation did not produce results.") 