## Creating Task

// FIXME: Need to define "computation"
`Task[A]` represents a *specification* for a computation that *after execution* will produce either a value of type `A`, fail with an error, or potentially never terminate.

We can create a `Task` using one of a variety of methods.

### Suspending evaluation

For instance, we can use `Task.eval` to evaluate the value of type `A` in the `Task` context:

```scala 
import monix.eval.Task

val task: Task[String] = Task.eval {
   println("Effect")
   "Hello!"
}
```

// FIXME: Need to define "effect"
Since a `Task` is just a specification for an effect, the actual execution will be _suspended_, which means that nothing will be printed until the `Task` is executed.

### Creating a `Task` from a value

There are other `Task` builders, like `Task.now`, that allow the creation of a `Task` from a value that is already evaluated.

```scala 
val task: Task[String] = Task.now("Hello!")
```

// FIXME: Need to define "side-effects" as compared to "effects"
If there were any side-effects from the evaluation of this value, they would not be suspended:

// FIXME: Avoid including commented code in code blocks—it's not always clear what they mean. Just explain them in the text before or after.
```scala 
val task: Task[String] = Task.now {
   println("Effect")
   "Hello!"
}
// => Effect
```

In this case, the string `"Effect"` will be printed immediately when the `Task` is constructed, and never again.
We need to make sure to only use this method with already evaluated values.
// FIXME: Why—need to explain our approach to controlling effects.

### Failed Tasks

If we'd like to create a `Task` that signals an error, we could use `Task.raiseError`:

// FIXME: Prefer real-world exceptions if possible, though is `DummyException` something that exists for a particular purpose?
```scala 
import monix.eval.Task
import monix.execution.exceptions.DummyException

val error = Task.raiseError(DummyException("boom"))
```

// QUESTION: I see that you're including all imports in all code samples, and for good reason: it makes the code copy-pastable in its entirety. Though it's not a convention I've adopted on ScalaZONE generally, because it makse the code too verbose. But maybe we could discuss whether the pros outweigh the cons...

// FIXME: *any* errors, or just nonfatal errors? (I'm not sure of the answer to this...)
`Task` will also catch any errors that are thrown and return them as a failed task, for instance:

// FIXME: I'm not sure of the current state of Scala 3-RC1, but maybe braceless syntax is possible here?
```scala 
import monix.eval.Task
import monix.execution.exceptions.DummyException

val alsoError = Task.eval {
   throw DummyException("boom"))
}
```

In general, it is recommended to use `raiseError`.

## Executing Task

Now that we have learned how to create simple tasks, let's see how we could run them to execute a series of instructions!

### Scheduler

When running a `Task`, we need to provide a [Scheduler](https://monix.io/docs/current/execution/scheduler.html).
It is equivalent to [ExecutionContext](https://docs.scala-lang.org/overviews/core/futures.html#execution-context) that is used to handle lower levels details of concurrency.
// FIXME: Needs more explanation about the purpose of the scheduler/execution context. We shouldn't assume that anyone already knows about `ExecutionContext`.

// FIXME: "Change it" - what is it, and what is the change?
We only have to pass it when running the `Task`, or if we would like to change it.

// FIXME: Good that we'll learn more later. A bit more explanation about what the Scheduler does should help to make it clear to the reader why it's an abstraction that we can leave to later. The reader will also be interested in why it is a "decent default", and why there could be alternatives.
We will learn more about `Scheduler` when we get to concurrency-related topics.
For now, we will stick to `monix.execution.Scheduler.global` since it is a good default.

### `runToFuture`

When inter-operating with libraries which use the `Future` type in Scala's standard library, we often need to convert a `Task` into a `Future`.
Monix `Task` can return a `CancelableFuture`, a type which extends Scala's `Future`, while also providing support for cancelling a computation.
// FIXME: Maybe need more explanation of what cancellation is. If this isn't the right time, maybe just say that it returns a `Future` since this is still true, even if it's returning a more precise type.

// FIXME: Convert to Scala 3 syntax with a `given`
// FIXME: Maybe give a more realistic example of a "slow" task.
// FIXME: I'd not describe cancellation as "changing our mind" - it's more a *need* to stop the computation.
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

### `runAsync`

// FIXME: I'm not sure "heavy" (which I changed to "heavyweight") is right, since a different thread implies a newly-allocated `Thread` object implies a new system process and associated call stack, etc...
If returning `Future` is too heavyweight for our needs, we could call `runAsync` that will run the `Task` on a different thread:

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
// FIXME: I think we need to explain the use of `Either`.

There is also `runAsyncAndForget` variant that doesn't take the callback.
// FIXME: and also doesn't provide any way to access the return value.

### `runSyncUnsafe`

`runSyncUnsafe` will block for a result and return an `A` (or throw an exception if there's an error):

```scala 
import monix.eval.Task
import monix.execution.Scheduler.Implicits.global

val task: Task[String] = Task.eval { println("Effect"); "Hello!" }

val s: String = task.runSyncUnsafe()
// => Effect
```
// FIXME: I'm generally replacing "`Thread`" with "thread" when we're talking about the concept, rather than the Java type used to represent it.

We need to be careful with `runSyncUnsafe` since it will block the current thread until the result has been evaluated.
For a short, synchronous `Task` this may not be a problem, but we often deal with long-running, asynchronous tasks
and we might end up blocking the `Thread` for a long time.
// FIXME: Why is this a problem? I think we can make reference to wasting resources, and maybe somewhere earlier we need to explain blocking.


### Exercises

Coding exercises are in the [monix-exercises repository](https://github.com/scalazone/monix-exercises/tree/main/monix-task-solutions/src/main/scala/scalazone/monix/lesson1), and the [Monix gitter channel](https://gitter.im/monix/monix) is available for any questions.
The [solutions](https://github.com/scalazone/monix-exercises/tree/main/monix-task-solutions/src/main/scala/scalazone/monix/lesson1) to the exercises are also available.

As a warmup, try to solve the following single-answer questions.

// FIXME: Do we need to return the string `"Hello!"`?
// FIXME: I'd generally avoid messages like "boom" since it doesn't help beginners understand the purpose of exceptions.
?---?
# How many times will `Effect` be printed?

```scala 
import monix.eval.Task
import monix.execution.Scheduler.Implicits.global

val task: Task[String] = Task.eval {
   println("Effect")
   "Hello!"
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
import monix.execution.Scheduler.Implicits.global

val task: Task[String] = Task.now {
   println("Effect")
   "Hello!"
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
import monix.execution.exceptions.DummyException
import monix.execution.Scheduler.Implicits.global

val task: Task[String] = Task.now { throw DummyException("BOOM") }

task.runAsyncAndForget
task.runAsyncAndForget
task.runAsyncAndForget
```

- [ ] the first `task.runAsyncAndForget` will throw an exception and others won't run
- [ ] three tasks will run and fail in the background
- [X] an exception will be thrown during creation of the `task` instance, and no tasks will run