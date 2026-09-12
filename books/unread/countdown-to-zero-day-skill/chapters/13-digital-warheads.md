# Chapter 13: Digital Warheads

## Thesis

Once analysts found Stuxnet's PLC payload, they still had to translate opaque machine code into a physical hypothesis about centrifuges. Three values in the code pointed to a Profibus card and two separate attack paths: one for an S7-315 system with frequency converters and another for an S7-417 system with valves. Reverse engineering, an emulator, public descriptions of the Natanz cascade, and a specialist's knowledge of device identifiers converged on a remarkably specific target model. The chapter demonstrates both the power and the limits of reconstructing a physical attack from code without direct access to the plant.

## Mechanism and source evidence

The 315 sequence recorded normal operation for about thirteen days, waited through a two-hour phase, and later repeated a roughly fifty-minute phase after a longer interval. It targeted frequency converters associated with Fararo Paya's `7050h` and Vacon's `9500h` identifiers, adjusting the programmed frequency from a normal range around 807–1210 Hz toward 1,410 Hz and 2 Hz. The 1,064 Hz operating value matched the expected IR-1 centrifuge speed, while the code's 186-device limit fit the described process. The 417 path was larger—around 40 blocks and 13,000 lines rather than roughly 15 blocks and 4,000 lines—and aimed at six arrays of 164 devices, but parts appeared disabled or incomplete in later variants.

## Distinctions and limitations

Programmed frequency is not the same as achieved rotor speed: acceleration limits meant the centrifuges might reach only about 1,324–1,381 Hz during the high-speed window. The code reveals intended manipulation and constraints, but not every valve state, exact Natanz configuration, or realized physical result. Analysts disagreed about whether the 417 path was fully operational and why the variants differed. The match between device identifiers, cascade structure, and Iranian enrichment technology is strong technical evidence for target design, but it remains distinct from public proof of authorship.

## Practical use

For defensive analysis, translate controller code into process variables with qualified control engineers, using a simulator or safe testbed. Check units, timing, ramp rates, device limits, safety interlocks, and the difference between requested and observed values. Compare binary hypotheses with maintenance and production records, but label any unobserved physical effect as modeled or inferred. Preserve the original logic and document every translation step so a later reviewer can distinguish source behavior from analyst interpretation.

## Connections

The chapter supplies the technical detail behind Chapter 8's sabotage claim and Chapter 10's test-bed reconstruction. Chapter 16 extends the 417 valve attack into a full historical sequence, while Chapter 17 compares the programmed cycles with IAEA centrifuge counts. Its “code as evidence, not omniscience” lesson is central to Chapter 18's qualified assessment of success.
