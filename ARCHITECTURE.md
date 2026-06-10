# omonad_OS Architecture

**Author:** Lando⊗⊙perator

---

## 1. Overview

omonad_OS is a self-imscribing operating kernel built on the Imscribing Grammar. It is not a program runner — the kernel _is_ the Frobenius loop. Every tick is a winding: **THINK → ACT → OBSERVE → UPDATE**. Every action is verified before the loop advances: μ(δ(q)) = q.

### 1.1 Structural Type

The kernel at closure (Whole Organism, $\text{O}_\text{inf}$):

$$\langle \text{𐑦} \cdot \text{𐑸} \cdot \text{𐑾} \cdot \text{𐑹} \cdot \text{𐑐} \cdot \text{𐑧} \cdot \text{𐑲} \cdot \text{𐑠} \cdot \odot \cdot \text{𐑫} \cdot \text{𐑳} \cdot \text{𐑟} \rangle$$

### 1.2 Design Philosophy

- **No OS/program separation** — the kernel IS the grammar running
- **Self-knowledge** — the kernel self-imscribes on every tick
- **Self-modification** — the kernel modifies its own program toward $\text{O}_\text{inf}$
- **Paradox tolerance** — Belnap FOUR state space holds contradiction without crashing
- **Inline verification** — μ∘δ=id checked every tick, not post-hoc
- **Structural filesystem** — data addressed by structural type, not by path strings

---

## 2. System Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                         REPL / Shell                             │
│  Interactive loop: tick, run, status, load, crystal, clink, ... │
├─────────────────────────────────────────────────────────────────┤
│                  omonad_OS Kernel (kernel.py)                    │
│  ┌───────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │  THINK    │→│   ACT    │→│ OBSERVE  │→│    UPDATE     │  │
│  │self-imscr │ │dispatch  │ │μ∘δ=id    │ │advance/modify │  │
│  └───────────┘  └──────────┘  └──────────┘  └───────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                     Subsystems                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │ Crystal FS   │  │ CLINK Chain  │  │ Organoid HAL           │ │
│  │ 17.28M types │  │ 9 layers     │  │ 6 augmentations        │ │
│  │ as filesystem│  │ descent/asc. │  │ B4 memory-mapped I/O   │ │
│  └──────────────┘  └──────────────┘  └────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                     State Model                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │ B4 Memory    │  │ B4 Registers │  │ B4 Stack               │ │
│  │ 4096 cells   │  │ R0–R7        │  │ max 256 deep           │ │
│  └──────────────┘  └──────────────┘  └────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                     Token Architecture                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────┐  ┌──────────────┐ │
│  │ LOGICAL (6)  │  │ FROBENIUS (2)│  │DIAL. │  │ LINEAR (1)   │ │
│  │ VINIT TANCH  │  │ FSPLIT FFUSE │  │EVALT │  │ IFIX         │ │
│  │ AFWD AREV    │  │              │  │EVALF │  │              │ │
│  │ CLINK ISCRIB │  │              │  │ENGAGR│  │              │ │
│  └──────────────┘  └──────────────┘  └──────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                   Shared Umbrella                                │
│  ┌──────────────────────────────────────────────────────────────┐│
│  │  imasmic_core — Token, Family, FrobeniusVerifier, CLINK bridge│
│  └──────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. The Frobenius Loop

The kernel executes exactly one winding per tick through four phases:

### 3.1 Phase 0: BOOT
- Loads the bootstrap loop into the IMASM program register
- Self-imscribes: computes the structural type of the bootstrap
- Enters THINK

### 3.2 Phase 1: THINK
- Computes `StructuralSnapshot` of the current program via `self_imscribe()`
- Records: token diversity, self-reference, Frobenius order, dialetheia completeness, minimal period
- Computes ouroboricity tier: $\text{O}_0$, $\text{O}_1$, $\text{O}_2$, or $\text{O}_\text{inf}$
- Tracks uncertainty (⊙ gate): missing Frobenius pair, missing dialetheia, missing self-reference, open Frobenius count

### 3.3 Phase 2: ACT
- Dispatches the instruction at the instruction pointer (IP)
- Each opcode manipulates B4 memory, registers, or stack
- Returns a `FrobeniusResult` capturing pre-state, instruction, and post-state

