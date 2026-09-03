# Situationion Reference Notes

## Project Lens

The public project overview hypothesizes that GPT-2 XL's middle layers (17-31 of 48, roughly 35-65% of depth) form transient, paraphrase-invariant situation models. The intended trajectory is early **assembly** of lexical and syntactic material, core-mid **stabilization** of semantic and discourse structure across paraphrases, and late **collapse** of that state into a next-token decision. In an autoregressive Transformer:

$$
P(x_1, \ldots, x_n) = P(x_1) \prod_{t=1}^{n-1} P(x_{t+1} \mid x_1, \ldots, x_t).
$$

A situation model is therefore not an explicit variable inside GPT-2. It is a proposed property of a region of the residual stream, to be tested geometrically and causally. Probes and attention patterns are evidence about a representation, not proof that the model uses it; controlled paraphrase tests and interventions provide the stronger evidence.

## 1. What does BERT learn about the structure of language?

**File:** `1WhatBertStructLang.pdf`  
**Authors:** Ganesh Jawahar, Benoit Sagot, and Djame Seddah (2019)

This paper argues that BERT's layers encode a rough linguistic hierarchy: lower layers retain surface and phrase-boundary information, middle layers are strongest for syntax, and higher layers carry more semantic information. The authors use layer-wise diagnostic classifiers on ten SentEval tasks, subject-verb agreement tests with increasing numbers of intervening nouns, and Tensor Product Decomposition Networks (TPDNs). A TPDN approximates a representation as a sum of filler-role bindings:

$$
\mathbf{r} = \sum_i \mathbf{f}_i \otimes \mathbf{r}_i,
$$

where $\mathbf{f}_i$ encodes a filler and $\mathbf{r}_i$ its structural role. Comparing its mean-squared reconstruction error to BERT hidden states lets the authors test whether positional, sequential, or tree-derived roles best explain the encoding. Tree-like role schemes approximate BERT particularly well, supporting a compositional, syntax-sensitive account. Agreement with longer dependencies shifts to deeper layers, so structure is not fully available at the bottom. For this project, it supplies the basic assembly prediction and a measurement template: show that syntax-sensitive geometry appears before the proposed situation representation, then show that paraphrase-invariant event-level geometry peaks later. It also cautions against treating a layer boundary as absolute: information is distributed and task-dependent.

## 2. BERT Rediscovers the Classical NLP Pipeline

**File:** `2BERTRedisClassicNLP.pdf`  
**Authors:** Ian Tenney, Dipanjan Das, and Ellie Pavlick (2019)

Tenney et al. find that BERT's information is ordered, in aggregate, much like a classical NLP pipeline: part-of-speech information appears first, then constituency/dependency structure and named entities, followed by semantic roles and coreference. Their edge-probing setup represents a candidate span or span pair with a learned scalar mixture of encoder layers:

$$
\mathbf{h} = \gamma \sum_l s_l \mathbf{h}_l,
\qquad s_l = \operatorname{softmax}(\mathbf{a})_l,
$$

where $s_l$ weights each layer and $\gamma$ is a learned scale. Lightweight classifiers predict annotations, while the mixture's center of gravity estimates where information is most usable. They also compare full mixtures with individual-layer probes and trace individual examples. The aggregate hierarchy is real, but individual sentences can defer or revise a lower-level interpretation after higher-level context resolves ambiguity. This is unusually relevant to Situationion: expect a broad middle-layer interval, not a single magic layer, and test dynamics per input as well as layer-averaged effects. A useful experiment is to measure whether paraphrase alignment rises after syntactic probes peak, while causal editing of that aligned subspace changes event/coreference or coherence judgments more than token-level form.

## 3. Analyzing the Structure of Attention in a Transformer Language Model

**File:** `3AnalzeAttentionStructure.pdf`  
**Author:** Jesse Vig (2019)

Vig analyzes GPT-2 small attention at head, model, and neuron granularity, using corpus-level comparisons to part-of-speech, dependency relations, and token distance alongside visual examples. The central result is a depth profile: heads target different parts of speech at different depths, attention aligns most strongly with dependency relations in middle layers, and the deepest layers capture the most distant relationships. If $A_{t,i}^{(l,h)}$ is the attention paid from token $t$ to token $i$ by head $h$ at layer $l$, an attention span can be expressed as:

$$
d^{(l,h)} = \sum_i A_{t,i}^{(l,h)}\lvert t-i\rvert.
$$

Relationship alignment can similarly be measured by whether $\arg\max_i A_{t,i}^{(l,h)}$ is an annotated dependent or governor. This is direct architectural precedent for the project's focus on GPT-2 middle layers: middle attention may be where the model binds local syntactic relations before later layers integrate farther context. But attention is only a routing signal, not the full representation. The project should pair head/span analysis with residual-stream geometry and ablations, asking whether the same middle-layer window is paraphrase-stable and necessary for discourse-level predictions.

## 4. A Primer in BERTology: What We Know About How BERT Works

