# transducers-py

This was a weekend project that had a go at porting Cognitect's transducer library to Python, loosely based on the [JavaScript version](https://github.com/cognitect-labs/transducers-js) by David Nolen.

## Project Status

Since then, Cognitect has made available [a complete Python version](https://github.com/cognitect-labs/transducers-python), which you should use instead. I might resume this in the future if I have the time, but as of January 4, 2015 this is considered deprecated.

## Why Transducers?

Because I find the concept appealing and more interesting than generators when composing operations (plus one can toss in regular functions as operations without having to cast them as generators). This is debatable, of course, but not something worth debating to smithereens.

It was also a learning experience, something to poke at and fiddle with in order to get a better understanding of the fundamentals.

Oh, and if you want to know about the `t_` prefix, that's simply because I intended to use these inside [Hy](http://hylang.org) and don't want to shadow any builtins - they'll map to `(t-foo)`, which is readable and fairly idiomatic as far as LISP dialects go.
