"""
Lunar Mining and ISRU (In-Situ Resource Utilization) Computational Model

This module provides computational models for:
- Lunar regolith composition and properties
- Mining operation simulations
- ISRU resource extraction processes
- Energy and resource efficiency calculations
"""

import numpy as np
from typing import Dict, Tuple, Optional
import matplotlib.pyplot as plt


# Physical Constants
LUNAR_GRAVITY = 1.62  # m/s^2
EARTH_GRAVITY = 9.81  # m/s^2
LUNAR_DAY = 29.5 * 24 * 3600  # seconds (Earth days)
LUNAR_NIGHT_TEMP = 100  # Kelvin (approximate)
LUNAR_DAY_TEMP = 400  # Kelvin (approximate)


class LunarRegolith:
    """
    Model for lunar regolith composition and properties.
    
    Based on Apollo mission data and remote sensing observations.
    """
    
    def __init__(self, region: str = "mare"):
        """
        Initialize regolith model for a specific lunar region.
        
        Args:
            region: 'mare' (dark plains) or 'highland' (brighter terrain)
        """
        self.region = region
        self.composition = self._initialize_composition()
        self.density = 1500  # kg/m^3 (average bulk density)
        self.grain_size = 70e-6  # meters (average grain size)
        
    def _initialize_composition(self) -> Dict[str, float]:
        """
        Initialize chemical composition by weight percentage.
        
        Returns:
            Dictionary of element/compound percentages
        """
        if self.region == "mare":
            # Mare basalt composition (approximate)
            return {
                'SiO2': 45.0,
                'Al2O3': 14.0,
                'FeO': 18.0,
                'MgO': 9.0,
                'CaO': 11.0,
                'TiO2': 3.0,
                'O2_available': 43.0,  # Oxygen in oxides
            }
        else:  # highland
            # Highland anorthosite composition (approximate)
            return {
                'SiO2': 45.0,
                'Al2O3': 24.0,
                'FeO': 6.0,
                'MgO': 7.0,
                'CaO': 16.0,
                'TiO2': 0.5,
                'O2_available': 44.0,
            }
    
    def get_oxygen_content(self) -> float:
        """
        Calculate available oxygen content in regolith.
        
        Returns:
            Oxygen content as weight percentage
        """
        return self.composition['O2_available']
    
    def get_metal_content(self) -> Dict[str, float]:
        """
        Calculate extractable metal content.
        
        Returns:
            Dictionary of metal percentages
        """
        # Simplified metal extraction potential
        return {
            'Fe': self.composition['FeO'] * 0.78,  # Iron from FeO
            'Al': self.composition['Al2O3'] * 0.53,  # Aluminum from Al2O3
            'Mg': self.composition['MgO'] * 0.60,  # Magnesium from MgO
            'Si': self.composition['SiO2'] * 0.47,  # Silicon from SiO2
            'Ti': self.composition['TiO2'] * 0.60,  # Titanium from TiO2
        }


class WaterIceExtraction:
    """
    Model for water ice extraction from polar permanently shadowed regions.
    """
    
    def __init__(self, ice_concentration: float = 5.0):
        """
        Initialize water ice extraction model.
        
        Args:
            ice_concentration: Water ice percentage by weight (0-30%)
        """
        self.ice_concentration = min(ice_concentration, 30.0)  # Max 30% observed
        self.extraction_efficiency = 0.8  # 80% extraction efficiency
        
    def calculate_water_yield(self, regolith_mass: float) -> float:
        """
        Calculate water yield from excavated regolith.
        
        Args:
            regolith_mass: Mass of excavated regolith (kg)
            
        Returns:
            Water yield (kg)
        """
        ice_mass = regolith_mass * (self.ice_concentration / 100.0)
        water_yield = ice_mass * self.extraction_efficiency
        return water_yield
    
    def calculate_energy_requirement(self, water_yield: float) -> float:
        """
        Calculate energy required for extraction.
        
        Args:
            water_yield: Desired water yield (kg)
            
        Returns:
            Energy requirement (MJ)
        """
        # Energy for:
        # 1. Heating regolith from 100K to 273K
        # 2. Sublimating ice
        # 3. Condensing water vapor
        
        heat_regolith = 0.8  # kJ/kg/K (specific heat of regolith)
        latent_heat_ice = 2834  # kJ/kg (sublimation enthalpy)
        temp_rise = 173  # K (100K to 273K)
        
        # Account for extraction efficiency
        ice_needed = water_yield / self.extraction_efficiency
        regolith_needed = ice_needed / (self.ice_concentration / 100.0)
        
        heating_energy = regolith_needed * heat_regolith * temp_rise / 1000  # MJ
        sublimation_energy = ice_needed * latent_heat_ice / 1000  # MJ
        
        total_energy = heating_energy + sublimation_energy
        return total_energy


