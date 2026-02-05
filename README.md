# 🧅 SituatiONION  
### Characterizing a Latent Situation-Modeling Regime in Transformer Mid-Layers
## Current Status : 
Established:
- a coherent conceptual framework and initial empirical evidence for a mid-layer situation-modeling regime.
  
Ongoing:
-  Work focuses on robustness checks, visualization improvements, and formalizing results for publication.

---

## Overview

**SituatiONION** is a research project investigating how transformer models internally construct and maintain *situation-like representations* across depth. Rather than treating transformers as uniform stacks, this work argues that **intermediate layers form a distinct, stable representational regime** responsible for assembling relational structure, constraints, and transient world models.

The project focuses on identifying, characterizing, and visualizing this regime—particularly in **GPT-2 XL**—using a combination of geometric analysis, layerwise probing, and controlled perturbations.

---

## Core Thesis

> **Intermediate transformer layers exhibit a stable, relational representational regime that assembles and maintains transient situation models, observable through geometric invariants and sensitivity to constraint perturbations.**

In other words:

- **Early layers** primarily encode lexical and syntactic features  
- **Late layers** prioritize output alignment and decision collapse  
- **Mid-layers** operate as a *situation-modeling bandwidth*, where meaning becomes structured, relational, and temporally coherent

---

## What This Project Studies

- Layerwise functional regimes rather than treating depth as homogeneous  
- Mid-layer representations where agents, goals, constraints, and relations cohere  
- Geometric structure of representations (e.g., stability, clustering, invariants)  
- Sensitivity to perturbations, especially constraint or state changes in input  
- Transient stability: how representations persist across layers before collapsing downstream  

---

## Methodological Approach

- Layer-by-layer activation analysis in transformer models (primarily GPT-2 XL)  
- Controlled prompt designs emphasizing state changes and relational structure  
- Geometric and representational diagnostics (e.g., similarity structure, trajectory behavior)  
- Visualization of representation flow across depth  
- Qualitative + quantitative alignment between internal dynamics and observable behavior  

This project treats representations as **flows through a system**, not static embeddings.

---

## Why “SituatiONION”?

- **Situation**: the project centers on internal situation models, not surface text  
- **ONION**: meaning is layered, assembled progressively, and only partially visible at any single layer  
- The metaphor reflects both **depth** and **structured emergence**, not opacity  

---

## Contributions / Goals

- Propose a conceptual model of mid-layer situation modeling in transformers  
- Provide evidence for a distinct intermediate representational regime  
- Develop clean visualizations that make internal dynamics legible  
- Bridge interpretability, reasoning, and architecture-level analysis  
- Offer tools and framing useful for future work on reasoning systems and agent design  

---