**File:** `4PrimerBertOlogy.pdf`  
**Authors:** Anna Rogers, Olga Kovaleva, and Anna Rumshisky (2020)

This survey of more than 150 BERT studies maps what was then known about BERT's architecture, pretraining, learned linguistic/world knowledge, fine-tuning behavior, compression, and interpretability. Its technical baseline is the Transformer encoder:

$$
\operatorname{Attention}(Q,K,V) = \operatorname{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V,
$$

with multi-head outputs concatenated and projected, and residual connections plus layer normalization carrying information through depth. The survey's important substantive conclusion is not that BERT has cleanly localized linguistic modules, but that probing, masked-token tests, and attention analyses consistently reveal structured knowledge with heavy redundancy and methodological ambiguity. It stresses that a successful probe can read information that the model does not causally use, and that attention weights are not automatically explanations. For Situationion, this is the methodological guardrail: define a null model, control lexical overlap and probe capacity, report layer-wise uncertainty, and validate any situation subspace with interventions or activation patching. It also motivates checking whether the effect is sparse, redundant, or spread across heads and MLPs rather than claiming localization from a single visualization.

## 5. A Primer on the Inner Workings of Transformer-Based Language Models

**File:** `5PrimerTransformer.pdf`  
**Authors:** Javier Ferrando, Gabriele Sarti, Arianna Bisazza, and Marta R. Costa-jussa (2024)

This decoder-focused interpretability primer connects the Transformer computation to modern mechanistic methods. For a token sequence $t$, a causal language model uses:

$$
P(t_1, \ldots, t_n) = P(t_1) \prod_{i=1}^{n-1}P(t_{i+1}\mid t_1,\ldots,t_i).
$$

Each block writes attention and MLP updates into a residual stream, and a final unembedding maps the stream to logits. The survey organizes evidence into behavior localization (input attribution, component importance, ablation, activation patching) and information decoding (probes, vocabulary-space or logit-lens methods, the linear representation hypothesis, and sparse autoencoders), then reviews known attention, MLP, residual-stream, and multi-component circuits. Its central lesson for this project is that a geometric middle-layer signature alone is descriptive: causal tests should patch or steer residual activations from one paraphrase into another and measure changes in logits, generated continuations, coherence, and event-role judgments. It also supplies a language for distinguishing a distributed latent situation state from a single interpretable feature, which is likely the more realistic target in GPT-2 XL.

## 6. Multi-Scale Probabilistic Generation Theory: A Hierarchical Framework for Interpreting Large Language Models

**File:** `6MultiScaleProbGenThry.pdf`  
**Authors:** Yukun Zhang and Qi Dong (2025 preprint)

This recent preprint proposes MSPGT, a three-scale account of generation: global context $G$, intermediate semantic structure $I$, and local token decision $L_t$. It replaces the flat autoregressive factorization

$$
P(X\mid C) = \prod_t P(x_t\mid x_{<t},C)
$$

with the approximate hierarchy

$$
P(X\mid C) \approx P(G\mid C)P(I\mid G,C)\prod_tP(x_t\mid L_t,I,G,C).
$$

To assign layers to scales, it combines mean attention span, adjacent-layer mutual information, and scale-specific probe peaks. Its attention metric is:

$$
d_{\mathrm{attn}}^{(l,h)} = \frac{1}{T}\sum_{t=1}^{T}\sum_{i=1}^{n}A_{t,i}^{(l,h)}\lvert t-i\rvert,
\qquad
d_{\mathrm{attn}}^{(l)} = \frac{1}{H}\sum_{h=1}^{H}d_{\mathrm{attn}}^{(l,h)}.
$$

Its adjacent-layer mutual information is:

$$
I(\mathbf{h}^{(l)};\mathbf{h}^{(l+1)}) = H(\mathbf{h}^{(l)}) + H(\mathbf{h}^{(l+1)}) - H(\mathbf{h}^{(l)},\mathbf{h}^{(l+1)}),
$$

with a proposed boundary when the first difference in this quantity falls more than two standard deviations below its mean. The three signals are combined as:

$$
S_{\mathrm{scale}}(l)=\alpha S_{\mathrm{probe}}(l)+\beta S_{\mathrm{attn}}(l)+\gamma S_{\mathrm{MI}}(l),
\qquad \alpha+\beta+\gamma=1.
$$

The authors report stable local/intermediate/global partitions across GPT-2, BERT, RoBERTa, and T5, and report that scale-targeted interventions affect lexical diversity, sentence structure/length, and discourse coherence respectively. This is the closest direct framing for Situationion, but it is a 2025 preprint and its claims should be independently reproduced. The project can sharpen MSPGT's broad intermediate scale into a concrete GPT-2 XL claim: layers 17-31 should show the predicted paraphrase invariance and causal sensitivity, with a distinct core at 23-26 if the proposed stabilization phase is real.

## 7. What Does BERT Look At? An Analysis of BERT's Attention

**File:** `7BertTtention.pdf`  
**Authors:** Kevin Clark, Urvashi Khandelwal, Omer Levy, and Christopher Manning (2019)

Clark et al. treat individual BERT attention heads as zero-training classifiers: for a source token, predict the token receiving maximum attention and compare it to annotated syntactic or coreference targets. They find recurring attention behaviors: delimiter or `[SEP]` focus, fixed positional offsets, and broad sentence-wide attention, with heads in the same layer often similar. A small number of heads capture specific relations strikingly well: direct objects, noun determiners, prepositional objects, and some coreferent mentions can exceed 75% accuracy, although no head is universally syntactic. They quantify head similarity with Jensen-Shannon distance between attention distributions:

$$
D_{\mathrm{JS}}(P\parallel Q)=\frac{1}{2}D_{\mathrm{KL}}(P\parallel M)+\frac{1}{2}D_{\mathrm{KL}}(Q\parallel M),
\qquad M=\frac{P+Q}{2},
$$

and use multidimensional scaling to reveal layer-local clusters, suggesting substantial redundancy. The key project implication is that interpretable heads can support hypotheses about which relations feed an emerging situation representation, but they are not the representation itself. For GPT-2 XL, identify relation-sensitive middle-layer heads, then test whether ablating them or their value/output contributions degrades paraphrase-invariant event geometry and downstream coherence more than matched control heads.

## 8. Strategies of Discourse Comprehension

**File:** `8Strategies of Discourse Comprehension ... Anna's Archive.pdf`  
**Authors:** Teun A. van Dijk and Walter Kintsch (1983)

This book develops a strategic, capacity-limited account of how people comprehend extended discourse. Comprehension builds a local propositional text base while continuously establishing coherence through referential links, causal relations, world knowledge, goals, and discourse schemas; it simultaneously constructs macrostructures, or topic-level summaries. The process is not a fixed sentence-by-sentence parser: readers make fast, defeasible inferences, retain selected propositions in a limited working-memory buffer, use schemas to select relevance, and revise or reconstruct information as later text arrives. The formal core is a mapping from micropropositions to macropropositions under macrorules such as deletion of irrelevant detail, generalization to a superordinate proposition, and construction of a global fact from its components. This is the conceptual foundation for Situationion: a situation representation should encode more than syntax or a bag of words. It should preserve entities, roles, events, causal/temporal links, goals, and the global topic enough that equivalent paraphrases converge while small changes to a key event or role do not. Controlled stimuli should manipulate these factors separately.

## 9. Toward a Model of Text Comprehension and Production

**File:** `9Toward_a_model_of_text_comprehension_and.pdf`  
**Authors:** Walter Kintsch and Teun A. van Dijk (1978)

This earlier article lays out the formal microstructure/macrostructure framework that the 1983 book extends. A discourse is represented as a coherent text base of propositions, not as an unstructured sequence of sentences. Microstructure concerns local predicate-argument propositions and their connections; macrostructure is the discourse topic or global meaning, produced recursively by semantic mapping rules that preserve entailment. The three principal macrorules are: delete a proposition that is not a direct or indirect interpretation condition for what follows; generalize a sequence to a proposition denoting an immediate superset; and construct a higher-level proposition whose components, conditions, or consequences are the original sequence. Schemas constrain these rules so summaries remain meaningful, and production can be viewed as selecting and expanding a macrostructure into a microstructure. For Situationion, this gives a crisp behavioral definition of the desired invariance: paraphrases sharing the same macropropositions should be near each other in the hypothesized core-middle state, whereas a role reversal, negation, causal change, or topic change should separate them even when lexical overlap is high. It also suggests evaluating the state against explicit proposition and event-graph annotations, not only free-form similarity scores.

## Synthesis: What the Reference Set Says About the Project

Taken together, references 1-3 and 7 support a depth-ordered story in which language models first make local form and syntax available, then encode relational structure in middle layers, and later integrate longer-distance information. References 4-5 add the crucial methodological warning: decodability and attention alignment are correlational; a credible claim about a latent situation model needs counterfactual controls and causal tests. Reference 6 states almost the same multi-scale hypothesis at a broad architectural level, but Situationion is more specific and therefore testable: it predicts an assembly/stabilization/collapse trajectory within GPT-2 XL layers 17-31, especially 23-26. References 8-9 say what situation should mean: a coherent, schema-guided model of entities, events, roles, causal/temporal relations, and global topic, compressed relative to sentence surface form.

A strong empirical package would:

1. Create matched paraphrase sets with preserved macrostructure and adversarial variants that change exactly one event-role, polarity, causal, or topic fact.
2. Measure per-layer representational similarity, with lexical-overlap and random-model controls.
3. Separately probe syntax, event roles/coreference, and discourse-topic/coherence to test the predicted ordering.
4. Inspect attention span and relation-sensitive heads as supporting, not decisive, evidence.
5. Patch, ablate, or steer candidate residual-stream subspaces in the core-middle window, testing whether continuation logits and discourse behavior change in the predicted way.

The distinctive payoff would be evidence that GPT-2 XL temporarily encodes a shared event and discourse state across paraphrases before converting it into a token-specific output distribution.
