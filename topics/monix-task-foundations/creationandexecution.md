## Creating Task

`Task[A]` represents a *specification* of a computation that *after executing* will produce either a value of type `A`, fail with an error, or never terminate.

We can create a `Task` using one of a variety of methods.

### Suspending evaluation

For instance, we can use `Task.eval` to evaluate the value of type `A` in `Task` context:

```scala 
import monix.eval.Task

val task: Task[String] = Task.eval { println("Effect"); "Hello!" }
```

Since a `Task` is just a specification of an effect, the actual execution will be suspended.
Nothing will be printed until the `Task` is executed.

### Creating Task from values

There are other builders, like `Task.now` that allows creating a `Task` from *already available* value:

```scala 
import monix.eval.Task

val task: Task[String] = Task.now("Hello!")
```

Note that if there were any side-effects, there would not be suspended:

```scala 
import monix.eval.Task

val task: Task[String] = Task.now { println("Effect"); "Hello!" }
// => Effect
```

In this case, the "Effect" will be printed right away, at the creation of the `Task` and never again.
We need to make sure to only use this method with already evaluated values.

### Failed Tasks

If we'd like to create a `Task` that signals an error, we could use `Task.raiseError`:

```scala 
import monix.eval.Task
import monix.execution.exceptions.DummyException

val error = Task.raiseError(DummyException("boom"))
```

`Task` will also catch any errors that are thrown and return them as a failed task, for instance:

```scala 
import monix.eval.Task
import monix.execution.exceptions.DummyException

val alsoError = Task.eval { throw DummyException("boom")) }
```

In general, it is recommended to use `raiseError`.

## Executing Task

Now that we have learned how to create simple tasks let's see how we could run them to execute specified instructions!

### Scheduler

When running a `Task`, we need to provide a [Scheduler](https://monix.io/docs/current/execution/scheduler.html).
It is an equivalent of [ExecutionContext](https://docs.scala-lang.org/overviews/core/futures.html#execution-context) that is used to handle lower levels details of concurrency.

We only have to pass it when running the `Task`, or if we would like to change it.

We will learn more about `Scheduler` when we get to concurrency-related topics.
For now, we will stick to `monix.execution.Scheduler.global` that is a decent default.

### runToFuture

When inter-operating with `Future`-based libraries, it is convenient to run `Task` into `Future`.
Monix `Task` returns `CancelableFuture` that extends standard Scala's `Future` and can plug into `Task` cancellation.

```scala 
import monix.eval.Task
import monix.execution.CancelableFuture
import scala.concurrent.duration._

implicit val s = monix.execution.Scheduler.global

val task = Task(1 + 1).delayExecution(1.second)

val result: CancelableFuture[Int] =
  task.runToFuture

// If we change our mind
result.cancel()
```

### runAsync

If returning `Future` is too heavy for our needs, we could call `runAsync` that will run the `Task` on a different `Thread`:

```scala 
import monix.eval.Task
import scala.concurrent.duration._

implicit val s = monix.execution.Scheduler.global

val task = Task(1 + 1).delayExecution(1.second)

val cancelable = task.runAsync {
  case Right(value) =>
    println(s"Successful value: $value")
  case Left(exception) =>
    System.err.println(s"ERROR: ${exception.getMessage}")
}

// If we change our mind...
cancelable.cancel()
```

There is also `runAsyncAndForget` variant that doesn't take the callback.

### runSyncUnsafe

`runSyncUnsafe` will block for a result and return an `A` (or throw an exception if there's an error):

```scala 
import monix.eval.Task
import monix.execution.Scheduler.Implicits.global

val task: Task[String] = Task.eval { println("Effect"); "Hello"! }

val s: String = task.runSyncUnsafe()
// => Effect
```

We should remember to be careful with `runSyncUnsafe` - it blocks the current `Thread` until there is a result.
For short, synchronous `Task` it might not be a problem, but we often deal with long-running, asynchronous tasks
and we might end up blocking the `Thread` for a long time.

### Exercises

You can find coding exercises in [the monix-exercises repository](https://github.com/scalazone/monix-exercises/tree/main/monix-task-solutions/src/main/scala/scalazone/monix/lesson1).
If you are stuck, feel free to ask questions at [Monix gitter channel](https://gitter.im/monix/monix),
or peek [at the solutions](https://github.com/scalazone/monix-exercises/tree/main/monix-task-solutions/src/main/scala/scalazone/monix/lesson1).

For the warmup, try to solve the following single answer questions.

?---?
# How many times "Effect" will be printed?
```scala 
import monix.eval.Task
import monix.execution.Scheduler.Implicits.global

val task: Task[String] = Task.eval { println("Effect"); "Hello"! }

task.runAsyncAndForget
task.runAsyncAndForget
task.runAsyncAndForget
```

- [ ] 0
- [ ] 1
- [X] 3

# How many times "Effect" will be printed?
```scala 
import monix.eval.Task
import monix.execution.Scheduler.Implicits.global

val task: Task[String] = Task.now { println("Effect"); "Hello"! }

task.runAsyncAndForget
task.runAsyncAndForget
task.runAsyncAndForget
```

- [ ] 0
- [X] 1
- [ ] 3

# What will be the result of this code?
```scala 
import monix.eval.Task
import monix.execution.exceptions.DummyException
import monix.execution.Scheduler.Implicits.global

val task: Task[String] = Task.now { throw DummyException("BOOM") }

task.runAsyncAndForget
task.runAsyncAndForget
task.runAsyncAndForget
```

- [ ] The first `task.runAsyncAndForget` will throw an error and others won't run
- [ ] Three tasks will run and fail in the background
- [X] The exception will be thrown at the `task` creation and no tasks will run