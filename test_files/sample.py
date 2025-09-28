import sys
import time

def raptor_print():
    # Simulate a dynamic update for a hackathon event
    for i in range(10):
        # Use \r to return to the beginning of the line and overwrite
        sys.stdout.write(f"\rRaptors Hackathon Progress: {i * 10}%")
        sys.stdout.flush()  # Ensure the output is displayed immediately
        time.sleep(0.5)
    
    # Final message after completion
    sys.stdout.write("\nRaptors Hackathon: Event Complete!\n")
    sys.stdout.flush()

# Run the print function
raptor_print()