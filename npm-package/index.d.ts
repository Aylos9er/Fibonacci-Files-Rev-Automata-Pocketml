/**
 * Fibonacci Reversible Automata - TypeScript Definitions
 * Author: j Mosij <mosij@icloud.com>
 */

declare class ReversePineConeFibonacciAutomata {
  /**
   * Size of the grid
   */
  gridSize: number;

  /**
   * Current state of the automaton (2D array)
   */
  state: number[][];

  /**
   * Current partition offset (0 or 1)
   */
  partitionOffset: number;

  /**
   * Create a new reversible Fibonacci automata
   * @param gridSize - Size of the grid (default: 89, a Fibonacci number)
   */
  constructor(gridSize?: number);

  /**
   * Rotate a 2x2 block 90 degrees
   * @param block - 2x2 array
   * @param clockwise - Rotation direction (default: true)
   * @returns Rotated block
   */
  rotateBlock90(block: number[][], clockwise?: boolean): number[][];

  /**
   * Apply Margolus "Critters" rule to a 2x2 block
   * @param block - 2x2 array
   * @param reverse - Apply rule in reverse (default: false)
   * @returns Transformed block
   */
  margolusBlockRule(block: number[][], reverse?: boolean): number[][];

  /**
   * Execute one step of the automaton
   * @param reverse - Run in reverse (default: false)
   */
  step(reverse?: boolean): void;

  /**
   * Run multiple forward steps
   * @param steps - Number of steps (default: 6, a Fibonacci number)
   */
  forward(steps?: number): void;

  /**
   * Run multiple reverse steps
   * @param steps - Number of steps (default: 13, a Fibonacci number)
   */
  backward(steps?: number): void;

  /**
   * Initialize the grid with a Fibonacci spiral pattern
   * Uses golden angle (137.5°) for optimal packing
   */
  initializeFibonacciSpiral(): void;

  /**
   * Get a copy of the current state
   * @returns Copy of the grid state
   */
  getState(): number[][];

  /**
   * Set the state from an array
   * @param newState - New grid state
   */
  setState(newState: number[][]): void;

  /**
   * Calculate entropy of current state
   * @returns Entropy value (0 to 1)
   */
  entropy(): number;
}

export = ReversePineConeFibonacciAutomata;
