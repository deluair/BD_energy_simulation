import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json # Keep for printing examples if needed

class EnergyResultsAnalyzer:
    """Analyze and visualize energy simulation results."""
    def __init__(self, results_data):
        """
        Initialize the analyzer with simulation results.
        Args:
            results_data (dict): The output dictionary from BangladeshEnergySimulation.run_simulation.
                                 Expected structure: {scenario_name: [yearly_results_list]}
        """
        if not isinstance(results_data, dict) or not results_data:
             raise ValueError("Invalid results_data format. Expected a non-empty dictionary.")
        self.results = results_data
        self.processed_data = self._process_results_to_dataframe()
        print(f"EnergyResultsAnalyzer initialized with results for scenarios: {list(results_data.keys())}")

    def _process_results_to_dataframe(self):
        """
        Processes the raw list-of-dicts results into pandas DataFrames for easier analysis.
        Returns:
            dict: A dictionary where keys are scenario names and values are pandas DataFrames
                  containing the yearly simulation results, flattened.
        """
        processed = {}
        for scenario, yearly_results_list in self.results.items():
            if not yearly_results_list:
                print(f"Warning: Scenario '{scenario}' has no results.")
                processed[scenario] = pd.DataFrame()
                continue
            # Use json_normalize for flattening the nested dictionaries
            try:
                df = pd.json_normalize(yearly_results_list, sep='_')
                # Ensure 'year' column exists and set as index
                if 'year' in df.columns:
                    df['year'] = pd.to_numeric(df['year']) # Ensure year is numeric
                    df = df.set_index('year')
                else:
                     print(f"Warning: 'year' column not found for scenario '{scenario}'. Index not set.")
                processed[scenario] = df
            except Exception as e:
                print(f"Error processing results for scenario '{scenario}': {e}")
                processed[scenario] = pd.DataFrame() # Assign empty df on error

        return processed

    def get_scenario_dataframe(self, scenario='baseline'):
        """Access the processed DataFrame for a specific scenario."""
        if scenario not in self.processed_data:
            print(f"Error: Processed data for scenario '{scenario}' not found.")
            return None
        return self.processed_data[scenario]

    def generate_energy_security_metrics(self, scenario='baseline'):
        """
        Calculate energy security indicators for a given scenario.
        Args:
            scenario (str): The name of the scenario to analyze.
        Returns:
            dict: Calculated energy security metrics over time.
        """
        print(f"Generating energy security metrics for scenario: {scenario}...")
        if scenario not in self.results:
            print(f"Error: Scenario '{scenario}' not found in results.")
            return None

        yearly_metrics = []
        for year_data in self.results[scenario]:
            # Placeholder calculations - needs actual data fields
            import_dependency = year_data.get('fuel', {}).get('import_share', 0.5) # Example
            reserve_margin = year_data.get('generation', {}).get('reserve_margin', 0.15) # Example
            yearly_metrics.append({
                'year': year_data['year'],
                'import_dependency': import_dependency,
                'reserve_margin': reserve_margin
            })

        print("Energy security metrics generated.")
        return {scenario: yearly_metrics}

    def analyze_transition_pathways(self, scenario='baseline'):
        """
        Assess energy transition trajectories (e.g., generation mix, emissions).
        Args:
            scenario (str): The name of the scenario to analyze.
        Returns:
            dict: Analysis of transition pathways over time.
        """
        print(f"Analyzing transition pathways for scenario: {scenario}...")
        if scenario not in self.results:
            print(f"Error: Scenario '{scenario}' not found in results.")
            return None

        pathway_data = []
        for year_data in self.results[scenario]:
            # Placeholder calculations
            generation_mix = year_data.get('generation', {}).get('mix', {'gas': 0.6, 'coal': 0.3, 'renewables': 0.1}) # Example
            emissions = year_data.get('environmental_impact', {}).get('total_co2_emissions', 0)
            renewable_share = generation_mix.get('renewables', 0)
            pathway_data.append({
                'year': year_data['year'],
                'generation_mix': generation_mix,
                'total_co2_emissions': emissions,
                'renewable_share': renewable_share
            })

        print("Transition pathway analysis complete.")
        return {scenario: pathway_data}

    def create_dashboard_data(self, scenario='baseline'):
        """
        Prepare data formatted for dashboard visualization.
        (Actual dashboard creation would use libraries like Dash/Plotly).
        Args:
            scenario (str): The name of the scenario to prepare data for.
        Returns:
            dict: Data structured for visualization components.
        """
        print(f"Preparing dashboard data for scenario: {scenario}...")
        # Placeholder: Combine results into structures suitable for plotting
        security_metrics = self.generate_energy_security_metrics(scenario)
        transition_analysis = self.analyze_transition_pathways(scenario)

        if not security_metrics or not transition_analysis:
            return None

        dashboard_data = {
            'scenario': scenario,
            'security_trends': security_metrics[scenario],
            'transition_trends': transition_analysis[scenario]
            # Add other processed data sections here
        }
        print("Dashboard data prepared.")
        return dashboard_data

    # --- Plotting Methods --- 

    def plot_generation_mix(self, scenario='baseline'):
        """Generate plot of generation mix (GWh) over time."""
        df = self.get_scenario_dataframe(scenario)
        if df is None or df.empty:
            return None
        
        # Identify generation mix columns (assuming prefix 'generation_dispatch_generation_mix_gwh_')
        gen_cols = [col for col in df.columns if col.startswith('generation_dispatch_generation_mix_gwh_')]
        if not gen_cols:
            print(f"Warning: No generation mix columns found for scenario '{scenario}'.")
            return None
        
        gen_df = df[gen_cols].copy()
        # Rename columns for clarity
        gen_df.columns = [col.split('_')[-1] for col in gen_cols]

        fig = go.Figure()
        for tech in gen_df.columns:
            fig.add_trace(go.Bar(
                x=gen_df.index, 
                y=gen_df[tech],
                name=tech
            ))
        
        fig.update_layout(
            title=f'Generation Mix by Technology (GWh) - {scenario}',
            xaxis_title='Year',
            yaxis_title='Generation (GWh)',
            barmode='stack'
        )
        return fig

    def plot_installed_capacity(self, scenario='baseline'):
        """Generate plot of installed capacity (MW) over time."""
        df = self.get_scenario_dataframe(scenario)
        if df is None or df.empty:
            return None
        
        # Identify capacity columns (assuming prefix 'start_of_year_capacity_')
        cap_cols = [col for col in df.columns if col.startswith('start_of_year_capacity_')]
        if not cap_cols:
             # Fallback: Try finding capacity from generation dispatch results
             cap_cols = [col for col in df.columns if col.startswith('generation_dispatch_capacity_details_')]
             if not cap_cols:
                 print(f"Warning: No capacity columns found for scenario '{scenario}'.")
                 return None
             # Rename based on fallback structure
             cap_df = df[cap_cols].copy()
             cap_df.columns = [col.split('_')[-1] for col in cap_cols]
        else:
            # Rename based on primary structure
            cap_df = df[cap_cols].copy()
            cap_df.columns = [col.split('_')[-1] for col in cap_cols]
            

        fig = go.Figure()
        for tech in cap_df.columns:
             fig.add_trace(go.Scatter(
                 x=cap_df.index, 
                 y=cap_df[tech],
                 mode='lines+markers', 
                 name=tech,
                 stackgroup='one' # Create stacked area chart
             ))
        
        fig.update_layout(
            title=f'Installed Capacity by Technology (MW) - {scenario}',
            xaxis_title='Year',
            yaxis_title='Capacity (MW)'
        )
        return fig

    def plot_emissions(self, scenario='baseline'):
        """Generate plot of CO2 emissions over time."""
        df = self.get_scenario_dataframe(scenario)
        if df is None or df.empty or 'environmental_impact_ghg_emissions_total_co2eq_tonnes' not in df.columns:
            print(f"Warning: CO2 emission data not found for scenario '{scenario}'.")
            return None

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['environmental_impact_ghg_emissions_total_co2eq_tonnes'] / 1e6, # Convert to Million Tonnes
            mode='lines+markers',
            name='Total CO2eq Emissions'
        ))
        fig.update_layout(
            title=f'Total GHG Emissions (Million Tonnes CO2eq) - {scenario}',
            xaxis_title='Year',
            yaxis_title='Emissions (Mt CO2eq)'
        )
        return fig

    def plot_access_rates(self, scenario='baseline'):
        """Generate plot of electricity access rates over time."""
        df = self.get_scenario_dataframe(scenario)
        if df is None or df.empty:
            return None
        
        access_cols = {
            'National': 'energy_access_aggregate_access_rates_national',
            'Urban': 'energy_access_aggregate_access_rates_urban',
            'Rural': 'energy_access_aggregate_access_rates_rural'
        }
        
        fig = go.Figure()
        for name, col in access_cols.items():
            if col in df.columns:
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df[col] * 100, # Convert to percentage
                    mode='lines+markers',
                    name=name
                ))
            else:
                print(f"Warning: Access rate column '{col}' not found for scenario '{scenario}'.")

        fig.update_layout(
            title=f'Electricity Access Rates (%) - {scenario}',
            xaxis_title='Year',
            yaxis_title='Access Rate (%)',
            yaxis_range=[df[access_cols['Rural']].min()*99 if access_cols['Rural'] in df else 90, 101] # Adjust range
        )
        return fig

    def plot_investment_gap(self, scenario='baseline'):
        """Generate plot of energy investment needs vs mobilized funds."""
        df = self.get_scenario_dataframe(scenario)
        if df is None or df.empty:
            return None
        
        needs_col = 'finance_investment_needs_total_investment_needs_m_usd'
        mobilized_col = 'finance_total_investment_mobilized_m_usd'
        gap_col = 'finance_financing_gap_m_usd'
        
        if not all(c in df.columns for c in [needs_col, mobilized_col, gap_col]):
            print(f"Warning: Investment data columns not found for scenario '{scenario}'.")
            return None

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df.index, y=df[mobilized_col], name='Mobilized Investment'))
        # Use scatter for needs to show the target line clearly
        fig.add_trace(go.Scatter(x=df.index, y=df[needs_col], mode='lines+markers', name='Investment Needs', line=dict(dash='dash')))
        # Optional: Plot the gap as a separate bar or line
        fig.add_trace(go.Bar(x=df.index, y=df[gap_col], name='Financing Gap', marker_color='red'))
        
        fig.update_layout(
            title=f'Energy Sector Investment (Million USD) - {scenario}',
            xaxis_title='Year',
            yaxis_title='Investment (Million USD)',
            barmode='group'
        )
        return fig

    # --- HTML Report Generation --- 

    def generate_html_report(self, scenario='baseline', output_dir='results'):
        """
        Generates an HTML report summarizing simulation results for a scenario,
        including embedded plots.

        Args:
            scenario (str): The name of the scenario to report.
            output_dir (str): The directory to save the report file in.

        Returns:
            str: The path to the generated HTML file, or None if failed.
        """
        print(f"Generating HTML report for scenario: {scenario}...")
        df = self.get_scenario_dataframe(scenario)
        if df is None or df.empty:
            print(f"Error: No data found for scenario '{scenario}'. Cannot generate report.")
            return None

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        report_filename = f"simulation_report_{scenario}.html"
        report_path = os.path.join(output_dir, report_filename)

        # Generate plots
        fig_gen_mix = self.plot_generation_mix(scenario)
        fig_capacity = self.plot_installed_capacity(scenario)
        fig_emissions = self.plot_emissions(scenario)
        fig_access = self.plot_access_rates(scenario)
        fig_investment = self.plot_investment_gap(scenario)

        # --- Assemble HTML --- 
        html_content = f"""\
<!DOCTYPE html>
<html>
<head>
    <title>Bangladesh Energy Simulation Report - {scenario}</title>
    <style>
        body {{ font-family: sans-serif; margin: 20px; }}
        h1, h2 {{ color: #333; }}
        .plot-container {{ margin-bottom: 40px; border: 1px solid #ddd; padding: 10px; }}
    </style>
    <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
</head>
<body>

<h1>Bangladesh Energy Simulation Results</h1>
<h2>Scenario: {scenario}</h2>

<div class="plot-container">
    <h2>Installed Capacity</h2>
    {fig_capacity.to_html(full_html=False, include_plotlyjs='cdn') if fig_capacity else '<p>Capacity plot could not be generated.</p>'}
</div>

<div class="plot-container">
    <h2>Generation Mix</h2>
    {fig_gen_mix.to_html(full_html=False, include_plotlyjs='cdn') if fig_gen_mix else '<p>Generation mix plot could not be generated.</p>'}
</div>

<div class="plot-container">
    <h2>GHG Emissions</h2>
    {fig_emissions.to_html(full_html=False, include_plotlyjs='cdn') if fig_emissions else '<p>Emissions plot could not be generated.</p>'}
</div>

<div class="plot-container">
    <h2>Electricity Access Rates</h2>
    {fig_access.to_html(full_html=False, include_plotlyjs='cdn') if fig_access else '<p>Access rates plot could not be generated.</p>'}
</div>

<div class="plot-container">
    <h2>Energy Sector Investment</h2>
    {fig_investment.to_html(full_html=False, include_plotlyjs='cdn') if fig_investment else '<p>Investment plot could not be generated.</p>'}
</div>

</body>
</html>
"""

        # Write HTML to file
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Report successfully saved to {report_path}")
            return report_path
        except Exception as e:
            print(f"Error writing HTML report file: {e}")
            return None

