# Cheatsheet

## Book map

| Need | Read first |
|---|---|
| Motivate a difficult technical team | [ch03](chapters/ch03-building-a-team.md), [ch15](chapters/ch15-canards.md) |
| Manage architecture and scope | [ch04](chapters/ch04-wallachs-golden-moment.md), [ch06](chapters/ch06-flying-upside-down.md) |
| Debug an intermittent system | [ch07](chapters/ch07-la-machine.md), [ch10](chapters/ch10-the-case-of-the-missing-nand-gate.md) |
| Handle scarce resources | [ch02](chapters/ch02-the-wars.md), [ch12](chapters/ch12-pinball.md) |
| Finish and hand off | [ch14](chapters/ch14-the-last-crunch.md), [ch17](chapters/ch17-epilogue.md) |
| Examine technology’s social use | [ch13](chapters/ch13-going-to-the-fair.md) |

## Decision rules

1. **If the project is interesting but not a product:** define cost, speed, reliability, compatibility, documentation, manufacturing, and customer handoff.
2. **If a date is needed:** choose the earliest date that cannot yet be disproved, but replace it with test evidence as uncertainty falls.
3. **If scope is expanding:** protect the one-board/core path; postpone bells and whistles until the product works.
4. **If a person signs up:** give consequential ownership, a clear interface, support, and an escape valve.
5. **If a rare failure appears:** reproduce → instrument → trace history → isolate one dependency → repair → regress.
6. **If resources are scarce:** make the next win concrete, but expose constraints that affect technical or ethical decisions.
7. **If a benchmark passes:** check the exact configuration, real workload, reliability, documents, manufacturing, and downstream owner.
8. **If credit is being assigned:** separate environment, catalyst, design, implementation, integration, and handoff.

## Tells and countermeasures

| Tell | Likely risk | Countermeasure |
|---|---|---|
| “Nothing happens unless pushed” | Schedule inertia or hidden dependency | Name the next observable push and owner |
| Repeated missed dates | Credibility debt | Publish remaining tests and uncertainty |
| “It’s just noise” | Intermittent logic or stale state | Capture history and compare repeated traces |
| Long hours feel compulsory | Signing-up culture becoming coercive | Use an escape valve and reset workload |
| A fix passes one test, another fails | Repair or fixture changed system state | Restore production configuration and regress |
| Team only knows its local piece | Integration gap | Assign a system integrator and test joins |
| Launch story names executives | Collective work erased | Preserve a layered attribution record |

## Compact system model

**Opportunity** creates a hard challenge → **signing up** supplies ownership → **distributed control** makes parallel work possible → **quick-and-dirty scope** buys schedule → **diagnostics** turn behavior into evidence → **release gates** establish readiness → **handoff** changes ownership. At every stage, check the costs: secrecy, supplier fragility, scarce resources, burnout, and the loss of meaning after the next game disappears.
