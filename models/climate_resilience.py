class ClimateResilienceModel:
    """Model climate impacts on energy systems and adaptation"""
    def __init__(self, config):
        """
        Initializes the climate resilience model.

        Args:
            config (dict): Configuration parameters for climate resilience, including:
                           - vulnerability_params: Infrastructure vulnerability to hazards.
                           - hazard_scenarios: Projections for cyclone intensity, flood levels, temp increase, SLR.
                           - adaptation_params: Costs and effectiveness of adaptation measures.
                           - baseline_resilience: Initial resilience score or metrics.
        """
        self.config = config
        self.vulnerability_params = config.get('vulnerability_params', {})
        self.hazard_scenarios = config.get('hazard_scenarios', {'rcp': 'rcp45'}) # Example scenario choice
        self.adaptation_params = config.get('adaptation_params', {'investment_effectiveness': 0.1})
        # Store current resilience state
        self.current_resilience_score = config.get('baseline_resilience', 0.4)
        self.cumulative_adaptation_investment = 0

        print("ClimateResilienceModel initialized.")

    def _simulate_cyclone_impacts(self, year, hazard_level, infrastructure_state, adaptation_measures):
        # Placeholder: Model damage based on cyclone intensity, infrastructure vulnerability, and protection.
        # Hazard level increases over time (example)
        cyclone_intensity_index = 1.0 + 0.02 * (year - 2025) * hazard_level.get('cyclone_factor', 1.0)
        # Vulnerability decreases with adaptation (e.g., undergrounding, tower strength)
        vulnerability_factor = max(0.1, 0.8 - adaptation_measures.get('cyclone_protection_score', 0) * 0.5)
        damage_cost = 50 * cyclone_intensity_index * vulnerability_factor # Example cost (Million USD/event)
        outage_duration_hours = 24 * cyclone_intensity_index * vulnerability_factor # Example
        print(f"  - Cyclone Impacts: Intensity {cyclone_intensity_index:.2f}, Vulnerability {vulnerability_factor:.2f}, Est. Damage ${damage_cost:.1f}M/event")
        return {'estimated_damage_cost_per_event_m_usd': damage_cost, 'estimated_outage_hours_per_event': outage_duration_hours}

    def _simulate_flooding_impacts(self, year, hazard_level, infrastructure_state, adaptation_measures):
        # Placeholder: Model damage based on flood depth/duration, substation elevation, defenses.
        flood_risk_index = 1.0 + 0.015 * (year - 2025) * hazard_level.get('flood_factor', 1.0)
        protection_level = adaptation_measures.get('flood_protection_score', 0)
        damage_cost = 30 * flood_risk_index * max(0.1, 1 - protection_level) # Example cost (Million USD/year)
        print(f"  - Flooding Impacts: Risk Index {flood_risk_index:.2f}, Protection {protection_level:.2f}, Est. Damage ${damage_cost:.1f}M/year")
        return {'estimated_annual_damage_cost_m_usd': damage_cost}

    def _simulate_temperature_effects(self, year, hazard_level, infrastructure_state, adaptation_measures):
        # Placeholder: Model derating of lines/plants, cooling constraints, HVAC demand spikes.
        temp_increase_deg_c = 0.05 * (year - 2025) * hazard_level.get('temp_factor', 1.0)
        derating_factor = 0.01 * temp_increase_deg_c # Example: 1% derating per degree C increase
        # Adaptation (e.g., high-temp conductors) reduces impact
        mitigation_factor = adaptation_measures.get('temp_adaptation_score', 0)
        net_derating = max(0, derating_factor * (1 - mitigation_factor))
        cooling_stress_index = temp_increase_deg_c * 0.1 # Example
        print(f"  - Temperature Effects: Temp Increase {temp_increase_deg_c:.2f}C, Net Derating {net_derating*100:.2f}%")
        return {'avg_derating_factor': net_derating, 'cooling_stress_index': cooling_stress_index}

    def _simulate_sea_level_rise_impacts(self, year, hazard_level, infrastructure_state, adaptation_measures):
        # Placeholder: Model coastal inundation risk, salinity impacts, relocation needs.
        slr_cm = 1.0 * (year - 2025) * hazard_level.get('slr_factor', 1.0) # Example SLR rate
        assets_at_risk_pct = min(1.0, 0.05 + slr_cm * 0.01) # Example % assets vulnerable
        adaptation_level = adaptation_measures.get('slr_adaptation_score', 0)
        net_risk_factor = max(0, assets_at_risk_pct * (1 - adaptation_level))
        print(f"  - Sea Level Rise: SLR {slr_cm:.1f}cm, Net Risk Factor {net_risk_factor:.3f}")
        return {'sea_level_rise_cm': slr_cm, 'net_risk_factor': net_risk_factor}

    def _simulate_climate_resilient_design(self, year, adaptation_investment):
        # Placeholder: Model adoption of forward-looking standards, increasing resilience score.
        self.cumulative_adaptation_investment += adaptation_investment
        investment_effectiveness = self.adaptation_params.get('investment_effectiveness', 0.1)
        # Resilience score increases with investment, but diminishing returns
        resilience_increase = investment_effectiveness * (adaptation_investment / 1000) * (1 - self.current_resilience_score)
        self.current_resilience_score = min(1.0, self.current_resilience_score + resilience_increase)
        # Map resilience score to specific adaptation measures scores (simplified)
        adaptation_scores = {
            'cyclone_protection_score': self.current_resilience_score * 0.8,
            'flood_protection_score': self.current_resilience_score * 0.7,
            'temp_adaptation_score': self.current_resilience_score * 0.5,
            'slr_adaptation_score': self.current_resilience_score * 0.6
        }
        print(f"  - Resilient Design: Investment ${adaptation_investment}M, New Resilience Score {self.current_resilience_score:.3f}")
        return {'overall_resilience_score': self.current_resilience_score, 'adaptation_measures_scores': adaptation_scores}

    def simulate_climate_impacts(self, year, hazard_scenarios, infrastructure_vulnerability, adaptation_investment, infrastructure_state):
        """
        Calculates climate effects and resilience improvements for the year.

        Args:
            year (int): The simulation year.
            hazard_scenarios (dict): Specific hazard projections for the year (e.g., cyclone frequency/intensity).
            infrastructure_vulnerability (dict): Current vulnerability state of grid/plants.
            adaptation_investment (float): Planned investment in adaptation measures for the year (e.g., Million USD).
            infrastructure_state (dict): Current state of grid/generation assets.

        Returns:
            dict: Summary of climate impacts and resilience status for the year.
        """
        print(f"Simulating climate impacts for year {year}...")

        # Determine current hazard levels based on scenarios (e.g., RCP)
        # Simplified: use factors from config
        hazard_factors = {
            'cyclone_factor': 1.0 if self.hazard_scenarios.get('rcp') == 'rcp45' else 1.5,
            'flood_factor': 1.0 if self.hazard_scenarios.get('rcp') == 'rcp45' else 1.3,
            'temp_factor': 1.0 if self.hazard_scenarios.get('rcp') == 'rcp45' else 1.2,
            'slr_factor': 1.0 if self.hazard_scenarios.get('rcp') == 'rcp45' else 1.4,
        }

        # Simulate effect of adaptation investment
        resilience_results = self._simulate_climate_resilient_design(year, adaptation_investment)
        adaptation_measures_scores = resilience_results['adaptation_measures_scores']

        # Simulate impacts from different hazards
        cyclone_results = self._simulate_cyclone_impacts(year, hazard_factors, infrastructure_state, adaptation_measures_scores)
        flood_results = self._simulate_flooding_impacts(year, hazard_factors, infrastructure_state, adaptation_measures_scores)
        temp_results = self._simulate_temperature_effects(year, hazard_factors, infrastructure_state, adaptation_measures_scores)
        slr_results = self._simulate_sea_level_rise_impacts(year, hazard_factors, infrastructure_state, adaptation_measures_scores)

        # Combine results
        # Estimate total annual damage cost (very simplified)
        total_damage_cost = cyclone_results['estimated_damage_cost_per_event_m_usd'] * hazard_scenarios.get('cyclone_frequency', 0.5) + \
                          flood_results['estimated_annual_damage_cost_m_usd'] # Add other costs?

        climate_summary = {
            'resilience_status': resilience_results,
            'cyclone_impacts': cyclone_results,
            'flooding_impacts': flood_results,
            'temperature_effects': temp_results,
            'sea_level_rise_impacts': slr_results,
            'estimated_total_annual_damage_m_usd': total_damage_cost,
            'overall_resilience_score': self.current_resilience_score
        }

        print(f"Climate impact simulation complete for {year}. Est. Annual Damage: ${total_damage_cost:.1f}M")
        # Return structure similar to placeholder in main_simulation for now
        # return {
        #     "estimated_climate_damage_cost": total_damage_cost,
        #     "resilience_level": self.current_resilience_score
        # }
        return climate_summary # Return detailed summary

    # Add methods for multi-hazard interactions, detailed vulnerability mapping later 