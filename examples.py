#!/usr/bin/env python3
"""
Example usage of the Lunar Mining and ISRU computational model.

This script demonstrates basic usage of the lunar_mining module
for various ISRU scenarios.
"""

from lunar_mining import (
    LunarRegolith,
    WaterIceExtraction,
    OxygenProduction,
    MiningOperation,
    ISRUFacility
)


def example_1_regolith_analysis():
    """Example 1: Analyze lunar regolith composition."""
    print("=" * 70)
    print("EXAMPLE 1: Regolith Composition Analysis")
    print("=" * 70)
    
    # Create regolith models for different regions
    mare = LunarRegolith(region="mare")
    highland = LunarRegolith(region="highland")
    
    print("\nMare Regolith:")
    print(f"  Oxygen content: {mare.get_oxygen_content():.1f}%")
    print(f"  Iron content: {mare.get_metal_content()['Fe']:.1f}%")
    print(f"  Aluminum content: {mare.get_metal_content()['Al']:.1f}%")
    
    print("\nHighland Regolith:")
    print(f"  Oxygen content: {highland.get_oxygen_content():.1f}%")
    print(f"  Iron content: {highland.get_metal_content()['Fe']:.1f}%")
    print(f"  Aluminum content: {highland.get_metal_content()['Al']:.1f}%")


def example_2_water_extraction():
    """Example 2: Water ice extraction simulation."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Water Ice Extraction")
    print("=" * 70)
    
    # Create water extractor with 5% ice concentration
    extractor = WaterIceExtraction(ice_concentration=5.0)
    
    # Calculate water yield from 1 tonne of regolith
    regolith_mass = 1000  # kg
    water_yield = extractor.calculate_water_yield(regolith_mass)
    energy_needed = extractor.calculate_energy_requirement(water_yield)
    
    print(f"\nExcavating {regolith_mass} kg of ice-bearing regolith:")
    print(f"  Water yield: {water_yield:.1f} kg")
    print(f"  Energy required: {energy_needed:.1f} MJ")
    print(f"  Specific energy: {energy_needed/water_yield:.1f} MJ/kg water")


def example_3_oxygen_production():
    """Example 3: Oxygen production from regolith."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Oxygen Production")
    print("=" * 70)
    
    # Create regolith and oxygen producer
    regolith = LunarRegolith(region="mare")
    oxygen_producer = OxygenProduction(regolith, efficiency=0.75)
    
    # Calculate oxygen production
    regolith_mass = 1000  # kg
    oxygen_yield = oxygen_producer.calculate_oxygen_yield(regolith_mass)
    energy_needed = oxygen_producer.calculate_energy_requirement(oxygen_yield)
    power_10kg_hr = oxygen_producer.calculate_power_requirement(10)
    
    print(f"\nProcessing {regolith_mass} kg of mare regolith:")
    print(f"  Oxygen yield: {oxygen_yield:.1f} kg")
    print(f"  Energy required: {energy_needed:.1f} MJ")
    print(f"  Specific energy: {energy_needed/oxygen_yield:.1f} MJ/kg O2")
    print(f"\nPower for 10 kg/hr production: {power_10kg_hr:.1f} kW")


def example_4_mining_operations():
    """Example 4: Mining operation simulation."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Mining Operations")
    print("=" * 70)
    
    # Create mining operation
    mining_op = MiningOperation(excavation_rate=100)  # kg/hr
    
    # Calculate capacity over different durations
    durations = [1, 8, 24, 168]  # hours
    duration_names = ["1 hour", "8 hours", "1 day", "1 week"]
    
    print(f"\nExcavation rate: {mining_op.excavation_rate} kg/hr")
    print("\nCapacity by duration:")
    
    for duration, name in zip(durations, duration_names):
        volume = mining_op.calculate_excavation_volume(duration)
        mass = mining_op.excavation_rate * duration
        print(f"  {name:10s}: {mass:6.0f} kg ({volume:5.1f} m³)")
    
    # Power requirements
    depth = 1.0  # meters
    power = mining_op.calculate_power_requirement(depth)
    print(f"\nPower required (1m depth): {power:.2f} kW")


def example_5_integrated_facility():
    """Example 5: Integrated ISRU facility simulation."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Integrated ISRU Facility")
    print("=" * 70)
    
    # Create polar facility (has water ice + regolith processing)
    polar_facility = ISRUFacility(region="polar")
    
    # Simulate 24-hour operation with different power levels
    power_levels = [50, 100, 200]
    
    print("\n24-hour operation results:")
    print("-" * 70)
    print("Power (kW) | Regolith (kg) | Water (kg) | Oxygen (kg)")
    print("-" * 70)
    
    for power in power_levels:
        results = polar_facility.simulate_operation(duration=24, power_available=power)
        print(f"   {power:3d}     |    {results['regolith_excavated_kg']:6.0f}   |   "
              f"{results['water_produced_kg']:5.1f}    |   {results['total_oxygen_kg']:6.1f}")


def example_6_mission_scenario():
    """Example 6: Mission scenario with crew requirements."""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Mission Scenario - 4 Person Crew")
    print("=" * 70)
    
    # Crew requirements
    crew_size = 4
    o2_per_person_day = 0.84  # kg
    water_per_person_day = 3.5  # kg
    mission_days = 180
    
    daily_o2_need = crew_size * o2_per_person_day
    daily_water_need = crew_size * water_per_person_day
    
    print(f"\nCrew size: {crew_size} people")
    print(f"Mission duration: {mission_days} days")
    print(f"\nDaily requirements:")
    print(f"  Oxygen: {daily_o2_need:.2f} kg/day")
    print(f"  Water: {daily_water_need:.2f} kg/day")
    
    # Create facility and optimize
    facility = ISRUFacility(region="polar")
    optimized = facility.optimize_production(target_oxygen=daily_o2_need, max_power=100)
    
    print(f"\nISRU facility configuration:")
    print(f"  Required power: {optimized['required_power_kW']:.1f} kW")
    print(f"  Excavation rate: {optimized['excavation_rate_kg_hr']:.1f} kg/hr")
    print(f"  Daily regolith: {optimized['regolith_needed_kg_day']:.1f} kg")
    
    # Calculate total mission requirements
    total_o2 = daily_o2_need * mission_days
    total_water = daily_water_need * mission_days
    total_regolith = optimized['regolith_needed_kg_day'] * mission_days
    
    print(f"\nTotal mission requirements:")
    print(f"  Total oxygen: {total_o2:.1f} kg")
    print(f"  Total water: {total_water:.1f} kg")
    print(f"  Total regolith: {total_regolith/1000:.1f} tonnes")
    
    # Economic analysis
    earth_launch_cost = 10000  # $/kg to lunar surface
    resupply_mass = total_o2 + total_water
    resupply_cost = resupply_mass * earth_launch_cost
    
    facility_mass = 5000  # kg (estimated)
    facility_cost = facility_mass * earth_launch_cost
    
    savings = resupply_cost - facility_cost
    
    print(f"\nEconomic analysis:")
    print(f"  Earth resupply cost: ${resupply_cost/1e6:.1f}M")
    print(f"  ISRU facility cost: ${facility_cost/1e6:.1f}M")
    print(f"  Net savings: ${savings/1e6:.1f}M")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("LUNAR MINING AND ISRU - EXAMPLE SCENARIOS")
    print("=" * 70)
    
    example_1_regolith_analysis()
    example_2_water_extraction()
    example_3_oxygen_production()
    example_4_mining_operations()
    example_5_integrated_facility()
    example_6_mission_scenario()
    
    print("\n" + "=" * 70)
    print("All examples completed successfully!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
