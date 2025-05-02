using System;
using System.Threading;
using Confluent.Kafka;

class Consumer
{
    public static void Run(string topic)
    {
        Console.WriteLine("Starting Kafka Consumer...");
        string bootstrapServers = Environment.GetEnvironmentVariable("KAFKA_BOOTSTRAP_SERVERS");

        if (string.IsNullOrEmpty(bootstrapServers))
        {
            Console.WriteLine("KAFKA_BOOTSTRAP_SERVERS environment variable is not set.");
            return;
        }
        else
        {
            Console.WriteLine($"KAFKA_BOOTSTRAP_SERVERS: {bootstrapServers}");
        }

        string groupId = "test-group";

        var config = new ConsumerConfig
        {
            BootstrapServers = bootstrapServers,
            GroupId = groupId,
            SecurityProtocol = SecurityProtocol.Plaintext,
            AutoOffsetReset = AutoOffsetReset.Earliest
        };

        using (var consumer = new ConsumerBuilder<Ignore, string>(config).Build())
        {
            consumer.Subscribe(topic);
            Console.WriteLine($"Subscribed to {topic}, waiting for messages...");

            CancellationTokenSource cts = new CancellationTokenSource();
            Console.CancelKeyPress += (_, e) =>
            {
                e.Cancel = true;
                cts.Cancel();
            };

            try
            {
                while (true)
                {
                    try
                    {
                        var result = consumer.Consume(cts.Token);
                        Console.WriteLine($"Received: {result.Message.Value}");
                    }
                    catch (OperationCanceledException)
                    {
                        break;
                    }
                }
            }
            finally
            {
                consumer.Close();
            }
        }
    }
}
