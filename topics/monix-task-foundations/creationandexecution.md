## Creating Task

`Task[A]` represents a _specification_ for a computation that, _after execution_, produces either a value of type `A`, fails with an error, or potentially never terminates.
In this context, a _computation_ represents any actions that we want to conduct as a part of our program. 
The actions can be anything from returning a value to performing the entire business logic of the application.
The "laziness" of execution is a crucial difference between Monix `Task` and Scala's `Future`, which starts running at the time of construction.

We can create a `Task` using one of a variety of methods.

### Suspending evaluation

One way to create a `Task` is to use `Task.eval` to evaluate the value of type `A` in the `Task` context:

```scala 
import monix.eval.Task

val task: Task[String] = Task.eval {
  println("Effect")
  "Hello!"
}
```

Since a `Task` is just a specification for an effect, the actual execution is _suspended_, which means that nothing is printed until the `Task` is actually executed.

### Creating a `Task` from a value

There are other `Task` builders, like `Task.now`, that lets you create a `Task` from a value that is already evaluated:

```scala 
import monix.eval.Task

val task: Task[String] = Task.now("Hello!")
```

If there are any side-effects from the evaluation of this value, they will not be suspended:

```scala 
import monix.eval.Task

val task: Task[String] = Task.now {
  println("Effect")
  "Hello!"
}
```

In this case, the string `"Effect"` will be printed immediately when the `Task` is constructed, and never again.
We need to make sure that we only use this method with values that are already evaluated.

### Failed Tasks

When we want to create a `Task` that signals an error, we can use `Task.raiseError`:

```scala 
import monix.eval.Task

val error = Task.raiseError(RuntimeException("Something went wrong"))
```

`Task` catches any _non-fatal_ errors that are thrown, and returns them as a failed task.
Errors, such as `OutOfMemoryError`, `StackOverflowError`, [and others](https://dotty.epfl.ch/api/scala/util/control/NonFatal$.html) are generally
considered not recoverable and if they happen, the current task, or entire JVM should shut down as quickly as possible:

```scala 
import monix.eval.Task

val alsoError = Task.eval {
  throw new RuntimeException("Something went wrong")
}
```

<!-- TODO: I think this sentence needs something at the very end. -->
In general, it is recommended to use `raiseError`.

## Executing Task

Now that we have learned how to create simple tasks, let's see how we can run them to execute a series of instructions!

### Scheduler

When running a `Task`, we need to provide a [Scheduler](https://monix.io/docs/current/execution/scheduler.html).
This process is similar to the [ExecutionContext](https://docs.scala-lang.org/overviews/core/futures.html#execution-context) that is used by `Future` to handle the low-level concurrency details.
`Scheduler` adds extra capabilities, such as running with a delay, at specific intervals, and cancellation of scheduled tasks.

We only have to pass `Scheduler` as an argument when running the `Task`. 
It is then kept in `Task`'s internal context, and used in the implementation of some of the operators.

This was just a brief introduction; we will learn more about `Scheduler` when we get to concurrency-related topics.
For now, we will stick to `monix.execution.Scheduler.global`, since it is a good default.

### `runToFuture`

When inter-operating with libraries that use the `Future` type in Scala's standard library, we often need to convert a `Task` into a `Future`.
Monix `Task` can start its execution and return the result in the context of `Future` with `runToFuture`:

```scala 
import monix.eval.Task
import scala.concurrent.duration.*
import monix.execution.Scheduler

given Scheduler = Scheduler.global

val task = Task(1 + 1).delayExecution(1.second)

val result: Future[Int] = task.runToFuture
```

### `runAsync`

If we want to run `Task` on a potentially different thread, but we don't need a `Future` in the end, then `runAsync` is a more efficient alternative:

```scala 
import scala.concurrent.duration.*
import monix.execution.Scheduler
  
given Scheduler = Scheduler.global

val task = Task(1 + 1).delayExecution(1.second)

task.runAsync {
  case Right(value) =>
    println(s"Successful value: $value")
  case Left(exception) =>
    System.err.println(s"ERROR: ${exception.getMessage}")
}
```

`runAsync` takes a callback function of type `Either[Throwable, A] => Unit` that is executed once `Task` finishes its execution.
The callback is called with `Right(value)` if the `Task` succeeds, and `Left(exception)` if the `Task` fails with an error.

<!-- TODO: note that this is only used for side effects? -->
There is also `runAsyncAndForget` variant that doesn't take the callback, and doesn't provide any way to access the return value.

### `runSyncUnsafe`

`runSyncUnsafe` blocks for a result and returns an `A` if it succeeds, or throws an exception if there's an error:

```scala 
import monix.eval.Task
import monix.execution.Scheduler
  
given Scheduler = Scheduler.global

val task: Task[String] = Task.eval { println("Effect"); "Hello!" }

val s: String = task.runSyncUnsafe()
```

We need to be careful with `runSyncUnsafe` since it blocks the current thread until the result is evaluated.
For a short, synchronous `Task` this may not be a problem, but we often deal with long-running, asynchronous tasks
that wait for responses from a different thread or JVM without doing any useful work themselves.
This can not only be wasteful, but also lead to hanging the entire application. We will look at it closer in the "Thread Management" lesson.

### Exercises

Coding exercises are in the [monix-exercises repository](https://github.com/scalazone/monix-exercises/tree/main/monix-task-solutions/src/main/scala/scalazone/monix/lesson1), and the [Monix gitter channel](https://gitter.im/monix/monix) is available for any questions.
The [solutions](https://github.com/scalazone/monix-exercises/tree/main/monix-task-solutions/src/main/scala/scalazone/monix/lesson1) to the exercises are also available.

As a warmup, try to solve the following single-answer questions.

?---?
# How many times will `Effect` be printed?

```scala 
import monix.eval.Task
import monix.execution.Scheduler

given Scheduler = Scheduler.global

val task: Task[Unit] = Task.eval {
  println("Effect")
}

task.runAsyncAndForget
task.runAsyncAndForget
task.runAsyncAndForget
```

- [ ] 0
- [ ] 1
- [X] 3

# How many times will `Effect` be printed?
```scala 
import monix.eval.Task
import monix.execution.Scheduler

given Scheduler = Scheduler.global

val task: Task[Unit] = Task.now {
  println("Effect")
}

task.runAsyncAndForget
task.runAsyncAndForget
task.runAsyncAndForget
```

- [ ] 0
- [X] 1
- [ ] 3

# What will be the result of executing this code?
```scala 
import monix.eval.Task
import monix.execution.Scheduler

given Scheduler = Scheduler.global

val task: Task[String] = Task.now { throw RuntimeException("Something went wrong") }

task.runAsyncAndForget
task.runAsyncAndForget
task.runAsyncAndForget
```

- [ ] the first `task.runAsyncAndForget` will throw an exception and others won't run
- [ ] three tasks will run and fail in the background
- [X] an exception will be thrown during creation of the `task` instance, and no tasks will run