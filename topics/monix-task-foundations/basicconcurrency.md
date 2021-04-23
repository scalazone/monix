One of the main appeals of Monix `Task` is rich support for asynchronous operations.

Let's start with quick definitions.

## Terminology

### Thread

Thread is a basic unit of CPU utilization. CPU can usually run up to 1 thread per CPU core at the same time.

JVM's `Thread` is an abstraction over operating system's native threads that is mapped 1:1. 
Each JVM thread has a corresponding native thread. By default, threads take about 1 MB of memory for their private stacks.

Threads can store some data in CPU's caches and registers, that needs to be cleared and/or restored when a new thread takes over.
This process is called a _context switch_ and it is considered quite expensive if high-throughput is a major concern.

### Synchronous Operation

All steps of the operation happen in sequence, one after another on the thread it started.

![Synchronous Operation](/api/content/courseImages/monix/sync_operation.svg)

### Asynchronous Operation

The operation was started on one thread, but at some point, it might be rescheduled and continue
execution on a different one. The asynchronous operation consists of synchronous steps. 

The point at what the synchronous step is about to be rescheduled, is called _asynchronous boundary_.

![Asynchronous Operation](/api/content/courseImages/monix/async_operation.svg)

### Concurrency

Several computations could be interleaved, e.g., two asynchronous computations taking turns to complete their synchronous steps.

![Concurrent operations](/api/content/courseImages/monix/conc_operation.svg)

### Parallelism

We talk about parallelism when multiple tasks can advance **at the same time**.
CPUs can typically execute N tasks in parallel where N = number of cores.

![Parallel operations](/api/content/courseImages/monix/par_operation.svg)

Note that asynchronicity, or concurrency do not imply parallelism.
For instance, we can have concurrency without the possibility of parallelism if we use a single thread.
On the other hand, any parallel operation is concurrent.

## Concurrency in Monix

Parallelism is done with dedicated operators, such as `parMap2`, or `parTraverse`.
Keep in mind, that parallelism with these operators is not guaranteed.
A more precise definition is that all "parallel" tasks will be started concurrently.
If there are free threads and CPU cores - they might execute in parallel.
We will look into task scheduling in a little more detail in the next lesson.

If any of the concurrent `Task`s fails, the resulting `Task` will fail with the first error,
and we will attempt to cancel the rest because we can no longer receive a successful result.

### parMap

We could use `parMap3` to call three independent services concurrently:

```scala 
val locationTask: Task[String] = ???
val phoneTask: Task[String] = ???
val addressTask: Task[String] = ???

// Potentially executed in parallel
val aggregate =
  Task.parMap3(locationTask, phoneTask, addressTask) {
    (location, phone, address) => "Gotcha!"
  }
```

Unlike Scala's `Future`, `Task`'s parallelism is explicit.
If we were to use `map3` instead of `parMap3` then the tasks would be started in sequence, one at a time.

### Task.sleep

We can use `Task.sleep` or `delayExecution` to temporarily stop the `Task` and reschedule it after a specified time.
Unlike `Thread.sleep`, no `Thread` is blocked and other tasks can freely execute on that `Thread`. 
This type of blocking is called _asynchronous_, or _semantic_ blocking.

The following code will take 2 seconds (after execution) even if we have only 1 thread:

```scala 
import scala.concurrent.duration.*
import monix.eval.Task

Task.parZip2(Task.sleep(1.second), Task.sleep(2.second))
```

### parTraverse

Just as we could transform a `List[Task[A]]` into `Task[List[A]]` in _sequence_, we can do the same concurrently with
`parSequence`, or `parTraverse`.

```scala 
import monix.eval.Task
import scala.concurrent.duration.*
import monix.execution.Scheduler

given Scheduler = Scheduler.global

val ta = Task { println("Effect1"); 1 }.delayExecution(1.second)
val tb = Task { println("Effect2"); 2 }.delayExecution(1.second)
val list: Task[Seq[Int]] = Task.parSequence(Seq(ta, tb))

list.runToFuture.foreach(println(_))
// => Effect1
// => Effect2
// => List(1, 2)

list.runToFuture.foreach(println(_))
// => Effect2
// => Effect1
// => List(1, 2)
```

Depending on scheduling, the tasks might execute differently, but the results are gathered in the original order.

## Exercises

You can find coding exercises in [the monix-exercises repository](https://github.com/scalazone/monix-exercises/blob/main/monix-task-exercises/src/main/scala/scalazone/monix/lesson4/ConcurrencyExercises.scala).
If you are stuck, feel free to ask questions at [Monix gitter channel](https://gitter.im/monix/monix),
or peek [at the solutions](https://github.com/scalazone/monix-exercises/blob/main/monix-task-solutions/src/main/scala/scalazone/monix/lesson4/ConcurrencyExercisesSolutions.scala).