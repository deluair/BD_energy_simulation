class EnergyFinanceModel:
    """Model energy sector investment and financing"""
    def __init__(self, config):
        """
        Initializes the energy finance model.

        Args:
            config (dict): Configuration parameters for energy finance, including:
                           - investment_needs: Rules/estimates for calculating annual investment needed.
                           - public_finance_params: ADP allocation trends, SOE capacity.
                           - private_finance_params: IPP framework status, risk perception.
                           - dev_finance_params: MDB/bilateral engagement levels, climate finance access.
                           - commercial_finance_params: Local bank capacity, capital market depth.
                           - household_finance_params: Rooftop solar/EE financing availability.
        """
        self.config = config
        self.investment_needs_params = config.get('investment_needs', {'cost_per_mw_new': 1.5}) # Million USD / MW
        self.public_finance_params = config.get('public_finance_params', {'adp_share_energy': 0.1})
        self.private_finance_params = config.get('private_finance_params', {'investor_risk_perception': 0.7})
        self.dev_finance_params = config.get('dev_finance_params', {'climate_finance_access_score': 0.6})
        self.commercial_finance_params = config.get('commercial_finance_params', {})
        self.household_finance_params = config.get('household_finance_params', {})
        # Store current finance state if needed
        self.cumulative_investment = 0

        print("EnergyFinanceModel initialized.")

    def _estimate_investment_needs(self, year, capacity_expansion_mw, grid_investment_needs):
        # Placeholder: Estimate total investment needed based on generation expansion and grid upgrades.
        generation_investment = capacity_expansion_mw * self.investment_needs_params.get('cost_per_mw_new', 1.5) # M USD
        grid_investment = grid_investment_needs.get('annual_investment_m_usd', 1000) # M USD
        total_needs = generation_investment + grid_investment
        print(f"  - Investment Needs: Generation ${generation_investment:.0f}M, Grid ${grid_investment:.0f}M, Total ${total_needs:.0f}M")
        return {'total_investment_needs_m_usd': total_needs}

    def _simulate_public_investment(self, year, total_needs, fiscal_space):
        # Placeholder: Model ADP allocations, SOE balance sheets, public debt constraints.
        adp_allocation = fiscal_space.get('total_adp_budget', 10000) * self.public_finance_params.get('adp_share_energy', 0.1)
        soe_investment = 500 # Example M USD from SOE resources
        public_investment = adp_allocation + soe_investment
        print(f"  - Public Investment: ADP ${adp_allocation:.0f}M, SOE ${soe_investment:.0f}M, Total ${public_investment:.0f}M")
        return {'total_public_investment_m_usd': public_investment}

    def _simulate_private_investment(self, year, total_needs, investment_climate):
        # Placeholder: Model IPP investments based on framework, risk perception, returns.
        # Example: Private investment proportional to needs, adjusted by risk/climate score
        risk_factor = max(0.1, 1 - self.private_finance_params.get('investor_risk_perception', 0.7)) # Lower risk -> higher factor
        climate_score = investment_climate.get('psp_environment_score', 0.5) # From GovernanceModel
        potential_private = total_needs * 0.6 # Assume private sector could cover 60%
        private_investment = potential_private * risk_factor * climate_score
        print(f"  - Private Investment: Potential ${potential_private:.0f}M, Actual ${private_investment:.0f}M (Risk: {risk_factor:.2f}, Climate: {climate_score:.2f})")
        return {'total_private_investment_m_usd': private_investment}

    def _simulate_development_finance(self, year, total_needs, climate_finance_access):
        # Placeholder: Model MDB/bilateral flows, climate finance mobilization.
        mdb_bilateral_base = 500 # Example M USD base lending
        climate_finance_mobilized = total_needs * 0.1 * climate_finance_access # Example: 10% of needs via climate finance, scaled by access score
        dev_finance = mdb_bilateral_base + climate_finance_mobilized
        print(f"  - Development Finance: Base ${mdb_bilateral_base:.0f}M, Climate ${climate_finance_mobilized:.0f}M, Total ${dev_finance:.0f}M")
        return {'total_development_finance_m_usd': dev_finance}

    def _simulate_commercial_financing(self, year, total_needs, local_market_depth):
        # Placeholder: Model domestic bank lending, capital market instruments.
        # Assume limited role initially
        commercial_lending = total_needs * 0.02 * local_market_depth.get('score', 0.3) # Example
        print(f"  - Commercial Financing: Total ${commercial_lending:.0f}M")
        return {'total_commercial_finance_m_usd': commercial_lending}

    def _simulate_household_investment(self, year, rooftop_solar_adoption, ee_uptake):
        # Placeholder: Model investment in rooftop solar, energy efficiency based on adoption rates.
        # Needs cost assumptions for rooftop solar ($/kW) and EE measures
        rooftop_mw_added = rooftop_solar_adoption.get('increase_mw', 100)
        household_solar_investment = rooftop_mw_added * 1.0 # Example $1M / MW installed cost
        household_ee_investment = ee_uptake.get('investment_m_usd', 50) # Example
        total_household = household_solar_investment + household_ee_investment
        print(f"  - Household Investment: Solar ${household_solar_investment:.0f}M, EE ${household_ee_investment:.0f}M, Total ${total_household:.0f}M")
        return {'total_household_investment_m_usd': total_household}

    def simulate_financial_flows(self, year, project_pipeline, financing_sources, risk_mitigation_tools, grid_investment_needs, fiscal_space, investment_climate, climate_finance_access, local_market_depth, household_adoption):
        """
        Projects investment trends and financing gaps for the year.

        Args:
            year (int): The simulation year.
            project_pipeline (list): Planned generation/transmission projects (from GenPortfolio/Grid).
            financing_sources (dict): Availability/terms of different sources.
            risk_mitigation_tools (dict): Status of guarantees, insurance etc.
            grid_investment_needs (dict): Estimated grid investment needed (from GridInfrastructure).
            fiscal_space (dict): Government budget constraints, ADP size.
            investment_climate (dict): Indicators of private sector investment attractiveness (from Governance).
            climate_finance_access (dict): Score/indicator of access to climate funds (from DevFinance? or Governance?).
            local_market_depth (dict): Indicators of local commercial finance capacity.
            household_adoption (dict): Results of household decisions on solar/EE (from specific agent model? or Access?).

        Returns:
            dict: Summary of investment needs, mobilized funds by source, and financing gap.
        """
        print(f"Simulating financial flows for year {year}...")

        # 1. Estimate Investment Needs
        # Needs total capacity expansion from GenerationPortfolioModel or RenewableTransitionModel
        # Assuming it's passed via project_pipeline or calculated separately
        capacity_expansion_mw = sum(item['capacity'] for item in project_pipeline if item['year'] == year) # Example extraction
        needs_results = self._estimate_investment_needs(year, capacity_expansion_mw, grid_investment_needs)
        total_needs = needs_results['total_investment_needs_m_usd']

        # 2. Simulate Investment Mobilization by Source
        public_inv = self._simulate_public_investment(year, total_needs, fiscal_space)
        private_inv = self._simulate_private_investment(year, total_needs, investment_climate)
        dev_fin = self._simulate_development_finance(year, total_needs, climate_finance_access.get('climate_finance_access_score', 0.6))
        comm_fin = self._simulate_commercial_financing(year, total_needs, local_market_depth)
        # Household investment might be separate or feed into needs calculation earlier
        hh_inv = self._simulate_household_investment(year, household_adoption.get('rooftop_solar', {}), household_adoption.get('energy_efficiency', {}))

        # 3. Calculate Total Mobilized and Gap
        total_mobilized = public_inv['total_public_investment_m_usd'] + \
                          private_inv['total_private_investment_m_usd'] + \
                          dev_fin['total_development_finance_m_usd'] + \
                          comm_fin['total_commercial_finance_m_usd'] + \
                          hh_inv['total_household_investment_m_usd']
        financing_gap = max(0, total_needs - total_mobilized)
        self.cumulative_investment += total_mobilized

        # Combine results
        finance_summary = {
            'investment_needs': needs_results,
            'mobilized_by_source': {
                'public': public_inv,
                'private': private_inv,
                'development_finance': dev_fin,
                'commercial': comm_fin,
                'household': hh_inv
            },
            'total_investment_mobilized_m_usd': total_mobilized,
            'financing_gap_m_usd': financing_gap,
            'cumulative_investment_m_usd': self.cumulative_investment
        }

        print(f"Financial flow simulation complete for {year}. Total Mobilized: ${total_mobilized:.0f}M, Gap: ${financing_gap:.0f}M")
        # Return structure similar to placeholder in main_simulation for now
        # return {
        #     "total_investment_mobilized": total_mobilized,
        #     "financing_gap": financing_gap,
        #     "fdi_inflow": private_inv['total_private_investment_m_usd'] # Assuming private = FDI for placeholder
        # }
        return finance_summary # Return detailed summary

    # Add methods for specific financing instrument modeling (green bonds, blended finance) later 