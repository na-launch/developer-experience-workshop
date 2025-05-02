using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.SignalR;
using Microsoft.Extensions.Hosting;
using Confluent.Kafka;

public class KafkaConsumerService : BackgroundService
{
    private readonly IHubContext<KafkaHub> _hubContext;
    // Keep track of the last subscribed topic.
    private string _currentSubscribedTopic = KafkaTopicManager.CurrentTopic;

    public KafkaConsumerService(IHubContext<KafkaHub> hubContext)
    {
        _hubContext = hubContext;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        string groupId = $"consumer-{Guid.NewGuid().ToString()}-group";
        var config = new ConsumerConfig
        {
            BootstrapServers = Environment.GetEnvironmentVariable("KAFKA_BOOTSTRAP_SERVERS"),
            GroupId = groupId,   
            AutoOffsetReset = AutoOffsetReset.Earliest
        };

        using var consumer = new ConsumerBuilder<Ignore, string>(config).Build();
        // Initially subscribe to the topic from the topic manager.
        _currentSubscribedTopic = KafkaTopicManager.CurrentTopic;
        consumer.Subscribe(_currentSubscribedTopic);
        Console.WriteLine($"Kafka Consumer started and subscribed to topic: {_currentSubscribedTopic}");

        await Task.Run(() => StartConsuming(consumer, stoppingToken), stoppingToken);
    }

    private async Task StartConsuming(IConsumer<Ignore, string> consumer, CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                // Check if the topic has changed.
                var desiredTopic = KafkaTopicManager.CurrentTopic;
                if (!string.Equals(desiredTopic, _currentSubscribedTopic, StringComparison.OrdinalIgnoreCase))
                {
                    _currentSubscribedTopic = desiredTopic;
                    consumer.Subscribe(_currentSubscribedTopic);
                    Console.WriteLine($"Re-subscribed to new topic: {_currentSubscribedTopic}");
                }

                // Wait for a message with a timeout of, say, 2 seconds.
                var result = consumer.Consume(TimeSpan.FromSeconds(2));
                if (result != null)
                {
                    Console.WriteLine($"Received message from Kafka: {result.Message.Value}");
                    await _hubContext.Clients.All.SendAsync("ReceiveMessage", result.Message.Value, stoppingToken);
                }
            }
            catch (ConsumeException ex)
            {
                Console.WriteLine($"Kafka error: {ex.Error.Reason}");
            }
            catch (OperationCanceledException)
            {
                // Graceful shutdown
                break;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Unexpected error: {ex.Message}");
            }
        }

        consumer.Close();
        Console.WriteLine("Kafka Consumer stopped.");
    }
}