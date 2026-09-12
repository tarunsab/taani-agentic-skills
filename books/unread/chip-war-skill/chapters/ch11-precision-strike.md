# Chapter 11: Precision Strike

## Core Idea

Vietnam revealed the limits of industrial firepower when bombs and missiles could not reliably hit their targets. Texas Instruments engineer Weldon Word used a simple laser sensor, a few transistors, and small wings to turn a standard “dumb” bomb into the Paveway guided bomb. The design principle was deliberately modest: cheap, familiar, simple, and reliable enough to train with and use widely. On May 13, 1972, twenty-four Paveways struck the Thanh Hoa Bridge after hundreds of earlier bombs had missed. The weapon did not win the guerrilla war, but it demonstrated how semiconductors could transform military effectiveness by improving the kill chain rather than increasing explosive volume.

## Frameworks Introduced

- **Cheap and familiar**: make a precision system inexpensive and simple enough for routine training and broad deployment.
  - When to use: when adoption and reliability matter more than maximum sophistication.
  - How: minimize connections, use existing platforms, and design for field familiarity.
- **Sensor-to-shooter kill chain**: acquire a target, track it, guide the weapon, and confirm the result.
  - When to use: when information processing can improve force effectiveness.

## Key Concepts

- **Paveway**: TI’s laser-guided bomb family.
- **Laser guidance**: using reflected laser energy to correct a weapon’s trajectory.
- **Vacuum tube**: a failure-prone predecessor to semiconductor guidance electronics.
- **Precision strike**: accurate delivery of force against a selected target.

## Mental Models

- Use “simple enough to train with” as a practical test for military technology.
- Think of sensors and guidance as force multipliers on existing platforms.

## Anti-patterns

- **Adding complexity before reliability**: the Sparrow missile’s vacuum tubes failed under humidity and vibration.
- **Equating better weapons with winning every war**: a precise weapon can solve an accuracy problem without solving a political conflict.

## Worked Example

Word started with the standard M-117 bomb, added wings, and placed a four-quadrant silicon sensor behind a lens. When the laser reflection shifted across the quadrants, circuitry moved the wings to correct the flight path. The Thanh Hoa Bridge went from zero hits in 638 attempts to direct hits with the new design.

## Key Takeaways

1. Improve the whole kill chain, not just the explosive payload.
2. Minimize connections and components when field reliability matters.
3. Use training frequency as a design requirement.

## Connects To

- **Ch 14**: precision strike becomes the Pentagon’s offset strategy.
- **Ch 27**: the Persian Gulf War validates the accumulated approach.
