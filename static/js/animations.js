import { animate, stagger, createTimeline } from 'https://cdn.jsdelivr.net/npm/animejs@4/lib/anime.esm.js';

animate('.especie-card', {
  opacity: [0, 1],
  y: [20, 0],
  duration: 600,
  delay: stagger(100)
});

import { createDraggable } from 'https://cdn.jsdelivr.net/npm/animejs@4/lib/anime.esm.js';

createDraggable('.square');