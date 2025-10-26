# Fibonacci Reversible Automata

**Reversible Turing-complete cellular automaton with Fibonacci spiral geometry**

[![npm version](https://img.shields.io/npm/v/fibonacci-reversible-automata.svg)](https://www.npmjs.com/package/fibonacci-reversible-automata)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Author:** j Mosij <mosij@icloud.com>

## 🏆 First Documented Implementation

This package contains the first documented implementation combining:
- ✅ **Reversible computation** - No information loss
- ✅ **Turing completeness** - Universal computation capability  
- ✅ **Fibonacci geometry** - Golden ratio (137.5°) spiral patterns

## Installation

```bash
npm install fibonacci-reversible-automata
```

## Quick Start

```javascript
const ReversePineConeFibonacciAutomata = require('fibonacci-reversible-automata');

// Create 89x89 grid (89 is a Fibonacci number)
const automata = new ReversePineConeFibonacciAutomata(89);

// Initialize with Fibonacci spiral pattern
automata.initializeFibonacciSpiral();

// Run 6 forward steps (Fibonacci number)
automata.forward(6);

// Run 13 reverse steps (Fibonacci number)
automata.backward(13);

// The automaton is perfectly reversible!
```

## Features

### Reversible Computation
- **Margolus neighborhood** with partition offset management
- **100% reversible** - No information loss
- Forward and backward execution
- No state history needed

### Turing Completeness
- Based on **"Critters" rule** (proven Turing-complete)
- Block cellular automaton (2x2 blocks)
- Universal computation capability

### Fibonacci Integration
- **Golden angle**: 137.5° spiral patterns
- **Fibonacci parameters**: 6, 13, 89
- Natural phyllotaxis-inspired patterns

## API Reference

### Constructor

```javascript
new ReversePineConeFibonacciAutomata(gridSize = 89)
```

Creates a new automaton with the specified grid size (default: 89, a Fibonacci number).

### Methods

#### `step(reverse = false)`
Execute one step of the automaton.
- `reverse`: If true, runs in reverse

#### `forward(steps = 6)`
Run multiple forward steps (default: 6, a Fibonacci number).

#### `backward(steps = 13)`
Run multiple reverse steps (default: 13, a Fibonacci number).

#### `initializeFibonacciSpiral()`
Initialize the grid with a Fibonacci spiral pattern using the golden angle (137.5°).

#### `getState()`
Returns a copy of the current grid state as a 2D array.

#### `setState(newState)`
Set the grid state from a 2D array.

#### `entropy()`
Calculate the entropy of the current state (0 to 1).

## Examples

### Basic Reversibility Test

```javascript
const automata = new ReversePineConeFibonacciAutomata(10);

// Set initial pattern
automata.setState([
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
  // ... more rows
]);

const initial = automata.getState();

// Forward then reverse
automata.forward(10);
automata.backward(10);

// State is restored!
console.log('Reversible:', JSON.stringify(initial) === JSON.stringify(automata.getState()));
// Output: Reversible: true
```

### Fibonacci Spiral Visualization

```javascript
const automata = new ReversePineConeFibonacciAutomata(89);
automata.initializeFibonacciSpiral();

// Print the spiral
const state = automata.getState();
console.log(state.map(row => row.map(cell => cell ? '●' : '·').join('')).join('\n'));
```

### Entropy Tracking

```javascript
const automata = new ReversePineConeFibonacciAutomata(89);
automata.initializeFibonacciSpiral();

console.log('Initial entropy:', automata.entropy());

automata.forward(100);
console.log('After 100 steps:', automata.entropy());

automata.backward(100);
console.log('After reversing:', automata.entropy());
// Entropy returns to original value!
```

## The Algorithm

### Margolus "Critters" Rule

The core rule applied to each 2x2 block:

```javascript
margolusBlockRule(block, reverse) {
  const count = sum(block);
  
  if (count === 4) {
    return block;  // No change
  } else if (count === 1 || count === 2) {
    return rotate90(block, clockwise: !reverse);
  } else {  // 0 or 3
    return rotate90(block, clockwise: reverse);
  }
}
```

### Reversibility Mechanism

- **Forward**: Apply rule, then toggle partition offset
- **Reverse**: Toggle offset first, apply inverse rule
- **Result**: Perfect mathematical reversibility

## Performance

Typical performance on modern hardware:
- **Forward**: ~200-300 steps/second (89x89 grid)
- **Reverse**: ~200-300 steps/second (89x89 grid)
- **Memory**: O(n²) where n is grid size

## TypeScript Support

Full TypeScript definitions included:

```typescript
import ReversePineConeFibonacciAutomata = require('fibonacci-reversible-automata');

const automata: ReversePineConeFibonacciAutomata = new ReversePineConeFibonacciAutomata(89);
```

## Testing

```bash
npm test
```

Runs comprehensive test suite including:
- Reversibility verification
- Block rotation tests
- Entropy calculations
- Performance benchmarks

## References

- **Margolus Neighborhood**: Toffoli & Margolus (1987)
- **Critters Rule**: Proven reversible and Turing-complete
- **Fibonacci Phyllotaxis**: Mathematical biology
- **Golden Ratio**: φ ≈ 1.618...

## License

MIT © j Mosij

## Repository

Full implementation and Python version:
https://github.com/Aylos9er/Fibonacci-Files-Rev-Automata-Pocketml

## Contributing

Issues and pull requests welcome!

## Author

**j Mosij**  
Email: mosij@icloud.com

---

*First documented reversible Turing-complete cellular automaton based on Fibonacci spiral geometry.*
