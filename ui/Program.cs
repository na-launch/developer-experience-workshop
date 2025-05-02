// All using directives must be at the very top.
using Microsoft.AspNetCore.SignalR;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Confluent.Kafka;
using Confluent.Kafka.Admin;
using System.Reflection;
using System.Linq;

// Top-level statements start here:
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllersWithViews();    // Add services to the container.
builder.Services.AddSignalR();                   // Add SignalR.
builder.Services.AddHostedService<KafkaConsumerService>();  // Add Kafka Consumer service.

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.MapHub<KafkaHub>("/kafkaHub");
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");
app.UseEndpoints(endpoints =>
{
    endpoints.MapFallbackToFile("index.html"); // Serves index.html if no route matches.
});

app.MapGet("/topics", () =>
{
    // Retrieve Kafka bootstrap servers from the environment variable.
    var bootstrapServers = Environment.GetEnvironmentVariable("KAFKA_BOOTSTRAP_SERVERS");
    if (string.IsNullOrWhiteSpace(bootstrapServers))
    {
        return Results.BadRequest("Kafka bootstrap servers not set.");
    }
    
    var adminConfig = new AdminClientConfig { BootstrapServers = bootstrapServers };
    using var adminClient = new AdminClientBuilder(adminConfig).Build();
    Metadata metadata = adminClient.GetMetadata(TimeSpan.FromSeconds(5));

    // Filter topics to exclude internal ones, e.g. "__consumer_offsets".
    var topics = metadata.Topics
        .Select(t => t.Topic)
        .Where(topic =>
            !string.IsNullOrWhiteSpace(topic) &&
            !topic.Equals("__consumer_offsets", System.StringComparison.OrdinalIgnoreCase))     // TODO This is causing the code to crash, not sure why
        .ToArray();

    return Results.Json(new { topics });
});

app.MapPost("/change_topic", (ChangeTopicRequest request) =>
{
    if (string.IsNullOrWhiteSpace(request.topic))
    {
        return Results.BadRequest(new { message = "Invalid topic." });
    }

    // Update the global topic.
    KafkaTopicManager.CurrentTopic = request.topic;
    return Results.Json(new { message = $"Topic changed to {request.topic}" });
});

app.Run();

// HELP! My neighbor's favorite topic is pets, but he always gets my cats name wrong!
// I've suggested he look on pk-kafka-kafka-bootstrap.pk-world.svc.cluster.local for my cats name
// Think you can find my cats name?
