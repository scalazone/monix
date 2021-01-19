## Causes of failure

`Task` can fail for the following reasons:
- It is created with `raiseError`
- It is created from a failed value of `Try`, or `Either`
- It is created from other failed effect like `Future`, or `cats.effect.IO`
- It was cancelled and `onCancelRaiseError` was called
- There was an exception thrown in any of `Task.eval`, `map`, `flatMap` etc.

Once a failure happens, the computation will be stopped, and the error will be returned as a result:

```scala 
import monix.eval.Task
import monix.execution.exceptions.DummyException
import monix.execution.Scheduler.Implicits.global

val fa = Task(println("A"))
val fb = Task.raiseError(DummyException("BOOM"))
val fc = Task(println("C"))

val task = fa.flatMap(_ => fb).flatMap(_ => fc)

task.runSyncUnsafe()
//=> A
//=> Exception in thread "main" monix.execution.exceptions.DummyException: BOOM
```

## Recovering from errors

Fortunately, we can handle the error with methods such as `onErrorHandleWith`:

```scala 
import monix.eval.Task
import monix.execution.exceptions.DummyException
import monix.execution.Scheduler.Implicits.global

val fa = Task(println("A"))
val fb = Task.raiseError(DummyException("BOOM"))
val fc = Task(println("C"))

val task = fa
  .flatMap(_ => fb)
  .onErrorHandleWith(_ => IO(println("B recovered")))
  .flatMap(_ => fc)
  .onErrorHandleWith(_ => IO(println("C recovered")))

task.runSyncUnsafe()
//=> A
//=> B recovered
//=> C
```

Let's keep in mind that these methods only handle errors up to the position of the handler,
so if the failure happens right after `onErrorHandleWith` then the `Task` will fail.

## Exposing errors

Instead of recovering from error right away, we can also handle it by _exposing_ it with `attempt`
which returns `Task[Either[A, B]]`, or `materialize` which returns `Task[Try[A]]`

It is not reflected in the type signature, but `Task` that is returned will be guaranteed to be successful.
At least, until the very next operation!

### Side note

If you are interested in a `Task` implementation with this information in the type signature, 
make sure to check out [Monix BIO](https://bio.monix.io/docs/introduction), or [ZIO](https://zio.dev/).

Regular `Task` implementation can also take advantage of [EitherT](https://typelevel.org/cats/datatypes/eithert.html) 
that is arguably less ergonomic, but can provide a similar powers.

However, we won't look into it in the first part of the course.

## Exercises

You can find coding exercises in [the monix-exercises repository](https://github.com/scalazone/monix-exercises/blob/main/monix-task-exercises/src/main/scala/scalazone/monix/lesson3/ErrorHandlingExercises.scala).
If you are stuck, feel free to ask questions at [Monix gitter channel](https://gitter.im/monix/monix),
or peek [at the solutions](https://github.com/scalazone/monix-exercises/blob/main/monix-task-solutions/src/main/scala/scalazone/monix/lesson3/ErrorHandlingExercisesSolutions.scala).

For the warmup, try to solve the following single answer questions.

?---?
# Which tasks will be printed?

```scala 
import monix.eval.Task
import monix.execution.exceptions.DummyException
import monix.execution.Scheduler.Implicits.global

val fa = Task(println("A"))
val fb = Task(println("B"))
val fc = Task(println("C"))
val fd = Task(println("D"))

val task = fa
  .flatMap(_ => fb)
  .onErrorHandleWith(_ => IO(println("B recovered")))
  .flatMap(_ => Task.raiseError(DummyException("BOOM")))
  .flatMap(_ => fc)
  .flatMap(_ => fd)

task.runSyncUnsafe()
```

- [X] A, B
- [ ] A, B, C, D
- [ ] A, B, C
- [ ] Other