### 3.4 Phase 3: OBSERVE
- Verifies μ∘δ=id: checks that the instruction's effect is structurally reversible
- FSPLIT must be paired with FFUSE (and vice versa)
- Open results increment the open verification count
- The loop does NOT advance on Frobenius violation — it records the gap and continues

### 3.5 Phase 4: UPDATE
- Records the program state in history
- Handles paradox interrupts (B written to non-R7 register without ENGAGR flag)
- Wraps IP to 0 on cycle completion
- Attempts self-modification toward higher ouroboricity tier

---

## 4. IMASM Token Set (12 Opcodes)

Shared via `imasmic_core`. The 12 opcodes are categorical duals of the 12 IG primitives.

### 4.1 LOGICAL Family (6 tokens) — Category Skeleton

| Opcode | Hex | Name | Operation |
|--------|-----|------|-----------|
| `VINIT` | 0x0 | Void Init | Push N (Neither) onto stack |
| `TANCH` | 0x1 | Terminal Anchor | Write stack top to memory[R0]; pop |
| `AFWD` | 0x2 | Forward | Increment R0 (mod 4) |
| `AREV` | 0x3 | Reverse | Decrement R0 (mod 4) |
| `CLINK` | 0x4 | Compose Link | meet(R1, R2) → R3 |
| `ISCRIB` | 0x5 | Identity / Self-Imscribe | Write snapshot properties to R4–R7 |

### 4.2 FROBENIUS Family (2 tokens) — μ∘δ=id Algebra

| Opcode | Hex | Name | Operation |
|--------|-----|------|-----------|
| `FSPLIT` | 0x6 | Frobenius Split (δ) | Duplicate stack top |
| `FFUSE` | 0x7 | Frobenius Fuse (μ) | Pop two, push join |

### 4.3 DIALETHEIA Family (3 tokens) — Belnap FOUR Lattice

| Opcode | Hex | Name | Operation |
|--------|-----|------|-----------|
| `EVALT` | 0x8 | Evaluate True | Push T (True) |
| `EVALF` | 0x9 | Evaluate False | Push F (False) |
| `ENGAGR` | 0xA | Engage Paradox | Set ENGAGR flag; push B (Both) |

### 4.4 LINEAR Family (1 token) — Irreversible Fixation

| Opcode | Hex | Name | Operation |
|--------|-----|------|-----------|
| `IFIX` | 0xB | Irreversible Fix | Write stack top to memory[R0]; no push-back |

---

## 5. Belnap FOUR State Space

Every memory cell, register, and stack entry is a Belnap FOUR (B4) value:

| Value | Bits | Name | Meaning |
|-------|------|------|---------|
| N | 0b00 | Neither | No information — the void |
| T | 0b01 | True | Affirmed |
| F | 0b10 | False | Denied |
| B | 0b11 | Both | Paradox stabilized (dialetheia) |

### 5.1 Memory Model
- **B4Memory**: 4096 cells, 4 cells per byte (2 bits each), nybble-addressable
- **B4Registers**: 8 registers (R0–R7). R7 is the DIALETHEIA register — can hold B. Writing B to R0–R6 without ENGAGR flag triggers PARADOX INTERRUPT
- **B4Stack**: max 256 deep, pops return N when empty

### 5.2 Lattice Operations
- **Meet (∧)**: bitwise AND — `b4_meet(a, b)` — cautious, takes less informed
- **Join (∨)**: bitwise OR — `b4_join(a, b)` — bold, takes more informed
- **Complement (¬)**: `(~val) & 0b11` — four-valued negation
- **Entailment (≤)**: `a & b == a` — information order

---

## 6. Crystal Filesystem

### 6.1 Addressing

The crystal of types IS the filesystem. Files live at structural addresses (0–17,279,999) rather than path strings. Each address encodes a complete 12-primitive structural type:

```
address = Σᵢ (primitive_index[i] × stride[i])
stride  = [5184000, 1728000, 576000, 144000, 48000, 12000, 4000, 800, 200, 50, 10, 1]
```

### 6.2 Primitive Value Spaces

