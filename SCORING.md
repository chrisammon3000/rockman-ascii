# Rockman Scoring System

This document outlines the scoring algorithm for the Rockman game.

## Scoring Components

1. **Base Score**: Start with 0 points.

2. **Time-based Scoring**:
   - Add 1 point for every second survived.

3. **Rock Avoidance Bonus**:
   - Add 5 points for each rock that falls off the bottom of the screen without hitting Rockman.

4. **Near-miss Bonus**:
   - Add 2 points for each rock that passes within 1 unit of Rockman without hitting him.

5. **Difficulty Multiplier**:
   - Start at 1.0 and increase by 0.1 every 30 seconds.
   - Multiply all points earned by this multiplier.

6. **Combo System**:
   - Keep track of consecutive rocks avoided without moving.
   - For each rock avoided in a combo, multiply its points by the combo count.
   - Reset the combo when Rockman moves or a rock passes too far from him.

7. **Level-up Bonus**:
   - Award 100 points every time the rocks_per_wave increases.

8. **Survival Milestone Bonuses**:
   - 500 points at 1 minute
   - 1000 points at 2 minutes
   - 2000 points at 5 minutes

9. **Score Decay**:
   - Subtract 1 point every 10 seconds after the 5-minute mark.

10. **Teleport Penalty**:
    - Subtract 50 points (multiplied by the current difficulty multiplier) each time Rockman teleports.

## Final Score Calculation

The final score is calculated as follows:

$$
\text{Final Score} = (\text{Base Score} + \text{Time Score} + \text{Rock Avoidance Score} + \text{Near-Miss Score} + \text{Level-up Bonuses} + \text{Survival Milestone Bonuses} - \text{Score Decay}) \times \text{Difficulty Multiplier}
$$

## Scoring Strategy

This scoring system encourages both survival and skillful play:
- Players are rewarded for staying alive as long as possible.
- Dodging rocks and achieving near-misses provide additional points.
- The combo system rewards players for staying in one place, adding risk and strategy.
- The difficulty multiplier ensures that points earned later in the game are worth more.
- Survival milestones give players short-term goals to aim for.
- The score decay prevents excessively high scores in very long games.
- The teleport penalty discourages overuse of the teleport ability, adding a risk-reward element to this powerful move.

Players can choose between playing it safe for consistent point gain or taking risks for higher scores.

## Implementation Considerations

When implementing this scoring system:
1. Keep track of the player's position and movement to calculate combos and near-misses.
2. Use a timer to manage time-based scoring, difficulty increases, and milestone bonuses.
3. Implement an efficient method to detect when rocks fall off the screen or pass near Rockman.
4. Update and display the current score in real-time during gameplay.
5. Consider adding visual or audio cues for significant scoring events (e.g., reaching a milestone or achieving a high combo).

## Future Enhancements

Possible future enhancements to the scoring system could include:
1. Special bonus rocks that are worth more points.
2. Achievements or badges for reaching certain score thresholds or performing specific feats.
3. A global high score leaderboard to encourage competition among players.
4. Different scoring modes or difficulties that players can choose from.

Remember to balance the scoring system through playtesting to ensure it remains fair and enjoyable for players of all skill levels.
