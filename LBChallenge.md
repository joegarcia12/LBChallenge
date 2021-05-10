# The Load Balancer challenge
Technical Challenge: Creating a basic application or service load balancer (concept). 

## Intro

> *We do love load balancing, so we need new lb-lovers to join our team.*  

In this challenge, we would like to explore the candidate’s ability to create an application or a service that simulates a load balancer and it's able to distribute the requests between 2 or more backend services. The aim of this challenge is not to create a full-blow load balancer (tcp or http server) + concurrency + http header manipulation + tls + balancer algorithms + health checks + stickiness, the main objective of this is checking the candidate capacity to understand a problem and come up with a solution which may do the job and the way to solve the different challenges which may arise to accomplish the objective.

## What to prioritize

* Basic requirements should be met.
* Basic requirements should be tested.
* Deliverable should be well structured. Consider extensibility. Consider readability.
* Your README should include:
  * How to run your program.
  * What you would do next, given more time (if anything)?

## Objective:
* Create a load balancer application or service with the capability to distribute the requests between 2 or more backend services.  
* Assume the most basic balancer algorithm: round-robin.  
* You can use any language, framework, it just needs to work.

## Extra balls:  
* Dynamic. The configuration is not hardcoded, it might be changed without modifying the code or the service, thus including a config file with any well-known markup language like yaml is a plus.  
* Healthcheck. The ability to take off/on or serve the response if any of the backend services is alive.
* Sorry page. If no backends are available avoid sending a "service unavailable (503)" response.
* Portable. Be able to run it on any OS.

