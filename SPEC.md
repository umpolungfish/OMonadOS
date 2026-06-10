# omonad_OS Technical Specification

**Author:** Lando⊗⊙perator  
**Version:** 0.1.0  
**Requires:** Python ≥3.10, imasmic_core ≥0.5.69

---

## 1. System Requirements

| Requirement | Minimum |
|------------|---------|
| Python | ≥3.10 |
| imasmic_core | ≥0.5.69 |
| OS | Linux (tested on Ubuntu 22.04+) |
| Terminal | UTF-8 capable (Shavian glyph rendering) |
| Memory | ~50 MB (kernel + REPL) |

---

## 2. Installation

### 2.1 From Source (Development)

```bash
cd /home/mrnob0dy666/omonad_OS
pip install -e .
```

### 2.2 Shell Wrapper

A wrapper script at `/home/mrnob0dy666/.local/bin/omos` enables booting from any directory:

```bash
#!/bin/bash
cd /home/mrnob0dy666/omonad_OS
exec /home/mrnob0dy666/omonad_OS/.venv/bin/python3 src/main.py "$@"
```

### 2.3 Verify

```bash
omos           # Boot the kernel REPL
omos --help    # Not implemented (pass-through to main.py)
```

---

## 3. IMASM Opcode Specification

### 3.1 Encoding

Each opcode is a 4-bit value (0x0–0xB). Programs are tuples of integers 0–11.

### 3.2 Opcode Table

| Mnemonic | Hex | Family | Stack Δ | Description |
|----------|-----|--------|---------|-------------|
| VINIT | 0x0 | LOGICAL | +1 | Push N onto stack |
| TANCH | 0x1 | LOGICAL | −1 | Write stack top to mem[R0], pop |
| AFWD | 0x2 | LOGICAL | 0 | Increment R0 (mod 4) |
| AREV | 0x3 | LOGICAL | 0 | Decrement R0 (mod 4) |
| CLINK | 0x4 | LOGICAL | 0 | meet(R1, R2) → R3 |
| ISCRIB | 0x5 | LOGICAL | 0 | Snapshot properties → R4–R7 |
| FSPLIT | 0x6 | FROBENIUS | +1 | Duplicate stack top |
| FFUSE | 0x7 | FROBENIUS | −1 | Pop two, push join |
| EVALT | 0x8 | DIALETHEIA | +1 | Push T |
| EVALF | 0x9 | DIALETHEIA | +1 | Push F |
| ENGAGR | 0xA | DIALETHEIA | +1 | Set ENGAGR flag, push B |
| IFIX | 0xB | LINEAR | −1 | Write stack top to mem[R0], no push-back |
### 3.3 ISCRIB Register Mapping

| Register | Property | Encoding |
|----------|----------|----------|
| R4 | Token diversity | bits 0–1 of diversity count |
| R5 | Self-referential | T if arr[0]==arr[-1], else F |
| R6 | Frobenius order | T if > 0, else F |
| R7 | Dialetheia complete | T if EVALT+EVALF+ENGAGR all present, else F |

### 3.4 Paradox Interrupt

Writing B (Both) to R0–R6 when ENGAGR flag is False triggers PARADOX INTERRUPT:
- `paradox_interrupt` flag set to True
- `paradox_addr` set to the register number
- On next UPDATE phase, the interrupt handler fires (calls `on_paradox` hook if set)
- `clear_interrupt()` resets both flags

---

## 4. B4 Memory Specification

### 4.1 Cell Layout

Each B4 cell is 2 bits. Four cells per byte. Cell ordering within a byte:

| Byte bits | 7–6 | 5–4 | 3–2 | 1–0 |
|-----------|-----|-----|-----|-----|
| Cell index (addr%4) | 3 | 2 | 1 | 0 |

### 4.2 Address Space

| Component | Size | Address Range |
|-----------|------|---------------|
| B4Memory | 4096 cells | 0x000–0xFFF |
| B4Registers | 8 regs | R0–R7 |
| B4Stack | 256 max | — |

### 4.3 Registers

