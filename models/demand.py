class DemandModel:
    """Model electricity consumption across sectors"""
    def __init__(self, config):
        """
        Initializes the demand model.

        Args:
            config (dict): Configuration parameters for demand modeling, including:
                           - base_demand_twh: Base year total demand or sector demands.
                           - sector_params: Parameters specific to each demand sector.
                                Example: {'residential': {'appliance_growth': ...}, ...}
                           - elasticity_params: Demand elasticity values (price, income).
        """
        self.config = config
        self.base_demand_twh = config.get('base_demand_twh', {})
        self.sector_params = config.get('sector_params', {})
        self.elasticity_params = config.get('elasticity_params', {})
        # Store current demand state if needed for year-on-year changes
        self.current_demand_twh = self.base_demand_twh.copy()
        print("DemandModel initialized.")

    def _project_residential_demand(self, year, drivers):
        # Placeholder: Model appliance ownership, cooling demand, urbanization, efficiency.
        base = self.current_demand_twh.get('residential', 50)
        growth_factor = 1 + drivers.get('gdp_growth', 0.06) * self.elasticity_params.get('income_elasticity_residential', 0.8)
        efficiency_factor = (1 - drivers.get('efficiency_improvement_residential', 0.01))
        demand_twh = base * growth_factor * efficiency_factor
        print(f"  - Residential Demand: {demand_twh:.2f} TWh")
        return demand_twh

    def _project_industrial_demand(self, year, drivers):
        # Placeholder: Model manufacturing GDP, energy intensity, SEZs, efficiency.
        base = self.current_demand_twh.get('industrial', 60)
        growth_factor = 1 + drivers.get('industrial_gdp_growth', 0.07) * self.elasticity_params.get('gdp_elasticity_industrial', 1.0)
        efficiency_factor = (1 - drivers.get('efficiency_improvement_industrial', 0.015))
        demand_twh = base * growth_factor * efficiency_factor
        print(f"  - Industrial Demand: {demand_twh:.2f} TWh")
        return demand_twh

    def _project_commercial_demand(self, year, drivers):
        # Placeholder: Model service sector growth, floor space, HVAC, efficiency.
        base = self.current_demand_twh.get('commercial', 30)
        growth_factor = 1 + drivers.get('service_sector_growth', 0.08) * self.elasticity_params.get('gdp_elasticity_commercial', 0.9)
        efficiency_factor = (1 - drivers.get('efficiency_improvement_commercial', 0.01))
        demand_twh = base * growth_factor * efficiency_factor
        print(f"  - Commercial Demand: {demand_twh:.2f} TWh")
        return demand_twh

    def _project_agricultural_demand(self, year, drivers):
        # Placeholder: Model irrigation electrification, groundwater depth, solar pumps.
        base = self.current_demand_twh.get('agricultural', 10)
        # Less sensitive to GDP, more to specific programs/water levels
        growth_factor = 1 + drivers.get('irrigation_expansion_rate', 0.02)
        efficiency_factor = (1 - drivers.get('solar_pump_adoption_rate', 0.05) * 0.5) # Solar pumps replace grid/diesel
        demand_twh = base * growth_factor * efficiency_factor
        print(f"  - Agricultural Demand: {demand_twh:.2f} TWh")
        return demand_twh

    def _project_transport_electrification_demand(self, year, drivers):
        # Placeholder: Model EV adoption scenarios, charging infrastructure.
        base = self.current_demand_twh.get('transport', 1)
        # Driven by EV adoption rates
        ev_adoption_rate = drivers.get('ev_adoption_rate', 0.1) # Cumulative adoption % target for the year
        base_transport_energy = 50 # Hypothetical total transport energy TWh (needs data)
        electrified_share = ev_adoption_rate * 0.1 # Assume EVs are 10% of transport energy needs
        demand_twh = base_transport_energy * electrified_share
        # Simple growth on previous year might be better if tracking EVs directly
        demand_twh = base * (1 + drivers.get('ev_fleet_growth', 0.30)) # Example 30% growth on previous year EV demand
        print(f"  - Transport Electrification Demand: {demand_twh:.2f} TWh")
        return demand_twh

    def project_demand(self, year, economic_growth_factors, structural_changes, efficiency_improvements, electrification_rates):
        """
        Calculates electricity demand by sector and region for the given year.

        Args:
            year (int): The simulation year.
            economic_growth_factors (dict): GDP growth, sectoral growth rates, etc.
            structural_changes (dict): Changes in economic structure (e.g., industrial share).
            efficiency_improvements (dict): Sectoral energy efficiency improvement rates.
            electrification_rates (dict): Rates of electrification in transport, agriculture etc.

        Returns:
            dict: Projected electricity demand by sector and total for the year (e.g., in TWh).
        """
        print(f"Projecting electricity demand for year {year}...")

        # Consolidate drivers from inputs
        drivers = {
            **economic_growth_factors,
            **structural_changes,
            **efficiency_improvements,
            **electrification_rates
        }

        # Project demand for each sector
        residential_demand = self._project_residential_demand(year, drivers)
        industrial_demand = self._project_industrial_demand(year, drivers)
        commercial_demand = self._project_commercial_demand(year, drivers)
        agricultural_demand = self._project_agricultural_demand(year, drivers)
        transport_demand = self._project_transport_electrification_demand(year, drivers)

        # Aggregate results
        projected_demand = {
            'residential': residential_demand,
            'industrial': industrial_demand,
            'commercial': commercial_demand,
            'agricultural': agricultural_demand,
            'transport': transport_demand,
            'total_demand': residential_demand + industrial_demand + commercial_demand + agricultural_demand + transport_demand
        }

        # Update current state for next year's calculation
        self.current_demand_twh = projected_demand.copy()
        del self.current_demand_twh['total_demand'] # Only store sectoral

        print(f"Demand projection complete for {year}. Total Demand: {projected_demand['total_demand']:.2f} TWh")
        # Return structure similar to placeholder in main_simulation for now
        # return {
        #     "total_demand": projected_demand['total_demand'],
        #     "residential": projected_demand['residential'],
        #     "industrial": projected_demand['industrial'],
        #     "commercial": projected_demand['commercial'],
        #     "agricultural": projected_demand['agricultural'],
        #     "transport": projected_demand['transport']
        # }
        return projected_demand # Return the detailed structure

    # Add methods for peak demand forecasting, regional disaggregation, etc. later 