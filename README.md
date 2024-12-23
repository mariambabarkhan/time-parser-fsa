# FSA: Finite State Automaton

This project implements a Finite State Automaton (FSA) framework that dynamically updates the "current time" (`today`) during runtime. The system ensures real-time accuracy for operations involving time-based transitions or calculations.

## Features

- **Dynamic Current Time**: The `today` value is fetched dynamically using the `get_current_time()` function whenever required.
- **Customizable States and Transitions**: Define states and transitions based on your specific use case.
- **Real-Time Updates**: Ensures that time-based conditions use the current datetime without requiring a restart.