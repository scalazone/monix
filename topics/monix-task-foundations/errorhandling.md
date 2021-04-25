## Causes of failure

<!-- TODO: this is a comment test -->

`Task` can fail for the following reasons:
- It is created with `raiseError`
- It is created from a failed value of `Try` or `Either`
- It is created from other failed effects like `Future` or `cats.effect.IO`
- It was cancelled and `onCancelRaiseError` was called
- There was an exception thrown in any of `Task.eval`, `map`, `flatMap`, etc.

Once a failure happens, the computation is stopped and the error is returned as a result:

```scala 
import monix.eval.Task
import monix.execution.Scheduler

given Scheduler = Scheduler.global

val fa = Task(println("A"))
val fb = Task.raiseError(RuntimeException("Something went wrong"))
val fc = Task(println("C"))

val task = fa.flatMap(_ => fb).flatMap(_ => fc)

task.runSyncUnsafe()
```

In this example the task `fa` prints `"A"`, and then the exception is thrown with the following message:

```
Exception in thread "main" java.lang.RuntimeException: Something went wrong
```

## Recovering from errors

Fortunately, we can handle the error with methods such as `onErrorHandleWith`:

```scala 
import monix.eval.Task
import monix.execution.Scheduler

given Scheduler = Scheduler.global

val fa = Task(println("A"))
val fb = Task.raiseError(RuntimeException("Something went wrong"))
val fc = Task(println("C"))

val task = fa
  .flatMap { _ => fb }
  .onErrorHandleWith { _ => Task(println("B recovered")) }
  .flatMap { _ => fc }
  .onErrorHandleWith { _ => Task(println("C recovered")) }

task.runSyncUnsafe()
```

In this case we see `"A"`, followed by `"B recovered"`, and then `"C"`.

Keep in mind that these methods only handle errors up to the position of the handler,
so if the failure happens right after `onErrorHandleWith`, the `Task` will fail with the new exception.

## Exposing errors

Instead of recovering from an error right away, we can also handle it by _exposing_ it with `attempt`,
which returns `Task[Either[A, B]]`, or `materialize`, which returns `Task[Try[A]]`.

It is not reflected in the type signature, but any `Task` that is returned is guaranteed to be successful.
(Or at least it is guaranteed until the next operation.)

### Side note

If you are interested in a `Task` implementation that includes this information in the type signature, 
check out [Monix BIO](https://bio.monix.io/docs/introduction) or [ZIO](https://zio.dev/).

The regular `Task` implementation can also take advantage of [EitherT](https://typelevel.org/cats/datatypes/eithert.html) 
which is arguably less ergonomic, but provides similar features.
However, we won't look into this implementation in the first part of this course.

## Exercises

You can find coding exercises in [the monix-exercises repository](https://github.com/scalazone/monix-exercises/blob/main/monix-task-exercises/src/main/scala/scalazone/monix/lesson3/ErrorHandlingExercises.scala).
If you are stuck, feel free to ask questions at [Monix gitter channel](https://gitter.im/monix/monix),
or peek [at the solutions](https://github.com/scalazone/monix-exercises/blob/main/monix-task-solutions/src/main/scala/scalazone/monix/lesson3/ErrorHandlingExercisesSolutions.scala).

For a warmup, try to solve the following single-answer question.

?---?
# Which tasks will be printed?

```scala 
import monix.eval.Task
import monix.execution.Scheduler

given Scheduler = Scheduler.global

val fa = Task(println("A"))
val fb = Task(println("B"))
val fc = Task(println("C"))
val fd = Task(println("D"))

val task = fa
  .flatMap { _ => fb }
  .onErrorHandleWith { _ => Task(println("B recovered")) }
  .flatMap { _ => Task.raiseError(new RuntimeException("Something went wrong")) }
  .flatMap { _ => fc }
  .flatMap { _ => fd }

task.runSyncUnsafe()
```

- [X] A, B
- [ ] A, B, C, D
- [ ] A, B, C
- [ ] Other