# Chapter 17: The Mystery of the Centrifuges

## Thesis

The 2009 and 2010 Stuxnet releases line up with a period of political crisis in Iran and worsening uncertainty about Natanz's centrifuges. A June 2009 version infected industrial gateway companies and later appeared to coincide with declining numbers of centrifuges enriching uranium; a March 2010 version spread much more widely after Behpajooh was infected. The chapter shows why the public investigation could connect infection logs, programmed cycles, IAEA counts, and known company roles while still failing to measure the exact physical effect. It also shows how an operation that had remained secret for years became exposed through an uncontrolled propagation path.

## Mechanism and source evidence

The June 2009 version used USB and print-spooler paths in addition to the earlier project-file route and reached Foolad, Behpajooh, Neda, and CGJ, companies associated with industrial control work and possible access to Natanz. Its payload raised frequency toward 1,410 Hz for a short period and later dropped it toward 2 Hz, while false data obscured the resulting stress and enrichment changes. By late 2009 and early 2010, IAEA reporting showed centrifuge removal and fluctuating counts, but the plant was also dealing with fragile IR-1 machines, hurried installation, sanctions, and technical learning. The March 2010 version struck Behpajooh, spread through Iran, the UK, Asia, and beyond, and eventually alerted Washington that the weapon had gone rogue.

## Distinctions and limitations

Correlation between a programmed attack cycle and a plant's changing count is not the same as a controlled experiment. The source challenges a reported story that an infected scientist carried Stuxnet out of Natanz because the forensic logs first showed generic contractor-company infections and no mechanism that reliably stopped spread outside the target. Operators could disinfect infected systems, but the public record cannot show whether they chose not to, could not keep up, or released later variants under different controls. Iran's later restriction of IAEA reporting reduced the independent visibility needed to settle the 2010 effect.

## Practical use

Incident response should build a timeline from endpoint logs, removable-media events, engineering changes, physical process data, supplier activity, and external reporting. Identify “gateway” organizations without accusing them of complicity; a contractor can be an unwitting carrier. Establish containment controls before broad infection occurs, and test whether they preserve safe operations. When source data becomes less available after an incident, record the resulting confidence loss rather than filling it with a confident narrative.

## Connections

This chapter is the empirical bridge between the payload reconstruction of Chapters 13 and 16 and the success debate of Chapter 18. It also explains why Chapter 6 emphasizes the danger of redundant propagation and why Chapter 19 treats uncontrollable spread as a strategic defect. The election and Fordow context links the malware timeline back to Chapter 5's political and nuclear background.
