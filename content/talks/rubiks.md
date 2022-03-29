---
title: "Rubik's Cubes with a sprinkle of combinatorics and group theory."
date: 2022-02-15T11:30:03+00:00
# weight: 1
# aliases: ["/first"]
tags: ["Group Theory"]
author: "Giorgio G."
# author: ["Me", "You"] # multiple authors
showToc: false
TocOpen: false
draft: false
hidemeta: false
math: true
comments: false
description: "A short talk given during a 'Quick fire Talk' organized by the Malta Mathematical Society."
hideSummary: false
searchHidden: false
ShowReadingTime: false
ShowBreadCrumbs: true
ShowPostNavLinks: true
cover:
    image: "<image path/url>" # image path/url
    alt: "<alt text>" # alt text
    caption: "<text>" # display caption under cover
    relative: false # when using page bundles set this to true
    hidden: true # only hide on current single page
---


{{< youtube jTcMj-INVyQ >}}


## Main Results:
---
**Definition:** Let $\mathcal{G_{\tiny 3}}$ be the set of possible 3 by 3 rubik's cube distinct states (_i.e. no corner twists, no sticker swapping etc._ ) reachable by a move $M$.

 We show that $\mathcal{G_{\tiny 3}}$ is a group under _move concatenation_ which is defined as follows:

<center>
If $M_{\tiny 1}$ and $M_{\tiny 2}$ are moves (<i>or thereby sequences of them</i>) then $M_{\tiny 1} * M_{\tiny 2}$ is simply the execution of move $M_{\tiny 1}$ followed by that of $M_{\tiny 2}$. 
</center>
</br >

It is also worth nothing that performing a move from two different states, is identical in both cases, as we do not look for the final state, but the sequence of moves it took to get there.


**Remark:** It is trivial, but not obvious, that there are so many ways we can scramble a rubik's cube. To obtain the following result, we rather observe a subset of all the possible permutations and combinations of putting together a rubik's cube. The group of interest, happens to be of this order.

$$\begin{aligned}o(\mathcal{G_{\tiny 3}}) &= \frac{12! \times 8! \times 3^8 \times 2^{12}}{2 \times 3} \\\\\\\\ &= 43, 252, 003, 274,489,856,000 \end{aligned}$$


