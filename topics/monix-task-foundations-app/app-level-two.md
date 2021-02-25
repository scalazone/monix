In this part, we will finish the remaining pieces that stop us from successfully running the app.

## Implementing Endpoints

We will connect the `ShipyardService` with endpoints in [Endpoints.scala file](https://github.com/scalazone/monix-exercises/blob/main/monix-task-app/src/main/scala/scalazone/monix/app/api/Endpoints.scala).

We have to map the domain errors to `ApiError` and then run `Task` into `Future` due to using Akka HTTP Backend.

Once that's done, we can expect the following test to pass:

```scala 
sbt "monix-task-app/testOnly EndpointsLevelTwoTests"
```

## HTTP Server

Before we can enjoy our program, we need to start [HttpServer](https://github.com/scalazone/monix-exercises/blob/main/monix-task-app/src/main/scala/scalazone/monix/app/HttpServer.scala) properly.

Once that's done, we can expect the following test to pass:

```scala 
sbt "monix-task-app/testOnly HttpServerLevelTwoTests"
```

## Running the Application

If the previous steps were completed successfully, we can now go and try it out!

``` 
sbt "monix-task-app/run"
```

``` 
[info] running scalazone.monix.app.Main
Go to: http://localhost:8080
Press any key to exit ...
```

The server will be available on the port printed (8080 by default), and the endpoints use `/order` path.
We can test it with `curl` or any REST API client.

POST Request:

``` 
curl -X POST -H "Content-Type: application/json" -d "{\"shipType\": \"Frigate\", \"crew\": 180, \"guns\": 26}" http://localhost:8080/orders
```

That should yield a response similar to the following:

``` 
{"id":"cad22496-1624-4de7-8203-21fb811cf60a"}
```

GET Request:

``` 
curl -X GET http://localhost:8080/orders/cad22496-1624-4de7-8203-21fb811cf60a
```

Resulting in:

``` 
{"orderId":"cad22496-1624-4de7-8203-21fb811cf60a","shipType":"Frigate","rate":"SixthRate","crewReady":0,"crewTotal":180,"gunsReady":0,"gunsTotal":26}
```

Experiment with different inputs to see potential errors.
