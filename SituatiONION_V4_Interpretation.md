## What V4 Means

In plain English, **V4 has changed the original hypothesis in a pretty
specific way**.

The original idea was roughly:

> **H1:** GPT-2 XL has a particularly important situation-processing
> region around layers 23--26.

Then V3 suggested an alternative:

> **H2:** Maybe situation information actually starts emerging earlier,
> around layers 8--12, and then persists through the middle.

**V4 suggests that neither simple story is completely right.**

------------------------------------------------------------------------

### What H1 Means Now

There **is something statistically special about layers 23--26 for some
representations**.

For the **Changed-token** readout, layers 23--26 are more
situation-sensitive than their neighboring layers, with a fairly
substantial standardized effect:

$$
d \approx 0.74
$$

For the **Final-token** readout, there is also a reliable local
enhancement:

$$
d \approx 0.58
$$

So the original 23--26 prediction was **not just random**. There is a
measurable local enhancement in this region for these two
representations.

However, situation information is **not confined to layers 23--26**.

The Changed-token readout reliably distinguishes paraphrases from
counterfactuals at **48/48 layers**, and the Final-token readout does so
at **43/48 layers**.

Therefore, layers 23--26 look more like a **local strengthening of an
already-existing signal**, rather than the point where a situation
representation suddenly appears.

This is why **H1 is only partially supported**.

------------------------------------------------------------------------

### What Happened to H2?

H2 predicted something like:

> Situation sensitivity generally begins around layers 8--12.

V4 shows that this is also too simple.

  Readout             Reliable Situation Separation
  ------------------- -------------------------------
  **Changed token**   **0--47**
  **Final token**     **1--2 and 7--47**
  **Event token**     **4--40 and 47**
  **Mean pool**       **11--45**
  **Max pool**        **None**

There is therefore no single moment where GPT-2 suddenly begins
representing the situation.

Instead, **different parts of the representation acquire or express
situation information at different depths**.

------------------------------------------------------------------------

### The Changed Token vs. Event Token Distinction

The **Changed token already separates the situations at layer 0**.
Because this readout directly examines the position where something was
changed, some distinguishing information is locally available from the
beginning.

The **Event token behaves differently**. Its reliable
situation-sensitive signal does not begin until layer 4. The signal then
develops through the network, becomes stronger through the middle
layers, and largely disappears after layer 40.

This is more consistent with information being **contextually integrated
or propagated** into the event representation as processing proceeds.

``` text
Changed information enters the network
              │
              ▼
       CHANGED TOKEN
    distinction available early
              │
              ▼
       contextual processing
              │
              ▼
        EVENT TOKEN
   begins reflecting the change
              │
              ▼
       MIDDLE NETWORK
    stronger differentiation
              │
              ▼
        LATE NETWORK
        signal weakens
```

V4 does not prove that this is the actual mechanism, but it provides a
concrete hypothesis that can be investigated in V5.

------------------------------------------------------------------------

### What Mean Pooling Tells Us

Mean pooling is technically reliably positive from layers 11--45.
However, its **absolute magnitude is extremely small**.

Statistically, $S(l) > 0$, but practically, $S(l) \approx 0$.

Situation-sensitive information may technically survive whole-sentence
averaging, but **pooling dramatically dilutes the signal**. Max pooling
performs even worse, with no reliably positive situation separation at
any layer.

Therefore:

> **Global pooling largely obscures the much stronger
> situation-sensitive structure visible at specific token positions.**

------------------------------------------------------------------------

### Why Max Pool Does Not Rescue H1

Max pooling produces a statistically positive core-middle difference:

$$
\Delta_{23:26} = 0.000023
$$

However, Max pooling itself has **0/48 reliably positive layers**.

Although layers 23--26 are technically slightly higher than their
neighboring layers under this readout, the underlying representation
does not reliably distinguish paraphrases from counterfactuals anywhere
in the network.

Therefore, the Max-pool result should be reported but **not interpreted
as substantive evidence for H1**.

------------------------------------------------------------------------

## What Did V4 Actually Discover?

> **GPT-2 XL contains situation-sensitive information across much of its
> depth, but that information is not represented uniformly. Different
> token representations express the information at different stages of
> processing. Layers 23--26 show a measurable local enhancement for
> Changed-token and Final-token representations, partially supporting
> the original SituatiONION hypothesis, but they are not an isolated or
> exclusive situation-processing region.**

Originally, the main question was:

$$
\boxed{\text{Where is the situation model?}}
$$

V4 suggests that a better question may be:

$$
\boxed{\text{How does situation information move and transform through the model?}}
$$

The original hypothesis looked roughly like:

``` text
early → early → SITUATION MODEL → late → late
                    23–26
```

The V4 results instead look more like:

``` text
                    GPT-2 XL DEPTH
0 ---------------------------------------------------- 47

Changed token   ████████████████████████████████████████
                     strong throughout

Event token         ████████████████████████████████
                     emerges → strengthens → fades

Final token      ██    █████████████████████████████████
                       broad contextual signal

Mean pool                 ·························
                          tiny diluted signal

                              ↑
                            23–26
                     local enhancement
                     for some readouts
```

Therefore, **layers 23--26 may still matter**, but probably not because
a single, monolithic "situation model" exists there.

Instead, this region may represent a point where **some
already-developing situation-sensitive representations become
particularly differentiated**.

------------------------------------------------------------------------

## Implication for V5

V5 should now investigate **what specific situation information is
decodable at different stages of processing**.

The next question becomes:

> **What information about the situation is represented at each depth,
> and how does that information change as it moves through the
> network?**

Layer-wise probes can test whether information about:

-   Agent and recipient roles
-   Events and states
-   Polarity
-   Causal relations
-   Temporal relations

becomes decodable along different trajectories.

If these situation components become decodable at different depths, that
would provide a much more mechanistic interpretation of the distributed
representational patterns discovered in V4.
