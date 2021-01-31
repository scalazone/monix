Welcome to the Monix course!

[Monix](https://monix.io/) is a high-performance Scala / Scala.js library for composing asynchronous, event-based programs.
The library provides several modules with different functionalities:

- [monix-execution](https://monix.io/api/current/monix/execution/index.html) with low level concurrency abstractions that is a companion to `scala.concurrent`.
- [monix-catnap](https://monix.io/api/current/monix/catnap/index.html) with purely functional, [Cats-Effect friendly](https://github.com/typelevel/cats-effect) abstractions.
- [monix-eval](https://monix.io/api/current/monix/eval/index.html) with `Task` and `Coeval` data types.
- [monix-reactive](https://monix.io/api/current/monix/reactive/index.html) with `Observable`, a Monix take on RxObservable with stronger functional influence.
- [monix-connect](https://connect.monix.io/) that is a set of connectors to use with Monix, similar in spirit to [Alpakka](https://doc.akka.io/docs/alpakka/current/).
- [monix-bio](https://bio.monix.io/docs/introduction) with `IO` that has typed errors.
- and others!

## Why Monix in particular?

Many other well-developed libraries are in a similar space to Monix.
- `Task` can be a competition to [cats.effect.IO](https://github.com/typelevel/cats-effect), [Future](https://docs.scala-lang.org/overviews/core/futures.html), and [zio.ZIO](https://zio.dev/).
- `Observable` serves a similar purpose to [Akka Streams](https://doc.akka.io/docs/akka/current/stream/index.html), [fs2.Stream](https://fs2.io/#/), and [ZIO Stream](https://zio.dev/docs/datatypes/datatypes_stream).

The unique attribute of Monix is that despite a preference for purely functional programming, we don't try to force it and aim to support impure libraries (Akka, anything Future-based) just as well as those from the FP ecosystem.

The `monix-execution` offering many utilities to use with `Future`, or a [Local's integration with Akka HTTP](https://monix.io/docs/current/execution/local.html#example-repository) are good examples.

However, even if using Monix is not attractive to you, there's quite a bit of universal information in the course that can be useful with any other library.

## What will you learn

The course is intended for Functional Programming beginners who have had either very little or no exposure to effects like `Task`.
Basic Scala knowledge is required, but not much beyond that.

During the beginner level of the course, we will start from nothing and learn how to use a `Task` and how it could be useful in real-life applications.

The first topic introduces Monix Task.

The second topic revolves around a more significant coding exercise that is meant to combine newly acquired knowledge to solve a use case,
that will give us a much better idea of how everything fits together and could be used in real projects.

## Exercises

At the end of each lesson, there are exercises that you can solve to improve your understanding of the topic.
There are two types of them:
- Coding exercises in the separate repository
- Quiz questions directly supported by ScalaZone platform

### Coding exercises

Since the platform does not (yet!) support coding exercises, we need to fork the following repository:
- https://github.com/scalazone/monix-exercises

Click the "Fork" button next to the "Star" and then clone your fork.

``` 
git clone git@github.com:your-github-username/monix-exercises.git
```

The repository includes all the exercises, their solutions, and unit tests that your answer should pass.

### Quiz questions

Some of these require you to select a single answer. So try this with an easy question now: choose the language
you would like to learn.

- [ ] F#
- [ ] Haskell
- [X] Scala
- [ ] Java
- [ ] Kotlin
- [ ] C#

Other questions allow you to choose multiple answers.

These are usually harder because, to get the question right, you must consider each possible
answer. Try this one now: select every programming language containing the letter `a` in its name.

* [ ] F#
* [X] Haskell
* [X] Scala
* [X] Java
* [ ] Kotlin
* [ ] C#

## Contributions

All contributions and feedback are welcome!

The source of the course is in [scalazone/monix](https://github.com/scalazone/monix) repository.

Exercises can be found at [scalazone/monix-exercises](https://github.com/scalazone/monix-exercises).

Sometimes there might be easy issues to pick up by anyone.

If you have any other improvement ideas, please open an issue or open a Pull Request.