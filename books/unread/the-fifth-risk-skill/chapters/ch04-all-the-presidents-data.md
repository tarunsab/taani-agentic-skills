# Chapter 4: III. All the President’s Data

## Core Idea

The chapter begins with Joplin, where the National Weather Service issued a timely warning but many residents did not act, exposing a gap between forecasting the hazard and understanding the people threatened by it. Kathy Sullivan concludes that government had spent billions collecting data about weather and almost none on how citizens interpreted warnings, trusted messengers, or chose shelter. The Department of Commerce, especially NOAA, is then revealed as a hidden information system: it runs the Census, economic statistics, patents, standards, satellites, radar, and the National Weather Service, although its name encourages people to think only about business or trade. DJ Patil’s path from chaos theory and ensemble weather forecasts to the first U.S. chief data scientist shows how public data can reveal patterns in weather, terrorism, opportunity, policing, and traffic safety. The data is valuable not merely because it exists, but because it is accessible, combined, analyzed, and translated into decisions; the Climate Corporation turns government weather, field, and soil records into insurance and farm recommendations. Lewis contrasts this public infrastructure with a private weather industry that depends on taxpayer-funded observations while marketing selective successes, and he uses ForecastAdvisor to distinguish aggregate evidence from anecdotes. Sullivan’s Weather-Ready Nation adds the human side: warnings must make the threat tangible, use trusted voices, include social scientists, and communicate uncertainty without burying the action in jargon. The chapter’s limit is that it offers illustrative cases rather than a full data-governance design; privacy, commercialization, and misuse appear as tensions, but the book does not resolve every trade-off.

## Frameworks Introduced

- **Ensemble forecasting**: Run a model repeatedly with reasonable variations in initial conditions so the spread of results represents uncertainty.
  - **When to use**: Whenever the underlying system is chaotic and a single forecast could imply false certainty.
  - **How**: Generate multiple forecasts, inspect their agreement or divergence, quantify predictability, and present a cone or range that supports decisions.
- **Data as public infrastructure**: Treat observations, records, models, and access systems as shared foundations from which both public services and private products can be built.
  - **When to use**: When evaluating whether a data asset should be hidden, sold, or made accessible.
  - **How**: Trace who paid to collect it, whether others can reproduce or improve on it, what public value is lost if access disappears, and how it becomes actionable knowledge.
- **Human-centered warning**: People respond to trusted human interpreters and concrete consequences, not necessarily to raw technical facts.
  - **When to use**: When accurate information is not changing behavior or when users cannot translate probabilities into action.
  - **How**: Study the receiver, use local trusted voices, state what the event means for a person’s home or safety, and preserve uncertainty without making the message inert.
- **The odd group in the room**: Add the missing discipline or stakeholder that can explain behavior the dominant technical group cannot.
  - **When to use**: When a scientific or operational team understands the physical threat but not the social response.
  - **How**: Invite outsiders early, let them shape the problem, and use small experiments to discover what works.
- **Intentionality in long-cycle systems**: Outcomes that do not happen naturally require explicit leadership, funding, and sequencing.
  - **When to use**: When an asset has long lead times, such as satellites, data archives, or scientific talent.
  - **How**: Decide what must be protected now, budget for successor capacity before the current asset fails, and keep the commitment visible.

## Key Concepts

- **National Oceanic and Atmospheric Administration (NOAA)**: Commerce Department agency that gathers weather, climate, ocean, and environmental data.
- **National Weather Service (NWS)**: Public forecasting and warning service whose observations underpin much private weather information.
- **Ensemble forecasting**: A forecast family created by varying initial conditions to expose uncertainty and predictability.
- **Cone of uncertainty**: A range communicating where a storm or outcome may go rather than presenting one path as certain.
- **Weather-Ready Nation**: Sullivan’s effort to make communities more resilient and responsive to weather threats.
- **Social science**: The behavioral expertise NOAA added to understand how people respond to risk information.
- **Data scientist**: A role Patil helped popularize for using data to discover patterns and make decisions.
- **ForecastAdvisor**: Floehr’s long-running comparison of forecast accuracy using a large archive of predictions.
- **Public good**: A broadly useful resource, such as weather data, whose social value exceeds one private buyer’s use.
- **Signal versus noise**: The problem of separating meaningful patterns from the mass of data and events around them.

## Mental Models

- **Measure the threat and the receiver**: A technically correct warning can fail if the institution has not studied how users perceive and act on it.
- **Data pipeline, not data pile**: Collection is only the first stage; access, computation, interpretation, and communication determine whether data changes odds.
- **Blackjack rather than prophecy**: Better forecasting shifts probabilities over time; it does not make every individual prediction certain.
- **Network stability**: Ask whether removing one node collapses a network or leaves it resilient, whether the network is a storm, a terrorist cell, a power grid, or an organization.

## Anti-patterns

- **Raw-data dumping**: Providing jargon, wind speeds, or probabilities without explaining what the user should expect and do.
- **Treating nonresponse as stupidity**: Blaming citizens before investigating trust, prior experience, social networks, and the credibility of the messenger.
- **Single-forecast certainty**: Hiding model disagreement instead of showing a range and the conditions under which predictability is low.
- **Anecdote-based superiority**: Selecting the forecasts on which a private service looks best while keeping the full record and severe-weather calls private.
- **Private capture of public infrastructure**: Restricting taxpayer-funded observations or warnings so a commercial intermediary can charge for access.
- **One-asset thinking**: Buying a single satellite or launching one program without funding the successors and staff required to keep the capability alive.
- **Trying to transform from the top without a network**: Designing a mission alone, or allowing the loudest specialist to ignore the outsiders who understand users.

## Worked Example

On May 16, 2017, the Storm Prediction Center tested a tornado model that produced consistent tornadoes even when its atmospheric assumptions varied. The model did not give Elk City a perfect future picture, but it increased the Weather Service’s confidence that a dangerous storm was forming and changed the language of its communication to a “tornado emergency.” Lonnie Risenhoover, a local emergency manager who trusted the Weather Service, used the additional information while driving into the storm, reported what he saw, and called for the warning before he otherwise might have done so. The sirens sounded about thirty minutes before the tornado hit, and more than two hundred homes and thirty-eight businesses were destroyed, yet the town recorded one fatality and eight bruises. The result came from a chain rather than a single model: experimental science, a public warning service, a trusted local intermediary, and residents who treated the warning as real. It illustrates Sullivan and Klockow’s point that the goal is not merely to describe the storm but to make the risk imaginable enough to change behavior. It also preserves the boundary of the evidence: the prototype was used by chance and the chapter does not claim that the same outcome is guaranteed in every storm.

## Key Takeaways

1. Model uncertainty explicitly; a range can be more decision-useful than a falsely precise point forecast.
2. Study the people who receive information as carefully as the phenomenon being measured.
3. Keep public data accessible and trace how it supports both safety and private innovation.
4. Use large records and aggregate comparisons to test marketing claims and selective anecdotes.
5. Add the missing behavioral, local, or domain group before assuming the technical team understands the whole problem.
6. Protect successor assets, archives, and talent before a long-cycle public capability reaches failure.

## Connects To

- **Chapter 1 — Prologue: Lost in Transition**: Data and expertise are part of the institutional memory a transition can either preserve or discard.
- **Chapter 2 — I. Tail Risk**: Ensemble models and open data improve the imagination needed to see systemic and low-visibility risks.
- **Chapter 3 — II. People Risk**: The value of a public program depends on who interprets it, who benefits, and whose motives shape access.
- **Chaos theory**: Small changes in initial conditions, information, or network structure can create large downstream differences.
