Few areas of the implementation could benefit from making them concurrent.

Let's go back to [ShipyardServiceImpl](https://github.com/scalazone/monix-exercises/blob/main/monix-task-app/src/main/scala/scalazone/monix/app/domain/ShipyardServiceImpl.scala) and go through them.

## CrewService

`CrewService` has a suspicious interface for a client to the external service.

```scala 
trait CrewService:
  def hireCrew(size: Int): OrderId
  def checkCrewStatus(orderId: OrderId): Option[CrewOrderStatus]
```

Both methods are synchronous, but we can assume that they will block the current thread while waiting for the external service to respond.

As we have learned in the _Thread Management_ lesson, it's dangerous to do it on the main Scheduler with a limited thread pool.
If we have 4 threads and four concurrent requests to `CrewService` that takes a long time to respond, we can't run anything else.
We should move it to a different thread pool, then.

## MarketService

Until now, we ordered guns from `OfficialMarket`, but there is also `SmugglersMarket` that perhaps could be faster or cheaper.
Some combinators would help us call both concurrently and continue with the first result.

## Parallelism

Orders from `CrewService` and `MarketService` are independent and could be started concurrently so that we could wait for both results simultaneously.

## Tests

We can test the changes with:

``` 
sbt "monix-task-app/testOnly *LevelThreeTests"
```

Or more specific:

``` 
sbt "monix-task-app/testOnly ConstructShipLevelThreeTests"
```

``` 
sbt "monix-task-app/testOnly GetShipStatusLevelThreeTests"
```

## Congratulations!

If everything is green, you have managed to finish the beginner level course about Monix Task!

We hope you have enjoyed it and feel more confident using `Task` or any other functional effect type.

If you have any feedback or ideas, feel free to [open an issue](https://github.com/scalazone/monix/issues) or a Pull Request.
