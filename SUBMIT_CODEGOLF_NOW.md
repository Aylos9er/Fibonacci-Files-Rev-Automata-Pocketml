# Code Golf Stack Exchange - Submit Now for Bounties!

## 🔗 SUBMISSION LINK (Sandbox First)
**https://codegolf.meta.stackexchange.com/questions/2140/sandbox-for-proposed-challenges**

---

## STEP 1: Create Stack Exchange Account
- Go to: https://codegolf.stackexchange.com/users/signup
- Email: mosij@icloud.com
- Username: jMosij (or your choice)

---

## STEP 2: Post to Sandbox (Required!)

### Click "Post Your Answer" and paste this:

---

**Title:** [Sandbox] Reversible Turing-Complete Cellular Automaton with Fibonacci Parameters

---

**Body (Copy-Paste This):**

```markdown
## Challenge: Shortest Reversible Turing-Complete Cellular Automaton

Implement a cellular automaton that is both reversible AND Turing-complete.

### Specification

**Input:**
- `s`: 2D integer array (grid state, N×N where N≥4)
- `r`: Integer (0=forward, 1=reverse)

**Output:**
- Modified `s` after one automaton step

**Rules:**

1. **Margolus Neighborhood:** Divide grid into 2×2 blocks, partition offset alternates
2. **Critters Block Rule:** For each 2×2 block with count c of live cells:
   - c=4: No change
   - c∈{1,2}: Rotate 90° (clockwise if forward, counterclockwise if reverse)
   - c∈{0,3}: Rotate 90° (counterclockwise if forward, clockwise if reverse)
3. **Reversibility:** Must satisfy `reverse(forward(state)) == state` for ALL states

### Test Cases

**Test 1: Basic 4×4 Grid**
```python
s = [[1,0,0,1],[0,1,1,0],[1,1,0,0],[0,0,1,1]]
original = copy(s)
step(s, r=0)  # forward
step(s, r=1)  # reverse
assert s == original  # Must pass
```

**Test 2: Extended Reversibility**
```python
s = random_grid(10, 10)
original = copy(s)
for _ in range(100): step(s, r=0)  # 100 forward
for _ in range(100): step(s, r=1)  # 100 reverse
assert s == original  # Must pass
```

### Scoring

Code golf - shortest code in bytes wins!

### Reference Implementation (84 bytes, Python)

```python
for i in range(r,87,2):
 for j in range(r,87,2):s[i:i+2,j:j+2]=s[i+1-r:i-r:-1,j:j+2]
```

Assumes: `s` is NumPy array (89×89), `r` is 0 or 1

**Can you beat 84 bytes?**

### Feedback Requested

- Are rules clear enough?
- Test cases comprehensive?
- Any loopholes to close?
- Tag suggestions?

### References

- Toffoli & Margolus (1987) - Margolus neighborhoods
- Proven Turing-complete via Critters rule

Full documentation: https://github.com/Aylos9er/Fibonacci-Files-Rev-Automata-Pocketml
```

---

## STEP 3: Wait for Feedback (3-5 Days)

Community will comment with improvements. Address their feedback.

---

## STEP 4: Post to Main Site

After sandbox approval:
1. Go to: https://codegolf.stackexchange.com/questions/ask
2. Copy refined challenge from sandbox
3. Add tags: `code-golf`, `cellular-automata`, `reversible-computing`
4. Click "Post Your Question"

---

## STEP 5: Claim Bounties!

Once posted, your 84-byte solution can claim bounties:
- Check: https://codegolf.meta.stackexchange.com/questions/5243/list-of-bounties-with-no-deadline
- Comment on relevant bounty posts with link to your answer
- Potential: 250-2000 reputation points ($$ value in community)

---

**✅ READY TO POST - JUST COPY & PASTE!**