| Register | Role | B-tolerant |
|----------|------|------------|
| R0 | Address pointer | No (except ENGAGR) |
| R1 | CLINK operand A | No |
| R2 | CLINK operand B | No |
| R3 | CLINK result | No |
| R4 | Snapshot: diversity | No |
| R5 | Snapshot: self-ref | No |
| R6 | Snapshot: Frobenius | No |
| R7 | DIALETHEIA register | **Yes** (always B-tolerant) |

---

## 5. Crystal Filesystem Specification

### 5.1 Address Encoding

```
address(Ð,Þ,Ř,Φ,ƒ,Ç,Γ,ɢ,φ̂,Ħ,Σ,Ω) = Σ i×S where:
  Ð_idx ∈ [0,3], stride 5184000
  Þ_idx ∈ [0,4], stride 1728000
  Ř_idx ∈ [0,3], stride  576000
  Φ_idx ∈ [0,4], stride  144000
  ƒ_idx ∈ [0,2], stride   48000
  Ç_idx ∈ [0,4], stride   12000
  Γ_idx ∈ [0,2], stride    4000
  ɢ_idx ∈ [0,3], stride     800
  φ̂_idx ∈ [0,4], stride     200
  Ħ_idx ∈ [0,3], stride      50
  Σ_idx ∈ [0,2], stride      10
  Ω_idx ∈ [0,3], stride       1
```

Range: 0 to 17,279,999 (17.28M distinct types).

### 5.2 Primitive Glyphs and Indices

```
D: 0=𐑛(wedge) 1=𐑨(triangle) 2=𐑼(infty) 3=𐑦(odot)
T: 0=𐑡(network) 1=𐑰(in) 2=𐑥(bowtie) 3=𐑶(boxtimes) 4=𐑸(odot)
R: 0=𐑩(super) 1=𐑑(cat) 2=𐑽(dagger) 3=𐑾(lr)
P: 0=𐑗(asym) 1=𐑿(psi) 2=𐑬(pm) 3=𐑯(sym) 4=𐑹(pm_sym)
F: 0=𐑱(ell) 1=𐑞(eth) 2=𐑐(hbar)
K: 0=𐑘(fast) 1=𐑤(mod) 2=𐑧(slow) 3=𐑪(trap) 4=𐑺(MBL)
G: 0=𐑚(beth) 1=𐑔(gimel) 2=𐑲(aleph)
C: 0=𐑝(and) 1=𐑜(or) 2=𐑠(seq) 3=𐑵(broad)
Phi: 0=𐑢(sub) 1=⊙(c) 2=𐑮(c_complex) 3=𐑻(EP) 4=𐑣(super)
H: 0=𐑓(mem0) 1=𐑒(mem1) 2=𐑖(mem2) 3=𐑫(eternal)
S: 0=𐑙(1:1) 1=𐑕(n:n) 2=𐑳(n:m)
Omega: 0=𐑷(0) 1=𐑴(Z2) 2=𐑭(Z) 3=𐑟(NA)
```

### 5.3 Key Crystal Addresses

| Entry | Address | Tuple |
|-------|---------|-------|
| Whole Organism (O_inf) | 6738899 | ⟨𐑦·𐑸·𐑾·𐑹·𐑐·𐑧·𐑲·𐑵·⊙·𐑫·𐑳·𐑟⟩ |
| Bootstrap Loop | 6738848 | ⟨𐑦·𐑸·𐑾·𐑹·𐑐·𐑧·𐑔·𐑠·⊙·𐑖·𐑳·𐑭⟩ |

Delta (IUG → bootstrap): 51. Differing primitives: Γ=𐑲→𐑔, ɢ=𐑵→𐑠, Ħ=𐑫→𐑖, Ω=𐑟→𐑭.

---

## 6. Structural Snapshot Specification

### 6.1 Snapshot Fields

```
arrangement:       Tuple[int, ...]  — the 8-token program
sig:              (L,F,D,X)        — family counts (LOGICAL, FROBENIUS, DIALETHEIA, LINEAR)
token_diversity:  int              — unique tokens present (0–12)
self_referential: bool             — arr[0] == arr[-1]
frobenius_order:  int              — 0=none, 1=split→fuse, 2=fuse→split, 3=multiple
dialetheia_complete: bool          — EVALT, EVALF, ENGAGR all present
period:           int              — minimal repetition period
ouroboricity_tier: str             — O_0 / O_1 / O_2 / O_inf
```