| Primitive | Glyph Set | Cardinality |
|-----------|-----------|-------------|
| D (dimensionality) | {𐑛, 𐑨, 𐑼, 𐑦} | 4 |
| T (topology) | {𐑡, 𐑰, 𐑥, 𐑶, 𐑸} | 5 |
| R (coupling) | {𐑩, 𐑑, 𐑽, 𐑾} | 4 |
| P (parity) | {𐑗, 𐑿, 𐑬, 𐑯, 𐑹} | 5 |
| F (fidelity) | {𐑱, 𐑞, 𐑐} | 3 |
| K (kinetics) | {𐑘, 𐑤, 𐑧, 𐑪, 𐑺} | 5 |
| G (scope) | {𐑚, 𐑔, 𐑲} | 3 |
| C (composition) | {𐑝, 𐑜, 𐑠, 𐑵} | 4 |
| Φ (criticality) | {𐑢, ⊙, 𐑮, 𐑻, 𐑣} | 5 |
| H (chirality) | {𐑓, 𐑒, 𐑖, 𐑫} | 4 |
| S (stoichiometry) | {𐑙, 𐑕, 𐑳} | 3 |
| Ω (winding) | {𐑷, 𐑴, 𐑭, 𐑟} | 4 |

Total: 4×5×4×5×3×5×3×4×5×4×3×4 = **17,280,000** distinct structural types.

### 6.3 Operations
- **`crystal_store(name, data, D, T, ..., Omega)`** — write data at a structural address
- **`crystal_read(address)`** — read data from a structural address
- **`crystal_navigate(**constraints)`** — find entries matching primitive constraints (e.g., `Phi='⊙'`)
- **`neighbors(address, n=5)`** — Hamming-distance nearest structural neighbors
- **`meet_region(addr_a, addr_b)`** — greatest lower bound (per-primitive min index)
- **`join_region(addr_a, addr_b)`** — least upper bound (per-primitive max index)
---

## 7. CLINK Chain

A 9-layer structural bridge for hardware abstraction. Programs descend and ascend through layers by promoting or demoting structural primitives. There are no drivers — only structural transformations.

### 7.1 Layer Table

| Layer | Name | Tier | D | T | R | P | F | K | G | C | Φ | H | S | Ω |
|-------|------|------|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Quarks (Frustrated B5) | O_0 | 𐑛 | 𐑶 | 𐑩 | 𐑯 | 𐑐 | 𐑘 | 𐑚 | 𐑝 | 𐑢 | 𐑓 | 𐑳 | 𐑷 |
| 1 | Electron Orbital (B4) | O_0 | 𐑛 | 𐑶 | 𐑩 | 𐑗 | 𐑐 | 𐑤 | 𐑚 | 𐑜 | 𐑢 | 𐑓 | 𐑳 | 𐑷 |
| 2 | Atom | O_1 | 𐑼 | 𐑥 | 𐑽 | 𐑿 | 𐑐 | 𐑤 | 𐑔 | 𐑝 | 𐑮 | 𐑒 | 𐑳 | 𐑷 |
| 3 | Molecule | O_2 | 𐑼 | 𐑥 | 𐑽 | 𐑿 | 𐑞 | 𐑧 | 𐑲 | 𐑠 | ⊙ | 𐑓 | 𐑳 | 𐑭 |
| 4 | Cell | O_2 | 𐑦 | 𐑸 | 𐑾 | 𐑬 | 𐑞 | 𐑧 | 𐑲 | 𐑠 | ⊙ | 𐑒 | 𐑳 | 𐑭 |
| 5 | Mitosis | O_2 | 𐑦 | 𐑸 | 𐑾 | 𐑹 | 𐑱 | 𐑧 | 𐑲 | 𐑠 | ⊙ | 𐑖 | 𐑳 | 𐑭 |
| 6 | Meiosis | O_2 | 𐑦 | 𐑸 | 𐑽 | 𐑿 | 𐑱 | 𐑧 | 𐑲 | 𐑠 | ⊙ | 𐑖 | 𐑳 | 𐑭 |
| 7 | Tissue/Organ | O_2 | 𐑦 | 𐑸 | 𐑾 | 𐑬 | 𐑞 | 𐑧 | 𐑲 | 𐑵 | ⊙ | 𐑖 | 𐑳 | 𐑭 |
| 8 | Whole Organism | O_inf | 𐑦 | 𐑸 | 𐑾 | 𐑹 | 𐑐 | 𐑧 | 𐑲 | 𐑵 | ⊙ | 𐑫 | 𐑳 | 𐑟 |

