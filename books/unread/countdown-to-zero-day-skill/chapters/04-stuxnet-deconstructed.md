# Chapter 4: Stuxnet Deconstructed

## Thesis

Stuxnet becomes intelligible when its “missile” and “warhead” are separated. Symantec researchers Eric Chien, Liam O'Murchu, and Nicolas Falliere found a broad Windows platform for delivery, concealment, and updating, followed by a narrow payload that activated only when a particular Siemens Step 7/WinCC and S7 PLC environment was present. The code could infect systems, survive reboots, spread through USB and local paths, and communicate or update through peers, yet remain dormant on most machines. This architecture explains how a weapon could travel widely while attempting to reserve its physical effects for a precise industrial target.

## Mechanism and source evidence

Stuxnet replaced the legitimate Siemens `s7otbxdx.DLL` with a doppelganger, renamed the original, and intercepted read and write operations between engineering software and the PLC. It checked for specific S7-315 and S7-417 configurations, injected commands into PLC blocks, hooked execution, and used resource cleanup to reduce forensic traces. The payload recorded a period of normal operations and replayed those readings while abnormal logic ran; it also interfered with an emergency-response layer so the process could not simply isolate a failing machine. Researchers found an inoculation value and a `myrtus`/`guava` path that encouraged theories about Iranian history, Israel, or engineering terminology, but the chapter presents these as speculation rather than attribution.

## Distinctions and limitations

The spread layer and process layer have different triggers, risks, and evidence. A host can be infected without being physically affected, while a precise payload can still create collateral exposure through its carrier and propagation mechanisms. A rootkit can hide software artifacts, but it cannot by itself prove what happened in the physical process. The source's discussion of an alleged 1982 Soviet pipeline sabotage and Iranian explosions also illustrates a recurring limitation: stories that fit a cyber-sabotage narrative may lack enough evidence to establish that cyber was the cause.

## Practical use

Analyze suspected ICS malware in layers: host delivery, persistence, engineering-software hooks, PLC logic, sensor/readback behavior, safety interlocks, and physical effect. Establish clean-room baselines for engineering software and controller logic, and compare reads and writes through an independent path. Inventory exact PLC models and process configurations; generic malware signatures are not enough for a process-specific threat. Containment should preserve the ability to recover to a known-safe logic state without trusting the compromised engineering workstation.

## Connections

This chapter is the technical hinge between the discovery story and the policy story. Chapter 6 expands the delivery paths; Chapter 8 explains the physical payload; Chapter 10 shows how Ralph Langner reproduced the PLC behavior. The clues and their uncertainty feed Chapter 11's attribution debate and Chapter 19's argument that a digital weapon carries its design knowledge into the world.