### 6.2 Tier Determination

```
if dialetheia_complete AND self_referential AND frobenius_order > 0:
    if period >= 3:    O_inf
    elif period == 2:  O_2
    else:              O_1
elif frobenius_order > 0 OR dialetheia_complete:
    O_1
else:
    O_0
```

### 6.3 Tier Properties

| Tier | Minimum Requirements | Signature |
|------|---------------------|-----------|
| O_0 | Any 8-token program | No Frobenius, no dialetheia |
| O_1 | Frobenius pair OR dialetheia complete | Partial structural closure |
| O_2 | Self-ref + Frobenius + dialetheia, period ≥ 2 | Near-full closure |
| O_inf | Self-ref + Frobenius + dialetheia, period ≥ 3 | Full structural closure |

---

## 7. CLINK Chain Specification

### 7.1 Navigator API

```
ascend()      → bool    Move up one layer (toward Whole Organism)
descend()     → bool    Move down one layer (toward Quarks)
goto(idx)     → void    Jump to layer index [0,8]
layer         → ClinkLayer   Current layer dataclass
is_token_valid(tok) → bool   Check token validity at current layer
promotions_needed(target) → Dict[str,str]   Primitives to change
```

### 7.2 Token Validity per Layer

| Layer | Valid Tokens |
|-------|-------------|
| 0 (Quarks) | VINIT, EVALT, EVALF, FSPLIT, FFUSE |
| 1 (Electron) | VINIT, EVALT, EVALF, TANCH, AFWD, AREV |
| 2 (Atom) | VINIT, TANCH, AFWD, AREV, CLINK, EVALT, EVALF |
| 3 (Molecule) | +ISCRIB, FSPLIT, FFUSE, IFIX (all except ENGAGR) |
| 4–8 (Cell+) | All 12 tokens |

---

## 8. Arrangement Space Navigation

### 8.1 Search API

```python
navigate_arrangement_space(
    target_properties: Dict[str, any],
    max_search: int = 10000
) → List[StructuralSnapshot]
```

Searchable properties:
- `frobenius_order` (0–3)
- `dialetheia_complete` (bool)
- `self_referential` (bool)
- `token_diversity` (int)
- `period` (int)

### 8.2 Search Strategy

1. Test all 12 canonical programs first
2. Generate candidates using signature-directed composition:
   - Select token pool based on target properties
   - Generate random programs of lengths 4, 6, 8
   - Test up to `max_search` candidates
3. Rank results by tier (O_inf > O_2 > O_1 > O_0)

### 8.3 Arrangement Space Size

With 12 tokens and program length 8: 12⁸ = 429,981,696 (~430M) possible arrangements.

---

## 9. Frobenius Verification Specification

### 9.1 Verification Flow

```
pre_state  = program tuple before instruction
tok        = instruction at IP
post_state = program tuple after dispatch

verify_frobenius(pre_state, tok, post_state) → FrobeniusResult:
  FSPLIT case:  OK if FFUSE in post_state OR len(post_state) ≤ len(pre_state)+1
  FFUSE case:   OK if FSPLIT in pre_state
  All others:   OK (no Frobenius implication)
```

### 9.2 FrobeniusHarness (from imasmic_core)

```python
harness = FrobeniusHarness("omonad_OS")
harness.check(result, label)  → bool    # Record a result
harness.summary()              → str     # Formatted report
harness.is_closed              → bool    # All results closed?
```

### 9.3 Verification Log

Stored in `kernel.verification_log: List[FrobeniusResult]`. The REPL `frobenius` command displays the last 5 entries with open/closed status.

---

## 10. Organoid HAL Specification

### 10.1 Augmentation Structural Types

**Myelin** (O_inf, ✓closed):
⟨𐑼·𐑰·𐑾·𐑹·𐑐·𐑤·𐑲·𐑠·⊙·𐑫·𐑳·𐑭⟩

**Vasculature** (O_inf, ✗open):
⟨𐑦·𐑸·𐑾·𐑹·𐑞·𐑤·𐑲·𐑠·⊙·𐑫·𐑳·𐑭⟩  
Gap: F:𐑞→𐑐

