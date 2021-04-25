## Monix Scheduler

`monix.execution.Scheduler` is an extension of Scala's `ExecutionContext`.
Internally, `Scheduler` governs a pool of threads and contains a work queue of `Task`s.
When there are tasks to execute, it schedules them to run on one of the JVM's available threads.
After this point, the operating system is responsible for physically running this thread on a CPU at some point.
This also means that using "parallel" operators does not guarantee true parallelism — it depends on the CPU.

`Task` runs on a given thread until it completes or *yields* control back to the `Scheduler`.
Once `yield` happens, the rest of the `Task` is rescheduled to continue on possibly — but not necessarily — a different thread.
This is as an _asynchronous boundary_.

Asynchronous boundaries happen when calling concurrent operators such as `executeAsync`, `shift`, `sleep`; polling
asynchronous data structures; at the beginning of parallel operators; and so on.
The default `ExecutionModel` of `Scheduler` also introduces automatic asynchronous boundaries every N flatMaps.

These operations will be scheduled on the "default" or "main" `Scheduler` unless the operator allows the user to explicitly specify a different one.
The default `Scheduler` is provided in one of two ways:
- It’s passed as a parameter when running the `Task` with methods like `runToFuture`, `runSyncUnsafe`, etc.
- It’s overwritten for the duration of the given `Task` with `executeOn`.

## Choosing a Scheduler

There is rarely a need for many different schedulers, but many applications have at least two:
- A "main" scheduler (e.g. `Scheduler.global` or `Scheduler.computation`) for most computations, those that are CPU-bound in particular
- A "blocking" scheduler (e.g. `Scheduler.io`) for computations which block threads

The main scheduler aims for maximal utilization of the CPU.
Ideally, we will have one thread per CPU core, so context switching is never required.
For that reason, the recommendation is to use a bounded thread pool with a size equal to the number of CPU's cores.

The blocking scheduler often has an unbounded, cached thread pool.
If we have a limited thread pool and block all available threads, we might end up with a deadlock when there is no thread left that could execute callbacks to unblock some of them.
The risk with an unbounded pool is that we might run out of memory if we create too many threads, so it's useful to limit the parallelism at a higher level.

## Scheduling

`Scheduler` has three execution models:
- `BatchedExecution` is the default, and inserts an asynchronous boundary per N `flatMap` calls
- `SynchronousExecution`, that doesn't insert any asynchronous boundaries on its own
- `AlwaysAsyncExecution`, which inserts asynchronous boundaries on all `flatMap` calls

If we use `SynchronousExecution` we can look at `flatMap` chains as synchronous steps:

```scala 
import monix.execution.Scheduler
import monix.eval.Task

given Scheduler =
  Scheduler.singleThread("test").withExecutionModel(ExecutionModel.SynchronousExecution)

def forever(i: Int): Task[Unit] = Task(println(i)).flatMap { _ => forever(i) }
```

In this example, we created a `Scheduler` with only a single thread that uses the `SynchronousExecution` model.
Then, we defined the `forever` Task, which creates an infinite `flatMap` loop.
Let's see what happens if we run two of those tasks concurrently:

```scala 
Task.parZip2(forever(1), forever(2)).runToFuture
```

Output:

```
1
1
1
1
1
1
1
1
...
```

This might seem surprising at first — only one of the `Task`s is ever executed!
The other one is stuck in the `Scheduler`'s queue because there is only one thread, and the first `Task` never completes and never yields back.

If we change the definition of `forever` by adding `executeAsync`:

```scala 
def forever(i: Int): Task[Unit] = Task(println(i)).flatMap(_ => forever(i).executeAsync)
```

We will now see `1` and `2` interleaved:

``` 
1
2
1
2
1
2
1
2
...
```

This example is a nice demonstration of the _fairness_ and _throughput_ concerns.
Because of fewer context switches, the code will be faster without any asynchronous boundaries — giving us a higher throughput — but it won't be _fair_ because some tasks
might wait a long time before having a chance to execute.

## Learning Resources

Here are some useful resources about concurrency that cover this topic in a more detail:

- [Cats-Effect Documentation](https://typelevel.org/cats-effect/concurrency/basics.html)
- [Concurrency In Scala with Cats-Effect](https://github.com/slouc/concurrency-in-scala-with-ce)
- [Dispelling the magic behind Concurrency in FP (Video Presentation)](https://monix.io/presentations/2019-dispelling-magic-behind-concurrency-in-fp.html)

## Exercises

You can find coding exercises in [the monix-exercises repository](https://github.com/scalazone/monix-exercises/blob/main/monix-task-exercises/src/main/scala/scalazone/monix/lesson5/ThreadManagementExercises.scala).
If you are stuck, feel free to ask questions at [Monix gitter channel](https://gitter.im/monix/monix),
or peek [at the solutions](https://github.com/scalazone/monix-exercises/blob/main/monix-task-solutions/src/main/scala/scalazone/monix/lesson5/ThreadManagementExercisesSolutions.scala).

?---?

# How will the tasks execute?

```scala 
import monix.execution.Scheduler
import monix.eval.Task

given Scheduler = Scheduler
  .singleThread("test")
  .withExecutionModel(ExecutionModel.SynchronousExecution)

val taskA: Task[Unit] = ???
val taskB: Task[Unit] = ???

Task.parZip2(taskA, taskB)
```

- [ ] A and B will potentially execute in parallel
- [ ] A and B will execute in parallel
- [X] A and B will execute synchronously
- [ ] A and B will interleave

# How will the tasks execute?

```scala 
import monix.execution.Scheduler
import monix.eval.Task

given Scheduler = Scheduler
  .fixedPool("test", poolSize = 4)
  .withExecutionModel(ExecutionModel.SynchronousExecution)

val taskA: Task[Unit] = ???
val taskB: Task[Unit] = ???

Task.parZip2(taskA, taskB)
```

- [X] A and B will potentially execute in parallel
- [ ] A and B will execute in parallel
- [ ] A and B will execute synchronously
- [ ] A and B will interleave

# How will the tasks execute?

```scala 
import monix.execution.Scheduler
import monix.eval.Task

given s1: Scheduler = Scheduler
  .fixedPool("test", poolSize = 2)
  .withExecutionModel(ExecutionModel.AlwaysAsyncExecution)

given s2: Scheduler = Scheduler
  .singleThread("test")
  .withExecutionModel(ExecutionModel.SynchronousExecution)

val taskA: Task[Unit] = Task.eval(???).executeOn(s1)
val taskB: Task[Unit] = Task.eval(???).executeOn(s1)
val taskC: Task[Unit] = Task.eval(???).executeOn(s2)

Task.parZip3(taskA, taskB, taskC)
```

- [X] All tasks will potentially execute in parallel
- [ ] All tasks will execute synchronously
- [ ] A and B will interleave, C potentially in parallel
- [ ] A and B will interleave, C synchronously
- [ ] A and B will potentially execute in parallel, C synchronously
