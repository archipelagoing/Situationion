 H1 Results (Core minus Neighbors):



  
    
       
      readout
      core_minus_neighbors
      ci_low
      ci_high
      effect_size
      supports_h1
    
  
  
    
      0
      Agent/recipient
      nan
      nan
      nan
      nan
      False
    
    
      1
      Changed token
      0.007023938978
      0.005593117842
      0.008458134362
      0.7442
      True
    
    
      2
      Event token
      -0.000271735340
      -0.000904475474
      0.000381947143
      -0.0642
      False
    
    
      3
      Final token
      0.001806217339
      0.001349741098
      0.002313051188
      0.5782
      True
    
    
      4
      Max pool
      0.000023465371
      0.000009425622
      0.000036684101
      0.2669
      True
    
    
      5
      Mean pool
      0.000025597867
      -0.000025359056
      0.000078566531
      0.0766
      False
    
  

Note for Max pool: Even if 'ci_low' appears as 0.000000000000 due to display precision, it might be a very small positive number (e.g., 1e-12), which is still classified as supporting H1.

H2 Results (Reliably Positive Layers):



  
    
       
      readout
      first_reliably_positive_layer
      last_reliably_positive_layer
      positive_layer_count
      contiguous_ranges
    
  
  
    
      0
      Agent/recipient
      nan
      nan
      0
      
    
    
      1
      Changed token
      0
      47
      48
      0-47
    
    
      2
      Event token
      4
      47
      38
      4-40 and 47
    
    
      3
      Final token
      1
      47
      43
      1-2 and 7-47
    
    
      4
      Max pool
      nan
      nan
      0
      
    
    
      5
      Mean pool
      11
      45
      35
      11-45
    
  



## V4 Conclusion

Under strict structural controls and held-out evaluation, situation-sensitive
separation generalized across several representation readouts, but its
trajectory depended strongly on where the model was measured.

### General Situation Separation

- **Changed token:** reliably positive at **48/48 layers (0-47)**.
- **Final token:** reliably positive at **43/48 layers**, with contiguous
  regions at **1-2 and 7-47**.
- **Event token:** reliably positive at **38/48 layers**, primarily across
  **4-40 and 47**.
- **Mean pool:** reliably positive at **35/48 layers (11-45)**, although
  the absolute separation remains very small.
- **Max pool:** no reliably positive situation separation at any layer.
- **Agent/recipient:** not evaluable in the aggregate analysis.

These results show that there is **no single universal emergence layer** for
situation-sensitive information. Instead, the onset and strength of separation
depend on the representation being measured.

### H1: Are Layers 23–26 Locally Privileged?

The preregistered layers 23–26 showed a reliable local enhancement relative
to neighboring layers for:

- **Changed token:** Δ = 0.00702,
  95% CI [0.00559, 0.00846], effect size = 0.744
- **Final token:** Δ = 0.00181,
  95% CI [0.00135, 0.00231], effect size = 0.578

The **Event-token** and **Mean-pool** readouts did not show a reliable
core-middle enhancement.

Max pooling produced a statistically positive but extremely small local
difference (Δ = 0.000023). Because Max pooling showed no reliably positive
situation separation at any layer, this effect is not interpreted as
substantive evidence for a situation-sensitive core-middle representation.

Overall, V4 provides **partial, readout-specific support for H1**. Layers
23–26 are locally enhanced for Changed-token and Final-token representations,
but situation-sensitive information is distributed much more broadly across
the network and is not uniquely confined to this region.

### H2: Does Situation Sensitivity Emerge Around Layers 8–12?

V4 does not support a single universal onset around layers 8–12. Reliable
separation begins at different depths depending on the readout: immediately
for the Changed token, early for the Event and Final tokens, and later for
Mean pooling.

The V3-generated H2 should therefore be revised to a broader conclusion:

> **Situation-sensitive information emerges and develops at different depths**
> **depending on the representation being measured, rather than appearing at**
> **one common transition point.**

These results establish **representational geometry under strict held-out**
**controls**. They do not establish that GPT-2 XL causally uses these
representations.

