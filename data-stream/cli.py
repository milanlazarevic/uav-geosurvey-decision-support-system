from uav_simulator import UAVSimulator, Colors
import sys


def main():
    try:
        simulator = UAVSimulator()
        simulator.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Interrupted by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
