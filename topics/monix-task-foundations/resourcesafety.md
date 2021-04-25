Many tasks use resources, such as a connection pool, a filehandle, or a socket.
It's crucial to close them when we finish using them, or else we will end up with resource leaks.

Consider the following method:

```scala 
import java.io.*

def readFirstLine(file: File): String =
  val reader = BufferedReader(FileReader(file))
  reader.readLine()
```

The method reads the line from the file, but it never closes the `BufferedReader`, which has a handle to system resources.

The standard solution to this problem is the `try-with-resources` pattern:

```scala 
import java.io.*

def readFirstLine(file: File): String =
  val reader = BufferedReader(FileReader(file))
  try reader.readLine() finally reader.close()
```

The `try-finally` block makes sure that `reader` is closed, even if `readLine()` throws an exception.
However, there are some issues with this pattern:
- If an exception is thrown, and then there is another exception in the finalizer, one is lost
- It does not support asynchronous execution

Scala comes with [scala.util.Using](https://www.scala-lang.org/API/current/scala/util/Using$.html), which addresses the first issue, but we need to
look elsewhere if we use asynchronous data types, such as Monix `Task`.

## bracket

Monix `Task` provides a `bracket` method that is meant for resource handling.
This what the previous examples look like with `bracket`:

```scala 
import java.io.*
import monix.eval.Task

def readFirstLine(file: File): Task[String] =
  val acquire = Task(BufferedReader(FileReader(file)))
  // Usage (the try block)
  val use: BufferedReader => Task[String] = in => Task(in.readLine())
  // Releasing the reader (the finally block)
  val release: BufferedReader => Task[Unit] = in => Task(in.close())

  acquire.bracket(use)(release)
```

Note how `acquire`, `use`, and `release` all accept `Task`.
In contrast to a plain `A`, the advantage is that we can benefit from `Task` capabilities, such as referentially transparent code and support for concurrency.
Be careful in the latter case because you might need to synchronize the access to the resource.

The resource — `BufferedReader` in this case — will be released regardless of the result of the `Task`, including cancelation.
A variant of `bracket` called `bracketCase` allows customizing the finalizer, depending on the exit case.

## guarantee

If all we need is to execute a given finalizer, we can use `guarantee` or `guaranteeCase`:

```scala 
val task: Task[A] = ...

task.guaranteeCase {
  case ExitCase.Completed => Task(println("Successful completion"))
  case ExitCase.Error(e)  => Task(println(s"Encountered an error: $e"))
  case ExitCase.Canceled  => Task(println("Task has been cancelled"))
}
```

In case of success, this code is equivalent to `task.flatMap(a => finalizer.map(_ => a))`.

As a `guaranteeCase` example that demonstrates error handling, the `Task` we create in this code first fails with the original error, and then the second error is added to it as a suppressed exception:

```scala
import monix.execution.Scheduler

given Scheduler = Scheduler.global

val task: Task[Unit] = Task
  .raiseError(RuntimeException("Task error"))
  .guaranteeCase {
    case ExitCase.Error(e) => Task.raiseError(RuntimeException("Finalizer error"))
    case _                 => Task.unit
  }

task
  .onErrorHandle { err =>
    // => java.lang.RuntimeException: Task error
    println(err)
    // => List(java.lang.RuntimeException: Finalizer error)
    println(err.getSuppressed.toList)
    ()
  }
  .runSyncUnsafe()
```

## Exercises

You can find coding exercises in [the monix-exercises repository](https://github.com/scalazone/monix-exercises/blob/main/monix-task-exercises/src/main/scala/scalazone/monix/lesson6/ResourceSafetyExercises.scala).
If you are stuck, feel free to ask questions at [Monix gitter channel](https://gitter.im/monix/monix),
or peek [at the solutions](https://github.com/scalazone/monix-exercises/blob/main/monix-task-solutions/src/main/scala/scalazone/monix/lesson6/ResourceSafetyExercisesSolutions.scala).

?---?

# What is Task providing that lacks in the try-with-resources pattern?

- [ ] Support for asynchronous code
- [ ] Better error reporting
- [ ] Support for purely functional code
- [X] All of the above

# What will happen with the errors?

```scala
Task
  .raiseError(RuntimeException("Task error"))
  .guaranteeCase {
    case ExitCase.Error(e) => Task.raiseError(RuntimeException("Finalizer error"))
    case _                 => Task.unit
  }
```

- [X] The `Task` will fail with the first error and suppress the second one.
- [ ] The `Task` will fail with the second error and suppress the first one.
- [ ] The `Task` will fail with the first error and report the other one to the Scheduler.
- [ ] The `Task` will fail with the first error and ignore the second one.
