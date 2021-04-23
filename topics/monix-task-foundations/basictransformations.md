## map

`Task` can be mapped with `map` which will apply a provided function to the result.

```scala 
import monix.eval.Task

val task10 = Task.now(10)
val task20 = task10.map(_ * 2)
```

Since `Task` is an immutable computation description, all transformations will create a *new* `Task`.

## flatMap

If we want to apply an _effectful_ (returning `Task`) function, we should take a look at `flatMap`:

```scala 
import monix.eval.Task

val task20 = Task { println("Calculating 20"); 20 }
val task40 = Task { println("Calculating 40"); 40 }

val task60 = task20.flatMap { result20 => task40.map { result40 => result20 + result40 } }
```

Alternatively, we could use Scala's `for comprehension` for the same result:

```scala 
for
  result20 <- task20
  result40 <- task40
yield result20 + result40
```

Tasks will execute in sequence, producing the following output after execution:

```
Calculating 20
Calculating 40
```

### Referential Transparency

Now that we know `flatMap`, it's the right moment to mention [referential transparency](https://en.wikipedia.org/wiki/Referential_transparency).
The property says that an expression can be replaced with its corresponding value without changing the program's behavior.
When people talk about *purely functional programming*, the pure part means referentially transparent.

Adding Integers is referentially transparent:

```scala 
val constInt = 5

constInt + constInt // always return 10
5 + 5               // always return 10
5 + constInt        // always return 10
constInt + 5        // always return 10
```

It's an excellent refactoring guarantee - It doesn't matter if we use `val`, `def`, `lazy val`, inline, or extract the code.
The result will always be the same, so we don't risk breaking the code with substitutions.

Some functions are not referentially transparent, and thus, not pure:

```scala 
import scala.util.Random

val randomInt = Random.nextInt(10)

randomInt + randomInt                   // 2 * randomInt
Random.nextInt(10) + Random.nextInt(10) // a sum of two random Integers
```

In this case, the result could be completely different, depending on how we write it, and we need to be very careful of
what we're doing, otherwise we could introduce subtle bugs.

Fortunately, effect types like `Task` have the power to turn any non-referentially transparent expression into a pure value!

Let's take a closer look at how `Task` satisfies this property:

```scala 
import scala.util.Random
import monix.eval.Task

// Nothing happens yet, just a description
val randomTask = Task.eval(Random.nextInt(10))

val reusedTask = Task.map2(randomTask, randomTask)(_ + _)
val inlinedTask = Task.map2(Task.eval(Random.nextInt(10)), Task.eval(Random.nextInt(10)))(_ + _)
```

Once we run `reusedTask` and `inlinedTask` they will both behave the same and generate a random `Integer` twice because
`randomTask` is just a specification of a program that knows how to generate integers.

We don't lose any power either, if we'd like to reuse the result, we can `map` it:

```scala 
randomTask.map(randomInt => randomInt + randomInt)
```

The behavior is always consistent.

## traverse

Other prevalent operators are `sequence` and `traverse`.

`Task.sequence` allows us to transform a `Seq[Task[A]]` into `Task[Seq[A]]` in sequence,
so each `Task` will be executed after the previous one successfully completes.

```scala 
import monix.eval.Task
import monix.execution.Scheduler

given Scheduler = Scheduler.global

val ta = Task { println("Effect1"); 1 }
val tb = Task { println("Effect2"); 2 }

val list: Task[Seq[Int]] =
  Task.sequence(Seq(ta, tb))

// We always get this ordering:
list.runToFuture.foreach(println(_))
//=> Effect1
//=> Effect2
//=> List(1, 2)
```

`Task.traverse` takes a `Seq[A]`, `f: A => Task[B]` and returns a `Task[Seq[B]]`.
This is similar to `Task.sequence` but it uses `f` to generate each `Task`.

All `Task.sequence` semantics hold, meaning the effects are ordered, and the tasks WILL NOT execute in parallel.

```scala 
import monix.eval.Task
import monix.execution.Scheduler

given Scheduler = Scheduler.global

def task(i: Int) = Task { println("Effect" + i); i }

val list: Task[Seq[Int]] =
  Task.traverse(Seq(1, 2)) { i => task(i) }

// We always get this ordering:
list.runToFuture.foreach(println)
//=> Effect1
//=> Effect2
//=> List(1, 2)
```

## Exercises

You can find coding exercises in [the monix-exercises repository](https://github.com/scalazone/monix-exercises/blob/main/monix-task-exercises/src/main/scala/scalazone/monix/lesson2/TransformationExercises.scala).
If you are stuck, feel free to ask questions at [Monix gitter channel](https://gitter.im/monix/monix),
or peek [at the solutions](https://github.com/scalazone/monix-exercises/blob/main/monix-task-solutions/src/main/scala/scalazone/monix/lesson2/TransformationExercisesSolutions.scala).