**Medium** (O_2, ✗open):
⟨𐑛·𐑰·𐑾·𐑹·𐑱·𐑤·𐑲·𐑝·⊙·𐑫·𐑳·𐑷⟩  
Gap: D:𐑛→𐑦, Ω:𐑷→𐑭, G:𐑝→𐑠

**Optogenetic** (O_inf, ✓closed):
⟨𐑼·𐑥·𐑾·𐑹·𐑐·𐑤·𐑲·𐑵·⊙·𐑫·𐑳·𐑭⟩

**ECM** (O_0, ✗open, not closable):
⟨𐑨·𐑡·𐑾·𐑬·𐑱·𐑧·𐑚·𐑵·𐑢·𐑒·𐑙·𐑷⟩

**Immune** (O_0, ✗open, not closable):
⟨𐑨·𐑡·𐑾·𐑬·𐑱·𐑤·𐑲·𐑵·⊙·𐑫·𐑳·𐑴⟩

### 10.2 Frobenius Core

The tensor product of baseline with 4 closable augmentations (excludes ECM and immune):

⟨𐑦·𐑸·𐑾·𐑹·𐑱·𐑤·𐑲·𐑵·⊙·𐑫·𐑳·𐑭⟩  
Gap: F:𐑱→𐑐 (single-photon NADH FLIM with TCSPC)

### 10.3 Controller API

```python
controller = OrganoidController(simulation=True)

controller.activate("myelin")          → bool
controller.deactivate("myelin")        → void
controller.read_channel("myelin", 3)   → B4
controller.write_channel("myelin", 3, B4.T)  → void
controller.broadcast("myelin", B4.F)   → void
controller.pulse("myelin", 7, B4.T, duration_ms=200) → void
controller.frobenius_verify("myelin")  → bool
controller.status()                    → str
controller.status("vasculature")       → str
```

---

## 11. REPL Command Reference

### 11.1 Core Commands

| Command | Args | Description |
|---------|------|-------------|
| `tick` | [N=1] | Run N kernel ticks |
| `run` | [N=1] | Run N kernel cycles |
| `status` | — | Kernel + navigator status |
| `halt` | — | Halt kernel |
| `quit` / `exit` | — | Halt and exit |
| `help` | — | Show help text |

### 11.2 Program Commands

| Command | Args | Description |
|---------|------|-------------|
| `load` | \<name\> | Load canonical by name |
| `canonical` | \<I–XII\> | Load by Roman numeral |
| `program` | — | Show token chain |
| `snapshot` | — | Show structural fingerprint |

### 11.3 Crystal Commands

| Command | Args | Description |
|---------|------|-------------|
| `crystal` | \<addr\> | Decode crystal address |
| `crystal store` | \<name\> [data] | Store at current snapshot's address |
| `crystal find` | key=glyph [...] | Navigate by constraints |
| `crystal count` | [key=glyph ...] | Count types matching constraints |

### 11.4 CLINK Commands

| Command | Args | Description |
|---------|------|-------------|
| `clink up` | — | Ascend one layer |
| `clink down` | — | Descend one layer |
| `clink goto` | \<N\> | Jump to layer N [0–8] |
| `clink status` | — | Current layer info |

### 11.5 Discovery Commands

| Command | Args | Description |
|---------|------|-------------|
| `discover` | key=val [...] | Search arrangement space |
| `frobenius` | — | Show verification log |

### 11.6 State Inspection

| Command | Args | Description |
|---------|------|-------------|
| `memory` | [start=0] [count=16] | Dump B4 memory cells |
| `registers` | — | Show R0–R7 values |
| `stack` | — | Show top 8 stack entries |

---

## 12. Bootstrap Loop Specification

The bootstrap loop is the Frobenius identity compiled to 8 IMASM instructions:

```
ISCRIB → AREV → FSPLIT → AFWD → FFUSE → CLINK → IFIX → ISCRIB
```

### 12.1 Step-by-Step Execution