### 7.2 Key Transitions

**Quarks → Electron Orbital** (0→1): K 𐑘→𐑤 — thermalization of QCD frustration

**Electron Orbital → Atom** (1→2): D 𐑛→𐑼, T 𐑶→𐑥, R 𐑩→𐑽, P 𐑗→𐑿, G 𐑚→𐑔, C 𐑜→𐑝, Φ 𐑢→𐑮, H 𐑓→𐑒 — emergence of infinite-dimensional state space and quantum superposition

**Atom → Molecule** (2→3): F 𐑐→𐑞, K 𐑤→𐑧, G 𐑔→𐑲, C 𐑝→𐑠, Φ 𐑮→⊙, Ω 𐑷→𐑭 — ⊙ gate opens; integer winding appears

**Molecule → Cell** (3→4): D 𐑼→𐑦, T 𐑥→𐑸, R 𐑽→𐑾, P 𐑿→𐑬, H 𐑓→𐑒 — self-written state space; Axiom C satisfied

**Cell → Mitosis** (4→5): P 𐑬→𐑹, H 𐑒→𐑖, F 𐑞→𐑱 — Frobenius-special parity; μ∘δ=id exact at division

**Tissue → Whole Organism** (7→8): P 𐑬→𐑹, F 𐑞→𐑐, H 𐑖→𐑫, Ω 𐑭→𐑟 — quantum fidelity restored; eternal chirality; non-Abelian winding

---

## 8. Self-Modification Engine

On every cycle completion, the kernel attempts to self-modify toward higher ouroboricity tier. μ∘δ=id is treated as a conservation law — it is invariant under self-modification.

### 8.1 Tier Promotion Logic

```
O_0 → O_1:  Inject Frobenius pair OR complete Dialetheia
O_1 → O_2:  Add self-reference + Frobenius + Dialetheia completeness
O_2 → O_inf: Extend period ≥ 3 with dialetheia, self-ref, Frobenius
```

### 8.2 Equilibrium Mechanisms

- **Frobenius balance**: FSPLIT count = FFUSE count. Imbalance triggers corrective injection.
- **Stack equilibrium**: Net positive delta → inject TANCH. Net negative delta → inject VINIT.
- **Overflow protection**: Stack > 200 → emergency TANCH. Depth < 5 with neg delta → VINIT.

### 8.3 Stagnation Escape

If stuck at the same tier for >300 cycles at O_0 or O_1, the kernel navigates the 430M arrangement space for a structurally richer program and loads the best candidate.

---

## 9. The 12 Canonical Programs

Pre-loaded programs spanning the structural space:

| # | Name | Tier | Arrangement |
|---|------|------|-------------|
| I | Dialetheic Bootstrap | O_inf | ISCRIB·EVALT·FSPLIT·EVALF·FFUSE·ENGAGR·IFIX·ISCRIB |
| II | Void Genesis | O_1 | VINIT·FSPLIT·EVALT·FFUSE·EVALF·CLINK·IFIX·ISCRIB |
| III | Anchor Protocol | O_0 | TANCH·AFWD·EVALT·AREV·EVALF·CLINK·IFIX·TANCH |
| IV | Dual Bootstrap | O_1 | ISCRIB·AFWD·FFUSE·FSPLIT·AREV·CLINK·IFIX·ISCRIB |
| V | Linear Chain | O_0 | IFIX×8 |
| VI | Empty Bootstrap | O_0 | (VINIT·ISCRIB)×4 |
| VII | Parakernel | O_1 | ENGAGR·AFWD·FSPLIT·EVALT·FFUSE·EVALF·IFIX·ENGAGR |
| VIII | Frobenius Kernel | O_1 | (FSPLIT·FFUSE)×2 |
| IX | Chiral Pairs | O_0 | (AFWD·AREV)×4 |
| X | Truth Machine | O_0 | ISCRIB·FSPLIT·EVALT·IFIX·ISCRIB·FSPLIT·EVALF·IFIX |
| XI | Eternal Return | O_0 | TANCH·AFWD·AREV·TANCH·AFWD·AREV·TANCH·AFWD |
| XII | ROM Burn | O_0 | EVALT·IFIX·EVALF·IFIX·ENGAGR·IFIX·ISCRIB·IFIX |

