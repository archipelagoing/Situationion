**1. Keep the current graph as a negative baseline. Record that mean-pooled whole-sentence cosine did not distinguish paraphrases from counterfactuals and did not support a special 23–26 region. Do not delete it or try to tune it away.**

**2. Test alternative representations on the exact same 8 examples first. Replace mean pooling with:

final-token hidden state
changed-token hidden state
event-verb token
agent/recipient token
maybe max pooling as a simple comparison

The goal is not “find the one that gives a bump at layer 24.” The goal is: which representation actually separates paraphrases from counterfactuals at al**l?

**3. Plot all of those readouts together. You want something like:

mean pooling
final token
changed token
event token

across all 48 layers. Then you can see whether saturation is specific to mean pooling.**

4. Add a token-level similarity diagnostic. For each triple, inspect which token positions actually change most across layers. This will tell you whether the semantic manipulation is localized instead of globally represented.


5. Only after you find a measurement that behaves sensibly, expand the dataset. Your own notebook explicitly says the current eight situations are pipeline checks and that the real dataset should contain hundreds of balanced triples with lexical-template and entity splits.


6. Then rerun the situation geometry on the larger dataset. At that point, ask whether layers 23–26 actually show a reliable local maximum. If they do, great. If they don't, that is also a legitimate result.

7. Then run the probes. Your notebook already has the layer-wise probe structure for things like agent, event, recipient, and relation information. This tells you where information is readable, even if raw cosine does not show it.
   
8. Keep the attention-span graph as supporting evidence, not the main result. Your notebook already correctly states that attention span is descriptive and cannot establish causal use.

9. Do causal patching last. Once you know what representation and layers look promising, use activation patching to test whether changing those hidden states actually changes model behavior. Your notebook already has the patching function and the right comparison idea: core-middle versus early, late, random, and lexical controls.

So the workflow I would use is:

baseline failure → diagnose saturation → compare readouts → choose a sensitive metric → expand dataset → rerun geometry → probes → attention analysis → causal patching → final decision