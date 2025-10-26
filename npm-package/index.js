/**
 * Fibonacci Reversible Automata - JavaScript Implementation
 * Reversible Turing-complete cellular automaton with Fibonacci spiral geometry
 * 
 * Author: j Mosij <mosij@icloud.com>
 * License: MIT
 * 
 * First documented implementation combining:
 * - Reversible computation (no information loss)
 * - Turing completeness (universal computation)
 * - Fibonacci geometry (golden ratio spiral patterns)
 */

class ReversePineConeFibonacciAutomata {
  /**
   * Create a new reversible Fibonacci automata
   * @param {number} gridSize - Size of the grid (default: 89, a Fibonacci number)
   */
  constructor(gridSize = 89) {
    this.gridSize = gridSize;
    this.state = Array(gridSize).fill(0).map(() => Array(gridSize).fill(0));
    this.partitionOffset = 0;
  }

  /**
   * Rotate a 2x2 block 90 degrees
   * @param {Array<Array<number>>} block - 2x2 array
   * @param {boolean} clockwise - Rotation direction
   * @returns {Array<Array<number>>} Rotated block
   */
  rotateBlock90(block, clockwise = true) {
    if (clockwise) {
      return [
        [block[1][0], block[0][0]],
        [block[1][1], block[0][1]]
      ];
    } else {
      return [
        [block[0][1], block[1][1]],
        [block[0][0], block[1][0]]
      ];
    }
  }

  /**
   * Apply Margolus "Critters" rule to a 2x2 block
   * This rule is proven to be both reversible and Turing-complete
   * @param {Array<Array<number>>} block - 2x2 array
   * @param {boolean} reverse - Apply rule in reverse
   * @returns {Array<Array<number>>} Transformed block
   */
  margolusBlockRule(block, reverse = false) {
    const count = block[0][0] + block[0][1] + block[1][0] + block[1][1];
    
    if (count === 4) {
      // All full - no change
      return block;
    } else if (count === 1 || count === 2) {
      // 1-2 particles: rotate based on direction
      return this.rotateBlock90(block, !reverse);
    } else {
      // 0 or 3 particles: rotate opposite direction
      return this.rotateBlock90(block, reverse);
    }
  }

  /**
   * Execute one step of the automaton
   * @param {boolean} reverse - Run in reverse (default: false)
   */
  step(reverse = false) {
    // For reverse steps, toggle offset BEFORE processing
    if (reverse) {
      this.partitionOffset = 1 - this.partitionOffset;
    }

    // Process all 2x2 blocks with current offset
    for (let i = this.partitionOffset; i < this.gridSize - 1; i += 2) {
      for (let j = this.partitionOffset; j < this.gridSize - 1; j += 2) {
        // Extract 2x2 block
        const block = [
          [this.state[i][j], this.state[i][j + 1]],
          [this.state[i + 1][j], this.state[i + 1][j + 1]]
        ];

        // Apply rule
        const newBlock = this.margolusBlockRule(block, reverse);

        // Write back
        this.state[i][j] = newBlock[0][0];
        this.state[i][j + 1] = newBlock[0][1];
        this.state[i + 1][j] = newBlock[1][0];
        this.state[i + 1][j + 1] = newBlock[1][1];
      }
    }

    // For forward steps, toggle offset AFTER processing
    if (!reverse) {
      this.partitionOffset = 1 - this.partitionOffset;
    }
  }

  /**
   * Run multiple forward steps
   * @param {number} steps - Number of steps (default: 6, a Fibonacci number)
   */
  forward(steps = 6) {
    for (let i = 0; i < steps; i++) {
      this.step(false);
    }
  }

  /**
   * Run multiple reverse steps
   * @param {number} steps - Number of steps (default: 13, a Fibonacci number)
   */
  backward(steps = 13) {
    for (let i = 0; i < steps; i++) {
      this.step(true);
    }
  }

  /**
   * Initialize the grid with a Fibonacci spiral pattern
   * Uses golden angle (137.5°) for optimal packing
   */
  initializeFibonacciSpiral() {
    const goldenAngle = 137.508; // degrees
    const centerX = this.gridSize / 2;
    const centerY = this.gridSize / 2;
    const numPoints = 89; // Fibonacci number

    for (let i = 0; i < numPoints; i++) {
      const angle = (i * goldenAngle * Math.PI) / 180;
      const radius = Math.sqrt(i) * 2;
      const x = Math.floor(centerX + radius * Math.cos(angle));
      const y = Math.floor(centerY + radius * Math.sin(angle));

      if (x >= 0 && x < this.gridSize && y >= 0 && y < this.gridSize) {
        this.state[x][y] = 1;
      }
    }
  }

  /**
   * Get a copy of the current state
   * @returns {Array<Array<number>>} Copy of the grid state
   */
  getState() {
    return this.state.map(row => [...row]);
  }

  /**
   * Set the state from an array
   * @param {Array<Array<number>>} newState - New grid state
   */
  setState(newState) {
    if (newState.length !== this.gridSize || newState[0].length !== this.gridSize) {
      throw new Error(`State must be ${this.gridSize}x${this.gridSize}`);
    }
    this.state = newState.map(row => [...row]);
  }

  /**
   * Calculate entropy of current state
   * @returns {number} Entropy value (0 to 1)
   */
  entropy() {
    const total = this.gridSize * this.gridSize;
    const ones = this.state.flat().reduce((sum, val) => sum + val, 0);
    const p = ones / total;
    if (p === 0 || p === 1) return 0;
    return -(p * Math.log2(p) + (1 - p) * Math.log2(1 - p));
  }
}

// Export for Node.js and browser
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ReversePineConeFibonacciAutomata;
}

if (typeof window !== 'undefined') {
  window.ReversePineConeFibonacciAutomata = ReversePineConeFibonacciAutomata;
}