# Example Usage (assumes 'results' dict exists from main_simulation run):
if __name__ == "__main__":
    # Dummy results data matching the expected structure
    dummy_results = {
        'baseline': [
            {'year': 2025, 'fuel': {'import_share': 0.4}, 'generation': {'reserve_margin': 0.2, 'mix': {'gas':0.7,'coal':0.2,'renewables':0.1}}, 'environmental_impact': {'total_co2_emissions': 50}},
            {'year': 2026, 'fuel': {'import_share': 0.45}, 'generation': {'reserve_margin': 0.18, 'mix': {'gas':0.65,'coal':0.2,'renewables':0.15}}, 'environmental_impact': {'total_co2_emissions': 52}}
        ],
        'high_renewables': [
            {'year': 2025, 'fuel': {'import_share': 0.35}, 'generation': {'reserve_margin': 0.22, 'mix': {'gas':0.6,'coal':0.1,'renewables':0.3}}, 'environmental_impact': {'total_co2_emissions': 45}},
            {'year': 2026, 'fuel': {'import_share': 0.38}, 'generation': {'reserve_margin': 0.20, 'mix': {'gas':0.55,'coal':0.05,'renewables':0.4}}, 'environmental_impact': {'total_co2_emissions': 42}}
        ]
    }

    analyzer = EnergyResultsAnalyzer(dummy_results)

    security = analyzer.generate_energy_security_metrics('baseline')
    print("\nSecurity Metrics (Baseline):")
    print(json.dumps(security, indent=2))

    transition = analyzer.analyze_transition_pathways('high_renewables')
    print("\nTransition Pathway (High Renewables):")
    print(json.dumps(transition, indent=2))

    dash_data = analyzer.create_dashboard_data('baseline')
    print("\nDashboard Data Structure (Baseline):")
    print(json.dumps(dash_data, indent=2))

    report_file = analyzer.generate_html_report(scenario='baseline')
    print(f"Report generated: {report_file}")

    report_file_hr = analyzer.generate_html_report(scenario='high_renewables')
    print(f"Report generated: {report_file_hr}") 