class OxygenProduction:
    """
    Model for oxygen production from lunar regolith using ISRU processes.
    
    Primary method: Molten regolith electrolysis
    """
    
    def __init__(self, regolith: LunarRegolith, efficiency: float = 0.75):
        """
        Initialize oxygen production model.
        
        Args:
            regolith: LunarRegolith object
            efficiency: Production efficiency (0-1)
        """
        self.regolith = regolith
        self.efficiency = efficiency
        
    def calculate_oxygen_yield(self, regolith_mass: float) -> float:
        """
        Calculate oxygen production from regolith.
        
        Args:
            regolith_mass: Mass of processed regolith (kg)
            
        Returns:
            Oxygen yield (kg)
        """
        oxygen_content = self.regolith.get_oxygen_content() / 100.0
        theoretical_yield = regolith_mass * oxygen_content
        actual_yield = theoretical_yield * self.efficiency
        return actual_yield
    
    def calculate_energy_requirement(self, oxygen_yield: float) -> float:
        """
        Calculate energy required for oxygen production.
        
        Args:
            oxygen_yield: Desired oxygen yield (kg)
            
        Returns:
            Energy requirement (MJ)
        """
        # Molten regolith electrolysis
        # Energy = heating to 1600°C + electrolysis
        
        regolith_needed = oxygen_yield / (self.efficiency * 
                                          self.regolith.get_oxygen_content() / 100.0)
        
        # Heating energy
        specific_heat = 0.8  # kJ/kg/K
        melting_temp = 1873  # K (1600°C)
        start_temp = 250  # K (average lunar surface)
        latent_heat = 400  # kJ/kg (melting)
        
        heating_energy = regolith_needed * specific_heat * (melting_temp - start_temp) / 1000  # MJ
        melting_energy = regolith_needed * latent_heat / 1000  # MJ
        
        # Electrolysis energy (approximate)
        electrolysis_energy = oxygen_yield * 15  # MJ/kg O2
        
        total_energy = heating_energy + melting_energy + electrolysis_energy
        return total_energy
    
    def calculate_power_requirement(self, oxygen_rate: float) -> float:
        """
        Calculate continuous power requirement.
        
        Args:
            oxygen_rate: Oxygen production rate (kg/hour)
            
        Returns:
            Power requirement (kW)
        """
        energy_per_kg = self.calculate_energy_requirement(1.0)  # MJ per kg
        power_kw = (energy_per_kg * oxygen_rate) / 3.6  # Convert to kW
        return power_kw


class MiningOperation:
    """
    Model for lunar mining operations including excavation and material handling.
    """
    
    def __init__(self, excavation_rate: float = 100.0):
        """
        Initialize mining operation model.
        
        Args:
            excavation_rate: Rate of excavation (kg/hour)
        """
        self.excavation_rate = excavation_rate
        self.regolith_density = 1500  # kg/m^3
        
    def calculate_excavation_volume(self, duration: float) -> float:
        """
        Calculate volume of regolith excavated.
        
        Args:
            duration: Operation duration (hours)
            
        Returns:
            Volume excavated (m^3)
        """
        mass_excavated = self.excavation_rate * duration
        volume = mass_excavated / self.regolith_density
        return volume
    
    def calculate_power_requirement(self, depth: float = 1.0) -> float:
        """
        Calculate power required for excavation.
        
        Args:
            depth: Average excavation depth (meters)
            
        Returns:
            Power requirement (kW)
        """
        # Power = work rate = force × velocity
        # Simplified model based on cutting resistance
        
        cutting_resistance = 50  # kPa (soil cutting resistance)
        bucket_area = 0.1  # m^2 (excavator bucket area)
        cutting_speed = (self.excavation_rate / self.regolith_density) / 3600  # m^3/s
        
        # Mechanical power
        mechanical_power = cutting_resistance * 1000 * bucket_area * cutting_speed / 1000  # kW
        
        # Account for lifting against lunar gravity
        lifting_power = (self.excavation_rate / 3600) * LUNAR_GRAVITY * depth / 1000  # kW
        
        # System efficiency
        efficiency = 0.6
        total_power = (mechanical_power + lifting_power) / efficiency
        
        return total_power


