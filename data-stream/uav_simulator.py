#!/usr/bin/env python3
"""
UAV Telemetry Simulator CLI
Simulates various CEP scenarios for testing Drools rules
"""

import time
import sys
from dataclasses import dataclass
from typing import Optional
from uav_websocket import UAVWebSocket, UAVTelemetry
import requests


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@dataclass
class FlightState:
    """Current flight telemetry state"""
    battery: float = 100.0
    signal: int = 100
    speed: float = 10.0
    hdop: float = 1.0
    satellites: int = 12
    fixType: str = "FIX_3D"
    
    def copy(self):
        """Create a copy of current state"""
        return FlightState(
            battery=self.battery,
            signal=self.signal,
            speed=self.speed,
            hdop=self.hdop,
            satellites=self.satellites,
            fixType=self.fixType
        )


class UAVSimulator:
    """Main simulator class"""
    
    def __init__(self):
        self.ws = UAVWebSocket()
        self.state = FlightState()
        self.running = False
        
    def connect(self) -> bool:
        """Connect to WebSocket server"""
        print(f"{Colors.OKBLUE}Connecting to UAV Decision Support System...{Colors.ENDC}")
        if self.ws.connect():
            print(f"{Colors.OKGREEN}✓ Connected successfully{Colors.ENDC}\n")
            return True
        else:
            print(f"{Colors.FAIL}✗ Connection failed{Colors.ENDC}\n")
            return False
    
    def send_telemetry(self, state: Optional[FlightState] = None):
        """Send current telemetry to server"""
        if state is None:
            state = self.state
            
        telemetry = UAVTelemetry(
            battery=state.battery,
            signal=state.signal,
            speed=state.speed,
            hdop=state.hdop,
            satellites=state.satellites,
            fixType=state.fixType
        )
        self.ws.send_message(telemetry)
        
    def print_telemetry(self, state: Optional[FlightState] = None):
        """Print current telemetry state"""
        if state is None:
            state = self.state
            
        # Battery color based on level
        if state.battery < 10:
            bat_color = Colors.FAIL
        elif state.battery < 20:
            bat_color = Colors.WARNING
        else:
            bat_color = Colors.OKGREEN
            
        # Signal color based on strength
        if state.signal == 0:
            sig_color = Colors.FAIL
        elif state.signal < 25:
            sig_color = Colors.WARNING
        else:
            sig_color = Colors.OKGREEN
            
        print(f"📊 {bat_color}Battery: {state.battery:.1f}%{Colors.ENDC} | "
              f"{sig_color}Signal: {state.signal}%{Colors.ENDC} | "
              f"Speed: {state.speed:.1f}m/s | "
              f"HDOP: {state.hdop:.1f} | "
              f"Sats: {state.satellites} | "
              f"Fix: {state.fixType}")
    
    def display_menu(self):
        """Display main menu"""
        print(f"\n{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.OKCYAN}UAV CEP Simulator - Test Scenarios{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*70}{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Current State:{Colors.ENDC}")
        self.print_telemetry()
        
        print(f"\n{Colors.BOLD}Available Scenarios:{Colors.ENDC}\n")
        
        # Level 1 - Basic scenarios
        print(f"{Colors.OKBLUE}Level 1 - Basic Detection:{Colors.ENDC}")
        print("  1. Battery Drainage (Rapid drop: >12% in 30s)")
        print("  2. Signal Lost (0%)")
        print("  3. Signal Weak (<25%)")
        print("  4. Overspeed (>15 m/s)")
        print("  5. GNSS Poor HDOP (>5.0)")
        print("  6. GNSS Few Satellites (<4)")
        print("  7. GNSS No Fix")
        
        # Level 2 - CEP patterns
        print(f"\n{Colors.WARNING}Level 2 - CEP Patterns:{Colors.ENDC}")
        print("  8. High Warning Frequency (4+ warnings in 2 minutes)")
        print("  9. Signal Degrading (3 consecutive drops in 60s)")
        print("  10. Rapid Battery Drain (CEP test: 40% → 25% in 30s)")
        
        # Level 3 - Composite scenarios
        print(f"\n{Colors.FAIL}Level 3 - Critical Scenarios:{Colors.ENDC}")
        print("  11. Risky Flight (Low battery + weak signal)")
        print("  12. Unstable Flight (Overspeed + poor GNSS)")
        print("  13. Critical Battery + Weak Signal → RTH")
        print("  14. Multiple Critical Conditions")
        
        # Other options
        print(f"\n{Colors.OKCYAN}Other Options:{Colors.ENDC}")
        print("  15. Normal Flight (Safe parameters)")
        print("  16. Custom Values")
        print("  17. Reset to Defaults")
        print("  0. Exit")
        
        print(f"\n{Colors.HEADER}{'='*70}{Colors.ENDC}")
    
    def scenario_battery_drainage(self):
        """Scenario 1: Rapid battery drainage"""
        print(f"\n{Colors.WARNING}▶ Scenario: Rapid Battery Drainage{Colors.ENDC}")
        print("Simulating battery drop from 40% to 25% over 30 seconds...")
        print("This should trigger: BATTERY_DRAIN_RAPID fact\n")
        
        # Start at 40%
        self.state.battery = 40.0
        print("Step 1: Battery at 40%")
        self.print_telemetry()
        self.send_telemetry()
        time.sleep(2)
        
        # Gradually drop to 25% over 30 seconds
        steps = 6
        drop_per_step = 15.0 / steps
        
        for i in range(steps):
            time.sleep(5)
            self.state.battery -= drop_per_step
            print(f"\nStep {i+2}: Battery dropping... ({30 - (i+1)*5}s remaining)")
            self.print_telemetry()
            self.send_telemetry()
        
        print(f"\n{Colors.OKGREEN}✓ Scenario complete - Check server logs for BATTERY_DRAIN_RAPID{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def scenario_signal_lost(self):
        """Scenario 2: Signal completely lost"""
        print(f"\n{Colors.FAIL}▶ Scenario: Signal Lost{Colors.ENDC}")
        print("Simulating complete signal loss...")
        print("Expected: SIGNAL_LOST fact → LAND decision\n")
        
        self.state.signal = 0
        self.print_telemetry()
        self.send_telemetry()
        
        print(f"\n{Colors.FAIL}✓ Signal lost - Drone should LAND immediately{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def scenario_signal_weak(self):
        """Scenario 3: Weak signal"""
        print(f"\n{Colors.WARNING}▶ Scenario: Weak Signal{Colors.ENDC}")
        print("Simulating weak signal (20%)...\n")
        
        self.state.signal = 20
        self.print_telemetry()
        self.send_telemetry()
        
        print(f"\n{Colors.WARNING}✓ Weak signal detected{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def scenario_overspeed(self):
        """Scenario 4: Overspeed"""
        print(f"\n{Colors.WARNING}▶ Scenario: Overspeed{Colors.ENDC}")
        print("Simulating overspeed (18 m/s, limit is 15 m/s)...")
        print("Expected: OVERSPEED fact → SLOW_DOWN action\n")
        
        self.state.speed = 18.0
        self.print_telemetry()
        self.send_telemetry()
        
        print(f"\n{Colors.WARNING}✓ Overspeed detected - Drone should SLOW_DOWN{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def scenario_gnss_poor_hdop(self):
        """Scenario 5: Poor GNSS HDOP"""
        print(f"\n{Colors.WARNING}▶ Scenario: GNSS Poor HDOP{Colors.ENDC}")
        print("Simulating poor HDOP (6.5, limit is 5.0)...\n")
        
        self.state.hdop = 6.5
        self.print_telemetry()
        self.send_telemetry()
        
        print(f"\n{Colors.WARNING}✓ Poor HDOP detected{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def scenario_gnss_few_satellites(self):
        """Scenario 6: Few satellites"""
        print(f"\n{Colors.WARNING}▶ Scenario: GNSS Few Satellites{Colors.ENDC}")
        print("Simulating too few satellites (3, minimum is 4)...\n")
        
        self.state.satellites = 3
        self.print_telemetry()
        self.send_telemetry()
        
        print(f"\n{Colors.WARNING}✓ Few satellites detected{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def scenario_gnss_no_fix(self):
        """Scenario 7: No GNSS fix"""
        print(f"\n{Colors.FAIL}▶ Scenario: GNSS No Fix{Colors.ENDC}")
        print("Simulating no GNSS fix...")
        print("Expected: GNSS_NO_FIX fact → LAND decision\n")
        
        self.state.fixType = "NONE"
        self.print_telemetry()
        self.send_telemetry()
        
        print(f"\n{Colors.FAIL}✓ No GNSS fix - Drone should LAND{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def scenario_high_warning_frequency(self):
        """Scenario 8: High warning frequency (4+ in 2 minutes)"""
        print(f"\n{Colors.WARNING}▶ Scenario: High Warning Frequency{Colors.ENDC}")
        print("Generating 4+ warnings in 2 minutes by oscillating parameters...")
        print("Expected: HIGH_WARNING_FREQUENCY fact → RETURN_HOME\n")
        
        initial_state = self.state.copy()
        
        # Generate warnings by alternating bad conditions
        warnings_to_trigger = [
            ("Low Battery", lambda: setattr(self.state, 'battery', 18)),
            ("Weak Signal", lambda: setattr(self.state, 'signal', 22)),
            ("Overspeed", lambda: setattr(self.state, 'speed', 16)),
            ("Poor HDOP", lambda: setattr(self.state, 'hdop', 5.5)),
        ]
        
        for i, (warning_name, trigger_func) in enumerate(warnings_to_trigger, 1):
            print(f"\nWarning {i}/4: Triggering {warning_name}...")
            
            # Reset to normal
            self.state = initial_state.copy()
            
            # Trigger specific warning
            trigger_func()
            
            self.print_telemetry()
            self.send_telemetry()
            
            time.sleep(15)  # 15 seconds between warnings
        
        print(f"\n{Colors.OKGREEN}✓ 4 warnings generated - Check for HIGH_WARNING_FREQUENCY{Colors.ENDC}")
        input("\nPress Enter to continue...")
        
        # Restore initial state
        self.state = initial_state
    
    def scenario_signal_degrading(self):
        """Scenario 9: Signal continuously degrading"""
        print(f"\n{Colors.WARNING}▶ Scenario: Signal Degrading{Colors.ENDC}")
        print("Simulating 3 consecutive signal drops in 60 seconds...")
        print("Pattern: 80% → 60% → 40% (20% drops every 30s)\n")
        
        signals = [80, 60, 40]
        
        for i, signal_strength in enumerate(signals, 1):
            self.state.signal = signal_strength
            print(f"Step {i}: Signal at {signal_strength}%")
            self.print_telemetry()
            self.send_telemetry()
            
            if i < len(signals):
                time.sleep(30)  # Wait 30 seconds between readings
        
        print(f"\n{Colors.OKGREEN}✓ Signal degradation pattern complete - Check for SIGNAL_DEGRADING{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def scenario_rapid_battery_drain_cep(self):
        """Scenario 10: Rapid battery drain CEP test"""
        print(f"\n{Colors.FAIL}▶ Scenario: Rapid Battery Drain (CEP Test){Colors.ENDC}")
        print("Testing CEP temporal pattern: 40% → 25% in exactly 30 seconds...")
        print("This tests the 'after[0s, 30s]' temporal operator\n")
        
        # First reading: 40%
        self.state.battery = 40.0
        print("T=0s: Battery at 40%")
        self.print_telemetry()
        self.send_telemetry()
        
        # Wait exactly 30 seconds
        print("\nWaiting 30 seconds...")
        for i in range(30):
            time.sleep(1)
            sys.stdout.write(f"\r⏱  {30-i}s remaining...")
            sys.stdout.flush()
        
        # Second reading: 25%
        print("\n\nT=30s: Battery at 25% (15% drop)")
        self.state.battery = 25.0
        self.print_telemetry()
        self.send_telemetry()
        
        print(f"\n{Colors.FAIL}✓ Rapid drain detected - Check for BATTERY_DRAIN_RAPID fact{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def scenario_risky_flight(self):
        """Scenario 11: Risky flight (low battery + weak signal)"""
        print(f"\n{Colors.WARNING}▶ Scenario: Risky Flight{Colors.ENDC}")
        print("Combining low battery (18%) + weak signal (22%)...")
        print("Expected: BATTERY_LOW + SIGNAL_WEAK → FLIGHT_RISKY → RETURN_HOME\n")
        
        self.state.battery = 18.0
        self.state.signal = 22
        
        self.print_telemetry()
        self.send_telemetry()
        
        print(f"\n{Colors.WARNING}✓ Risky flight conditions - Drone should RETURN_HOME{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def scenario_unstable_flight(self):
        """Scenario 12: Unstable flight (overspeed + poor GNSS)"""
        print(f"\n{Colors.WARNING}▶ Scenario: Unstable Flight{Colors.ENDC}")
        print("Combining overspeed (17 m/s) + poor GNSS (HDOP 6.0, 3 sats)...")
        print("Expected: OVERSPEED + GNSS_POOR_HDOP → FLIGHT_UNSTABLE → SLOW_DOWN\n")
        
        self.state.speed = 17.0
        self.state.hdop = 6.0
        self.state.satellites = 3
        
        self.print_telemetry()
        self.send_telemetry()
        
        print(f"\n{Colors.WARNING}✓ Unstable flight - Drone should SLOW_DOWN{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def scenario_critical_battery_weak_signal(self):
        """Scenario 13: Critical battery + weak signal"""
        print(f"\n{Colors.FAIL}▶ Scenario: Critical Battery + Weak Signal{Colors.ENDC}")
        print("Combining critical battery (8%) + weak signal (20%)...")
        print("Expected: BATTERY_CRITICAL + SIGNAL_WEAK → CRITICAL → RETURN_HOME\n")
        
        self.state.battery = 8.0
        self.state.signal = 20
        
        self.print_telemetry()
        self.send_telemetry()
        
        print(f"\n{Colors.FAIL}✓ CRITICAL condition - Drone should RETURN_HOME immediately{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def scenario_multiple_critical(self):
        """Scenario 14: Multiple critical conditions"""
        print(f"\n{Colors.FAIL}▶ Scenario: Multiple Critical Conditions{Colors.ENDC}")
        print("Simulating worst-case scenario with multiple failures...\n")
        
        print("Stage 1: Normal flight")
        self.state = FlightState()
        self.print_telemetry()
        self.send_telemetry()
        time.sleep(3)
        
        print("\nStage 2: Battery getting low...")
        self.state.battery = 25.0
        self.print_telemetry()
        self.send_telemetry()
        time.sleep(3)
        
        print("\nStage 3: Signal starts degrading...")
        self.state.signal = 40
        self.print_telemetry()
        self.send_telemetry()
        time.sleep(3)
        
        print("\nStage 4: GNSS problems...")
        self.state.hdop = 5.5
        self.state.satellites = 4
        self.print_telemetry()
        self.send_telemetry()
        time.sleep(3)
        
        print("\nStage 5: CRITICAL - Battery critical + signal weak!")
        self.state.battery = 9.0
        self.state.signal = 20
        self.print_telemetry()
        self.send_telemetry()
        
        print(f"\n{Colors.FAIL}✓ Multiple critical conditions - Emergency RTH required!{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def scenario_normal_flight(self):
        """Scenario 15: Normal safe flight"""
        print(f"\n{Colors.OKGREEN}▶ Scenario: Normal Flight{Colors.ENDC}")
        print("Resetting to safe flight parameters...")
        print("Expected: SAFE state → CONTINUE mission\n")
        
        self.state = FlightState(
            battery=85.0,
            signal=95,
            speed=10.0,
            hdop=1.2,
            satellites=12,
            fixType="FIX_3D"
        )
        
        self.print_telemetry()
        self.send_telemetry()
        
        print(f"\n{Colors.OKGREEN}✓ Normal flight - All parameters in safe range{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def scenario_custom_values(self):
        """Scenario 16: Custom values"""
        print(f"\n{Colors.OKCYAN}▶ Scenario: Custom Values{Colors.ENDC}")
        print("Enter custom telemetry values:\n")
        
        try:
            self.state.battery = float(input("Battery (0-100): "))
            self.state.signal = int(input("Signal (0-100): "))
            self.state.speed = float(input("Speed (m/s): "))
            self.state.hdop = float(input("HDOP: "))
            self.state.satellites = int(input("Satellites: "))
            fix_type = input("Fix Type (NONE/FIX_2D/FIX_3D/RTK): ").upper()
            self.state.fixType = fix_type if fix_type else "FIX_3D"
            
            print()
            self.print_telemetry()
            self.send_telemetry()
            
            print(f"\n{Colors.OKGREEN}✓ Custom values sent{Colors.ENDC}")
        except ValueError as e:
            print(f"{Colors.FAIL}Invalid input: {e}{Colors.ENDC}")
        
        input("\nPress Enter to continue...")
    
    def scenario_reset(self):
        """Scenario 17: Reset to defaults"""
        print(f"\n{Colors.OKBLUE}▶ Resetting to default values...{Colors.ENDC}\n")
        # send the reset request to remove all facts from the system
        response = requests.post("http://localhost:8080/api/telemetry/reset")
        print(f"\n{Colors.OKBLUE}▶ {response.text} {Colors.ENDC}\n")

        self.state = FlightState()
        self.print_telemetry()
        self.send_telemetry()
        print(f"\n{Colors.OKGREEN}✓ Reset complete{Colors.ENDC}")
        time.sleep(2)
    
    def run(self):
        """Main run loop"""
        if not self.connect():
            return
        
        # Send initial telemetry
        self.send_telemetry()
        
        scenario_map = {
            '1': self.scenario_battery_drainage,
            '2': self.scenario_signal_lost,
            '3': self.scenario_signal_weak,
            '4': self.scenario_overspeed,
            '5': self.scenario_gnss_poor_hdop,
            '6': self.scenario_gnss_few_satellites,
            '7': self.scenario_gnss_no_fix,
            '8': self.scenario_high_warning_frequency,
            '9': self.scenario_signal_degrading,
            '10': self.scenario_rapid_battery_drain_cep,
            '11': self.scenario_risky_flight,
            '12': self.scenario_unstable_flight,
            '13': self.scenario_critical_battery_weak_signal,
            '14': self.scenario_multiple_critical,
            '15': self.scenario_normal_flight,
            '16': self.scenario_custom_values,
            '17': self.scenario_reset,
        }
        
        while True:
            self.display_menu()
            choice = input(f"\n{Colors.BOLD}Select scenario (0-17): {Colors.ENDC}").strip()
            
            if choice == '0':
                print(f"\n{Colors.OKBLUE}Shutting down simulator...{Colors.ENDC}")
                break
            
            scenario_func = scenario_map.get(choice)
            if scenario_func:
                try:
                    scenario_func()
                except KeyboardInterrupt:
                    print(f"\n{Colors.WARNING}Scenario interrupted{Colors.ENDC}")
                    input("\nPress Enter to continue...")
            else:
                print(f"{Colors.FAIL}Invalid choice. Please select 0-17.{Colors.ENDC}")
                time.sleep(2)
        
        print(f"{Colors.OKGREEN}Goodbye!{Colors.ENDC}\n")