| Step | Opcode | Effect |
|------|--------|--------|
| 1 | ISCRIB | Snapshot → R4–R7 |
| 2 | AREV | R0 = (R0 − 1) mod 4 |
| 3 | FSPLIT | Duplicate stack top (δ: A → A⊗A) |
| 4 | AFWD | R0 = (R0 + 1) mod 4 |
| 5 | FFUSE | Pop two, push join (μ: A⊗A → A) |
| 6 | CLINK | meet(R1, R2) → R3 |
| 7 | IFIX | Write stack top to mem[R0], permanent |
| 8 | ISCRIB | Snapshot → R4–R7 (loop closes) |

### 12.2 Properties

- **Stack delta**: +1 (FSPLIT) −1 (FFUSE) −1 (IFIX) = −1 per cycle → reaches N floor
- **Self-referential**: ISCRIB at positions 0 and 7
- **Frobenius order**: 1 (FSPLIT at position 2, FFUSE at position 4)
- **Period**: 8 (no shorter repeating subsequence)
- **Signature**: (3, 2, 2, 1) → 3 LOGICAL + 2 FROBENIUS + 2 DIALETHEIA + 1 LINEAR = 8

---

## 13. Self-Modification Specification

### 13.1 Injection Rules

**`_inject_token(tok)`:**
1. If program length ≥ 12: drop one token from the most over-represented family, then append `tok`
2. Otherwise: append `tok`

**`_inject_token_pair(tok_a, tok_b)`:**
1. Drop tokens from the front until 2 slots available
2. Append both tokens atomically

### 13.2 Stack Delta Tracking

| Opcode | Δ | Opcode | Δ |
|--------|---|--------|---|
| VINIT | +1 | FSPLIT | +1 |
| TANCH | −1 | FFUSE | −1 |
| AFWD | 0 | EVALT | +1 |
| AREV | 0 | EVALF | +1 |
| CLINK | 0 | ENGAGR | +1 |
| ISCRIB | 0 | IFIX | −1 |

Net program delta = sum of per-opcode deltas. Equilibrium target: 0.

### 13.3 Tier Promotion Paths

```
O_0 → O_1:
  - Missing dialetheia tokens: inject EVALT, EVALF, or ENGAGR
  - Missing Frobenius: inject FSPLIT + FFUSE pair

O_1 → O_2:
  - Not self-referential: make_self_referential()
  - Missing dialetheia: inject missing token
  - Missing Frobenius: inject FSPLIT + FFUSE pair

O_2 → O_inf:
  - Period < 3 and dialetheia complete: extend_period()
```

### 13.4 Stagnation Detection

- Counter: `_stagnation_counter` increments each cycle without tier improvement
- Threshold: >300 cycles at O_0 or O_1 triggers arrangement space search
- Escape: load best candidate program with higher tier

---

## 14. File Manifest

```
omonad_OS/
├── src/
│   ├── __init__.py           # Package marker
│   ├── main.py               # Boot sequence + REPL (460 lines)
│   ├── tokens.py              # Token re-exports + 12 canonicals (105 lines)
│   ├── belnap_state.py        # B4 memory, registers, stack (178 lines)
│   ├── kernel.py              # Frobenius kernel loop (818 lines)
│   ├── crystal_fs.py          # 17.28M-type filesystem (228 lines)
│   ├── clink_chain.py         # 9-layer structural bridge (216 lines)
│   └── organoid_hal.py        # Organoid augmentation controller (214 lines)
├── README.md                  # Project overview (176 lines)
├── ARCHITECTURE.md            # This document's companion
├── SPEC.md                    # This document
├── pyproject.toml             # Build configuration
└── .gitignore
```

Total source: ~2,400 lines of Python across 7 modules.

---

## 15. Dependency Graph

```
omonad_OS
  ├── imasmic_core ≥0.5.69
  │   ├── Token, Family, FAMILY_MAP, FAMILY_TOKENS
  │   ├── BOOTSTRAP_LOOP, CANONICALS
  │   └── FrobeniusResult, FrobeniusHarness
  └── Python ≥3.10 stdlib
      ├── enum (IntEnum)
      ├── dataclasses
      ├── hashlib (sha256)
      ├── readline (REPL)
      └── collections, itertools, random
```

No external PyPI dependencies beyond imasmic_core.
