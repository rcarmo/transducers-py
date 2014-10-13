# transducers-py

This is a first attempt at porting Cognitect's transducer library to Python, loosely based on the [JavaScript version](https://github.com/cognitect-labs/transducers-js) by David Nolen.

## Why Transducers?

Because I find the concept appealing and more interesting than generators when composing operations (plus one can toss in regular functions as operations without having to cast them as generators). This is debatable, of course, but not something worth debating to smithereens.

It is also a learning experience, something to poke at and fiddle with in order to get a better understanding.

Oh, and if you want to know about the `t_` prefix, that's simply because I intend to use these inside [Hy](http://hylang.org) and don't want to shadow any builtins - they'll map to `(t-foo)`, which is readable and fairly idiomatic as far as LISP dialects go.

## Project Status

Currently adding tests (using `nose`) and refactoring some things to be slightly more Pythonic while keeping them functional. Progress is expected to be slow, and things to be partially broken for a few weeks.

Fixes and pull requests are most welcome.
