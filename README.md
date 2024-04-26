# LFSR Module

This module contains the implementation of a Linear Feedback Shift Register (LFSR), a mechanism used to generate pseudo-random binary sequences. LFSRs are widely used in fields such as cryptography and digital communication, particularly in the generation and analysis of stream ciphers.

## Features

- **Customizable Size:** Set the register size according to your needs.
- **Initial Status Setup:** Begin with a predefined status to maintain consistency across operations.
- **XOR List:** Define custom XOR taps for the feedback function.
- **Continuation Capability:** Optionally continue from the last output of a previous LFSR run.

## Usage

1. **Initialization:** Create an instance of the LFSR class with the desired size, initial status, and XOR taps.
2. **Generate Sequence:** Use the instance methods to generate or manipulate the sequence as per your application requirements.

## Example

```python
# Create an LFSR instance
lfsr = LFSR(size=16, status=0b1011011100110110, xor_list=[1, 5, 6])

# Generate a sequence or perform other operations
output = lfsr.next_bit()
print(f"Output bit: {output}")
```

## Applications in Cryptanalysis

LFSRs have a known vulnerability when used in certain stream cipher configurations, such as those found in the Content Scramble System (CSS) used for DVD encryption. This module can simulate LFSR sequences that might be used in cryptanalytic attacks to understand or exploit weaknesses in these systems.

## Requirements

- This module requires Python 3.x.

## Testing
### Running Test Functions
At the end of the code, there are several test functions that you can uncomment to check the behavior of the LFSR implementation. These tests help verify various aspects of the LFSR under different conditions and configurations.

To run the tests, uncomment the test function calls in the `if __name__ == "__main__":` block at the end of the script. Not every LFSR configuration will have a cycle of 2^n - 1 iterations, so these tests can help ensure your specific setup works correctly.

```python
if __name__ == "__main__":
    # To test the LFSR functionality, uncomment the desired test functions below:

    test0() # Test LFSR with 8-bit register to ensure no duplicate sequences
    test1() # Test LFSR with 17-bit register to ensure no duplicate sequences
    test2() # Test LFSR with 25-bit register to ensure no duplicate sequences
    test3() # Test encoding with message '0xffffffffff' expecting output '0xffffb66c39'
    test6() # Simulate an attack on Content Scrambling System (CSS) using LFSR
```