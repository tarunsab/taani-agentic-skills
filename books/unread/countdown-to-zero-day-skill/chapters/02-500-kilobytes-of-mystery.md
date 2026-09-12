# Chapter 2: 500 Kilobytes of Mystery

## Thesis

The code's unusual size and internal organization make Stuxnet a different class of investigation from ordinary malware triage. Liam O'Murchu at Symantec receives samples on July 16, 2010 and finds a compressed object around 500 kilobytes, far larger than common worms and even much larger than Conficker. The size is not decorative bulk: it contains layered, encrypted components and a carefully coordinated set of capabilities. The chapter follows analysts as they move from a Windows infection pattern toward the hypothesis that the program was built for a specific industrial environment.

## Mechanism and source evidence

Symantec uses a follow-the-sun handoff so analysts can work continuously, but the sample still requires manual reverse engineering because automated classification cannot explain an unknown zero-day chain. O'Murchu and colleagues unpack layers, identify command-and-control domains in Denmark and Malaysia, and see functionality for collecting information and updating copies. A sinkhole maps infections and shows a concentration in the Middle East, especially Iran, while Siemens software appears to be the unusual common denominator. These observations suggest industrial espionage or reconnaissance, but at this point they do not establish Natanz, physical sabotage, or a state sponsor.

## Distinctions and limitations

Malware size is a clue about engineering effort, not proof of mission. A program can target an industrial ecosystem for credential theft, process espionage, sabotage, or several purposes at once. Internet command servers show an available communications path, not necessarily that the final payload requires live remote control; later analysis shows that important behavior can be local and condition-triggered. The infection map also records where systems were exposed, not which hosts were intended targets or whether every victim was relevant to the operation.

## Practical use

For a large unknown sample, preserve the original and build a capability inventory before writing a narrative. Separate propagation, collection, command channels, environmental checks, and destructive behavior. Sinkhole data should be treated as a biased sample shaped by DNS, connectivity, and the defenders' visibility. Use industrial software names as a lead for asset discovery, then confirm the exact controller and process conditions rather than assuming that every customer of a vendor is the target.

## Connections

This chapter sets up Chapter 4's layered architecture and Chapter 10's industrial reconstruction. Its uncertainty about motive is resolved only when analysts locate PLC-specific code and sensor deception in Chapter 8. The pattern also generalizes to the book's treatment of Duqu and Flame: reconnaissance, collection, and sabotage can share a technical family without having the same immediate objective.