class ISRUFacility:
    """
    Integrated ISRU facility model combining all processes.
    """
    
    def __init__(self, region: str = "polar"):
        """
        Initialize ISRU facility.
        
        Args:
            region: Location ('polar' for ice, 'mare' or 'highland' for regolith processing)
        """
        self.region = region
        
        if region == "polar":
            self.water_extractor = WaterIceExtraction(ice_concentration=5.0)
            self.regolith = LunarRegolith("mare")
        else:
            self.regolith = LunarRegolith(region)
            self.water_extractor = None
            
        self.oxygen_producer = OxygenProduction(self.regolith)
        self.mining_op = MiningOperation(excavation_rate=100.0)
        
    def simulate_operation(self, duration: float, power_available: float) -> Dict[str, float]:
        """
        Simulate ISRU facility operation over time.
        
        Args:
            duration: Operation duration (hours)
            power_available: Available power (kW)
            
        Returns:
            Dictionary with production metrics
        """
        results = {
            'duration_hours': duration,
            'power_available_kW': power_available,
            'regolith_excavated_kg': 0,
            'water_produced_kg': 0,
            'oxygen_produced_kg': 0,
            'power_utilization': 0,
        }
        
        # Calculate mining capacity
        mining_power = self.mining_op.calculate_power_requirement()
        
        if mining_power > power_available:
            # Power-limited operation
            regolith_mass = (power_available / mining_power) * self.mining_op.excavation_rate * duration
        else:
            regolith_mass = self.mining_op.excavation_rate * duration
            
        results['regolith_excavated_kg'] = regolith_mass
        
        # Water production (if polar region)
        if self.water_extractor:
            water_yield = self.water_extractor.calculate_water_yield(regolith_mass)
            results['water_produced_kg'] = water_yield
            
            # Electrolysis: split water into H2 and O2
            # H2O -> H2 + O2 (mass ratio 2:16, so 88.9% of water mass is O2)
            results['oxygen_from_water_kg'] = water_yield * 0.889
        
        # Oxygen production from regolith
        oxygen_from_regolith = self.oxygen_producer.calculate_oxygen_yield(regolith_mass * 0.5)
        results['oxygen_produced_kg'] = oxygen_from_regolith
        
        # Total oxygen
        if self.water_extractor:
            results['total_oxygen_kg'] = results['oxygen_from_water_kg'] + oxygen_from_regolith
        else:
            results['total_oxygen_kg'] = oxygen_from_regolith
            
        # Calculate actual power usage
        total_power_needed = mining_power
        if total_power_needed > 0:
            results['power_utilization'] = min(1.0, power_available / total_power_needed)
        
        return results
    
    def optimize_production(self, target_oxygen: float, max_power: float) -> Dict[str, float]:
        """
        Optimize operation to meet oxygen production target.
        
        Args:
            target_oxygen: Target oxygen production (kg/day)
            max_power: Maximum available power (kW)
            
        Returns:
            Optimized operation parameters
        """
        # Iterative optimization to find best configuration
        hours_per_day = 24
        
        results = self.simulate_operation(hours_per_day, max_power)
        
        scale_factor = target_oxygen / results['total_oxygen_kg'] if results['total_oxygen_kg'] > 0 else 1.0
        
        optimized = {
            'required_power_kW': max_power * scale_factor,
            'excavation_rate_kg_hr': self.mining_op.excavation_rate * scale_factor,
            'oxygen_production_kg_day': target_oxygen,
            'regolith_needed_kg_day': results['regolith_excavated_kg'] * scale_factor,
            'scale_factor': scale_factor,
        }
        
        return optimized


def visualize_production_rates(facility: ISRUFacility, duration_days: int = 30):
    """
    Visualize ISRU production over time.
    
    Args:
        facility: ISRUFacility instance
        duration_days: Simulation duration (days)
    """
    days = np.arange(0, duration_days + 1)
    water_production = []
    oxygen_production = []
    power_required = []
    
    for day in days:
        results = facility.simulate_operation(24, power_available=100)
        water_production.append(results.get('water_produced_kg', 0) * day)
        oxygen_production.append(results['total_oxygen_kg'] * day)
        power_required.append(facility.mining_op.calculate_power_requirement())
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Production over time
    ax1.plot(days, oxygen_production, 'b-', label='Oxygen', linewidth=2)
    if facility.water_extractor:
        ax1.plot(days, water_production, 'c--', label='Water', linewidth=2)
    ax1.set_xlabel('Time (days)')
    ax1.set_ylabel('Cumulative Production (kg)')
    ax1.set_title('ISRU Production Over Time')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Power requirements
    processes = ['Mining', 'Water\nExtraction', 'Oxygen\nProduction']
    powers = [
        facility.mining_op.calculate_power_requirement(),
        50 if facility.water_extractor else 0,
        facility.oxygen_producer.calculate_power_requirement(10)
    ]
    
    ax2.bar(processes, powers, color=['brown', 'cyan', 'blue'])
    ax2.set_ylabel('Power Requirement (kW)')
    ax2.set_title('Process Power Requirements')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig


if __name__ == "__main__":
    # Example usage
    print("=== Lunar Mining and ISRU Simulation ===\n")
    
    # Create ISRU facility at polar region
    facility = ISRUFacility(region="polar")
    
    # Simulate 24-hour operation
    results = facility.simulate_operation(duration=24, power_available=100)
    
    print("24-Hour Operation Results:")
    print(f"  Regolith Excavated: {results['regolith_excavated_kg']:.1f} kg")
    print(f"  Water Produced: {results.get('water_produced_kg', 0):.1f} kg")
    print(f"  Oxygen Produced: {results['total_oxygen_kg']:.1f} kg")
    print(f"  Power Utilization: {results['power_utilization']*100:.1f}%")
    
    # Optimization example
    print("\n=== Optimization for 100 kg O2/day ===")
    optimized = facility.optimize_production(target_oxygen=100, max_power=100)
    print(f"  Required Power: {optimized['required_power_kW']:.1f} kW")
    print(f"  Excavation Rate: {optimized['excavation_rate_kg_hr']:.1f} kg/hr")
    print(f"  Daily Regolith: {optimized['regolith_needed_kg_day']:.1f} kg")
