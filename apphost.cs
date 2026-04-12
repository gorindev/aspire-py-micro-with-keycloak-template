#:sdk Aspire.AppHost.Sdk@13.2.1
#:package Aspire.Hosting.GitHub.Models@13.2.1
#:package Aspire.Hosting.JavaScript@13.2.1
#:package Aspire.Hosting.Python@13.2.1
#:package Aspire.Hosting.Redis@13.2.1
#:package Aspire.Hosting.Yarp@13.2.1

using Aspire.Hosting;
using Aspire.Hosting.Yarp.Transforms;

var builder = DistributedApplication.CreateBuilder(args);

// PARAMETERS
var apiKey = builder
    .AddParameter("github-api-key", secret: true);

// INFRASTRUCTURE
var ai = builder
    .AddGitHubModel("ai",  "openai/gpt-4o-mini")
    .WithApiKey(apiKey);

var cache = builder
    .AddRedis("cache");

// SERVICES
var weather = builder
    .AddUvicornApp("weather", "./services/weather", "main:app")
    .WithUv()
    .WithReference(cache)
    .WaitFor(cache)
    .WithHttpHealthCheck("/health")
    .WithHttpsEndpoint();

var weatherAiOutfit = builder
    .AddUvicornApp("weather-ai-outfit", "./services/weather-ai-outfit", "main:app")
    .WithUv()
    .WithReference(ai)
    .WaitFor(ai)
    .WithHttpHealthCheck("/health")
    .WithHttpsEndpoint();

// FRONTEND
var frontend = builder
    .AddViteApp("frontend", "./frontend")
    .WithExternalHttpEndpoints();

// GATEWAY
var gateway = builder
    .AddYarp("gateway")
    .WithConfiguration(yarp =>
    {
        yarp.AddRoute("/weather/api/{**catch-all}", weather)
            .WithTransformPathRemovePrefix("/weather");

        yarp.AddRoute("/weather-ai-outfit/api/{**catch-all}", weatherAiOutfit)
            .WithTransformPathRemovePrefix("/weather-ai-outfit");

        if (builder.ExecutionContext.IsRunMode)
        {
            // In dev mode, proxy all other requests to Vite dev server
            yarp.AddRoute("{**catch-all}", frontend);
        }
    })
    .WithHttpsEndpoint()
    .WithExternalHttpEndpoints()
    .PublishWithStaticFiles(frontend);

frontend.WithReference(gateway).WaitFor(gateway);

builder.Build().Run();
