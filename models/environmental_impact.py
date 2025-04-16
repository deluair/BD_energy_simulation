class EnvironmentalImpactModel:
    """Model environmental dimensions of energy system"""
    def __init__(self, config):
        """
        Initializes the environmental impact model.

        Args:
            config (dict): Configuration parameters for environmental impacts, including:
                           - emission_factors: GHG, SOx, NOx, PM2.5 factors per technology/fuel (e.g., tCO2eq/MWh).
                           - water_factors: Water withdrawal/consumption per technology (e.g., m3/MWh).
                           - land_use_factors: Land area per technology (e.g., sqkm/MW).
                           - waste_factors: Waste generation per technology (e.g., tonnes_ash/MWh).
                           - mitigation_params: Costs/effectiveness of mitigation measures (e.g., FGD, CCS).
        """
        self.config = config
        self.emission_factors = config.get('emission_factors', {})
        self.water_factors = config.get('water_factors', {})
        self.land_use_factors = config.get('land_use_factors', {})
        self.waste_factors = config.get('waste_factors', {})
        self.mitigation_params = config.get('mitigation_params', {})
        print("EnvironmentalImpactModel initialized.")

    def _calculate_ghg_emissions(self, generation_mix_gwh, emission_factors):
        # Placeholder: Calculate CO2eq emissions based on generation and factors.
        total_co2eq_tonnes = 0
        for tech, gwh in generation_mix_gwh.items():
             # Example factor: tonnes CO2eq / MWh
             factor = emission_factors.get(tech, {}).get('co2eq_t_per_mwh', 0)
             total_co2eq_tonnes += gwh * 1000 * factor # Convert GWh to MWh
        print(f"  - GHG Emissions: {total_co2eq_tonnes / 1e6:.2f} Million tonnes CO2eq")
        return {'total_co2eq_tonnes': total_co2eq_tonnes}

    def _calculate_air_quality_impacts(self, generation_mix_gwh, emission_factors):
        # Placeholder: Calculate SOx, NOx, PM2.5 emissions.
        total_sox_tonnes = 0
        total_nox_tonnes = 0
        total_pm25_tonnes = 0
        for tech, gwh in generation_mix_gwh.items():
             tech_factors = emission_factors.get(tech, {})
             total_sox_tonnes += gwh * 1000 * tech_factors.get('sox_t_per_mwh', 0)
             total_nox_tonnes += gwh * 1000 * tech_factors.get('nox_t_per_mwh', 0)
             total_pm25_tonnes += gwh * 1000 * tech_factors.get('pm25_t_per_mwh', 0)
        print(f"  - Air Quality: SOx {total_sox_tonnes:.0f} t, NOx {total_nox_tonnes:.0f} t, PM2.5 {total_pm25_tonnes:.0f} t")
        return {'sox_tonnes': total_sox_tonnes, 'nox_tonnes': total_nox_tonnes, 'pm25_tonnes': total_pm25_tonnes}

    def _calculate_water_energy_nexus(self, generation_mix_gwh, capacity_details_mw, water_factors):
        # Placeholder: Calculate water withdrawal and consumption.
        total_withdrawal_m3 = 0
        total_consumption_m3 = 0
        for tech, gwh in generation_mix_gwh.items():
             tech_factors = water_factors.get(tech, {})
             # Factors might be per MWh generated or per MW capacity installed (especially for hydro)
             total_withdrawal_m3 += gwh * 1000 * tech_factors.get('withdrawal_m3_per_mwh', 0)
             total_consumption_m3 += gwh * 1000 * tech_factors.get('consumption_m3_per_mwh', 0)
        print(f"  - Water Nexus: Withdrawal {total_withdrawal_m3 / 1e6:.1f} Mm3, Consumption {total_consumption_m3 / 1e6:.1f} Mm3")
        return {'water_withdrawal_million_m3': total_withdrawal_m3 / 1e6, 'water_consumption_million_m3': total_consumption_m3 / 1e6}

    def _calculate_land_use_impacts(self, capacity_details_mw, land_use_factors):
        # Placeholder: Calculate total land area occupied by generation facilities.
        total_land_use_sqkm = 0
        for tech, mw in capacity_details_mw.items():
             factor = land_use_factors.get(tech, {}).get('sqkm_per_mw', 0)
             total_land_use_sqkm += mw * factor
        print(f"  - Land Use: Total {total_land_use_sqkm:.1f} sqkm")
        return {'total_land_use_sqkm': total_land_use_sqkm}

    def _calculate_waste_management(self, generation_mix_gwh, waste_factors):
        # Placeholder: Calculate coal ash, nuclear waste, end-of-life panels/batteries.
        coal_ash_tonnes = 0
        nuclear_waste_tonnes = 0 # Placeholder for spent fuel etc.
        for tech, gwh in generation_mix_gwh.items():
             tech_factors = waste_factors.get(tech, {})
             coal_ash_tonnes += gwh * 1000 * tech_factors.get('coal_ash_t_per_mwh', 0)
             # Add other waste streams (solar panels, batteries based on retirement/replacement)
        print(f"  - Waste Management: Coal Ash {coal_ash_tonnes:.0f} t")
        return {'coal_ash_tonnes': coal_ash_tonnes, 'nuclear_waste_tonnes': nuclear_waste_tonnes}

    def calculate_impacts(self, year, generation_dispatch_results, technology_parameters, mitigation_measures):
        """
        Calculates environmental footprints and mitigation effects for the year.

        Args:
            year (int): The simulation year.
            generation_dispatch_results (dict): Output from GenerationPortfolioModel.simulate_dispatch,
                                                containing 'generation_mix_gwh' and 'capacity_details'.
            technology_parameters (dict): Parameters of the current generation fleet.
            mitigation_measures (dict): Status of deployed mitigation tech (e.g., CCS readiness).

        Returns:
            dict: Summary of environmental impacts for the year.
        """
        print(f"Calculating environmental impacts for year {year}...")

        generation_mix_gwh = generation_dispatch_results.get('generation_mix_gwh', {})
        capacity_details_mw = generation_dispatch_results.get('capacity_details', {})

        # Apply mitigation effects to factors (simplified example)
        # In reality, this would adjust factors based on installed mitigation tech (FGD, SCR, CCS etc.)
        mitigated_emission_factors = self.emission_factors.copy() # Start with base factors
        # Example: If CCS is active on coal, reduce its CO2 factor
        if mitigation_measures.get('ccs_on_coal', False):
             if 'coal' in mitigated_emission_factors:
                 mitigated_emission_factors['coal']['co2eq_t_per_mwh'] *= (1 - self.mitigation_params.get('ccs_capture_rate', 0.9))

        # Calculate impacts for each category
        ghg_results = self._calculate_ghg_emissions(generation_mix_gwh, mitigated_emission_factors)
        air_quality_results = self._calculate_air_quality_impacts(generation_mix_gwh, mitigated_emission_factors)
        water_results = self._calculate_water_energy_nexus(generation_mix_gwh, capacity_details_mw, self.water_factors)
        land_use_results = self._calculate_land_use_impacts(capacity_details_mw, self.land_use_factors)
        waste_results = self._calculate_waste_management(generation_mix_gwh, self.waste_factors)

        # Combine results
        environmental_summary = {
            'ghg_emissions': ghg_results,
            'air_quality': air_quality_results,
            'water_nexus': water_results,
            'land_use': land_use_results,
            'waste_management': waste_results
        }

        print(f"Environmental impact calculation complete for {year}.")
        # Return structure similar to placeholder in main_simulation for now
        # return {
        #     "total_co2_emissions": ghg_results['total_co2eq_tonnes'] / 1e6, # Million tonnes CO2eq
        #     "pm25_emissions": air_quality_results['pm25_tonnes'] / 1e3, # Thousand tonnes
        #     "water_withdrawal": water_results['water_withdrawal_million_m3'],
        #     "land_use": land_use_results['total_land_use_sqkm']
        # }
        return environmental_summary # Return detailed summary

    # Add methods for lifecycle assessment, biodiversity impacts later 