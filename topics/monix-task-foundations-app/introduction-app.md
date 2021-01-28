In the previous topic, we have covered many features of the Monix Task on a high level.
Hopefully, the exercises helped absorb the information, but it cannot be obvious how to apply and combine all the different pieces when writing actual applications.

The next exercise aims to remedy this issue. We are going to go through writing a straightforward but fully functioning HTTP Service.
To keep things simple, it won't be exactly like a real, production-ready application (that might come in the future levels of the course :) ) It should give us a decent idea of how the main features of Monix Task can fit together.

## What's the App about

The service deals with constructing ships.
We are going to implement two endpoints:
- `POST /orders` that order construction of a new ship.
- `GET /orders/{orderID}` that queries the given order's construction status.

HTTP Server will be written using [tapir](https://tapir.softwaremill.com/en/latest/) with [Akka HTTP](https://doc.akka.io/docs/akka-http/current/) backend.
JSON (de)serialization will be handled by [circe](https://github.com/circe/circe).

In the process, we will learn how to use Monix Task with some of the most popular Scala libraries and safely interoperate with impure code.

The exercise's primary focus will be getting familiar with `Task` basics, simple concurrency in practice, and interoperability.

The domain model is kept basic as that's not the focus of this part of the course.

## Levels

The development of the App is split into three stages:
- Implementing the business logic of `ShipyardService` with a proper error handling
- Connecting the service to HTTP Endpoints and finishing `HttpServer` to be able to run the application
- Adding concurrency to the `ShipyardService`

## Setup

The App's skeleton is in the [monix-exercises repository](https://github.com/scalazone/monix-exercises) that should be forked and then cloned.

We are mainly interested in the [monix-task-app module](https://github.com/scalazone/monix-exercises/tree/main/monix-task-app/src/main/scala/scalazone/monix/app).

We can compile the App with:

``` 
sbt "monix-task-app/compile"
```

The exercises come with tests.
In the beginning, all of them will fail, but we should make sure they can run properly:

``` 
sbt "monix-task-app/test"
```

As we proceed, more and more tests will turn green.

We can also run individual tests:

``` 
sbt "monix-task-app/testOnly ConstructShipLevelOneTests"
```

The tests are split into three levels that correspond to the next lessons in this topic.
It is possible to run the entire level of tests at once with the following command:

``` 
sbt "monix-task-app/testOnly *LevelOneTests"
```

If the project has been built without any issues (apart from those that we have mentioned), we are ready to go to the next lesson to start writing the App!