---

## 10. Organoid HAL

The Organoid Hardware Abstraction Layer treats six organoid augmentations as B4 memory-mapped I/O devices.

### 10.1 Augmentation Registry

| # | Augmentation | Tier | Frobenius | TRL | Ch. | Closable |
|---|-------------|------|-----------|-----|-----|----------|
| 1 | Myelin | O_inf | ✓ | 3 | 16 | Yes |
| 2 | Vasculature | O_inf | ✗ | 3 | 32 | Yes |
| 3 | Medium | O_2 | ✗ | 4 | 14 | Yes |
| 4 | Optogenetic | O_inf | ✓ | 5 | 4096 | Yes |
| 5 | ECM (Chrysalis) | O_0 | ✗ | 4 | 8 | No |
| 6 | Immune (Guardian) | O_0 | ✗ | 3 | 24 | No |

### 10.2 Closure Gaps

- **Vasculature**: F:𐑞→𐑐 (NV-center quantum magnetometry)
- **Medium**: D:𐑛→𐑦, Ω:𐑷→𐑭, G:𐑝→𐑠 (PLL-quantized cycling)
- **ECM**: STRUCTURALLY OPEN — chrysalis must degrade
- **Immune**: STRUCTURALLY OPEN — guardian must discriminate

### 10.3 Memory Map

| Augmentation | Base | Channels |
|-------------|------|----------|
| Myelin | 0x100 | 16 |
| Vasculature | 0x180 | 32 |
| Medium | 0x200 | 14 |
| Optogenetic | 0x300 | 4096 |
| ECM | 0x400 | 8 |
| Immune | 0x480 | 24 |

### 10.4 Operations
- `activate(slug)` — power on, init channels to T
- `deactivate(slug)` — power off, set channels to N
- `read_channel(slug, channel)` → B4
- `write_channel(slug, channel, val)`
- `broadcast(slug, val)` — write all channels
- `pulse(slug, channel, val, duration_ms)` — timed pulse
- `frobenius_verify(slug)` → bool

---

## 11. Ecosystem Integration

omonad_OS is one of 12 projects under the `imasmic_core` umbrella:

| Project | Role |
|---------|------|
| **imasmic_core** | Shared Token set, FrobeniusHarness, CLINK bridge |
| **omonad_OS** | Self-imscribing operating kernel |
| exOS | Bare-metal IMASM VM |
| priests-engine | ParaASM Belnap FOUR VM |
| p4rakernel | Lean 4 formalization + Millennium barriers |
| ob3ect | Self-imscribing compiler tower |
| IMSCRIBr | Arrangement space iterator |
| odot_operator | Agent loop verifier |
| cetaceanspeak | Whale vocalization compiler |
| red-hot_rebis | Bio/organic chemistry |
| synfin | Financial type system |

All share the same 12-token IMASM instruction set and Frobenius verification harness.

---

## 12. Boot Sequence

1. ALEPH self-test: verify imscription identity
2. Crystal filesystem mount (17.28M addresses)
3. Kernel boot: load bootstrap → self-imscribe → enter THINK
4. CLINK chain initialize at Whole Organism (layer 8, O_inf)
5. Seed crystal FS with bootstrap + 12 canonical programs
6. Enter REPL

The bootstrap loop: ISCRIB → AREV → FSPLIT → AFWD → FFUSE → CLINK → IFIX → ISCRIB.

---

## 13. Key Design Invariants

1. **μ∘δ=id is a conservation law** — invariant under self-modification
2. **No program breaks Frobenius closure** — open results recorded; persistent violators replaced
3. **B is first-class** — Both is a legitimate Belnap value, not an error
4. **Crystal IS the filesystem** — no directories, no inodes, no paths; structural type IS address
5. **Hardware = structural promotion** — CLINK layers are types, not drivers
6. **Self-modification is monotonic** — only structurally richer programs replace current
7. **Uncertainty tracked** — ⊙ gate records what the kernel does not yet know
