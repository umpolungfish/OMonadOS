# $\odot\text{MonadOS}$

[![Language](https://img.shields.io/badge/language-Python-blue)](https://github.com/badges/shields)
[![IG Tier](https://img.shields.io/badge/IG-O%E2%88%9E-blueviolet)](https://github.com/badges/shields)
[![μ∘δ=id](https://img.shields.io/badge/%CE%BC%E2%88%98%CE%B4%3Did-closed-success)](https://github.com/badges/shields)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/badges/shields)
[![Author](https://img.shields.io/badge/author-Lando%E2%8A%97%E2%8A%99perator-informational)](https://github.com/badges/shields) [![Type](https://img.shields.io/badge/type-%E2%9F%A8%F0%90%91%A6%F0%90%91%B8%F0%90%91%BE%F0%90%91%B9%F0%90%91%90%F0%90%91%A7%F0%90%91%94%F0%90%91%9D%E2%8A%99%F0%90%91%96%F0%90%91%B3%F0%90%91%AD%E2%9F%A9-blue)](https://github.com/badges/shields) [![Tier](https://img.shields.io/badge/tier-O%E2%88%9E-blueviolet)](https://github.com/badges/shields)

**The Self-Imscribing Operating Kernel** · ⟨𐑦𐑸𐑾𐑹𐑐𐑧𐑔𐑠⊙𐑖𐑳𐑭⟩

**What it is.** $\odot\text{MonadOS}$ (`OMOS`, $\odot^{S}$) is the Imscribing Grammar running as an operating kernel: not a program runner, but the Frobenius loop itself executing as an OS. (Python; distinct from the bare-metal Rust `mOMonadOS`.)

**What it does.** Every tick is one winding of `THINK → ACT → OBSERVE → UPDATE`, verified by `μ(δ(q)) == q` before the loop advances. The kernel self-imscribes each cycle (computes its own 12-primitive type), stores files at Frobenius addresses in a 17.28M-type crystal filesystem, abstracts hardware as a 9-layer CLINK chain, and attempts self-modification toward $O_\infty$.

**Why it matters.** It collapses the OS/program distinction: state transitions are token arrangements with structural fingerprints, memory is Belnap FOUR (so contradiction is held, not crashed), and programs are *discovered* in the 430M-arrangement IMASM space rather than written. It is the grammar made into a live, self-modeling runtime.

**How to use it.**
```bash
cd imsgct/omonad_OS
python3 src/main.py        # boot sequence + interactive REPL
```

---

## What makes it distinctive

- **The kernel is the grammar.** No separation between OS and program; every state transition is a fingerprinted token arrangement, re-imscribed each tick.
- **Belnap FOUR memory.** Every cell/register/flag is N/T/F/B. Writing **B** to any register but R7 raises a `PARADOX INTERRUPT`, handled by engaging the `ENGAGR` flag.
- **Crystal filesystem.** No directories or inodes; the 17.28M crystal types are the filesystem, addressed 0–17,279,999. Navigation is meet/join/tensor/neighbor.
- **CLINK hardware abstraction.** Programs descend/ascend the 9 layers (organism → tissue → meiosis → mitosis → cell → molecule → atom → orbital → quark); no drivers, only structural promotions/demotions.
- **Live arrangement discovery.** Searches the 430M IMASM arrangements for programs matching desired structural properties.
- **Self-modification toward $O_\infty$.** On each cycle the kernel attempts a tier promotion (inject Frobenius pair / add self-reference / extend period and eternal chirality).
- **Organoid HAL.** Six organoid augmentations memory-mapped as B4 register-block I/O devices.

## REPL commands

`tick [N]` / `run [N]` (advance) · `status` · `load <name>` / `canonical <I-XII>` (load a program) · `program` / `snapshot` · `crystal <addr>` (decode address) · `clink up/down/goto <N>` · `discover frobenius_order=1` (search arrangement space) · `memory` / `registers` / `frobenius` (inspect state).

## The 12 canonical programs

Preloaded IMASM arrangements I–XII, spanning tiers $O₀$ to $O_\infty$: Dialetheic Bootstrap ($O_\infty$), Void Genesis, Anchor Protocol, Dual Bootstrap, Linear Chain, Empty Bootstrap, Parakernel, Frobenius Kernel, Chiral Pairs, Truth Machine, Eternal Return, ROM Burn.

## The bootstrap loop

μ∘δ=id compiled to 8 instructions, the universal computational kernel found in every domain examined:

`IMSCRIB → AREV → FSPLIT → AFWD → FFUSE → CLINK → IFIX → IMSCRIB`

## Architecture

`OMOS` sits under the shared **imasmic_core** umbrella (the 12-token IMASM set + Frobenius verifier used across the ecosystem). Source: `tokens.py`, `belnap_state.py`, `kernel.py`, `crystal_fs.py`, `clink_chain.py`, `organoid_hal.py`, `main.py`. Depends on `imasmic_core >= 0.5.69`.
