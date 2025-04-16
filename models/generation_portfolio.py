import pandas as pd # Assuming parameters might be in DataFrames

class GenerationPortfolioModel:
    """Model power generation mix and capacity evolution"""
    def __init__(self, base_year_capacity, technology_parameters,
                 expansion_pipeline, retirement_schedule,
                 dispatch_merit_order, operational_constraints):
        """
        Initializes the generation portfolio.

        Args:
            base_year_capacity (dict): Capacity (e.g., MW) per technology type in the base year.
                                       Example: {'gas': 10000, 'coal': 5000, 'solar': 500}
            technology_parameters (dict): Detailed parameters for each technology.
                                          Example: {'gas': {'efficiency': 0.5, 'ramp_rate': ..., 'min_load': ...}, ...}
            expansion_pipeline (list): List of planned capacity additions.
                                       Example: [{'year': 2026, 'tech': 'solar', 'capacity': 500}, ...]
            retirement_schedule (list): List of planned capacity retirements.
                                        Example: [{'year': 2028, 'tech': 'gas', 'plant_id': 'old_gas_1', 'capacity': 100}, ...]
            dispatch_merit_order (list): Order of technologies for economic dispatch.
                                         Example: ['nuclear', 'hydro', 'solar', 'wind', 'gas_cc', 'coal', 'gas_oc', 'liquid']
            operational_constraints (dict): System-wide or technology-specific constraints.
                                            Example: {'min_gas_take': ..., 'max_coal_utilization': ...}
        """
        self.current_capacity = base_year_capacity.copy() # Active capacity in the current simulation year
        self.technology_parameters = technology_parameters
        # Convert pipeline/retirement schedules for easier lookup (e.g., DataFrame or dict keyed by year)
        self.expansion_pipeline_df = pd.DataFrame(expansion_pipeline)
        self.retirement_schedule_df = pd.DataFrame(retirement_schedule)
        self.dispatch_merit_order = dispatch_merit_order
        self.operational_constraints = operational_constraints
        self.detailed_fleet = self._initialize_detailed_fleet(base_year_capacity, technology_parameters)

        print(f"GenerationPortfolioModel initialized with base capacity: {self.current_capacity}")

    def _initialize_detailed_fleet(self, base_capacity, tech_params):
        # Placeholder: In a real model, this would represent individual plants/units
        # with their specific parameters (age, efficiency, location etc.)
        # For now, aggregate by technology type.
        fleet = {}
        for tech, capacity in base_capacity.items():
             fleet[tech] = {
                 'total_capacity': capacity,
                 'parameters': tech_params.get(tech, {})
                 # Add more details like number of units, average age etc. later
             }
        return fleet

    def update_capacity(self, year):
        """
        Updates the current generation capacity based on expansion and retirement schedules for the given year.

        Args:
            year (int): The simulation year for which to update capacity.
        """
        print(f"Updating capacity for year {year}...")

        # Add new capacity from expansion pipeline
        expansions_this_year = self.expansion_pipeline_df[self.expansion_pipeline_df['year'] == year]
        for _, project in expansions_this_year.iterrows():
            tech = project['tech']
            capacity_addition = project['capacity']
            self.current_capacity[tech] = self.current_capacity.get(tech, 0) + capacity_addition
            # Update detailed fleet (simplified)
            if tech in self.detailed_fleet:
                 self.detailed_fleet[tech]['total_capacity'] += capacity_addition
            else:
                 self.detailed_fleet[tech] = {
                     'total_capacity': capacity_addition,
                     'parameters': self.technology_parameters.get(tech, {})
                 }
            print(f"  + Added {capacity_addition} MW of {tech} capacity.")

        # Remove retired capacity
        retirements_this_year = self.retirement_schedule_df[self.retirement_schedule_df['year'] == year]
        for _, retirement in retirements_this_year.iterrows():
            tech = retirement['tech']
            capacity_reduction = retirement['capacity']
            if tech in self.current_capacity:
                self.current_capacity[tech] -= capacity_reduction
                if self.current_capacity[tech] <= 0:
                    del self.current_capacity[tech] # Remove tech if capacity is zero or less
                # Update detailed fleet (simplified)
                if tech in self.detailed_fleet:
                     self.detailed_fleet[tech]['total_capacity'] -= capacity_reduction
                     if self.detailed_fleet[tech]['total_capacity'] <= 0:
                         del self.detailed_fleet[tech]

                print(f"  - Retired {capacity_reduction} MW of {tech} capacity.")
            else:
                print(f"  ! Warning: Attempted to retire {capacity_reduction} MW of {tech}, but no capacity found.")

        print(f"Updated capacity for {year}: {self.current_capacity}")

    def simulate_dispatch(self, year, demand_profile, fuel_conditions, grid_constraints):
        """
        Simulates the generation dispatch to meet demand based on merit order,
        fuel availability, technical constraints, and capacity.

        Args:
            year (int): The simulation year.
            demand_profile (object): Represents the electricity demand (e.g., hourly profile for the year).
            fuel_conditions (dict): Availability and prices of fuels.
            grid_constraints (dict): Constraints from the grid model (e.g., transmission limits).

        Returns:
            dict: Dispatch results, including generation mix, costs, unserved energy, etc.
        """
        print(f"Simulating dispatch for year {year}...")
        # Placeholder: This requires a sophisticated dispatch model (e.g., unit commitment/economic dispatch)
        # Inputs: self.current_capacity, self.dispatch_merit_order, self.technology_parameters,
        #         self.operational_constraints, demand_profile, fuel_conditions, grid_constraints.
        # Outputs: Generation by tech, variable costs, emissions (if calculated here), curtailment, unserved energy.

        # Simple placeholder logic: Assume total generation meets a target (e.g., demand + reserve)
        # and allocate based purely on available capacity (ignoring merit order, fuel, etc.)
        total_demand = demand_profile.get('total_demand', 100) # Get total demand from profile (e.g., TWh)
        target_generation = total_demand * 1.1 # Assume 10% reserve margin needed

        total_available_capacity = sum(self.current_capacity.values())
        if total_available_capacity == 0:
             return {
                'generation_mix_gwh': {}, # GWh by tech
                'total_generation_gwh': 0,
                'variable_cost': 0,
                'unserved_energy_gwh': target_generation, # Assuming TWh demand needs conversion
                'curtailment_gwh': 0,
             }


        # Extremely simplified generation allocation based on capacity share
        generation_mix_gwh = {}
        generated_gwh = 0
        # Convert TWh demand to GWh for this example
        target_generation_gwh = target_generation * 1000

        for tech in self.dispatch_merit_order:
            if tech in self.current_capacity:
                 # Simplified: Assign generation proportional to capacity share up to the target
                 # In reality, needs simulation over time (e.g. 8760 hours) with capacity factors, ramp rates etc.
                 potential_gen = (self.current_capacity[tech] / total_available_capacity) * target_generation_gwh
                 actual_gen = min(potential_gen, target_generation_gwh - generated_gwh) # Don't exceed target
                 generation_mix_gwh[tech] = actual_gen
                 generated_gwh += actual_gen
                 if generated_gwh >= target_generation_gwh:
                     break

        unserved_energy_gwh = max(0, target_generation_gwh - generated_gwh)

        dispatch_results = {
            'generation_mix_gwh': generation_mix_gwh, # GWh by tech
            'total_generation_gwh': generated_gwh,
            'variable_cost': generated_gwh * 50, # Example cost ($/MWh) -> total $
            'unserved_energy_gwh': unserved_energy_gwh,
             'curtailment_gwh': 0, # Placeholder
             'capacity_details': self.current_capacity.copy() # Snapshot of capacity for this year
        }
        print(f"Dispatch simulation complete for {year}. Total Generation: {generated_gwh:.2f} GWh")
        return dispatch_results

    # Add methods for specific fleet modeling details (aging curves, maintenance) later if needed.

    # Add methods for specific fleet modeling (Natural Gas, Coal, etc.) later 