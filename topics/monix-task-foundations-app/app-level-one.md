## Structure of the App

Before we dive into exercises, let's explain the structure of the service.

The code is split into three packages:
- `api` with endpoints definitions.
- `domain` that contains `ShipConstructionOrderRepository` and `ShipyardService`.
  In-memory implementation for the repository is already provided, and the focus of the exercise is to implement `ShipyardService`, which takes other services and repository as dependencies.
- `external` that contains `CrewService` and `MarketService` that are supposed to be treated as clients to external services and should not be modified.
  In a real application, those could be reached via GRPC, REST API, Message Queue, etc.

Then there is `Main`, `HttpServer` and some files with models.
In a larger codebase, it might be useful to separate `api` and `domain` models in different modules and organize them more neatly.

## ShipyardService

We are going to start with implementing the business logic of [ShipyardServiceImpl](https://github.com/scalazone/monix-exercises/blob/main/monix-task-app/src/main/scala/scalazone/monix/app/domain/ShipyardServiceImpl.scala).

The service exposes two methods:
- 
  ```scala
def getShipStatus(orderId: OrderId): Task[Either[ShipGetStatusError, ShipConstructionStatus]]`
```
- 
```scala
def constructShip(orderRequest: ShipConstructionOrderRequest): Task[Either[ShipConstructionError, OrderId]]
```

`constructShip` expects the following model that needs to be validated:

```scala 
case class ShipConstructionOrderRequest(shipType: ShipType, crew: Int, guns: Int)
```

For instance, we can't allow a Frigate with only one cannon.
We will be using [rating system of the Royal Navy](https://en.wikipedia.org/wiki/Rating_system_of_the_Royal_Navy), but that part is already implemented.

After validating input, we will have to order guns from the `MarketService` and hire crew from `CrewService`.

The logic of `getShipStatus` goes as follows:
- Find the order in the `ShipConstructionOrderRepository`
  If order exists, call `MarketService` and `CrewService` for guns and crew's current status, respectively.
- Create a status from responses, or an error.

Return types follow a relatively common pattern of returning recoverable errors _as values_.
The caller knows from the signature the expected errors that they will have to handle or propagate higher in the chain.
Of course, `Task` can still fail with a `Throwable` error, but this pattern considers them non-recoverable.

One of the issues with `Task[Either[E, A]]` is that if we want to short-circuit as soon as we have a `Left`, we have to do it independently.

Some ways to achieve it are the following:
- Locally (within the method), raise selected errors as a known subtype of `Throwable` and then map them before returning from the function.
  For instance:
  ```scala 
  case class TypedError(msg: String)
  case class BarError() extends Throwable with NoStackTrace
  
  def foo: Task[Either[TypedError, Unit]] =
    val callBar = bar.onErrorHandleWith { ex => Task.raiseError(BarError()) }
    // (...) other logic
    
    result.onErrorRecoverWith {
      case BarError() => Task.left(TypedError("bar failed"))
    }
  ```
- Use [EitherT](https://typelevel.org/cats/datatypes/eithert.html).
- Use an effect type with built-in error channel like [Monix BIO](https://bio.monix.io/docs/introduction), or [ZIO](https://zio.dev/).

We will try the first approach in the exercises, but you are free to experiment on your own; tests should pass regardless.

Exercises that are of interest to us have a comment with "EXERCISE LEVEL 1" included, for instance:

```scala
/** EXERCISE LEVEL 1
 *
 * If any of the orders is not found, map it to the respective error
 */
```

Once all exercises are solved, `ConstructShipLevelOneTests` and `GetShipStatusLevelOneTests` should pass:

```scala
sbt "monix-task-app/testOnly *LevelOneTests"
```

Good luck!
